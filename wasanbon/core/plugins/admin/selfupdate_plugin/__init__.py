import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):
    """ This provides self update function for wasanbon """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.git']

    def __call__(self, argv):
        """ Self update of wasnabon """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag

        print "NOT IMPLEMENTED YET"
        return -1
        
