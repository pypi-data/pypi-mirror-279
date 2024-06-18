import time
import datetime
from .utils import time2type
from enum import Enum

class Aggregator(Enum):
    """
    Enum to describe aggregation method to use.
    Note that this aggregation functions should
    be supported at the backend level.
    """
    COUNT = 1
    COUNT_ERRORS = 2
    COUNT_NAN = 3
    FIRST = 4
    LAST = 5
    MIN = 6
    MAX = 7
    AVG = 8
    STD_DEV = 9


class AbstractReader(object):
    """
    Subclass this class to create a PyTangoArchiving Reader for your specific DB

    e.g. TimeDBReader(AbstractReader)
    """

    def __init__(self, config='',**kwargs):
        '''
        Config can be an string like user:passwd@host
        or a json-like dictionary "{'user':'...','password':'...','database':}"
        '''
        try:
            self.set_default_time_type(kwargs.get('time_type',None))
            self.db = YourDb(**(config or kwargs))
        except:
            raise Exception('WrongDatabaseConfig')
        return

    def get_connection(self):
        """
        Return the connection object to avoid a client
        to open one for custom queries.
        The returned object will be implementation specific.
        """
        return self.db

    def set_default_time_type(self, time_type):
        """
        Choose the default time type to return on queries (integer, float, datetime, string)
        """
        self.default_time_type = time_type or datetime.datetime

    def get_default_time_type(self, data_time = None):
        """
        if data time is given, converts it to default_time_type
        """
        if data_time is None:
            return self.default_time_type
        else:
            return time2type(data_time, self.default_time_type)

    def get_attributes(self, active=False, pattern=''):
        """
        Queries the database for the current list of archived attributes.
        arguments:
            active: True: only attributes currently archived
                    False: all attributes, even the one not archiving anymore
            pattern: '' :filter for attributes to retrieve
        """
        return list()

    def is_attribute_archived(self, attribute, active=False):
        """
        Returns if an attribute has values in DB.

        arguments:
            attribute: fqdn for the attribute.
            active: if true, only check for active attributes,
                    otherwise check all.
        """
        return True

    def get_last_attribute_value(self, attribute, time_bound=None, n=1, columns=["data_time", "value_r"]):
        """
        Returns last value inserted in DB for an attribute

        arguments:
            attribute: fqdn for the attribute.
            columns: list of columns to query, default to data_time and value_r.
            time_bound: upper bound for data_time, if None should default to now()
            n: number of samples, default to 1.
        returns:
            [(epoch, r_value, w_value, quality, error_desc)]
        """

        return self.get_last_attributes_values([attribute], columns=columns, time_bound=time_bound, n=n)[attribute][0]

    def get_last_attributes_values(self, attributes, time_bound=None, n=1, columns=["data_time", "value_r"]):
        """
        Returns the n last values inserted before time in DB for a list of attributes

        arguments:
            attribute: fqdn for the attribute.
            columns: list of columns to query, default to data_time and value_r.
            time_bound: upper bound for data_time, if None defaults to now().
            n: number of samples, default to 1.
        returns:
            {'att1':[(epoch, r_value, w_value, quality, error_desc)],
             'att2':[(epoch, r_value, w_value, quality, error_desc)],
             ...
            }
        """

        return self.get_closer_attributes_values(attributes, time_bound=time_bound, n=(-n), columns=columns)

    def get_next_attribute_value(self, attribute, time_bound=None, n=1, columns=["data_time", "value_r"]):
        """
        Returns the n next value inserted after time in DB for an attribute

        arguments:
            attribute: fqdn for the attribute.
            columns: list of columns to query, default to data_time and value_r.
            time_bound: lower bound for data_time, if None defaults to datetime.datetime.min
            n: number of samples, default to 1.
        returns:
            [(epoch, r_value, w_value, quality, error_desc)]
        """

        return self.get_closer_attributes_values([attribute], time_bound=time_bound, n=n, columns=columns)[attribute][0]

    def get_next_attributes_values(self, attributes, time_bound=None, n=1, columns=["data_time", "value_r"]):
        """
        Returns the n next values inserted after time in DB for a list of attributes

        arguments:
            attribute: fqdn for the attribute.
            columns: list of columns to query, default to data_time and value_r.
            time_bound: lower bound for data_time, if None defaults to datetime.datetime.min
            n: number of samples, default to 1.
        returns:
            [(epoch, r_value, w_value, quality, error_desc)]
        """
        
        return self.get_closer_attributes_values(attributes, columns=columns, time_bound=time_bound, n=n)

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
        
        return {attributes[0]: n*[(time_bound, 0., 0., 0, "")]}


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
        return self.get_attributes_values([attribute], start_date, stop_date, decimate=decimate, correlate=False, **params)[attribute]

    def get_attribute_values_asynch(self, attribute,
            start_date, stop_date=None,
            decimate=None, callback=None,
            subprocess=False,
            **params):
        """
        This method executes get_attribute_values in a background process,
        triggering callback(values) when finished.

        Implementation must support the creation of a new connection.
        """
        if callback is None:
            raise Exception('Callback is required!')

        import pyhdbpp.utils as phu
        kwargs = dict(params)
        kwargs.update({'attribute':attribute, 'start_date':start_date,
            'stop_date':stop_date, 'decimate':decimate,
            'sp_timeout':300, 'asynch':True})
        if subprocess:
            r = phu.AsynchronousFunction(phu.SubprocessMethod,
                    args=(self.get_attribute_values,),
                    kwargs = kwargs, callback = callback, start = True)
        else:
            r = phu.AsynchronousFunction(self.get_attribute_values,
                kwargs = kwargs, callback = callback, start = True)
        return r

    def get_attributes_values(self, attributes,
            start_date, stop_date=None,
            decimate=None,
            correlate = False,
            columns = 'time, r_value',
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
        return {'attr0': [(time.time(), 0., 0., 0, '')]
                , 'attr1': [(time.time(), 0., 0., 0, '')]}

    def test_attributes(self,attributes,epoch=-3600):
        print('Current time: {}, {}'.format(time.time(),datetime.datetime.now()))
