import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ Manage RT-Component in Package """

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc', 'admin.rtcprofile', 'admin.builder', 'admin.systeminstaller']


    #@property
    #def rtc(self):
    #    import rtc
    #    return rtc

    @manifest
    def list(self, args):
        """ List RTC in current Package """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        self.parser.add_option('-d', '--detail', help='Long Format (default=False)', default=False, action='store_true', dest='detail_flag')        
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        long  = options.long_flag
        detail = options.detail_flag
        if detail: long = True
        #package = wasanbon.plugins.admin.package.package
        #package = admin.package

        #admin_rtc = admin.rtc.rtc
        pack = admin.package.get_package_from_path(os.getcwd())

        rtcs = admin.rtc.get_rtcs_from_package(pack, verbose=verbose)
        for r in rtcs:
            if not long:
                print ' - ' + r.rtcprofile.basicInfo.name
            elif long:
                print r.rtcprofile.basicInfo.name + ' : '
                print '  basicInfo : '
                print '    description : ' + r.rtcprofile.basicInfo.description
                print '    category    : ' + r.rtcprofile.basicInfo.category
                print '    vendor      : ' + r.rtcprofile.basicInfo.vendor
                if len(r.rtcprofile.dataports):
                    print '  dataports : '
                    for d in r.rtcprofile.dataports:
                        if not detail:
                            print '     - ' + d.name
                        else:
                            print '    name     : ' + d.name
                            print '    portType : ' + d.portType
                            print '    type     : ' + d.type
                            
            if detail:
                print '  language : '
                print '    kind        : ' + r.rtcprofile.language.kind
            if long or detail:
                print ''
        return 0
                
    @manifest
    def build(self, args):
        self.parser.add_option('-o', '--only', help='Build Only (Not Install) (default=False)', default=False, action='store_true', dest='only_flag')
        self.parser.add_option('-s', '--standalone', help='Install Standalone Mode (default=False)', default=False, action='store_true', dest='standalone_flag')
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        only = options.only_flag
        standalone = options.standalone_flag

        wasanbon.arg_check(argv, 4)
        pack = admin.package.get_package_from_path(os.getcwd())
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(pack, verbose=verbose)
        else:
            rtcs = [admin.rtc.get_rtc_from_package(pack, argv[3], verbose=verbose)]

        retval = 0
        for rtc in rtcs:
            ret, msg = admin.builder.build_rtc(rtc.rtcprofile, verbose=verbose)
            if not ret:
                retval = -1
            else:
                if not only:
                    admin.systeminstaller.install_rtc_in_package(pack, rtc, verbose=verbose, standalone=standalone)

        return retval


    @manifest
    def clean(self, args):
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag

        if verbose: sys.stdout.write('# Cleanup RTCs\n')

        wasanbon.arg_check(argv, 4)
        pack = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(pack, verbose=verbose)
        else:
            rtcs = [admin.rtc.get_rtc_from_package(pack, argv[3], verbose=verbose)]

        retval = 0
        for rtc in rtcs:
            if verbose: sys.stdout.write('# Cleanuping RTC %s\n' % rtc.rtcprofile.basicInfo.name)
            
            ret, msg = admin.builder.clean_rtc(rtc.rtcprofile, verbose=verbose)
            if not ret:
                retval = -1

        return retval
