import os, sys, traceback
import WSB
from plugin import *

class MgrSystemPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'mgrSystem')

    def chdir_pkg_and_do(self, pkg, function):
        """ Change directory to pkg. When pkg not found, error raised. """
        dir = check_output('package', 'directory', pkg).strip()
        cwd_ = os.getcwd()
        os.chdir(dir)
        retval = function()
        os.chdir(cwd_)
        return retval


    def run(self, packageName, systemName, build, activate):
        """ Run System """
        self.debug('run(%s, %s, %s, %s)' % (packageName, systemName, build, activate))
        
        def _run():
            try:
                sub = ['system', 'run', '-v']
                if not activate:
                    sub = sub + ['-q']
                if not build:
                    sub = sub + ['-p']
                
                p = mgr_call(*sub)
                return self.return_value(True, '', True)
            except Exception, ex:
                traceback.print_exc()
        return self.chdir_pkg_and_do(packageName, _run)

    def terminate(self, packageName):
        """ Terminate System """
        self.debug('terminate(%s)' % (packageName))
        
        def _terminate():
            try:
                sub = ['system', 'terminate', '-v']
                p = mgr_call(*sub)
                return self.return_value(True, '', True)
            except Exception, ex:
                traceback.print_exc()
        return self.chdir_pkg_and_do(packageName, _terminate)

    def is_running(self, pkg):
        """ Check System is running or not """
        self.debug('is_running(%s)' % (pkg))
        
        def _is_running():
            try:
                sub = ['system', 'is_running']
                stdout = check_mgr_output(*sub).strip()
                return self.return_value(True, '', stdout == 'True')
            except Exception, ex:
                traceback.print_exc()
        return self.chdir_pkg_and_do(pkg, _is_running)



