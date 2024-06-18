"""
Provide basic class to operate scope
Created by Eugeniy E. Mikhailov 2021/11/29
"""
from qolab.hardware.scpi import SCPIinstr
from qolab.hardware.basic import BasicInstrument
from qolab.data.trace import TraceSetSameX
import yaml

class Scope(BasicInstrument):

    # Minimal set of methods to be implemented by a scope.
    def __init__(self, *args, **kwds):
        BasicInstrument.__init__(self, *args, **kwds)
        self.config['Device type']='Scope'
        self.config['Device model'] = 'Generic Scope Without Hardware interface'
        self.config['FnamePrefix'] = 'scope'
        self.numberOfChannels = 0
        # deviceProperties must have 'get' and preferably 'set' methods available,
        # i.e. 'SampleRate' needs getSampleRate() and love to have setSampleRate(value)
        # they will be used to obtain config and set device according to it
        self.deviceProperties.update({'SampleRate', 'TimePerDiv', 'TrigDelay', 'TriggerMode', 'Roll', 'Run' })
        # same is applied to channelProperties but we need setter/getter with channel number
        # i.e.  VoltsPerDiv ->  getChanVoltsPerDiv(chNum) and setSampleRate(chNum, value)
        self.channelProperties = {'VoltsPerDiv', 'VoltageOffset', }

    def getTrace(self, chNum, availableNpnts=None, maxRequiredPoints=None, decimate=True):
        # Should work with minimal arguments list 
        # but might be faster if parameters provided: less IO requests
        # old_trg_mode = self.getTriggerMode()
        # self.setTriggerMode('STOP'); # to get synchronous channels
        raise NotImplementedError( 'getTrace function is not implemented' )
        # if old_trg_mode != "STOP":
            # short speed up here with this check
            # self.setTriggerMode(old_trg_mode)

    def getTriggerMode(self):
        # we expect NORM, AUTO, SINGLE, STOP
        raise NotImplementedError( 'getTriggerMode function is not implemented' )

    def setTriggerMode(self, mode):
        # we expect NORM, AUTO, SINGLE, STOP
        raise NotImplementedError( 'setTriggerMode function is not implemented' )

    def getAllTraces(self, availableNpnts=None, maxRequiredPoints=None, decimate=True):
        allTraces=TraceSetSameX('scope traces')
        allTraces.config['tags']['DAQ']=self.getConfig()
        old_trg_mode = self.getTriggerMode()
        self.setTriggerMode('STOP'); # to get synchronous channels
        for chNum in range(1, self.numberOfChannels+1):
            allTraces.addTrace( self.getTrace(chNum, availableNpnts=availableNpnts, maxRequiredPoints=maxRequiredPoints, decimate=decimate) )
        # restore scope to the before acquisition mode
        if old_trg_mode != "STOP":
            # short speed up here with this check
            self.setTriggerMode(old_trg_mode)
        return( allTraces )

    def plot(self, **kwargs):
        allTraces=self.getAllTraces(**kwargs)
        allTraces.plot()

    def save(self, fname=None, item_format='e', availableNpnts=None, maxRequiredPoints=None, decimate=True, extention='dat'):
        allTraces = self.getAllTraces(availableNpnts=availableNpnts, maxRequiredPoints=maxRequiredPoints, decimate=decimate)
        allTraces.config['item_format']=item_format
        if fname is None:
            fname = self.getNextDataFile(extention=extention)
        allTraces.save(fname)
        print(f'Data saved to: {fname}')
        return(fname)


class ScopeSCPI(SCPIinstr, Scope):
    """     
    Do not instantiate directly, use
    rm = pyvisa.ResourceManager()
    ScopeSCPI(rm.open_resource('TCPIP::192.168.0.2::INSTR'))
    """
    def __init__(self, resource, *args, **kwds):
        SCPIinstr.__init__(self, resource)
        Scope.__init__(self, *args, **kwds)
        self.config['DeviceId'] = str.strip(self.idn)

from .sds1104x import SDS1104X
from .sds2304x import SDS2304X

