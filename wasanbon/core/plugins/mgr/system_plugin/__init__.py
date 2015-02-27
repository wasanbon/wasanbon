import os, sys, signal, time, traceback, threading

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

endflag = False
ev = threading.Event()

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc', 'admin.systeminstaller', 
                'admin.systemlauncher', 'admin.systembuilder', 'admin.nameserver', 'admin.systemeditor']

    def _print_rtcs(self):
        pack = admin.package.get_package_from_path(os.getcwd())
        for rtc in admin.rtc.get_rtcs_from_package(pack):
            print rtc.rtcprofile.basicInfo.name
        
    @manifest 
    def install(self, args):
        self.parser.add_option('-f', '--force', help='Force option (default=True)', default=True, action='store_true', dest='force_flag')
        self.parser.add_option('-s', '--standalone', help='Install Standalone RTC(default=False)', default=False, action='store_true', dest='standalone_flag')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        force  = options.force_flag
        standalone = options.standalone_flag
        wasanbon.arg_check(argv, 4)

        pack = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        if argv[3] == 'all':
            rtcs = admin.rtc.get_rtcs_from_package(pack, verbose=verbose)
        else:
            rtcs = [admin.rtc.get_rtc_from_package(pack, arg, verbose=verbose) for arg in argv[3:]]
        
        retval = 0
        for rtc in rtcs:
            ret = admin.systeminstaller.install_rtc_in_package(pack, rtc, verbose=verbose, 
                                                               preload=True,
                                                               precreate=True,
                                                               copy_conf=True,
                                                               rtcconf_filename="",
                                                               copy_bin=True,
                                                               standalone=standalone,
                                                               conffile=None)
            if ret != 0:
                retval = ret

        return retval

    @manifest
    def uninstall(self, args):
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag

        pack = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        rtcs = [admin.rtc.get_rtc_from_package(pack, arg, verbose=verbose) for arg in argv[3:]]
        retval = 0
        for rtc in rtcs:
            ret = admin.systeminstaller.uninstall_rtc_from_package(pack, rtc, verbose=verbose)

            if ret != 0:
                retval = ret
        return retval

    @manifest
    def terminate(self, args):
        #self.parser.add_option('-b', '--background', help='Launch in background(default=False)', default=False, action='store_true', dest='background_flag')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        #background = options.background_flag

        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        try:
            admin.systembuilder.deactivate_system(package, verbose=verbose)
        except wasanbon.BuildSystemException, ex:
            sys.stdout.write('# Build System Failed.\n')
        except:
            traceback.print_exc()
            return -1
        finally:
            try:
                admin.systemlauncher.exit_all_rtcs(package, verbose=verbose)
                admin.systemlauncher.terminate_system(package, verbose=verbose)
            except:
                return -1
            return -1
        return 0
        

    @manifest
    def run(self, args):
        """ Launch System """
        #self.parser.add_option('-f', '--force', help='Force option (default=True)', default=True, action='store_true', dest='force_flag')
        #self.parser.add_option('-s', '--standalone', help='Install Standalone RTC(default=False)', default=False, action='store_true', dest='standalone_flag')
        self.parser.add_option('-b', '--background', help='Launch in background(default=False)', default=False, action='store_true', dest='background_flag')
        self.parser.add_option('-w', '--wakeuptimeout', help='Timeout of Sleep Function when waiting for the wakeup of RTC-Daemons', default=5, dest='wakeuptimeout', action='store', type='float')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        background = options.background_flag
        wakeuptimeout = options.wakeuptimeout
        #force  = options.force_flag
        #standalone = options.standalone_flag
        
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        global endflag
        endflag = False
        try:
            processes = admin.systemlauncher.launch_system(package, verbose=verbose)
            print wakeuptimeout
            time.sleep(wakeuptimeout)
            admin.systembuilder.build_system(package, verbose=verbose)

            admin.systembuilder.activate_system(package, verbose=verbose)

            if background:
                return 0

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

            endflag = False
            while not endflag:
                try:
                    time.sleep(0.1)
                except IOError, e:
                    print e
                    pass
                pass

            admin.systembuilder.deactivate_system(package, verbose=verbose)
            
        except wasanbon.BuildSystemException, ex:
            sys.stdout.write('# Build System Failed.\n')

        except:
            traceback.print_exc()
            return -1
        finally:
            try:
                if not background:
                    admin.systemlauncher.exit_all_rtcs(package, verbose=verbose)
                    admin.systemlauncher.terminate_system(package, verbose=verbose)
            except:
                return -1
            return -1
        return 0


    @manifest
    def build(self, args):
        """ Build System in Console interactively """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag

        package = admin.package.get_package_from_path(os.getcwd())
        nss = admin.nameserver.get_nameservers_from_package(package, verbose=verbose)
        
        pairs = admin.systemeditor.get_connectable_pairs(nss, verbose=verbose)
        print pairs
