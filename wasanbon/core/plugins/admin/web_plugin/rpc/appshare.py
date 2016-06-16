import os, sys, traceback
import WSB
from plugin import *


class AppsharePlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'appshare')
    
    def echo(self, msg):
        self.debug('echo(%s)' % msg)
        return self.return_value(True, '', msg)

    def list(self):
        self.debug('list')
        stdout = check_output('web', 'list_appshare')
        import yaml
        d = yaml.load(stdout)
        return self.return_value(True, '', d)

    def download(self, appName, version):
        self.debug('download %s %s' % (appName, version))
        cmd = ['web', 'download_appshare', appName]
        if len(version) > 0:
            cmd = cmd + ['-s', version]
        stdout = check_output(*cmd).strip()
        return self.return_value(True, '', True)

