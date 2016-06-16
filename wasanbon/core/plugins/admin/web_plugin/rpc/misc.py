import os, sys
import WSB
from plugin import *


class MiscPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'misc')
    
    def echo(self, msg):
        self.debug('echo(%s)' % msg)
        return self.return_value(True, '', msg)


    def version(self):
        self.debug('version')
        stdout = check_output('version')
        platform_version = stdout.split('\n')[0].split()[-1]
        wasanbon_version = stdout.split('\n')[1].split()[-1]
        res = {'platform':platform_version, 
               'version':wasanbon_version}
        return self.return_value(True, '', res)

    def status(self):
        self.debug('status')
        stdout = check_output('status')
        dic = {}
        for line in stdout.split('\n'):
            if len(line.strip()) == 0:
                continue
            if line.strip().startswith('- Checking'):
                continue
            name = line.split()[1]
            status = line.split()[-1]
            dic[name] = status
        return self.return_value(True, '', dic)
