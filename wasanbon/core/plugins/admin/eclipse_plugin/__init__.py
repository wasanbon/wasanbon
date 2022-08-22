import os
import sys
import subprocess
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ Eclipse management Plugin. """

    def __init__(self):
        # PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def launch_eclipse(self, workbench=".", argv=None, nonblock=True, verbose=False):
        """ Launch Eclipse. 
        :param string workbench: Directory of workspace.
        :param list<string> argv: Command-line argument for eclipse.
        :param bool nonblock: If true, this function returns immediately, if false, this function blocks until ecilpse halts.
        :param bool verbose: message verbosity
        :rtype int:
        :return: Zero if success. Non-zero if failed.
        """
        eclipse_dir = os.path.join(wasanbon.home_path, 'eclipse')
        curdir = os.getcwd()

        if not os.path.isdir(eclipse_dir):
            sys.stdout.write('# eclipse directory is not Found. $ wasanbon-admin.py environment update_path. \n')
            return -1

        eclipse_cmd = admin.environment.path['eclipse']

        # Set Environmental Variable
        env = os.environ
        env['RTM_ROOT'] = wasanbon.get_rtm_root()
        if sys.platform == 'win32':
            env['PATH'] = env['RTM_ROOT'] + 'jre\\bin;' + env['PATH']

        if not os.path.isdir(workbench) or workbench == '.':
            if verbose:
                sys.stdout.write("## Starting eclipse in current directory.\n")
            cmd = [eclipse_cmd]
        else:
            if verbose:
                sys.stdout.write("## Starting eclipse in current package directory(%s).\n" % workbench)
            cmd = [eclipse_cmd, '-data', workbench]
        if argv != None:
            cmd = cmd + argv

        if sys.platform == 'win32':
            stdout = None
            stderr = None
            p = subprocess.Popen(cmd, creationflags=512, env=env, stdout=stdout, stderr=stderr)
        elif sys.platform == 'darwin':
            stdout = None
            stderr = None
            p = subprocess.Popen(cmd, env=env, stdout=stdout, stderr=stderr)
        else:
            stdout = None if verbose else subprocess.PIPE
            stderr = None if verbose else subprocess.PIPE
            p = subprocess.Popen(cmd, env=env, stdout=stdout, stderr=stderr)

        if not nonblock:
            p.wait()

        os.chdir(curdir)
        return 0

    @manifest
    def launch(self, argv):
        """ Launch Eclipse.
        $ wasanbon-admin.py eclipse launch
        """
        self.parser.add_option('-d', '--directory', help='Workspace Directory (default=select when launched)',
                               default=".", action='store', dest='directory')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag  # This is default option
        directory = options.directory
        if len(argv) > 3:
            args = argv[3:]
        else:
            args = None
        self.launch_eclipse(workbench=directory, argv=args, verbose=verbose)
        return 0
