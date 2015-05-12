import os, sys, subprocess
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def launch_eclipse(self, workbench=".", argv=None, nonblock=True, verbose=False):
        eclipse_dir = os.path.join(wasanbon.home_path, 'eclipse')
        if sys.platform == 'darwin':
            eclipse_dir = os.path.join(eclipse_dir, 'Eclipse.app/Contents/MacOS')
        curdir = os.getcwd()

        if not os.path.isdir(eclipse_dir):
            sys.stdout.write('# Install ecipse by $wasanbon-admin.py environment install eclipse\n')
            return -1
        os.chdir(eclipse_dir)

        if sys.platform == 'win32':
            eclipse_cmd = 'eclipse.exe'
        else:
            eclipse_cmd = './eclipse'

        # Set Environmental Variable
        env = os.environ
        env['RTM_ROOT'] = wasanbon.get_rtm_root()

        if not os.path.isdir(workbench) or workbench == '.':
            if verbose: sys.stdout.write("## Starting eclipse in current directory.\n")
            cmd = [eclipse_cmd]
        else:
            if verbose: sys.stdout.write("## Starting eclipse in current package directory(%s).\n" % workbench)
            cmd = [eclipse_cmd, '-data', workbench]
        if argv != None:
            cmd = cmd + argv

        stdout = None if verbose else subprocess.PIPE
        stderr = None if verbose else subprocess.PIPE
        if sys.platform == 'win32':
            p = subprocess.Popen(cmd, creationflags=512, env=env, stdout=stdout, stderr=stderr)
        else:
            p = subprocess.Popen(cmd, env=env, stdout=stdout, stderr=stderr)

        if not nonblock:
            p.wait()

        os.chdir(curdir)
        
    @manifest
    def launch(self, argv):
        """ This is help text
        """
        #self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        #force   = options.force_flag

        self.launch_eclipse()
        return 0
