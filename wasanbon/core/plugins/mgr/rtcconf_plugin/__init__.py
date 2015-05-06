import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

rtcconf_keys = ['config.version',
             'openrtm.version',
             'manager.name',
             'manager.naming_formats',
             'manager.is_master',
             'manager.corba_servant',
             'corba.master_manager',
             'manager.shutdown_on_nortcs',
             'manager.shutdown_auto',
             'manager.auto_shutdown_duration',
             'corba.args',
             'corba.endpoint',
             'corba.endpoints',
             'corba.nameservers',
             'corba.nameservice.replace_endpoint',
             'corba.alternate_iiop_addresses',
             'naming.enable',
             'naming.type',
             'naming.formats',
             'naming.update.enable',
             'naming.update.interval',
             'naming.update.rebind',
             'manager.modules.load_path',
             'manager.modules.preload',
             'manager.modules.abs_path_allowed',
             ## 'manager.modules.config_ext',
             ## 'manager.modules.config_path',
             ## 'manager.modules.detect_loadable',
             ## 'manager.modules.init_func_suffix',
             ## 'manager.modules.init_func_prefix',
             ## 'manager.modules.download_allowed',
             ## 'manager.modules.download_dir',
             ## 'manager.modules.download_cleanup',
             'manager.components.precreate',
             'logger.enable',
             'logger.file_name',
             'logger.date_format',
             'logger.log_level',
             'timer.enable',
             'timer.tick',
             'exec_cxt.periodic.type',
             'exec_cxt.periodic.rate',
             'sdo.service.provider.available_services',
             'sdo.service.provider.enabled_services',
             'sdo.service.provider.providing_services',
             'sdo.service.consumer.available_services',
             'sdo.service.consumer.enabled_services',
             ]



class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtcconf']

    @manifest
    def show(self, argv):
        """ show rtcconf status
        """
        self.parser.add_option('-l', '--long', help='Long Format option (default=False)', default=False, action='store_true', dest='long_flag')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        long = options.long_flag


        package = admin.package.get_package_from_path(os.getcwd())
        rtcconf_paths = package.rtcconf
        for language, rtcconf_path in rtcconf_paths.items():
            rtcconf = admin.rtcconf.RTCConf(rtcconf_path)
            sys.stdout.write('%s :\n' % language)
            sys.stdout.write('  path  : %s\n' % rtcconf_path)
            if long:
                sys.stdout.write('  value : \n')
                for key in rtcconf_keys:
                    sys.stdout.write('    %s : "%s"\n' % (key, rtcconf[key].strip()))

        return 0

    def _print_alts(self, args):
        argv = [a for a in args if not a.startswith('_')]
        if len(argv) == 4:
            for l in ['C++', 'Java', 'Python']:
                print l
        elif len(argv) > 4:
            self._print_keys(args)
        pass

    def _print_keys(self, args):
        for k in rtcconf_keys:
            print k

    @manifest
    def get(self, args):
        options, argv = self.parse_args(args[:], self._print_alts)
        verbose = options.verbose_flag # This is default option

        package = admin.package.get_package_from_path(os.getcwd())
        rtcconf_paths = package.rtcconf
        
        wasanbon.arg_check(argv, 5)
        lang = argv[3]
        key  = argv[4]

        print admin.rtcconf.RTCConf(package.rtcconf[lang])[key]

    @manifest
    def set(self, args):
        options, argv = self.parse_args(args[:], self._print_alts)
        verbose = options.verbose_flag # This is default option

        package = admin.package.get_package_from_path(os.getcwd())
        rtcconf_paths = package.rtcconf
        
        wasanbon.arg_check(argv, 6)
        lang = argv[3]
        key  = argv[4]
        val  = argv[5]

        rtcconf = admin.rtcconf.RTCConf(package.rtcconf[lang])
        rtcconf[key] = val
        rtcconf.sync()
