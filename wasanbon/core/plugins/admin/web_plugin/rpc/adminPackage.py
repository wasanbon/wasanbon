import os, sys, traceback
import WSB
from plugin import *

class AdminPackagePlugin(PluginObject):

    def __init__(self):
        PluginObject.__init__(self, 'adminPackage')

    def list(self, running):
        self.debug('list(running=%s)' % running)
        try:
            sub = ['package', 'list', '-l']
            if running:
                sub = sub + ['-r']
            stdout = check_output(*sub)
            #open('log.txt', 'w').write(stdout)
            return self.return_value(True, '', (stdout))
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])

    def running_list(self):
        self.debug('running_list()')
        try:
            stdout = check_output('package', 'list', '-l', '-r')
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])


    def delete(self, pkg):
        self.debug('delete(%s)' % pkg)
        try:
            stdout = check_output('package', 'delete', pkg, '-r').strip()
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
