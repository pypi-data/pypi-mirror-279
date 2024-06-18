import yaml
import time
from qolab.file_utils import get_next_data_file
from qolab.tsdb import tsdb_append_metric_for_class_setter_or_getter

class BasicInstrument:
    """ This is the most basic instrument class """
    def __init__(self, config={}, device_nickname=None, tsdb_ingester=None):
        """ 
        device_nickname - used to separate similar instruments,
                          also used as a tag in Time Series DB (TSDB) logging,
                          if not set we fallbacl to 'Device type'
        tsdb_ingester   - used to log to TSDB if not set, the log entry is skipped
        config          - used to add or override default entries
        """
        self.config = {}
        self.config['Device type'] = 'Basic Instrument'
        self.config['Device model'] = 'Model is unset'
        self.config['DeviceId'] = None
        self.config['DeviceNickname'] = device_nickname; # to separate similar instruments
        self.config['FnamePrefix'] = 'basicInstrument'
        self.config['SavePath'] = './data'
        for k, v in config.items():
            self.config[k]=v
        self.tsdb_ingester = tsdb_ingester
        # deviceProperties must have 'get' and preferably 'set' methods available,
        # i.e. 'SampleRate' needs getSampleRate() and love to have setSampleRate(value)
        # they will be used to obtain config and set device according to it
        # self.deviceProperties = {'SampleRate', 'TimePerDiv', 'TrigDelay', };
        self.deviceProperties = {'TimeStamp'}

    def __repr__(self):
        s = ''
        s += f'{self.__class__.__name__}('
        s += 'config={'
        cstr=[]
        for k, v in self.config.items():
            if v is not None:
                cstr.append(
                    f"'{k}'"
                    ': '
                    f"'{v}'")
        s += ', '.join(cstr)
        s += '}'
        if self.tsdb_ingester is not None:
            s += f', tsdb_ingester={self.tsdb_ingester}'
        s += ')'
        return(s)

    def tsdb_append(f):
        return tsdb_append_metric_for_class_setter_or_getter()(f)

    def getChannelsConfig(self):
        chconfig = {}
        if not hasattr(self, 'numberOfChannels'):
            return chconfig

        for chNum in range(1, self.numberOfChannels+1):
            chNconfig = {}
            for p in self.channelProperties:
                getter = f'getChan{p}'
                if  not hasattr(self, getter):
                    print(f'warning no getter for {p}, i.e. {getter} is missing')
                    continue
                res = getattr(self, getter)(chNum) 
                chNconfig[p] = res
            chconfig[chNum] = chNconfig
        return chconfig

    def getConfig(self):
        config = self.config.copy()
        dconfig = {}
        for p in self.deviceProperties:
            if hasattr(self, p) or hasattr(type(self), p):
                dconfig[p] = getattr(self, p)
                continue
            getter = f'get{p}'
            if  not hasattr(self, getter):
                print(f'warning no getter for {p}, i.e. {getter} is missing')
                continue
            res = getattr(self, getter)() 
            dconfig[p] = res
        config['DeviceConfig'] = dconfig
        if not hasattr(self, 'numberOfChannels'):
            return config
        config['ChannelsConfig']=self.getChannelsConfig();
        return config

    def setConfig(self, cfg):
        new_config = cfg.copy()
        device_config = new_config.pop('DeviceConfig')
        self.config.update(new_config)
        for p, v in device_config.items():
            setter = f'set{p}'
            if  hasattr(self, setter):
                # we have something like setProperty
                getattr(self, setter)(v) 
                continue
            if hasattr(self, p) or hasattr(type(self), p):
                # we have attribute Property
                setattr(self, p, v)
                continue
            print(f'warning: both {setter} and attribute {p} are missing, skipping {p}')
            # self.deviceProperties.add(p)
            # setattr(self, p, v)

    def getTimeStamp(self):
        return  time.strftime("%Y/%m/%d %H:%M:%S")

    def getHeader(self):
        header = yaml.dump(self.getConfig(), default_flow_style=False, sort_keys=False)
        header = header.split('\n')
        return header
    
    def getNextDataFile(self, extention='dat'):
        fname = get_next_data_file(self.config['FnamePrefix'], self.config['SavePath'], extention=extention)
        return fname

