import subprocess, sys, traceback

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def _print_alternatives(self, args):
        print 'run'

    @manifest
    def run(self, argv):
        """ Do Selfupdate  through pip
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag

        if not force:
            print '# Add Force flag (-f).'
            return -1

        print '# This is test admin plugin'
        cmd = ['pip', 'install', '-U', '--user', 'wasanbon']
        return subprocess.call(cmd)


