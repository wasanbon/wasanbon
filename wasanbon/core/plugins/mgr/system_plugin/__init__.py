import os, sys, signal, time, traceback, threading

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

endflag = False
ev = threading.Event()

class Plugin(PluginFunction):
    """ System Management (Launch, Installing RTCs, Configuration, and Connection) """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 
                'admin.package', 
                'admin.rtc', 
                'admin.systeminstaller', 
                'admin.systemlauncher', 
                'admin.systembuilder', 
                'admin.nameserver',
                'admin.systemeditor',
                'admin.rtcconf']

    def _print_rtcs(self, args):
        pack = admin.package.get_package_from_path(os.getcwd())
        for rtc in admin.rtc.get_rtcs_from_package(pack):
            print rtc.rtcprofile.basicInfo.name
        
    @manifest 
    def install(self, args):
        """ Install RTCs to System
        $ mgr.py system install [RTC_NAME]
        """
        self.parser.add_option('-f', '--force', help='Force option (default=True)', default=True, action='store_true', dest='force_flag')
        self.parser.add_option('-s', '--standalone', help='Install Standalone RTC(default=False)', default=False, action='store_true', dest='standalone_flag')
        self.parser.add_option('-d', '--duplicate', help='Allow Duplicate RTC Creation(default=False)', default=False, action='store_true', dest='allow_duplicate')
        options, argv = self.parse_args(args[:], self._print_rtcs)
        verbose = options.verbose_flag
        force  = options.force_flag
        standalone = options.standalone_flag
        allow_duplicate = options.allow_duplicate
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
                                                               conffile=None, 
                                                               allow_duplication=allow_duplicate)

            
            if ret != 0:
                retval = ret

        return retval

    @manifest
    def uninstall(self, args):
        """ Uninstall RTC from system.
        $ mgr.py system uninstall [RTC_NAME]
        """
        
        options, argv = self.parse_args(args[:], self._print_rtcs)
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
    def is_running(self, args):
        """ Check System is running or not 
        $ mgr.py system is_running
        This command will output True or False on console.
        """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        #background = options.background_flag

        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        print admin.systemlauncher.is_launched(package)

        return 0
        
    @manifest
    def terminate(self, args):
        """ Terminate Launched System.
        $ mgr.py system terminate
        """
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
                traceback.print_exc()
                return -1
            return -1
        return 0


    @manifest
    def run(self, args):
        """ Launch System 
        $ mgr.py system run """
        #self.parser.add_option('-f', '--force', help='Force option (default=True)', default=True, action='store_true', dest='force_flag')
        #self.parser.add_option('-s', '--standalone', help='Install Standalone RTC(default=False)', default=False, action='store_true', dest='standalone_flag')
        self.parser.add_option('-b', '--background', help='Launch in background(default=False)', default=False, action='store_true', dest='background_flag')
        self.parser.add_option('-w', '--wakeuptimeout', help='Timeout of Sleep Function when waiting for the wakeup of RTC-Daemons', default=5, dest='wakeuptimeout', action='store', type='float')
        self.parser.add_option('-f', '--file', help='Build System with Specific RTSProfile (must be placed in system_dir', default=None, dest='systemfile', action='store', type='string')
        self.parser.add_option('-p', '--plain', help='Plain Launch. Without building/activating system.', default=False, dest='plain_flag', action='store_true')
        self.parser.add_option('-q', '--quiet', help='Build system but do not activate RTCs.', default=False, dest='quiet_flag', action='store_true')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        background = options.background_flag
        wakeuptimeout = options.wakeuptimeout
        systemfile = options.systemfile
        plain = options.plain_flag
        quiet = options.quiet_flag

        if plain:
            quiet = True
            
        #force  = options.force_flag
        #standalone = options.standalone_flag
            
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)

        if systemfile:
            systemfile = os.path.join(package.get_systempath(), systemfile)

        started_nss = []
        nss = admin.nameserver.get_nameservers_from_package(package, verbose=verbose)
        for ns in nss:
            if not admin.nameserver.is_running(ns, verbose=verbose, try_count=5, interval=5.0):
                sys.stdout.write('## Nameserver %s is not running.\n' % ns.path)
                if ns.address == 'localhost' or ns.address == '127.0.0.1':
                    if verbose: '# Start Nameserver %s\n' % ns.path
                    admin.nameserver.launch(ns, verbose=verbose)
                    started_nss.append(ns)
                    wasanbon.sleep(5.0)

        global endflag
        endflag = False
        try:
            processes = admin.systemlauncher.launch_system(package, verbose=verbose)
            wasanbon.sleep(wakeuptimeout)
            if not plain:

                admin.systembuilder.build_system(package, 
                                                 verbose=verbose, 
                                                 system_file=systemfile)

                if not quiet:
                    admin.systembuilder.activate_system(package, 
                                                        verbose=verbose,
                                                        system_file=systemfile)

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
                    languages = ['Java', 'Python', 'C++']
                    stopped = []
                    for l in languages:
                        stopped.append(not admin.systemlauncher.is_rtcd_launched(package, l, verbose=verbose))
                    stopped.append(not admin.systemlauncher.is_standalone_rtcs_launched(package, verbose=verbose))
                    if all(stopped):
                        endflag = True
                except IOError, e:
                    print e
                    pass
                pass

            if not plain:
                admin.systembuilder.deactivate_system(package, 
                                                      verbose=verbose, 
                                                      system_file=systemfile)
            
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

        for ns in started_nss:
            if verbose: '# Stopping Nameserver %s\n' % ns.path
            admin.nameserver.terminate(ns, verbose=verbose)

        return 0



    @manifest
    def build(self, args):
        """ Build System in Console interactively 
        $ mgr.py system build """
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

            for ns in nss:
                ns.refresh(verbose=verbose)
            # Interactive Connect
            pairs = admin.systemeditor.get_connectable_pairs(nss, verbose=verbose)
            from wasanbon import util
            for pair in pairs:
                if util.no_yes('# Connect? (%s->%s)\n' % (admin.systembuilder.get_port_full_path(pair[0]),
                                                          admin.systembuilder.get_port_full_path(pair[1]))) == 'yes':
                    while True:
                        try:
                            admin.systembuilder.connect_ports(pair[0], pair[1], verbose=verbose)
                            sys.stdout.write('## Connected.\n')
                            break
                        except Exception, ex:
                            if verbose:
                                traceback.print_exc()
                                pass
                            sys.stdout.write('## Failed. \n')
                            if util.yes_no('### Retry?') == 'no':
                                break
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
                    sys.stdout.write('# Input System Name (%s):' % package.name)
                    systemName = raw_input()
                    if len(systemName) == 0:
                        systemName = package.name
                    sys.stdout.write('# Input Description of System (abstract):')
                    abstract = raw_input()
                    
                    sys.stdout.write('## Vendor Name = %s\n' % vendorName)
                    sys.stdout.write('## Version     = %s\n' % version)
                    sys.stdout.write('## System Name = %s\n' % systemName)
                    sys.stdout.write('## Abstract    = %s\n' % abstract)
                    if util.yes_no('# Okay?') == 'yes':
                        break
                    else:
                        sys.stdout.write('# Retry')

                for i in range(5):
                    try:
                        sys.stdout.write('# Saving to %s\n' % filepath)
                        admin.systemeditor.save_to_file(nss, filepath, 
                                                        system_name=systemName,
                                                        abstract=abstract,
                                                        version=version,
                                                        vendor=vendorName,
                                                        verbose=verbose)
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


    @manifest
    def configure(self, args):
        """ Configure system interactively in console.
        $ mgr.py system configure """
        self.parser.add_option('-f', '--file', help='Configure with Specific RTSProfile (must be placed in system_dir', default=None, dest='systemfile', action='store', type='string')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        package = admin.package.get_package_from_path(os.getcwd())
        if options.systemfile:
            filename = os.path.join(package.get_systempath(), options.systemfile)
        else:
            filename = package.default_system_filepath
        from rtsprofile.rts_profile import RtsProfile
        file = open(filename, 'r')
        rtsprofile = RtsProfile(xml_spec = file)
	del(file)
        rtc_names = [rtc.instance_name for rtc in rtsprofile.components]
        
        from wasanbon import util
        def select_rtc(ans):
            rtc = rtsprofile.components[ans]
            confs = []
            active_conf_index = -1
            if len(rtc.configuration_sets) != 0:
                for i, conf in enumerate(rtc.configuration_sets):
                    if conf.id == rtc.active_configuration_set:
                        active_conf_index = i
                        confs = conf.configuration_data
            conf_names = [conf.name +':' + conf.data for conf in confs]
        
            def select_conf(ans2):
                key = confs[ans2].name
                sys.stdout.write('## INPUT (%s):' % key)
                val = raw_input()
                if util.yes_no('# %s = %s. Okay?' % (key, val)) == 'yes':
                    rtc.configuration_sets[active_conf_index].configuration_data[ans2].data = val
                    return True
                return False
            util.choice(conf_names, select_conf, msg='# Select Configuration')
            return False
        
        util.choice(rtc_names, select_rtc, msg='# Select RTC')
        
        if util.yes_no("Save System?") != 'yes':
            sys.stdout.write('# Aborted \n')
            return 0
        while True:
            if util.no_yes('Rename Filename?') == 'yes':
                filepath = os.path.join(package.get_systempath(), raw_input('Filename:'))
            else:
                filepath = filename
                newfile = filepath + wasanbon.timestampstr()
                try:
                    os.rename(filepath, newfile)
                except Exception, e:
                    sys.stdout.write('## Exception occurred when renaming file.\n')
                    traceback.print_exc()
                    continue
            try:
                fout = open(filepath, 'w')
                fout.write(rtsprofile.save_to_xml())
                fout.close()
            except:
                sys.stdout.write('## Exception occurred when saving file.\n')
                traceback.print_exc()
                continue
            break

        return 0

    @manifest
    def switch(self, args):
        """ Switch RT-System 
        $ mgr.py system switch [SYSTEM_FILENAME] 
        The SYSTEM_FILENAME file must be included in RTS_DIR (defined in setting.yaml) """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        
        package = admin.package.get_package_from_path(os.getcwd())
        filenames = [file for file in os.listdir(package.get_systempath()) if file.endswith('.xml')]
        from wasanbon import util
        def filter_func(ans):
            file = filenames[ans]
            import yaml
            dict = yaml.load(open(package.setting_file_path, 'r'))
            setting_file_path = package.setting_file_path
            archive_path = os.path.join(package.path, 'backup')
            if not os.path.isdir(archive_path):
                os.mkdir(archive_path)
            archived_file_path = os.path.join(archive_path, 'setting.yaml' + wasanbon.timestampstr())
            os.rename(setting_file_path, archived_file_path)
            dict['application']['system'] = file
            open(setting_file_path, 'w').write(yaml.dump(dict, encoding='utf8', allow_unicode=True, default_flow_style=False))
            return False

        util.choice(filenames, filter_func, msg='# Select System File')
        return 0
    
    @manifest
    def list(self, args):
        """ List Systems installed.
        $ mgr.py system list """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        long = options.long_flag

        package = admin.package.get_package_from_path(os.getcwd())
        filenames = [file for file in os.listdir(package.get_systempath()) if file.endswith('.xml') and not file.startswith('.')]

        defaultSystemPath = package.default_system_filepath
        for file in filenames:
            path = os.path.join(package.get_systempath(), file)
            if not long:
                sys.stdout.write('- %s\n' % file)
            else:
                from rtsprofile import rts_profile
                try:
                    rtsp = rts_profile.RtsProfile(open(os.path.join(package.get_systempath(), file), 'r'))
                except:
                    sys.stdout.write('%s : \n' % file)
                    sys.stdout.write('  status : error\n')
                    if verbose:
                        traceback.print_exc()
                    continue
                #sys.stdout.write(str(dir(rtsp)))
                sys.stdout.write('%s : \n' % file)
                sys.stdout.write('  default  : %s\n' % str(defaultSystemPath == path))
                sys.stdout.write('  status   : success\n')
                sys.stdout.write('  id       : %s\n' % rtsp.id)
                sys.stdout.write('  abstract : %s\n' % rtsp.abstract)
                if len(rtsp.components) > 0:
                    sys.stdout.write('  components:\n')
                    for comp in rtsp.components:
                        sys.stdout.write('    %s : \n' % comp.instance_name)
                        sys.stdout.write('      id                       : %s\n' % comp.id)
                        sys.stdout.write('      path_uri                 : %s\n' % comp.path_uri)
                        sys.stdout.write('      is_required              : %s\n' % comp.is_required)
                        sys.stdout.write('      active_configuration_set : %s\n' % comp.active_configuration_set)
                        if len(comp.configuration_sets) > 0:
                            sys.stdout.write('      configurations_sets :\n')
                            for conf_set in comp.configuration_sets:
                                sys.stdout.write('        %s : \n' % conf_set.id)
                                for conf in conf_set.configuration_data:
                                    sys.stdout.write('          %s : %s\n' % (conf.name, conf.data))
                    

    @manifest
    def list_rtc(self, args):
        """ List RTCs installed.
        $ mgr.py system list """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        
        package = admin.package.get_package_from_path(os.getcwd())
        rtcconf_paths = package.rtcconf
        for language, rtcconf_path in rtcconf_paths.items():
            rtcconf = admin.rtcconf.RTCConf(rtcconf_path)
            sys.stdout.write('%s :\n' % language)
            sys.stdout.write('  conf_file : %s\n' % rtcconf_path)
            sys.stdout.write('  rtcd :\n')
            sys.stdout.write('    uri            : %s\n' % rtcconf['corba.master_manager'])
            sys.stdout.write('    nameservers    : %s\n' % rtcconf['corba.nameservers'])
            sys.stdout.write('    installed_rtcs : %s\n' % rtcconf['manager.components.precreate'])

    
    @manifest
    def dump(self, args):
        self.parser.add_option('-f', '--file', help='Build System with Specific RTSProfile (must be placed in system_dir', default=None, dest='systemfile', action='store', type='string')
        options, argv = self.parse_args(args[:])
        systemfile = options.systemfile
        verbose = options.verbose_flag
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)

        if systemfile is None:
            systemfile = package.default_system_filepath
        else:
            systemfile = os.path.join(package.get_systempath(), systemfile)

        if not os.path.isfile(systemfile):
            print '# File Not Found.'
            return -1

        for line in open(systemfile, 'r'):
            sys.stdout.write(line)
        return 0


    @manifest
    def cat(self, args):
        self.parser.add_option('-f', '--file', help='Build System with Specific RTSProfile (must be placed in system_dir', default=None, dest='systemfile', action='store', type='string')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        systemfile = options.systemfile
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        if systemfile is None:

            systemfile = package.default_system_filepath
        else:
            systemfile = os.path.join(package.get_systempath(), systemfile)

        if os.path.isfile(systemfile):
            newfile = systemfile + wasanbon.timestampstr()
            os.rename(systemfile, newfile)

        fout = open(systemfile, 'w')
        fout.write(argv[3])
        fout.close()

        sys.stdout.write('Success\n')
        return 0

    @manifest
    def copy(self, args):
        self.parser.add_option('-f', '--force', help='Force Delete without yes/no option (default=False)', default=False, dest='force_flag', action='store_true')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        force = options.force_flag
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        wasanbon.arg_check(argv, 5)
        srcfile = argv[3]
        dstfile = argv[4]
        srcfile_relpath = os.path.join(package.get_systempath(fullpath=False), srcfile)
        srcfile_fullpath = os.path.join(package.get_systempath(), srcfile)
        if not os.path.isfile(srcfile_fullpath):
            sys.stdout.write('## No System File exists.\n')
            return -1

        dstfile_fullpath = os.path.join(package.get_systempath(), dstfile)
        if os.path.isfile(dstfile_fullpath):
            if not force:
                from wasanbon import util
                if util.no_yes('# Overwrite? (%s):' % systemfile_relpath) == 'no':
                    sys.stdout.write('## Aborted.\n')
                    return 0
            newfile = dstfile_fullpath + wasanbon.timestampstr()
            os.rename(dstfile_fullpath, newfile)
        
        import shutil
        shutil.copyfile(srcfile_fullpath, dstfile_fullpath)
        sys.stdout.write('## Success\n')
        return 0
        

    @manifest
    def delete(self, args):
        self.parser.add_option('-f', '--force', help='Force Delete without yes/no option (default=False)', default=False, dest='force_flag', action='store_true')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        force = options.force_flag
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        systemfile = argv[3]
        systemfile_relpath = os.path.join(package.get_systempath(fullpath=False), systemfile)
        systemfile_fullpath = os.path.join(package.get_systempath(), systemfile)
        if not os.path.isfile(systemfile_fullpath):
            sys.stdout.write('## No System File exists.\n')
            return -1

        if not force:
            from wasanbon import util
            if util.no_yes('# Delete? (%s):' % systemfile_relpath) == 'no':
                sys.stdout.write('## Aborted.\n')
                return 0
        
        newfile = systemfile_fullpath + wasanbon.timestampstr()
        os.rename(systemfile_fullpath, newfile)

        sys.stdout.write('## Success\n')
        return 0
