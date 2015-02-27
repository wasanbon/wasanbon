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

        return 0


    @manifest
    def build(self, args):
        """ Build System in Console interactively """
        self.parser.add_option('-b', '--background', help='Launch in background(default=False)', default=False, action='store_true', dest='background_flag')
        self.parser.add_option('-w', '--wakeuptimeout', help='Timeout of Sleep Function when waiting for the wakeup of RTC-Daemons', default=5, dest='wakeuptimeout', action='store', type='float')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        background = options.background_flag
        wakeuptimeout = options.wakeuptimeout
        #force  = options.force_flag


        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        global endflag
        endflag = False
        try:
            processes = admin.systemlauncher.launch_system(package, verbose=verbose)
            time.sleep(wakeuptimeout)


            package = admin.package.get_package_from_path(os.getcwd())
            nss = admin.nameserver.get_nameservers_from_package(package, verbose=verbose)

            # Interactive Connect
            pairs = admin.systemeditor.get_connectable_pairs(nss, verbose=verbose)
            from wasanbon import util
            for pair in pairs:
                if util.no_yes('# Connect? (%s->%s)\n' % (admin.systembuilder.get_port_full_path(pair[0]),
                                                          admin.systembuilder.get_port_full_path(pair[1]))) == 'yes':
                    try:
                        admin.systembuilder.connect_ports(pair[0], pair[1], verbose=verbose)
                        sys.stdout.write('## Connected.\n')
                    except Exception, ex:
                        if verbose:
                            traceback.print_exc()
                            
                        sys.stdout.write('## Failed.\n')
                pass

            rtc_names = []
            rtcs = []
            for ns in nss:
                rtc_names = rtc_names + [admin.systembuilder.get_component_full_path(rtc) for rtc in ns.rtcs]
                rtcs = rtcs + ns.rtcs

            # Interactive Configure
            def select_rtc(ans):
                confs = admin.systemeditor.get_active_configuration_data(rtcs[ans])
                conf_names = [conf.name +':' + conf.data for conf in confs]
        
                def select_conf(ans2):
                    key = confs[ans2].name
                    sys.stdout.write(' INPUT (%s):' % key)
                    val = raw_input()
                    if util.yes_no('%s = %s. Okay?' % (key, val)) == 'yes':
                        admin.systembuilder.set_active_configuration_data(rtcs[ans], key, val)
                        return True
                    return False
                util.choice(conf_names, select_conf, msg='Select Configuration')
                return False
            util.choice(rtc_names, select_rtc, msg='Select RTC')


            #Save Running System
            if util.yes_no('# Save System ?') == 'yes':
                filename = os.path.basename(package.default_system_filepath)
                while True:
                    if util.yes_no('# Rename filename? (default:%s)' % filename) == 'yes':
                        while True:
                            sys.stdout.write('# Input:')
                            val = raw_input()
                            if util.yes_no('# New Filename = %s. Okay?' % val) == 'yes':
                                filename = val
                                break
                            pass
                        pass
                    # File check
                    filepath = os.path.join(package.get_systempath(fullpath=True), filename)
                    sys.stdout.write('## Saving to %s\n' % filepath)
                    if os.path.isfile(filepath):
                        if util.yes_no('## Overwrite?') == 'yes':
                            newfilename = filepath + wasanbon.timestampstr()
                            sys.stdout.write('## Rename existing file to %s\n' % os.path.basename(newfilename))
                            os.rename(filepath, newfilename)
                            break
                    else:
                        break

                while True:
                    sys.stdout.write('# Input Vendor Name:')
                    vendorName = raw_input()
                    sys.stdout.write('# Input Version:')
                    version = raw_input()
                    sys.stdout.write('# Input System Name (%s)' % package.name)
                    systemName = raw_input()
                    if len(systemName) == 0:
                        systemName = package.name
                    
                    sys.stdout.write('## Vendor Name = %s\n' % vendorName)
                    sys.stdout.write('## Version     = %s\n' % version)
                    sys.stdout.write('## System Name = %s\n' % systemName)
                    if util.yes_no('# Okay?') == 'yes':
                        break
                    else:
                        sys.stdout.write('# Retry')

                for i in range(5):
                    try:
                        sys.stdout.write('# Saving to %s\n' % filepath)
                        admin.systemeditor.save_to_file(nss, filepath, verbose=verbose)
                        break
                    except:
                        traceback.print_exc()
                        time.sleep(1.0)                        
                        pass
                pass
            else:
                sys.stdout.write('## Aborted.')
            
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

        return 0

