import os, sys, traceback, time
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


filepath = os.path.join(os.getcwd(), 'test_report.yaml')
pkg_name = 'hogehoge1'

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.binder', 'admin.repository', 'mgr.rtc', 'mgr.system' ]


    def test(self, pack, *args):
        #print 'test function called with arg %s, %s' % (repr(pack), args)
        log('#'*24)
        log('Test %s :' % args[0])
        command = 'wasanbon-admin.py' if pack == admin else './mgr.py'
        cmd = command + ' '
        for arg in args:
            cmd = cmd + arg + ' '
        log('  cmd : %s' % cmd)
        try:
            argv = [arg.strip() for arg in cmd.split(' ') if len(arg.strip()) != 0]
            retval = getattr(getattr(pack, args[0]), args[1])(argv)
            log('  retval : %s' % retval)
        except Exception ,e:
            traceback.print_exc()
            log('  exception : %s' % repr(e))
        log('#'*24)            

    @manifest
    def __call__(self, argv):
        """ Manifesting __call__ function is available but not recommended """
        print '# Starting Testing Sequence'


        if os.path.isfile(filepath):
            os.rename(filepath, filepath + wasanbon.timestampstr())
            pass

        open(filepath, 'w').close()
        cons = open('console_output.txt', 'w')
        sys.stdout = cons


        self.test(admin, 'environment', 'init', '-v')

        self.test(admin, 'binder', 'list', '-v')
        self.test(admin, 'binder', 'packages', '-v')
        self.test(admin, 'binder', 'rtcs', '-v')


        self.test(admin, 'package', 'list', '-v')

        self.test(admin, 'package', 'create', pkg_name, '-v')
        self.test(admin, 'package', 'directory', pkg_name, '-v')
        curdir = os.getcwd()
        os.chdir(os.path.join(os.getcwd(), pkg_name))
        self.test(mgr, 'rtc', 'list', '-v')

        os.chdir(curdir)
        self.test(admin, 'package', 'delete', pkg_name, '-r', '-v')

        #repo_names = ['test_project01']
        repo_names = ['test_project01', 'test_project02', 'test_project03']
        for repo_name in repo_names:
            self.test(admin, 'repository', 'clone', repo_name, '-v')
            os.chdir(os.path.join(curdir, repo_name))
            self.test(mgr, 'rtc', 'list', '-v')
            self.test(mgr, 'rtc', 'build', 'all', '-v')

            timeout = 3.0
            self.test(mgr, 'system', 'run', '-v', '-b', '-w', str(timeout))
            time.sleep(timeout*1.5)
            self.test(mgr, 'system', 'terminate', '-v')

            if not os.path.isfile('testout.txt'):
                log("testout.txt not found.")
            else:
                with open("testout.txt", "r") as f:
                    val = int(f.read().strip())
                    log("testout.txt == %d" % val)
            
            self.test(mgr, 'rtc', 'clean', 'all', '-v')
            os.chdir(curdir)
            self.test(admin, 'package', 'delete', repo_name, '-v', '-r')


            
        
def log(str__):
    print str__
    with open(filepath, 'a') as f:
        f.write(str__ + '\n')
