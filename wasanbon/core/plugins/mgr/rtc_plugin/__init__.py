import os, sys, signal, time, traceback, threading
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

ev = threading.Event()
endflag = False
class Plugin(PluginFunction):
    """ Manage RT-Component in Package """

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 
                'admin.package', 
                'admin.rtc', 
                'admin.rtcconf',
                'admin.rtcprofile', 
                'admin.builder', 
                'admin.systeminstaller',
                'admin.systemlauncher',
                'admin.editor']


    #@property
    #def rtc(self):
    #    import rtc
    #    return rtc

    def _print_rtcs(self, args):
        pack = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(pack)
        for r in rtcs:
            print r.rtcprofile.basicInfo.name

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
                            print '    ' + d.name + ':'
                            #print '      name     : ' + d.name
                            print '      portType : ' + d.portType
                            print '      type     : ' + d.type
                if len(r.rtcprofile.serviceports):
                    print '  serviceports :'
                    for s in r.rtcprofile.serviceports:
                        if not detail:
                            print '     - ' + s.name
                        else:
                            print '    ' + s.name + ':'
                            #print '      name     : ' + s.name
                            for i in s.serviceInterfaces:
                                print '      ' + i.name + ':'
                                print '        type         : ' + i.type
                                print '        instanceName : ' + i.instanceName
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
        options, argv = self.parse_args(args, self._print_rtcs)
        verbose = options.verbose_flag
        if sys.platform == 'win32':
            if verbose: sys.stdout.write('# In Windows, always build with verbose option.\n')
            verbose = True
        only = options.only_flag
        standalone = options.standalone_flag

        wasanbon.arg_check(argv, 4)
        pack = admin.package.get_package_from_path(os.getcwd())
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(pack, verbose=verbose)
        else:
            rtcs = [admin.rtc.get_rtc_from_package(pack, argv[3], verbose=verbose)]
            
        return_value_map = {}
        retval = 0
        for rtc in rtcs:
            sys.stdout.write('# Building RTC (%s)\n' % rtc.rtcprofile.basicInfo.name)
            ret, msg = admin.builder.build_rtc(rtc.rtcprofile, verbose=verbose)
            return_value_map[rtc.rtcprofile.basicInfo.name] = ret
            if not ret:
                sys.stdout.write('## Failed.\n')
                retval = -1
            else:
                sys.stdout.write('## Success.\n')
                if not only:
                    if not standalone:
                        # Confirm if this rtc is 
                        standalone_flag = admin.systeminstaller.is_installed(pack, rtc, verbose=verbose, standalone=True)
                    else:
                        standalone_flag = standalone
                    sys.stdout.write('## Installing RTC (standalone=%s).\n' % (standalone_flag is True))
                    admin.systeminstaller.install_rtc_in_package(pack, rtc, verbose=verbose, standalone=standalone_flag)
                    sys.stdout.write('### Success.\n')

        if verbose:
            sys.stdout.write('Build Summary:\n')
            for key, value in return_value_map.items():
                sys.stdout.write(' - Build RTC (' + key + ')' + ' '*(25-len(key)) + ('Success' if value else 'False') + '\n')
        return retval


    @manifest
    def clean(self, args):
        options, argv = self.parse_args(args, self._print_rtcs)
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


    @manifest
    def delete(self, args):
        """ Delete Package
        # Usage $ wasanbon-admin.py package delete [PACK_NAME]"""
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(args[:], self._print_rtcs)
        verbose = options.verbose_flag
        force = options.force_flag

        pack = admin.package.get_package_from_path(os.getcwd())
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(pack, verbose=verbose)
        else:
            rtcs = [admin.rtc.get_rtc_from_package(pack, argv[3], verbose=verbose)]
        import shutil
        for rtc in rtcs:
            if os.path.isdir(rtc.path):
                sys.stdout.write('# Deleting RTC (%s)\n' % rtc.rtcprofile.basicInfo.name)
                def remShut(*args):
                    import stat
                    func, path, _ = args 
                    os.chmod(path, stat.S_IWRITE)
                    os.remove(path)
                    pass
                shutil.rmtree(rtc.path, onerror = remShut)
                    

    @manifest
    def edit(self, args):
        """ Edit RTC with editor """
        options, argv = self.parse_args(args[:], self._print_rtcs)
        verbose = options.verbose_flag
        pack = admin.package.get_package_from_path(os.getcwd())
        rtc = admin.rtc.get_rtc_from_package(pack, argv[3], verbose=verbose)
        admin.editor.edit_rtc(rtc, verbose=verbose)

    @manifest
    def run(self, args):
        """ Run just one RTC """
        options, argv = self.parse_args(args[:], self._print_rtcs)
        verbose = options.verbose_flag
        package = admin.package.get_package_from_path(os.getcwd())
        rtc = admin.rtc.get_rtc_from_package(package, argv[3], verbose=verbose)
        return self.run_rtc_in_package(package, rtc, verbose=verbose)

    def run_rtc_in_package(self, package, rtc, verbose=False, background=False):
        global endflag
        endflag = False
        def signal_action(num, frame):
            print ' - SIGINT captured'
            ev.set()
            global endflag
            endflag = True
            pass

        signal.signal(signal.SIGINT, signal_action)

        if sys.platform == 'win32':
            sys.stdout.write(' - Escaping SIGBREAK...\n')
            signal.signal(signal.SIGBREAK, signal_action)
            pass
        
        sys.stdout.write('# Executing RTC %s\n' % rtc.rtcprofile.basicInfo.name)
        rtcconf_path = package.rtcconf[rtc.rtcprofile.language.kind]
        rtcconf = admin.rtcconf.RTCConf(rtcconf_path, verbose=verbose)
        rtc_temp = os.path.join("conf", "rtc_temp.conf")
        if os.path.isfile(rtc_temp):
            os.remove(rtc_temp)
            pass
        rtcconf.sync(verbose=True, outfilename=rtc_temp)
        admin.systeminstaller.uninstall_all_rtc_from_package(package, rtcconf_filename=rtc_temp, verbose=True)
        admin.systeminstaller.install_rtc_in_package(package, rtc, rtcconf_filename=rtc_temp, copy_conf=False)

        try:
            admin.systemlauncher.launch_rtcd(package, rtc.rtcprofile.language.kind, rtcconf=rtc_temp, verbose=True)
            if background:
                return 0
            while not endflag:
                try:
                    time.sleep(0.1)
                except IOError, e:
                    print e
                    pass
                pass
            pass
        except:
            traceback.print_exc()
            return -1
        if verbose: sys.stdout.write('## Exitting RTC Manager.\n')
        admin.systemlauncher.exit_all_rtcs(package, verbose=verbose)
        admin.systemlauncher.terminate_system(package, verbose=verbose)
        return 0

    def terminate_rtcd(self, package, verbose=False):
        if verbose: sys.stdout.write('# Terminating RTCDs.\n')
        admin.systemlauncher.exit_all_rtcs(package, verbose=verbose)
        admin.systemlauncher.terminate_system(package, verbose=verbose)
        return 0

    @manifest 
    def download_profile(self, args):
        """ Run just one RTC """
        self.parser.add_option('-w', '--wakeuptimeout', help='Timeout of Sleep Function when waiting for the wakeup of RTC-Daemons', default=5, dest='wakeuptimeout', action='store', type='float')
        options, argv = self.parse_args(args[:], self._print_rtcs)
        verbose = options.verbose_flag
        wakeuptimeout = options.wakeuptimeout

        package = admin.package.get_package_from_path(os.getcwd())
        rtc = admin.rtc.get_rtc_from_package(package, argv[3], verbose=verbose)
        if self.run_rtc_in_package(package, rtc, verbose=verbose, background=True) != 0:
            return -1
        wasanbon.sleep(wakeuptimeout)        
        rtcp = admin.rtcprofile.create_rtcprofile(rtc, verbose=verbose)
        print admin.rtcprofile.tostring(rtcp)
        self.terminate_rtcd(package, verbose=verbose)
        return 0
        
    
    @manifest 
    def verify_profile(self, args):
        """ Run just one RTC """
        self.parser.add_option('-w', '--wakeuptimeout', help='Timeout of Sleep Function when waiting for the wakeup of RTC-Daemons', default=5, dest='wakeuptimeout', action='store', type='float')
        options, argv = self.parse_args(args[:], self._print_rtcs)
        verbose = options.verbose_flag
        wakeuptimeout = options.wakeuptimeout

        package = admin.package.get_package_from_path(os.getcwd())
        sys.stdout.write('# Starting RTC.\n')
        rtc = admin.rtc.get_rtc_from_package(package, argv[3], verbose=verbose)
        if self.run_rtc_in_package(package, rtc, verbose=verbose, background=True) != 0:
            return -1
        wasanbon.sleep(wakeuptimeout)
        sys.stdout.write('# Acquiring RTCProfile from Inactive RTC\n')
        rtcp = admin.rtcprofile.create_rtcprofile(rtc, verbose=verbose)
        self.terminate_rtcd(package, verbose=verbose)
        sys.stdout.write('# Comparing Acquired RTCProfile and Existing RTCProfile.\n')
        retval = admin.rtcprofile.compare_rtcprofile(rtc.rtcprofile, rtcp, verbose=verbose)
        if retval:
            sys.stdout.write('Failed.\n# RTCProfile must be updated.\n')
            return -1
        sys.stdout.write('Succeeded.\n# RTCProfile is currently matches to binary.\n')
        return 0
        

    @manifest 
    def update_profile(self, args):
        """ Run just one RTC and compare the profile between the existing RTC.xml and launched RTC, then save RTC.xml """
        self.parser.add_option('-f', '--file', help='RTCProfile filename (default="RTC.xml")', default='RTC.xml', dest='filename', action='store', type='string')
        self.parser.add_option('-d', '--dryrun', help='Just output on console', default=False, dest='dry_flag', action='store_true')
        self.parser.add_option('-w', '--wakeuptimeout', help='Timeout of Sleep Function when waiting for the wakeup of RTC-Daemons', default=5, dest='wakeuptimeout', action='store', type='float')
        options, argv = self.parse_args(args[:], self._print_rtcs)
        verbose = options.verbose_flag
        dry = options.dry_flag
        filename = options.filename
        wakeuptimeout = options.wakeuptimeout

        wasanbon.arg_check(argv, 4)
        rtc_name = argv[3]

        package = admin.package.get_package_from_path(os.getcwd())
        sys.stdout.write('# Starting RTC.\n')
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        standalone = admin.systeminstaller.is_installed(package, rtc, standalone=True, verbose=verbose)
        if standalone:
            admin.systemlauncher.launch_standalone_rtc(package, rtc, stdout=True, verbose=verbose)
            pass
        else:
            if self.run_rtc_in_package(package, rtc, verbose=verbose, background=True) != 0:
                return -1
        wasanbon.sleep(wakeuptimeout)
        sys.stdout.write('# Acquiring RTCProfile from Inactive RTC\n')
        rtcp = admin.rtcprofile.create_rtcprofile(rtc, verbose=verbose)

        if standalone:

            pass
        else:
            self.terminate_rtcd(package, verbose=verbose)
        sys.stdout.write('# Comparing Acquired RTCProfile and Existing RTCProfile.\n')
        retval = admin.rtcprofile.compare_rtcprofile(rtc.rtcprofile, rtcp, verbose=verbose)
        if retval:
            filepath = os.path.join(rtc.path, filename)

            if not dry:
                outstr = admin.rtcprofile.tostring(retval, pretty_print=True)
                if outstr == None:
                    sys.stdout.write('# RTC Profile save failed.\n')
                    return -1
                if os.path.isfile(filepath):
                    f = filepath + wasanbon.timestampstr()
                    os.rename(filepath, f)
                    pass

                fout = open(filepath, 'w')
                fout.write(outstr)
                fout.close()
            else:
                sys.stdout.write(admin.rtcprofile.tostring(retval, pretty_print=True))

            sys.stdout.write('Succeed.\n')
            
            return 0
        sys.stdout.write('Succeed.\n')
        return 0
        
