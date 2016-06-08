import os, sys, traceback
import WSB
from plugin import *

class AdminRepositoryPlugin(PluginObject):

    def __init__(self):
        PluginObject.__init__(self, 'adminRepository')

    def list(self):
        self.debug('list()')
        try:
            stdout = check_output('repository', 'list', '-l')
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])

    def clone(self, pkg):
        self.debug('clone(%s)' % pkg)
        try:
            p = call('repository', 'clone', pkg, '-v')
            stdout, stderr = p.communicate()
            
            return self.return_value(True, '', (p.returncode, stdout))
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
