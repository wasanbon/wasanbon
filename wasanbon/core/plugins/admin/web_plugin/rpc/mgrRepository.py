import os, sys, traceback
import WSB
from plugin import *

class MgrRepositoryPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'mgrRepository')

    def chdir_pkg_and_do(self, pkg, function):
        """ Change directory to pkg. When pkg not found, error raised. """
        dir = check_output('package', 'directory', pkg).strip()
        cwd_ = os.getcwd()
        os.chdir(dir)
        retval = function()
        os.chdir(cwd_)
        return retval

        
    def list(self, pkg):
        """ Listing RT-components in package $pkg """
        self.debug('list(%s)' % pkg)
        def _list():
            try:
                sub = ['repository', 'list', '-l'] 
                stdout = check_mgr_output(*sub)
                return self.return_value(True, '', stdout)
            except Exception, ex:
                traceback.print_exc()
                return self.return_value(False, 'Exception: %s' % str(ex), [])
        return self.chdir_pkg_and_do(pkg, _list)

    def clone(self, pkg, rtc):
        """ Cloning RT-component $rtc in package $pkg """
        self.debug('clone(%s, %s)' % (pkg, rtc))
        def _clone():
            try:
                sub = ['repository', 'clone', rtc] 
                p = mgr_call(*sub)
                stdout, stderr = p.communicate()
                #stdout = check_mgr_output(*sub)
                return self.return_value(True, '', (p.returncode, stdout))
            except Exception, ex:
                traceback.print_exc()
                return self.return_value(False, 'Exception: %s' % str(ex), [])
        return self.chdir_pkg_and_do(pkg, _clone)

    def repositories(self, pkg):
        res = WSB.getRtcRepositoryList(pkg)
        return [True, res]

    def repository_pull(self, package, rtc):
        res = WSB.pullRTCRepository(package, rtc)
        return [True, res]

    def repository_push(self, package, rtc):
        res = WSB.pushRTCRepository(package, rtc)
        return [True, res]

    def repository_commit(self, package, rtc, comment):
        res = WSB.commitRTCRepository(package, rtc, comment)
        return [True, res]

    def longlist(self,pkg):
        res = WSB.getRTCLongList(pkg)
        return [True, res]


    def profile(self, pkg, rtc):
        res = WSB.getRTCProfile(pkg, rtc)
        return [True, res]
