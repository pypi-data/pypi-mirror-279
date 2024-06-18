#!/usr/bin/env python3

import sys, re, traceback, time
from concurrent.futures import ThreadPoolExecutor
from ..abstract import AbstractReader
from ..utils import *
from ..reader import reader

# MultiDB schema is now tango-dependent
# future releases .yaml based to be implemented
try:
    import tango
except:
    tango = None
    
DEBUG = os.getenv('PYHDBPP_DEBUG') or '-v4' in sys.argv

# MultiDBReader

class MultiDBReader(AbstractReader):
    
    def __init__(self, config='',**kwargs):
        """
        config would be:
         - a list of dbnames
         - a comma-separated string
         - a {dbname:config} dictionary
        
        if just names are given, config for each db 
        will be read from tango db
        """
        logger.debug('MultiDBReader(config={},kwargs={})'.format(
            config, kwargs))
        self.readers = {}
        self.attributes = {}
        self.configs = {}
        self.tangodb = tango.Database()
        self.threaded = kwargs.get('threaded',False)
        self.timeout_s = kwargs.get('timeout_s',0)

        # List of schemas in string format
        if isinstance(config,str):# and ',' in config:
            config = [s.strip() for s in config.split(',')]
            props = [s for s in config if s.startswith('$')]
            for p in props:
                config.remove(p)
                p = p.strip('$')
                v = self.tangodb.get_property('HDB++',p)[p]
                v = [v] if isinstance(v,(str,bytes)) else v
                config.extend(v)
                logger.debug('MultiDBReader(...): {} = {}'.format(p,v))

        # List of schemas to load
        if isinstance(config,list):
            config = dict((s, load_config_from_tango(s,tangodb=self.tangodb))
                for s in config)
            
        # Dict of {schema:config}
        if isinstance(config,dict):
            for k,data in config.items():
                try:
                    if isinstance(data, str):
                        data = load_config_from_tango(v,tangodb=self.tangodb)
                    data['persistent'] = ''
                    rd = reader(apiclass=data['apiclass'],
                                config=data,)
                                #persistent=False)
                    self.configs[k] = data
                    self.readers[k] = rd
                except Exception as e:
                    logger.warning('Unable to load %s schema' % k)
                    self._trace(traceback.format_exc())
                    #raise e

        if self.threaded:
            self.executor = ThreadPoolExecutor(max_workers=len(self.readers) or 1)
        else:
            self.executor = None
        
        self.get_attributes(load=True)
        
    def __del__(self):
        for k,rd in self.readers.items():
            del rd
        
    def _trace(self,*args):
        if DEBUG:
            print(time2str(time.time()),'MultiDB',*args)


    def get_connection(self, attribute=None, schema=None, epoch=0):
        """
        Return the db connections used to acquire an attribute or schema
        at a given date.
        If no schema or attribute is provided, returns all connections.
        The returned object will be implementation specific.
        """
        self._trace('get_connection', attribute, schema, epoch)
        if isinstance(epoch,str):
            epoch = str2time(epoch)

        if attribute and not schema:
            # this call gets the attribute name as it is archived
            attribute = self.get_attribute_name(attribute)
            schemas = {}
            for k in self.readers:
                reader = self.readers[k]
                attrs = self.attributes[k]
                # if reader.is_attribute_archived(attribute):
                if attribute in attrs:
                    if epoch:
                        rdc = reader.config
                        start = rdc.get('start_date',0)
                        stop = rdc.get('stop_date',0)
                        start = time2type(start,float)
                        stop = time2type(stop,float)
                        if start < 0:
                            start = now() + start
                        if stop < 0:
                            stop = now() + stop
                        elif not stop:
                            stop = END_OF_TIME

                        if not start <= epoch <= stop:
                            continue

                    schemas[k] = reader
                    
            return schemas

        elif schema and attribute:
            return self.readers.get(schema).is_attribute_archived(attribute)
        elif schema:
            return self.readers.get(schema,None)
        else:
            return self.readers


    def get_attributes(self, active=False, pattern='', load=False, timeout_s=0):
        """
        Queries the database for the current list of archived attributes.
        
        Once it has been queried, result is cached unless load=True is passed.
        
        arguments:
            active: True: only attributes currently archived
                    False: all attributes, even the one not archiving anymore
            regexp: '' :filter for attributes to retrieve
        """
        timeout_s = timeout_s or self.timeout_s

        if load or not self.attributes:

            if not self.threaded:
                for k,v in self.readers.items():
                    self.attributes[k] = [a.lower() for a in v.get_attributes()]

            else:
                methods = {k:db.get_attributes for k,db in self.readers.items()}
                data = TimedThreadPoolExecution(methods,executor=self.executor,default=[],workers=None)
                for k,v in data.items():
                    self.attributes[k] = [a.lower() for a in v]

                #with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.readers)) as ex:
                #ex = self.executor
                #results = {k: ex.submit(db.get_attributes)
                #        for k,db in self.readers.items()}
                #for k,v in results.items():
                #    self.attributes[k] = [a.lower() for a in v.result()]

                #     ex = self.executor
                #     results = {}
                #     t0 = time.time()
                #     for k,db in self.readers.items():
                #         results[k] = ex.submit(db.get_attributes)
                #     pending = list(self.readers.keys())
                #     while pending and time.time() < (t0 + timeout_s):
                #         for k,v in results.items():
                #             if v.done():
                #                 self.attributes[k] = [a.lower() for a in v.result()]
                #                 pending.remove(k)
                #         time.sleep(1e-3)
                #     if pending:
                #         for k in pending:
                #             self.attributes[k] = []
                #         print('multidb.get_attributes():Unable to get {} attributes in less than {} seconds'
                #               .format(pending,timeout_s))

        # self._trace('get_attributes',pattern)

        return sorted(set(a for k,v in self.attributes.items() for a in v
                    if not pattern or attr_match(pattern,a)))
    
    def get_attribute_name(self,attribute):
        """
        get attribute name as it is used in hdb++ (e.g. FQDN)
        """
        fqdn = attr_translate(attribute)
        brief = attr_translate(attribute, brief=True)
        pattern = "(%s)|(%s)" % (fqdn,brief)
        attrs = self.get_attributes(pattern=pattern, load=False)
        if fqdn in attrs:
            return fqdn
        elif len(attrs)>1:
            logger.warning('{} matches: {}'.format(attribute,attrs))
            raise Exception('MultipleAttributeMatches:{}'.format(attrs))
        elif not len(attrs):
            raise Exception('AttributeNotArchived:{}'.format(attribute))
        r =  attrs[0]
        self._trace('get_attribute_name', attribute, ':', r)
        return r

    def is_attribute_archived(self, attribute, *args, **kwargs):
        """
        Returns if an attribute has values in DB.

        arguments:
            attribute: fqdn for the attribute.
            active: if true, only check for active attributes,
                    otherwise check all.
            brief: returns bool instead of list of dbs
        """
        try:
            brief = kwargs.get('brief',False)
            if brief:
                return bool(self.get_attribute_name(attribute))
            else:
                return list(self.get_connection(attribute).keys())
        except Exception as e:
            logger.info('is_attribute_archived({}): {}'.format(
                attribute, e))
            return False if brief else []

    def get_closer_attributes_values(self, attributes, time_bound=None, n=1, columns=["data_time", "value_r"]):
        """
        Returns the n closer values inserted around time in DB for a list of attributes.
        If n is negative it will get the last inserted values, if positive it will get the next.

        arguments:
            attribute: fqdn for the attribute.
            columns: list of columns to query, default to data_time and value_r.
            time_bound: lower bound for data_time, if None should default to now()
            n: number of samples, default to 1.
        returns:
            [(epoch, r_value, w_value, quality, error_desc)]
        """
        logger.debug('multidb.get_closer_attributes_values({},{},{})'
                     .format(attributes,time_bound,n))
        result = {}
        if time_bound is None and n > 0:
            n = -n #defaults to last value
        for attribute in attributes:
            try:
                dbs = self.get_connection(attribute, epoch = time.time())
                logger.debug('multidb: {} archived by {}'.format(attribute,dbs.keys()))
                if self.threaded:
                    methods = {k:db.get_closer_attributes_values for k,db in dbs.items()}
                    args = {k:(([attribute],),{'time_bound':time_bound,'n':n}) for k in methods}
                    values = TimedThreadPoolExecution(methods,args,self.executor,default=None,timeout_s=60)
                    values = {k:v[attribute] for k,v in values.items()}
                else:
                    values = {k:db.get_closer_attributes_values([attribute],time_bound=time_bound,n=n)[attribute]
                              for k,db in dbs.items()}

                # results = {k:
                #         ex.submit(db.get_closer_attributes_values,
                #             [attribute], time_bound=time_bound, n=n)
                #         for k,db in dbs.items()}
                #
                # values = {k:results[k].result()[attribute]
                #         for k,db in dbs.items()}

                # print(attribute,values)
                result[attribute] = sorted(values.values())[-1]
            except:
                traceback.print_exc()
                result[attribute] = None
        return result

#     def get_last_attribute_value(self, attribute, time_bound=None):
#         """
#         Returns last value inserted in DB for an attribute
#
#         arguments:
#             attribute: fqdn for the attribute.
#             time_bound: datetime, end of the period to query.
#                          if None, no period is applied
#         returns:
#             (epoch, r_value, w_value, quality, error_desc)
#         """
#         attribute = self.get_attribute_name(attribute)
#
#         dbs = self.get_connection(attribute, epoch = time.time())
#         #with concurrent.futures.ThreadPoolExecutor(max_workers=len(dbs)) as ex:
#         ex = self.executor
#         results = {k:
#                 ex.submit(db.get_last_attributes_values,
#                     [attribute], time_bound=time_bound)
#                 for k,db in dbs.items()}
#
#         values = {k:results[k].result()[attribute]
#                   for k,db in dbs.items()}
#
#         return sorted(values.values())[-1]
#
#     def get_last_attributes_values(self, attributes,
#             columns = 'time, r_value', time_bound = None):
#         """
#         Returns last values inserted in DB for a list of attributes
#
#         arguments:
#             attribute: fqdn for the attribute.
#             columns: requested columns separated by commas
#             time_bound: datetime, end of the period to query.
#                          if None, no period is applied
#         returns:
#             {'att1':(epoch, r_value, w_value, quality, error_desc),
#              'att2':(epoch, r_value, w_value, quality, error_desc),
#              ...
#             }
#         """
#         #return dict((a,self.get_last_attribute_values(a)) for a in attributes)
#         results,data = {},{}
#         with ThreadPoolExecutor(max_workers=len(attributes)) as ex:
#             results = {a:ex.submit(
#                 self.get_last_attribute_value, a, time_bound=time_bound)
#                 for a in attributes}
#             data = {k:v.result() for k,v in results.items()}
#         return data

    def get_attribute_values(self, attribute,
            start_date, stop_date=None,
            decimate = None,
            **params):
        """
        Returns attribute values between start and stop dates.

        arguments:
            attribute: fqdn for the attribute.
            start_date: datetime, beginning of the period to query.
            stop_date: datetime, end of the period to query.
                       if None, now() is used.
            decimate: aggregation function to use in the form:
                      {'timedelta0':(MIN, MAX, ...)
                      , 'timedelta1':(AVG, COUNT, ...)
                      , ...}
                      if None, returns raw data.
        returns:
            [(epoch0, r_value, w_value, quality, error_desc),
            (epoch1, r_value, w_value, quality, error_desc),
            ... ]
        """
        attribute = self.get_attribute_name(attribute)
        if isinstance(start_date,(int,float)) and start_date < 0:
            start_date = now() + start_date
        stop_date = stop_date or now()
        
        #db = self.get_connection(attribute)
        #return db.get_attribute_values(attribute, start_date, stop_date, 
                                       #decimate, **params)
    
        dbs = self.get_connection(attribute, epoch = stop_date)

        if not self.threaded:
            db = list(dbs.values())[0]
            return db.get_attribute_values(attribute, start_date, stop_date,
                                       decimate, **params)
        else:
            #with concurrent.futures.ThreadPoolExecutor(max_workers=len(dbs)) as ex:
            ex = self.executor
            results = {k:
                    ex.submit(db.get_attribute_values,
                        attribute, start_date, stop_date, decimate, **params)
                    for k,db in dbs.items()}
            values = {k:results[k].result() for k,db in dbs.items()}

            ks = [k for k,v in values.items() if len(v)]
            self._trace({k:len(v) for k,v in values.items()})
            if len(ks)==1:
                return values[ks[0]]
            else:
                result = [] #sorted(t for k in ks for t in values[k])
                ts = sorted((values[k][0][0],k) for k in ks)
                for t,k in ts:
                    if not result or t > result[-1][0]:
                        result.extend(values[k])
                return result

    def get_attributes_values(self, attributes,
            start_date, stop_date=None,
            decimate = None,
            correlate = False,
            **params):
        """
        Returns attributes values between start and stop dates
        , using decimation or not, correlating the values or not.

        arguments:
            attributes: a list of the attributes' fqdn
            start_date: datetime, beginning of the period to query.
            stop_date: datetime, end of the period to query.
                       if None, now() is used.
            decimate: aggregation function to use in the form:
                      {'timedelta0':(MIN, MAX, ...)
                      , 'timedelta1':(AVG, COUNT, ...)
                      , ...}
                      if None, returns raw data.
            correlate: if True, data is generated so that
                       there is available data for each timestamp of
                       each attribute.
            columns: columns separated by commas
                    time, r_value, w_value, quality, error_desc                       

        returns:
            {'attr0':[(epoch0, r_value, w_value, quality, error_desc),
            (epoch1, r_value, w_value, quality, error_desc),
            ... ],
            'attr1':[(...),(...)]}
        """

        if not self.threaded:
            return dict((a, self.get_attribute_values(
                            a, start_date, stop_date, decimate))
                            for a in attributes
                        )
        else:
            results,data = {},{}
            with ThreadPoolExecutor(max_workers=len(attributes)) as ex:
                for a in attributes:
                    results[a] = ex.submit(
                        self.get_attribute_values, a,
                        start_date, stop_date, decimate=decimate,
                        correlate=correlate,
                        **params)

                for a in attributes:
                    data[a] = results[a].result()
                    self._trace(a,len(data[a]))
        
        return data
