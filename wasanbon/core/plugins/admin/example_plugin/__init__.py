import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    @manifest
    def __call__(self, argv):
        """ Manifesting __call__ function is available but not recommended """
        print ' # this is plain function'
        pass

    @manifest
    def show(self, argv):
        """ This is print function
        """
        print " # This is example plugin's print function"

    def _print_alternatives(self, args):
        print 'hoo'
        print 'foo'
        print 'hoge'
        print 'yah'

    @manifest
    def echo(self, argv):
        """ This is help text
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag

        if verbose:
            print '# Verbosity option is ON!'

        if force:
            print '# Force Option is ON!'

        print '# This is test admin plugin'
        if len(argv) > 2:
            for p in argv[3:]:
                print p

