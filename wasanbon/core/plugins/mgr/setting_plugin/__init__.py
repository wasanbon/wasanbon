import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment',
                'admin.package']


    #def _print_alternatives(self, args):
    #    print 'hoo'
    #    print 'foo'
    #    print 'hoge'
    #    print 'yah'

    @manifest
    def upgrade(self, argv):
        """ This is help text
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag

        package = admin.package.get_package_from_path(os.getcwd())
        setting = package.setting

        # Check system filepath
        system_file = setting['system']
        if os.path.isfile(os.path.join(package.path, system_file)):
            # Old manner
            setting['RTS_DIR'] = os.path.dirname(system_file)
            setting['system'] = os.path.basename(system_file)
            pass


        # Check conf filepath
        
            
