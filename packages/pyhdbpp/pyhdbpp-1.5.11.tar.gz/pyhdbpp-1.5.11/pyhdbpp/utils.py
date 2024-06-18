#!/usr/bin/env python3

import sys
import argparse
import logging
import logging.handlers
import os
import datetime
import time
import importlib
import collections.abc
import traceback
import re
import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor

# Tango Utilities

def init_logger(log_level=logging.DEBUG):
    logger = logging.getLogger('hdbpp_reader')
    stdout_formatter = logging.Formatter(
        "%(asctime)s hdbpp_reader[%(process)d]:"
        " %(message)s", "%Y-%m-%d %H:%M:%S")
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(stdout_formatter)
    logger.addHandler(stdout_handler)
    logger.setLevel(log_level)
    return logger


if os.getenv('PYHDBPP_DEBUG',False):
    log_level = 'DEBUG'
else:
    log_level = os.getenv('LOG_LEVEL','WARNING')
logger = init_logger(getattr(logging,log_level.upper(),'WARNING'))


def attr_translate(model, brief=False):
    if brief and model.count('/') > 3:
        model = '*/' + '/'.join(model.rsplit('/')[-4:])
    model = str(model).lower().replace('.*','*').replace('*','%')
    if ':' not in model:
        model = '%/' + model + '$'
    return model


def attr_match(pattern, model):
    if '*' in pattern and '.*' not in pattern:
        pattern = pattern.replace('*','.*')
    pattern = pattern.lower().replace('%','.*')
    if not pattern.endswith('$'):
        pattern += '$'
    if not pattern.startswith('^'):
        pattern = '^' + pattern
    return re.match(pattern, model)


def parse_config_string(connect_str):
    """
    Parse a connect string into the various element to initiate a connection.
    Arguments:
        connect_str : str -- user:password@host:port/database
    Returns:
        dict -- dictionary of values from the connect string.
    """
    config = {}
    logger.debug('parse_config_str(%s)' % connect_str)
    if not any(c in connect_str for c in '@:/'):
        # Unparsable string, check tango properties
        config =  load_config_from_tango(connect_str)
    
    if not config:
        try:
            logger.debug('parse_config_str(%s)' % connect_str)
            config_split, config['database'] = connect_str.split('/')
            user_pass, host_port = config_split.split('@')
            i = user_pass.find(':')
            config['user'] = user_pass[:i]
            config['password'] = user_pass[i+1:]
            j = host_port.find(':')
            config['host'] = host_port[:j]
            config['port'] = host_port[j+1:]
        
        except Exception as e:
            logger.debug(traceback.print_exc())
            logger.error(str(e))
   
    return config or None


def load_config_from_tango(schema, root = 'HDB++', tango_host = '', tangodb = None):
    """
    Load config from TangoDB using tango://ObjectName.PropertyName
    Current version only accept Tango Free Properties
    """
    try:
        logger.info('load_config_from_tango({},{},{})'.format(schema,root,tango_host))
        schema = str(schema).replace('tango:','').strip('/')
        if '.' in schema:
            root,schema = schema.rsplit('.',1)
        if ':' in root:
            tango_host, root = schema.split('/')
            
        if tangodb is None:
            import tango
            if tango_host:
                tangodb = tango.Database(*tango_host.split(':'))
            else:
                tangodb = tango.Database()
                tango_host = '%s:%s' % (tangodb.get_db_host(), tangodb.get_db_port())
        
        if root.count('/')>=2:
            # Loading from device
            p = 'LibConfiguration'
            logger.debug("tangodb.get_device_property({},{})".format(root,p))
            props = tangodb.get_device_property(root,p).get(p,[])
        else:
            # Loading from free-property
            logger.debug("tangodb.get_property({},{})".format(root,schema))
            props = tangodb.get_property(root,schema)[schema]
        
        if not props:
            logger.warning('No config found for {}.{}.{}'.format(tango_host,root,schema))
            return None
        config = dict(str(l).split('=') for l in props if '=' in l)
        logger.info('%s.%s.%s.config: %s' % (tango_host, root, schema, config))
        
        if '@' in config.get('config',''):
            config.update(parse_config_string(config['config']))

        # fill missing fields
        config['database'] = config.get('database',
                            config.get('db_name',
                           config.get('dbname','hdbpp')))
        config['user'] = config.get('user','')                            
        config['password'] = config.get('password',
                            config.get('passwd',
                           config.get('token','')))
        config['config'] = config.get('config', '%s:%s@%s:%s/%s' % (
            config.get('user','user'), config.get('password','...'), 
            config.get('host','localhost'),
            config.get('port','3306'), config.get('database','hdbpp')))

        if 'apiclass' not in config:
            if 'mysql' in str(config).lower() or 'maria' in str(config).lower():
                config['apiclass'] = 'pyhdbpp.mariadb.MariaDBReader'
            elif 'timescale' in str(config).lower():
                config['apiclass'] = 'pyhdbpp.timescaledb.TimescaleDbReader'
            elif tangodb.get_property('HDB++','multidb')['multidb']:
                config['apiclass'] = 'pyhdbpp.multidb.MultiDBReader'
            print('guessing apiclass from config ... {}'.format(config['apiclass']))

        return config
    
    except Exception as e:
        logger.error(traceback.format_exc())
        return None

########################################################################
## Subprocess method from fandango
########################################################################

def SubprocessMethod(obj, *args, **kwargs):
    """
    arguments (this will be extracted from kwargs):
        object : object to extract method or callable
        sp_method :  string or callable to get from object
        sp_timeout : seconds
        sp_callback : optional method to be called

    Method for executing reader.get_attribute_values in background
    with a timeout (30 s by default)

    In fact, it allows to call any object method passed by name;
    or just pass a callable as object.

    This method could be embedded in a thread with very high timeout
    to trigger a callback when data is received.

    This advanced behavior can be implemented using AsynchronousFunction

    example:
    reader,att = PyTangoArchiving.Reader(),'just/some/nice/attribute'
    dates = '2014-06-23 00:00','2014-06-30 00:00'
    values = SubprocessMethod(reader,'get_attribute_values',
        att,*dates,timeout=10.)

    or

    def callback(v):
        print('>> received %d values'%len(v))

    #sp_callback does not override callback
    SubprocessMethod(reader,
        'get_attribute_values',att,*dates,
        sp_timeout=10.,callback=callback)

    >> received 414131 values
    """
    sp_method = kwargs.pop('sp_method',None)
    sp_timeout = kwargs.pop('sp_timeout',30.)
    sp_callback = kwargs.pop('sp_callback',None)

    #Using pipe because it's faster than queue and more efficient
    local,remote = multiprocessing.Pipe(False)

    def do_it(o,m,conn,*a,**k):
        try:
            if None in (o, m):
                m = o or m
            elif isinstance(m,str):
                m = getattr(o, m)
            # print m,a,k
            conn.send(m(*a, **k))
            # conn.close()
        except Exception as e:
            traceback.print_exc()
            conn.send(e)

    args = (obj,sp_method,remote)+args
    proc = multiprocessing.Process(target=do_it,args=args,kwargs=kwargs)
    #print('New Process(%s)' % str(do_it))
    proc.daemon = True
    proc.start()
    t0 = time.time()
    result = None
    event = threading.Event()

    while time.time()<t0+sp_timeout:
        if local.poll():
            result = local.recv()
            break
        event.wait(0.1)

    local.close(), remote.close()  # close pipes
    #print("Join Process(%s)" % str(do_it))
    proc.terminate(), proc.join()  # close process

    if time.time() > t0 + sp_timeout:
        result = Exception("TimeOut(%s,%s)!" % (str(obj), sp_timeout))
    if sp_callback:
        sp_callback(result)
    elif isinstance(result, Exception):
        raise result

    return result


class AsynchronousFunction(threading.Thread):
    """This class executes a given function in a separate thread
    When finished it sets True to self.finished, a threading.Event object
    Whether the function is thread-safe or not is something that must be managed in the caller side.
    If you want to autoexecute the method with arguments just call:
    t = AsynchronousFunction(lambda:your_function(args),start=True)
    while True:
        if not t.isAlive():
            if t.exception: raise t.exception
            result = t.result
            break
        print 'waiting ...'
        threading.Event().wait(0.1)
    print 'result = ',result
    """
    __instances__ = []

    def __init__(
        self,
        function,
        args=None,
        kwargs=None,
        callback=None,
        pause=0.0,
        start=False,
    ):
        """
        It just creates the function object.
        If pause!=0 or start=True, the function will be called
        """
        self.function = function
        self.result = None
        self.exception = None
        self.finished = threading.Event()
        self.finished.clear()
        threading.Thread.__init__(self)
        self.callback = callback
        self.pause = pause
        self.wait = self.finished.wait
        self.daemon = False
        self.args = args or []
        self.kwargs = kwargs or {}
        if self.pause or start:
            self.start()

    def run(self):
        AsynchronousFunction.__instances__.append(self)
        #with get_tango_thread_context():
        try:
            if self.pause:
                self.wait(self.pause)
            self.result = self.function(*self.args, **self.kwargs)
        except Exception as e:
            self.result = None
            self.exception = e
        # Not really needed, simply call AsynchronousFunction.isAlive()
        # to know if it has finished
        self.finished.set()
        if self.callback:
            try:
                self._bg = AsynchronousFunction(
                    self.callback,
                    start=True,
                    args=[self.result] if self.result is not None else [],
                )
            except:
                traceback.print_exc()

def TimedThreadPoolExecution(method,arguments=[],executor=None,timeout_s=None, wait=1e-3, default=None, workers=None):
    """
        Method can be a callable or a dictionary {key:callable}
        Argument list will be a dict of {key:(args,kwargs)} to be passed to method
        The length of argument_list will be the number of workers if no executor is passed

        Example:
            methods = {k:db.get_attributes for k,db in self.readers.items()}
            args = {k:([],{}) for k in self.readers}
            data = TimedThreadPoolExecution(methods,args,self.executor,default=[])
            for k,v in data.items():
                self.attributes[k] = [a.lower() for a in v]

            dbs = self.get_connection(attribute, epoch = time.time())
            logger.debug('multidb: {} archived by {}'.format(attribute,dbs.keys()))
            methods = {k:db.get_closer_attributes_values for k,db in dbs.items()}
            args = {k:(([attribute],),{'time_bound':time_bound,'n':n}) for k in methods}
            values = TimedThreadPoolExecution(methods,args,self.executor,default=None,timeout_s=60)
            values = {k:v[attribute] for k,v in values.items()}

    """
    t00 = time.time()
    timeout_s = timeout_s or 5*86400.

    if isinstance(method,dict):
        keys = list(method.keys())
    elif isinstance(arguments,dict):
        keys = list(arguments.keys())
    elif isinstance(arguments,list):
        arguments = {t[0]:t for t in arguments}
        keys = list(arguments.keys())
    else:
        keys = []

    if workers is 1:
        #Forcing single-threaded execution
        executor = None
    else:
        workers = len(keys) or 1
        executor = executor or ThreadPoolExecutor(max_workers=workers)

    logger.debug('TimedThreadPoolExecution({},n={})'.format(executor,workers))

    t0 = time.time()

    futures = {}
    for k in keys:
        v = arguments[k] if isinstance(arguments,dict) else arguments
        if isSequence(arguments):
            if len(arguments)==2 and isinstance(arguments[-1],dict):
                args, kwargs = (v[0],v[1])
            else:
                args, kwargs = arguments, {}
        elif isinstance(arguments,dict):
            args,kwargs = [],arguments
        else:
            args = [arguments]

        kwargs = kwargs or {}
        m = method[k] if isinstance(method,dict) else method
        # print(m,args,kwargs)
        # print(m(*args,**kwargs))
        if executor:
            futures[k] = executor.submit(m,*args,**kwargs)
        else:
            futures[k] = m

    results = {}
    pending = list(futures.keys())
    while len(pending) and time.time() < (t0+timeout_s):
        for k,v in futures.items():
            if k in pending:
                if executor and v.done():
                    try:
                        results[k] = v.result()
                    except Exception as e:
                        print('TimedThreadPoolExecution failed:',k,e)
                        results[k] = default
                elif not executor:
                    # unthreaded execution
                    results[k] = v(*args,**kwargs)
                if k in results:
                    pending.remove(k)
                    logger.debug('ttpe(%s): %s done' % (executor,k))
        time.sleep(wait)

    if pending:
        logger.warning('ThreadPoolExecution:Unable to get {} results in less than {} seconds'
                       .format(pending,timeout_s))
        for k in pending:
            results[k] = default_value

    logger.debug('TimedThreadPoolExecution({},n={}) finished in {} seconds'
                 .format(executor,workers,time.time()-t00))
    return results
    
########################################################################
# Time and String conversion methods from Fandango
########################################################################

import time, datetime, re, traceback

END_OF_TIME = 1024*1024*1024*2-1 #Jan 19 04:14:07 2038

TIME_UNITS = { 'ns': 1e-9, 'us': 1e-6, 'ms': 1e-3, '': 1, 's': 1, 'm': 60, 
    'h': 3600, 'd': 86.4e3, 'w': 604.8e3, 'M': 30*86.4e3, 'y': 31.536e6 }
TIME_UNITS.update((k.upper(),v) for k,v in list(TIME_UNITS.items()) if k!='m')

#@todo: RAW_TIME should be capable to parse durations as of ISO 8601
RAW_TIME = ('^(?:P)?([+-]?[0-9]+[.]?(?:[0-9]+)?)(?: )?(%s)$'
            % ('|').join(TIME_UNITS)) # e.g. 3600.5 s

MYSQL_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
ISO_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

global DEFAULT_TIME_FORMAT
DEFAULT_TIME_FORMAT = MYSQL_TIME_FORMAT

ALT_TIME_FORMATS = [ ('%s%s%s' % (
    date.replace('-',dash),separator if hour else '',hour)) 
        for date in ('%Y-%m-%d','%y-%m-%d','%d-%m-%Y',
                        '%d-%m-%y','%m-%d-%Y','%m-%d-%y')
        for dash in ('-','/')
        for separator in (' ','T')
        for hour in ('%H:%M','%H:%M:%S','%H','')]


def set_default_time_format(dtf, test = True):
    """
    Usages:
    
        set_default_time_format('%Y-%m-%d %H:%M:%S')
            or
        set_default_time_format(ISO_TIME_FORMAT)
        
    """
    if test:
        str2time(time2str(cad = dtf), cad = dtf)
    global DEFAULT_TIME_FORMAT
    DEFAULT_TIME_FORMAT = dtf


def now():
    return time.time()


def time2tuple(epoch=None, utc=False):
    if epoch is None: epoch = now()
    elif epoch<0: epoch = now()-epoch
    if utc:
        return time.gmtime(epoch)
    else:
        return time.localtime(epoch)


def tuple2time(tup):
    return time.mktime(tup)


def date2time(date,us=True):
    """
    This method would accept both timetuple and timedelta
    in order to deal with times coming from different
    api's with a single method
    """
    try:
      t = tuple2time(date.timetuple())
      us = us and getattr(date,'microsecond',0)
      if us: t+=us*1e-6
      return t
    except Exception as e:
      try:
        return date.total_seconds()
      except:
        raise e


def date2str(date, cad = '', us=False):
    #return time.ctime(date2time(date))
    global DEFAULT_TIME_FORMAT
    cad = cad or DEFAULT_TIME_FORMAT
    t = time.strftime(cad, time2tuple(date2time(date)))
    us = us and getattr(date,'microsecond',0)
    if us: t+='.%06d'%us
    return t


def time2date(epoch=None):
    if epoch is None: epoch = now()
    elif epoch<0: epoch = now()-epoch
    return datetime.datetime.fromtimestamp(epoch)


def utcdiff(t=None):
    return now() - date2time(datetime.datetime.utcnow())  


def time2str(epoch=None, cad='', us=False, bt=True,
             utc=False, iso=False):
    """
    cad: introduce your own custom format (see below)
    use DEFAULT_TIME_FORMAT to set a default one
    us=False; True to introduce ms precission
    bt=True; negative epochs are considered relative from now
    utc=False; if True it converts to UTC
    iso=False; if True, 'T' will be used to separate date and time
    
    cad accepts the following formats:
        (see https://strftime.org/
        https://docs.python.org/3/library/datetime.html#format-codes)
    
    %a  Locale's abbreviated weekday name
    %A 	Locales full weekday name
    %b 	Locales abbreviated month name
    %B 	Locales full month name
    %c 	Locales appropriate date and time representation
    %d 	Day of the month as a decimal number [01,31]
    %H 	Hour (24-hour clock) as a decimal number [00,23]
    %I 	Hour (12-hour clock) as a decimal number [01,12]
    %j 	Day of the year as a decimal number [001,366]
    %m 	Month as a decimal number [01,12]
    %M 	Minute as a decimal number [00,59]
    %p 	Locales equivalent of either AM or PM
    %S 	Second as a decimal number [00,61]
    %U 	Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]
    All days in a new year preceding the first Sunday are considered to be in week 0
    %w 	Weekday as a decimal number [0(Sunday),6]
    %W 	Week number of the year (Monday as the first day of the week) as a decimal number [00,53]
    All days in a new year preceding the first Monday are considered to be in week 0
    %x 	Locales appropriate date representation
    %X 	Locales appropriate time representation
    %y 	Year without century as a decimal number [00,99]
    %Y 	Year with century as a decimal number
    %Z 	Time zone name (no characters if no time zone exists)
    %% 	A literal '%' character
    """
    if epoch is None:
        epoch = now()
    elif bt and epoch < 0:
        epoch = now()+epoch
    global DEFAULT_TIME_FORMAT
    if cad:
        cad = 'T'.join(cad.split(' ',1)) if iso else cad
    else:
        cad = ISO_TIME_FORMAT if iso else DEFAULT_TIME_FORMAT

    t = time.strftime(cad,time2tuple(epoch,utc=utc))
    if us:
        v = '.%06d'%(1e6 * (epoch % 1))
        if isinstance(us,int):
            v = v[:-(6-us)]
        t += v
    return t


epoch2str = time2str


def str2time(seq='', cad='', throw=True, relative=False):
    """ 
    :param seq: Date must be in ((Y-m-d|d/m/Y) (H:M[:S]?)) format or -N [d/m/y/s/h]
    
    See RAW_TIME and TIME_UNITS to see the units used for pattern matching.
    
    The conversion itself is done by time.strptime method.
    
    :param cad: You can pass a custom time format
    :param relative: negative times will be converted to now()-time
    :param throw: if False, None is returned instead of exception
    """
    try: 
        if seq in (None,''): 
            return time.time()
        if 'NOW-' in seq:
            seq,relative = seq.replace('NOW',''),True
        elif seq=='NOW':
            return now()
        
        t, seq = None, str(seq).strip()
        if not cad:
            m = re.match(RAW_TIME,seq) 
            if m:
                #Converting from a time(unit) format
                value,unit = m.groups()
                t = float(value)*TIME_UNITS[unit]
                return t # must return here
                
        #Converting from a date format
        ms = re.match('.*(\.[0-9]+)$',seq) #Splitting the decimal part
        if ms: 
            ms,seq = float(ms.groups()[0]),seq.replace(ms.groups()[0],'')

        if t is None:
            #tf=None will try default system format
            global DEFAULT_TIME_FORMAT
            time_fmts = ([cad] if cad else 
                         [DEFAULT_TIME_FORMAT,None] + ALT_TIME_FORMATS)
            for tf in time_fmts:
                try:
                    tf = (tf,) if tf else () 
                    t = time.strptime(seq,*tf)
                    break
                except: 
                    pass
                
        v = time.mktime(t)+(ms or 0)
        if relative and v<0:
            v = now()-v
        return v
    except: 
        if throw:
            raise Exception('PARAMS_ERROR','unknown time format: %s' % seq)
        else:
            return None
        

str2epoch = str2time


def time2gmt(epoch=None):
    if epoch is None: epoch = now()
    return tuple2time(time.gmtime(epoch))


def timezone():
    t = now()
    from past import old_div
    return old_div(int(t-time2gmt(t)),3600)


# Auxiliary methods:

def ctime2time(time_struct):
    try:
      return (float(time_struct.tv_sec)+1e-6*float(time_struct.tv_usec))
    except:
      return -1


def mysql2time(mysql_time,us=True):
    try:
      return date2time(mysql_time,us=us)
      #t = time.mktime(mysql_time.timetuple())
    except:
      return -1

def time2type(data_time, time_type):
    """
    expected formats: str, datetime, int/float, tuple

    Usage:

    In [7]: pyhdbpp.time2type(pyhdbpp.datetime.datetime.now(),str)
    Out[7]: '2024-06-04 17:07:51'

    In [8]: pyhdbpp.time2type(pyhdbpp.datetime.datetime.now(),float)
    Out[8]: 1717513676.449958

    In [9]: pyhdbpp.time2type(pyhdbpp.time2type(pyhdbpp.datetime.datetime.now(),float),pyhdbpp.datetime)
    Out[9]: datetime.datetime(2024, 6, 4, 17, 8, 10, 787057)

    """
    # print('time2type', data_time, time_type)
    if time_type is datetime:
        time_type = datetime.datetime
    elif time_type is time:
        time_type = float
    if isinstance(data_time, time_type):
        return data_time
    if isinstance(data_time,(int,float)):
        if data_time <= 0:
            data_time = time.time() + data_time
        else:
            data_time = data_time
    elif isinstance(data_time, datetime.datetime):
        data_time = date2time(data_time)
    elif isinstance(data_time, str):
        data_time = str2time(data_time)
    elif hasattr(data_time, 'tv_sec'):
        data_time = ctime2time(data_time)
    else:
        # Dictionaries and sequences treated recursively
        if isinstance(data_time,tuple): #and all(isinstance(t,int) for t in data_time[:5])
            try:
                data_time = tuple2time(data_time)
                return time2type(data_time, time_type)
            except:
                # is not a timetuple, just continue
                pass

        if hasattr(data_time,'keys'):
            return {k : time2type(v, time_type)
                    for k, v in data_time.items()}

        elif isSequence(data_time):
            if len(data_time):
                # Trying to avoid recursion if possible
                if isinstance(data_time[0], time_type):
                    # if data_time is already (time, value, ...) tuple
                    return data_time
                elif not isSequence(data_time[0]):
                    # data_time is sequence, but element 0 is not time_type nor seq
                    data_time = list(data_time)
                    data_time[0] = time2type(data_time[0], time_type)
                    return data_time
                else:
                    # if data_time is a nested sequence
                    if len(data_time[0]):
                        if isinstance(data_time[0][0], time_type):
                            # if data_time is a [(time,value)] list
                            return data_time
                    else:
                        return data_time #empty list
            else:
                return data_time #empty list

            # It will get here only for non optimized lists
            return [time2type(t, time_type) for t in data_time]

    # Returning standard types
    if time_type is time:
        time_type = float
    if time_type in (int, float):
        return time_type(data_time)
    elif time_type in (datetime, datetime.datetime):
        return time2date(data_time)
    elif time_type is str:
        return time2str(data_time)
    elif time_type in (list, tuple):
        return time2tuple(data_time)

WILDCARDS = "^$*+?{\|"  # r'[]()


def is_regexp(seq, wildcards=WILDCARDS):
    """
    This function is just a hint, use it with care.
    This function is an overload of the one in fandango, for convenience
    """
    return any(c in wildcards for c in seq)

def isString(seq):
    """
    Returns True if seq type can be considered as string

    @TODO: repleace by this code:
      import types;isinstance(seq,types.StringTypes)
    """
    if isinstance(seq, (str,bytes,bytearray)):
        return True  # It matches most python str-like classes
    if any(
        s in str(type(seq)).lower()
        for s in (
            "vector",
            "array",
            "list",
        )
    ):
        return False
    if "qstring" == str(type(seq)).lower():
        return True  # It matches QString
    return False

def isNumber(seq):
    # return operator.isNumberType(seq)
    if isinstance(seq, bool):
        return False
    try:
        float(seq)
        return True
    except:
        return False

def isDate(seq, cad=""):
    try:
        seq and str2time(seq, cad=cad)
    except:
        return False
    else:
        return bool(seq)

def isCallable(obj):
    return callable(obj)

def isSequence(seq, iterators=True, **kwargs):
    """
    It excludes Strings, dictionaries but includes generators
    unless iterators=False is set as argument,
    otherwise only fixed-length objects are accepted
    """
    if isinstance(seq, (list, set, tuple)):
        return True
    if isString(seq):
        return False
    if hasattr(seq, "items"):
        return False
    if iterators:
        if hasattr(seq, "__iter__"):
            return True
    elif hasattr(seq, "__len__"):
        return True
    return False

def export_to_text(table, order=None, **kwargs):
    """
    It will convert a [(timestamp,value)] array in a CSV-like text.
    Order will be used to set the order to data columns (date and timestamp will be always first and second).

    Other parameters are available:

      sep : character to split values in each row
      arrsep : character to split array values in a data column
      linesep : characters to insert between lines

    """
    sep = kwargs.get("sep", "\t")
    arrsep = kwargs.get("arrsep", kwargs.get("separator", ", "))
    linesep = kwargs.get("linesep", "\n")

    start = time.time()
    if not hasattr(table, "keys"):
        table = {"attribute": table}
    if not order or not all(k in order for k in table):
        keys = list(sorted(table.keys()))
    else:
        keys = sorted(list(table.keys()), key=order.index)

    csv = sep.join(["date", "time"] + keys) + linesep

    def value_to_text(s):
        v = (
            str(s) if not isSequence(s) else arrsep.join(map(str, s))
        ).replace("None", "")
        return v

    # def time_to_text(t):
    #     # Taurus Trend timestamp format
    #     return (time2str(t, cad="%Y-%m-%d_%H:%M:%S")
    #             + (".{0:0.3f}".format((t % 1)))).lstrip("0")

    ml = min(len(v) for v in list(table.values()))
    for i in range(ml):  # len(table.values()[0])):
        csv += sep.join(
            [
                #time_to_text(list(table.values())[0][i][0]),
                time2str(list(table.values())[0][i][0],ISO_TIME_FORMAT,us=3),
                str(list(table.values())[0][i][0]),
            ]
            + [value_to_text(table[k][i][1]) for k in keys]
        )
        csv += linesep

    print(("Text file generated in %d milliseconds" % (1000 * (time.time() - start))))
    return csv
