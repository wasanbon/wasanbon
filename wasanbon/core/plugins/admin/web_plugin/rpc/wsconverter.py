import os, sys, traceback
import WSB
from plugin import *

class WSConverterPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'wsconverter')

    def start(self, port):
        """ Start WebSocket Converter Process. Returns Process ID and Name."""
        p = call('wsconverter', 'start', '-p', str(port))
        return self.return_value(True, '', ('wsconverter', p.pid))

    def stop(self):
        """ Stop WebSocket Converter Process. """
        p = call('wsconverter', 'stop')
        return self.return_value(True, '', True)

