#!/usr/bin/env python3

import sys, re, traceback, os, time
from concurrent.futures import ThreadPoolExecutor
from ..abstract import AbstractReader
from ..utils import *

try:
    import MySQLdb as mariadb
except:
    import pymysql as mariadb

DEBUG = os.getenv('PYHDBPP_DEBUG') or '-v4' in sys.argv
if DEBUG:
    print('using %s as mariadb' % mariadb)

# MariaDBReader

class MariaDBReader(AbstractReader):
    """
    read-only API for hdb++ databases, based on PyTangoArchiving AbstractReader
    """
    
    def __init__(self, config='', **kwargs):
        """
        Arguments accepted by pymysql connections:

        :param host: Host where the database server is located
        :param user: Username to log in as
        :param password: Password to use.
        :param database: Database to use, None to not use a particular one.
        :param port: MySQL port to use, default is usually OK. (default: 3306)
        :param persistent=True: whether to use different mysql connection between queries (False required for multi-threading)
        :param bind_address: When the client has multiple network interfaces, specify
            the interface from which to connect to the host. Argument can be
            a hostname or an IP address.
        :param unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
        :param read_timeout: The timeout for reading from the connection in seconds (default: None - no timeout)
        :param write_timeout: The timeout for writing to the connection in seconds (default: None - no timeout)
        :param charset: Charset you want to use.
        :param sql_mode: Default SQL_MODE to use.
        :param read_default_file:
            Specifies  my.cnf file to read these parameters from under the [client] section.
        :param conv:
            Conversion dictionary to use instead of the default one.
            This is used to provide custom marshalling and unmarshaling of types.
            See converters.
        :param use_unicode:
            Whether or not to default to unicode strings.
            This option defaults to true for Py3k.
        :param client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
        :param cursorclass: Custom cursor class to use.
        :param init_command: Initial SQL statement to run when connection is established.
        :param connect_timeout: Timeout before throwing an exception when connecting.
            (default: 10, min: 1, max: 31536000)
        :param ssl:
            A dict of arguments similar to mysql_ssl_set()'s parameters.
        :param read_default_group: Group to read from in the configuration file.
        :param compress: Not supported
        :param named_pipe: Not supported
        :param autocommit: Autocommit mode. None means use server default. (default: False)
        :param local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
        :param max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
            Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
        :param defer_connect: Don't explicitly connect on contruction - wait for connect call.
            (default: False)
        :param auth_plugin_map: A dict of plugin names to a class that processes that plugin.
            The class will take the Connection object as the argument to the constructor.
            The class needs an authenticate method taking an authentication packet as
            an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
            (if no authenticate method) for returning a string from the user. (experimental)
        :param server_public_key: SHA256 authentication plugin public key value. (default: None)
        :param db: Alias for database. (for compatibility to MySQLdb)
        :param passwd: Alias for password. (for compatibility to MySQLdb)
        :param binary_prefix: Add _binary prefix on bytes and bytearray. (default: False)
        """
        if config and isinstance(config,(str,bytes)):
            config = self.parse_config(config)

            
        self.config = config or {}
        self.config.update(kwargs)
        self.db = None
        self.database = self.config.get('database','hdbpp')
        self.user = self.config.get('user','')
        self.password = self.config.get('password','')
        self.port = int(self.config.get('port','3306'))
        self.host = self.config.get('host','localhost')
        self.decimate = self.config.get('decimate',None)
        self.persistent = self.config.get('persistent',True)
        if self.decimate:
            if re.match('[0-9]+',self.decimate):
                self.decimate = int(self.decimate)
            elif str(self.decimate).lower().strip() == 'false':
                self.decimate = False
            elif str(self.decimate).lower().strip() in ('true','yes'):              
                decimate = True # decimation chosen by api

        self.attributes = {}
        self.tables = {} #table creators
        self.max_workers = 3
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.debug = kwargs.get('debug',False)
        
        # Persistency is optional to allow multi-threading
        if self.persistent:
            self._trace('Creating persistent connection to DB')
            self.db = self._connect()
        
    def __del__(self):
        if getattr(self,'_cursor',None):
            self._cursor.close()
        if getattr(self,'db',None):
            self.db.close()
            
    def _trace(self,*args,**kwargs):
        if DEBUG or kwargs.get('error',False):
            print(time.ctime(),self.host,self.database,*args)
        
    def _connect(self):
        self._trace('{}.connect()'.format(self.database))
        try:
            db = mariadb.connect(database=self.database,
                user=self.user, password=self.password, port=self.port, 
                host=self.host)        
        except: #Old Debian 9 API
            db = mariadb.connect(db=self.database,
                user=self.user, passwd=self.password, port=self.port, 
                host=self.host)                    
        return db
        
    def _query(self, query, prune = False, renew = False):
        """
        query: SQL code
        prune: if True, remove duplicated values (row[1:])
        renew: create a new db connection, close on exit
        """
        renew = not self.db or renew
        self._trace('{}.Query("{}",renew={})'.format(self.database, query, renew))
        try:
            db = self.db if not renew else self._connect()
            _cursor = db.cursor()
            _cursor.execute(query)
            if prune:
                r,l = [],True
                while l:
                    try:
                        l = _cursor.fetchone()
                        if l and (not r or l[1:] != r[-1][1:]):
                            r.append(l)
                    except:
                        self._trace(r[-1:], l)
                        traceback.print_exc()
                        break
                return r
            else:
                return _cursor.fetchall()
        except Exception as e:
            print('!'*80)
            self._trace(query, e, error=True)
            raise e
        finally:
            try:
                _cursor.close()
            except:
                pass
            try:
                renew and db.close()
            except:
                pass
        
    def _describe_table(self,table):
        if not self.tables.get(table,None):
            self.tables[table] = self._query('describe %s' % table)
        return self.tables[table]
    
    def parse_config(self,config):
        """
        config string as user:password@host:port/database
        or dictionary like
        """
        try:
            if not isinstance(config,str):
                config = dict(config)
            elif re.match('.*[:].*[@].*',config):
                h = config.split('@')
                u,p = h[0].split(':')
                config = {'user':u,'password':p}
                if '/' in h[1]:
                    config['host'],config['database'] = h[1].split('/')
                else:
                    config['host'] = h[1]
                if ':' in config['host']:
                    config['host'],config['port'] = config['host'].split(':')
            else:
                if ';' in config:
                    config = '{%s}' % config.replace(';',',')
                if '{' in config:
                    config = dict(eval(config))
        except:
            raise Exception('Wrong format in config, should be dict-like')
        return config        

    def get_attributes(self, active=False, pattern='', load=False):
        """
        Queries the database for the current list of archived attributes.
        
        Once it has been queried, result is cached unless load=True is passed.
        
        arguments:
            active: True: only attributes currently archived
                    False: all attributes, even the one not archiving anymore
            regexp: '' :filter for attributes to retrieve
        """
        if load or not self.attributes:
            self.get_attribute_id_table('*')
            
        if pattern:
            return [a for a in self.attributes if attr_match(pattern,a)]
            
        return sorted(self.attributes.keys())
    
    def get_attribute_name(self,attribute):
        """
        get attribute name as it is used in hdb++ (e.g. FQDN)
        """
        attribute = attr_translate(attribute)
        attrs = self.get_attributes(pattern=attribute, load=False)
        if len(attrs)>1:
            raise Exception('MultipleAttributeMatches')
        return attrs[0] if attrs else None

    def is_attribute_archived(self, attribute, active=False):
        """
        Returns if an attribute has values in DB.

        arguments:
            attribute: fqdn for the attribute.
            active: if true, only check for active attributes,
                    otherwise check all.
        """
        return bool(self.get_attribute_name(attribute))
    
    def get_attribute_id_table(self, attribute=''):
        """
        for each matching attribute returns name, ID and table name
        
        if no attribute or wildcard is given, all attribute info is loaded
        """
        if attribute and attribute not in ('*','%'):
            attribute = self.get_attribute_name(attribute)

        if attribute in self.attributes:
            return [self.attributes[attribute]] # return cached
        
        q = "select att_name,att_conf_id,data_type "
        q += " from att_conf as AC, att_conf_data_type as ACD where "
        q += "AC.att_conf_data_type_id = ACD.att_conf_data_type_id"
        if attribute and attribute not in ('*','%'):
            q += " and att_name like '%s'" % attribute
        
        data = [(a,i,'att_'+t) for (a,i,t) in self._query(q)]               
        self.attributes.update((str(t[0]).lower(),t) for t in data)
        return data
    
    def get_attribute_frequency(self, attribute, n = 100, values = None):
        values = values or self.get_last_attributes_values([attribute],n = n)
        n = len(values)
        if not n:
            return 0
        t0, t1 = values[0][0],values[-1][0]
        if not abs(t0-t1):
            return 0
        return float(n)/abs(t0-t1)


    def get_closer_attributes_values(self, attributes, time_bound=None, n=1, columns=[], cast = 'DOUBLE', **kwargs):
        """
        Returns the n closer values inserted around time in DB for a list of attributes.
        If n is negative it will get the last inserted values, if positive it will get the next.

        arguments:
            attribute: fqdn for the attribute.
            columns: list of columns to query, default to data_time and value_r, quality, error.
            time_bound: lower bound for data_time, if None should default to now()
            n: number of samples, default to 1.
        returns:
            [(epoch, r_value, w_value, quality, error_desc)]
        """
        logger.debug('mariadb({}).get_closer_attributes_values({},{},{})'.format(self.database,attributes,time_bound,n))
        data = {}
        order = 'desc' if n<0 else ''
        if not columns:
            columns = 'data_time, value_r, quality, att_error_desc_id'
        elif isSequence(columns):
            columns = ','.join(columns)
        columns = columns.replace(' ','')

        if cast and 'data_time' in columns.split(',') and 'cast' not in columns.lower():
            columns = columns.replace('data_time',
                'CAST(UNIX_TIMESTAMP(data_time) AS %s)' % cast)
        self._trace(columns)
        
        for attr in attributes:
            try:
                a,i,t = self.get_attribute_id_table(attr)[0]
                tdesc = str(self._query('describe %s'%t))
                tcol = ('int_time' if 'int_time' in tdesc else 'data_time')
                cols = ','.join(c for c in columns.split(',') 
                    if c.strip() in tdesc or 'cast' in c.lower())

                where = 'att_conf_id = %s' % i
                if time_bound:
                    tb = time2type(time_bound,str)
                    tb = self.str2mysqlsecs(tb) if tcol == 'int_time' else ("%s" % tb)
                    if n<0:
                        where += ' and %s <= "%s"' % (tcol, tb)
                    else:
                        where += ' and %s > "%s"' % (tcol, tb)

                q = ('select %s from %s where %s order by %s %s limit %s'
                        % (cols, t, where, tcol, 'desc' if n<0 else '', abs(n)))
                self._trace(q)
                data[attr] = self._query(q)
                self._trace(attr,'done')

            except:
                self._trace(traceback.format_exc())
                raise Exception('AttributeNotFound: %s' % a) 

        return data

    def get_mysqlsecsdiff(self,date=None):
        """
        Returns the value to be added to dates when querying int_time tables
        """
        if date is None: 
            date = time2str()
        if isinstance(date,(int,float)): 
            date = time2str(date)
        return self._query(
            "select (TO_SECONDS('%s')-62167222800) - UNIX_TIMESTAMP('%s')" 
            % (date,date))[0][0]
    
    def str2mysqlsecs(self,date):
        """ converts given date to int mysql seconds() value """
        rt = str2time(date)
        return int(rt+self.get_mysqlsecsdiff(date))
    
    def mysqlsecs2time(self,int_time,tref=0):
        """ converts a mysql secons() value to epoch """
        tref = tref or int_time
        return int_time - self.get_mysqlsecsdiff(time2str(tref))    
    
    def _correct_dates(self, start_date, stop_date=None):
        if stop_date is None:
            stop_date = now()
        start_date = time2type(start_date, str)
        stop_date = time2type(stop_date, str)
        return start_date, stop_date
    
    def _query_attribute_values(self, attribute, 
                start_date, stop_date,
                decimate=None, correlate=False, 
                columns='', cast='DOUBLE', aggr=None,
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

        a = attribute
        columns = columns or 'data_time, value_r, quality, att_error_desc_id'
        start_date,stop_date = self._correct_dates(start_date, stop_date)
        renew = params.get('renew',params.get('asynch',False))

        try:
            a,i,t = self.get_attribute_id_table(a)[0]
            self._trace('get_attribute_id_table({}) => {},{}'.format(a,i,t))
            
            int_time = 'int_time' in str(self._describe_table(t))
            if isinstance(start_date, datetime.datetime):
                start_date = date2str(start_date)
                stop_date = date2str(stop_date)
                
            tb, te = self.str2mysqlsecs(start_date),self.str2mysqlsecs(stop_date)
            b,e = (tb, te) if int_time else (
                    "'%s'" % start_date, "'%s'" % stop_date)
            
            cols = ','.join(c for c in columns.split(',') 
                            if c.strip() in str(self.tables[t]))
            
            if aggr and not "(value_r)" in cols:
                if aggr.lower() == 'maxmin':
                    cols = cols.replace('value_r', "max(value_r),min(value_r),")
                else:
                    cols = cols.replace('value_r', str(aggr)+'(value_r)')

            if 'data_time,' in cols:
                cols = cols.replace('data_time,',
                    'CAST(UNIX_TIMESTAMP(data_time) AS %s),' % cast)

            tcol = 'int_time' if int_time else 'data_time'
            q = ('select %s from %s where '
                'att_conf_id = %s and %s between %s and %s '
                % (cols, t, i, tcol, b, e))
            
            if decimate is True:
                # decimation set to limit buffer size to 1080p (plotting)
                decimate = int((te-tb)/1080.)
                
            if decimate:
                decimate = int(decimate)
                q += ' and value_r is not NULL group by '
                if int_time:
                    q += '(%s DIV %d)' % ('int_time', decimate)
                else:
                    q += '(FLOOR(%s/%d))' % (
                        'UNIX_TIMESTAMP(data_time)', decimate)
                if 'array' in t:
                    q += ',idx'
                    
            q += ' order by %s_time' % ('data','int')[int_time]
            
            self._trace(q)
            # repeated integer values will be decimated here?
            data = self._query(q, prune=decimate, renew = renew)
            self._trace('obtained data: {}'.format(len(data),'L'))
            if data:
                self._trace(str(data[-1]))
            return data
            
        except:
            import traceback
            traceback.print_exc()
            return []
            
    def get_attribute_values(self, attribute,
            start_date, stop_date=None,
            decimate=None,
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
        decimate = self.decimate if decimate is None else decimate
        attribute = self.get_attribute_name(attribute)
        start_date, stop_date = self._correct_dates(start_date,stop_date)
        fstart, fstop = str2time(start_date),str2time(stop_date)        

        self._trace('get_attribute_values({},{},{},{},{})'
            .format(attribute,start_date,stop_date,decimate,params))
        if not params.get('split',False):
            r = self.get_attributes_values([attribute], start_date, stop_date, 
                                        decimate, **params)
            #print(r.keys(),start_date,stop_date)
            return r[attribute]
        else:
            delta = float(fstop-fstart)/self.max_workers
            results,data = {},[]
            for i in range(self.max_workers):
                t0,t1 = fstart+i*delta,fstart+(i+1)*delta
                self._trace(' subquery({},{})'.format(time2str(t0),time2str(t1)))
                results[i] = self.executor.submit(
                    self._query_attribute_values,attribute,t0,t1,
                        decimate=decimate, correlate=False,
                        params=params)
            for i in range(self.max_workers):
                self._trace(i,'done')
                data.extend(results[i].result())
            return data

    def get_attributes_values(self, attributes,
            start_date, stop_date=None,
            decimate=None,
            correlate = False,
            columns = '', cast='DOUBLE',
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
                      {'timedelta0':(MIN, MAX,...)
                      , 'timedelta1':(AVG, COUNT,...)
                      ,...}
                      if None, returns raw data.
            correlate: if True, data is generated so that
                       there is available data for each timestamp of
                       each attribute.
            columns: columns separated by commas
                    time, r_value, w_value, quality, error_desc
            cast: it may be "DOUBLE" for return time as native python floats
                    or DECIMAL(17,6) to return full precission with us

        returns:
            {'attr0':[(epoch0, r_value, w_value, quality, error_desc),
            (epoch1, r_value, w_value, quality, error_desc),
            ... ],
            'attr1':[(...),(...)]}
        """
        start_date, stop_date = self._correct_dates(start_date, stop_date)
        self._trace('get_attributes_values',attributes,start_date,stop_date,correlate,columns,cast,params)
        results,data = {},{}
        self._trace(time.ctime(),time.time(),'preparing queries')
        with ThreadPoolExecutor(max_workers=len(attributes)) as ex:
            for a in attributes:
                results[a] = ex.submit(
                    self._query_attribute_values, a,
                    start_date, stop_date, decimate=decimate,
                    correlate=correlate, columns=columns, cast=cast,
                    **params)
            
            dones = []
            self._trace(time.ctime(),time.time(),'waiting results')
            while True:
                time.sleep(1e-02)
                for a in attributes:
                    if a not in dones and results[a].done():
                        dones.append(a)
                        self._trace(time.ctime(),time.time(),a+' done')
                        data[a] = results[a].result()
                        self._trace(a,len(data[a]))

                if len(dones) == len(results):
                    break

        return data
    
    
##############################################################################
           
if __name__ == '__main__':
    abstract.main(apiclass=MariadbReader,timeformatter=time2str)
    
