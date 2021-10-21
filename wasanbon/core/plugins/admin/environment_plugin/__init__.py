import os
import sys
import traceback
import optparse
import subprocess
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest
#from . import setup
#from .setup import *
from wasanbon.core.plugins.admin.environment_plugin import setup
import shutil


class Plugin(PluginFunction):
    """ Environment initialization functions Plugin.
        Use to initialize wasanbon environment."""

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    @manifest
    def status(self, args):
        """ This command shows Environment status for wasanbon.
        $ wasanbon-admin.py environment status
        """
        sys.stdout.write('# Showing the status of wasanbon environment initialization...\n')
        _, _ = self.parse_args(args[:])

        for key, value in list(self.path.items()):
            sys.stdout.write('%s : %s\n' % (key, value))
        return 0

    @manifest
    def update_path(self, args):
        """ Update Search Path for commands.
        $ wasanbon-admin.py environment update_path
        """
        _, _ = self.parse_args(args[:])
        verbose = True  # options.verbose_flag

        self._update_path(verbose=verbose)
        return 0

    @manifest
    def init(self, args):
        """ This command must be called first.
        $ wasanbon-admin.py environment init
        """
        _, _ = self.parse_args(args[:])
        verbose = True  # options.verbose_flag

        sys.stdout.write('# Initializing .wasanbon directory....\n')

        sys.stdout.write('## Platform: %s\n' % wasanbon.platform())

        # self._copy_path_yaml_from_setting_dir(force=force, verbose=verbose)
        self._update_path(verbose)

        return 0

    @manifest
    def register(self, args):
        """ Register some specific information of users. 1. account of github.com, 2. version of Visual Studio (in windows) 
        $ wasanbon-admin.py environment register
        """
        self.parser.add_option('-u', '--username', help='Username of github.com', default=None, dest='username', action='store', type='string')
        self.parser.add_option('-p', '--password', help='Password of github.com', default=None, dest='password', action='store', type='string')
        self.parser.add_option('-t', '--token', help='Access Token of github.com', default=None, dest='token', action='store', type='string')
        if sys.platform == 'win32':
            self.parser.add_option('-c', '--compiler', help='Compiler of Win32 system', default='', dest='compiler', action='store', type='string')
        options, _ = self.parse_args(args[:])

        verbose = True  # options.verbose_flag

        if os.path.isfile(wasanbon.register_file):
            try:
                open(wasanbon.register_file, 'w').close()
            except:
                sys.stdout.write(
                    """# Creating Register file failed.\n This may be caused by incorrectly initialized the path of $HOME/.wasanbon.\n Use wasanbon-admin.py environment init command.\n""")
                return -1

        sys.stdout.write('# Input Username and Password and Token of github.com\n')
        user, passwd, token = wasanbon.user_pass(options.username, options.password, options.token, True)

        # Try to register
        reg_dict = {'github.com': {
            'username': user,
            'password': passwd,
            'token': token},
        }

        if sys.platform == 'win32':
            if len(options.compiler) == 0:
                sys.stdout.write('# Input compiler of current system [default=Visual Studio 12]')
                comp = input()
                options.compiler = comp
            reg_dict['compiler'] = options.compiler

        sys.stdout.write('# Saving registration data...\n')
        import yaml
        open(wasanbon.register_file, 'w').write(yaml.dump(reg_dict))
        sys.stdout.write('## Success\n')
        return 0

    @property
    def setting_path(self):
        """ This plugin's setting directory path. This includes OS dependent information like packages. """
        setting_path = os.path.join(__path__[0], 'settings', wasanbon.platform())
        if not os.path.isdir(setting_path):
            sys.stdout.write('# Error. UnsupportedPlatform (%s)\n' % wasanbon.platform())
            raise wasanbon.UnsupportedPlatformException()
        return setting_path

    def getIDE(self):
        """ Environment's default IDE (Integrated Development Environment) like Visual Studio. """
        return wasanbon.IDE

    @property
    def path(self):
        """ Environment's command paths. Ex., paths for cmake, doxygen, git, svn, and so on. """
        path_filename = os.path.join(wasanbon.home_path, 'path.yaml')
        if not os.path.isfile(path_filename):
            return {}
        try:
            yaml = __import__('yaml')
            return yaml.safe_load(open(path_filename, 'r'))
        except ImportError as e:
            return {}

    @manifest
    def setup_bashrc(self, verbose=False):
        """ Setup bashrc profile. In Ubuntu, $HOME/.bashrc. In OSX, $HOME/.bash_profile.
        $ wasanbon-admin.py environment setup_bashrc
        """
        if sys.platform == 'darwin':
            filename = '.bash_profile'
        elif sys.platform == 'linux':
            filename = '.bashrc'
        else:
            return -1

        start_str = '#-- Starting Setup Script of wasanbon --#'
        stop_str = '#-- Ending Setup Script of wasanbon --#'
        target = os.path.join(wasanbon.get_home_path(), filename)
        script = open(os.path.join(__path__[0], "settings", wasanbon.platform(), "bashrc"), "r").read()

        if verbose:
            sys.stdout.write('# Initializing $HOME/%s\n' % filename)

        if os.path.isfile(target):
            erase = False
            file = open(target, "r")
            fout = open(target + '.bak', "w")
            for line in file:
                if line.strip() == start_str:
                    erase = True
                    continue

                elif line.strip() == stop_str:
                    erase = False
                    continue

                if not erase:
                    fout.write(line)
                    pass
                pass

            file.close()
            fout.close()

            os.remove(target)
            os.rename(target + ".bak", target)

            fout = open(target, "a")
        else:
            fout = open(target, "w")
            pass

        fout.write("\n\n" + start_str + "\n")
        fout.write(script)
        fout.write("\n" + stop_str + "\n\n")

        fout.close()
        return 0

    def _update_path(self, verbose=False):
        self._copy_path_yaml_from_setting_dir(force=False, verbose=verbose)
        import yaml
        path_filename = os.path.join(wasanbon.home_path, 'path.yaml')
        dir = yaml.safe_load(open(path_filename, 'r'))
        hints = yaml.safe_load(open(os.path.join(self.setting_path, 'hints.yaml'), 'r'))

        path_dict = {}
        for key, value in list(dir.items()):
            hints_org = hints[key]
            hints_ = [h.replace('$HOME', wasanbon.get_home_path()) for h in hints_org]
            new_path = setup.search_command(key, value, hints_, verbose=verbose)
            path_dict[key] = new_path

            if key == 'eclipse':
                # create eclipse link
                eclipse_dir = os.path.join(wasanbon.home_path, 'eclipse')
                if not os.path.isdir(eclipse_dir):
                    os.mkdir(eclipse_dir)

        yaml.dump(path_dict, open(path_filename, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)

    def _copy_path_yaml_from_setting_dir(self, force=False, verbose=False):
        src = os.path.join(self.setting_path, 'path.yaml')
        dst = os.path.join(wasanbon.home_path, 'path.yaml')
        if not os.path.isfile(dst) or force:
            shutil.copy2(src, dst)
