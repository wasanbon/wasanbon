import os, sys, shutil

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ This plugin provides APIs to install RTCs into System (automatically editting rtc.conf for rtcd to load RTCs when launched) """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.rtcconf', 'admin.rtc']

    def get_installed_rtc_names(self, package, language='all', verbose=False):
        rtcs = []
        languages = ['C++', 'Java', 'Python']
        
        if language != 'all':
            languages = [language]
        for lang in languages:
            rtcconf = admin.rtcconf.RTCConf(package.rtcconf[lang])
            key = 'manager.components.precreate'
            rtcs = rtcs + [rtc.strip() for rtc in rtcconf[key].split(',') if len(rtc.strip()) != 0]
        return rtcs

    def __get_rtc_name_from_standalone_command(self, package, cmd):
        rtc_launch_cmd = cmd.split()[0]
        post_fix = 'Comp'
        if sys.platform == 'win32':
            post_fix = 'Comp.exe'
        if rtc_launch_cmd.startswith(package.get_binpath(fullpath=False)) and rtc_launch_cmd.endswith(post_fix):
            return rtc_launch_cmd[len(package.get_binpath(fullpath=False))+1:-(len(post_fix))]
        elif rtc_launch_cmd.startswith(package.get_rtcpath(fullpath=False)) and rtc_launch_cmd.endswith('.py'):
            elems = rtc_launch_cmd.split('/')
            cmd = elems[len(elems)-1]
            return cmd[:-(3)]
        else:
            return ""

    def get_rtcd_nameservers(self, package, verbose=False):
        all_nss = {}
        for lang in ['C++', 'Java', 'Python']:
            rtcconf = admin.rtcconf.RTCConf(package.rtcconf[lang])
            key  = 'corba.nameservers'
            nss = []
            for ns in [ns.strip() for ns in rtcconf[key].split(',')]:
                if not ':' in ns: ns = ns + ':2809'
                if not ns in nss: nss.append(ns)
            all_nss[lang] = nss
        return all_nss
        
    def get_rtcd_manager_addresses(self, package, verbose=False):
        all_nss = self.get_rtcd_nameservers(package, verbose=verbose)

        manager_addrs = {}
        for lang in ['C++', 'Java', 'Python']:
            rtcconf = admin.rtcconf.RTCConf(package.rtcconf[lang])
            naming_rule_of_manager = rtcconf['manager.naming_formats'] # %n_cpp.mgr
            name = naming_rule_of_manager.replace('%n', 'manager').strip()
            
            if len(all_nss[lang]) == 0:
                manager_addrs[lang] = ['localhost:2809/%s' % name]
            else:
                manager_addrs[lang] = [ns + '/'+ name for ns in all_nss[lang]]
        return manager_addrs
        
    def get_installed_standalone_rtc_names(self, package, verbose=False):
        rtcs = []
        setting = package.setting
        cmds = setting.get('standalone', [])
        for cmd in cmds:
            rtc_name = self.__get_rtc_name_from_standalone_command(package, cmd)
            if len(rtc_name) == 0: continue
            try:
                rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
                rtcs.append(rtc_name)
            except wasanbon.RTCNotFoundException:
                pass
        return rtcs

    def is_installed(self, package, rtc, verbose=False, standalone=False):
        name = rtc.rtcprofile.basicInfo.name
        if not standalone:
            return name in self.get_installed_rtc_names(package, verbose=verbose)
        else:
            return name in self.get_installed_standalone_rtc_names(package, verbose=verbose)


    

    def install_rtc_in_package(self, package, rtc, verbose=False, 
                               preload=True, precreate=True, copy_conf=True, 
                               rtcconf_filename="", 
                               copy_bin=True, standalone=False, conffile=None, allow_duplication=False):
        if verbose: sys.stdout.write('# Installing RTC in package %s\n' % package.name)

        if not standalone and self.is_installed(package, rtc, standalone=True, verbose=verbose):
            if verbose:
                sys.stdout.write('## RTC (%s) is already installed as standalone.\n' % rtc.name)
                sys.stdout.write('## Install standalone again.\n')
            standalone = True
        
        if standalone:
            name = rtc.rtcprofile.basicInfo.name
            targetconf = os.path.join(package.get_confpath(), 'rtc_' + name + '.conf')
            conffilepath = package.rtcconf[rtc.rtcprofile.language.kind]
            shutil.copy(conffilepath, targetconf)
            rtcconf = admin.rtcconf.RTCConf(targetconf)
            rtcconf['manager.modules.load_path'] = ''
            rtcconf['manager.modules.preload'] = ''
            rtcconf['manager.components.precreate'] = ''
            rtcconf['manager.is_master'] = 'NO'
            rtcconf['logger.file_name'] = './log/standalonertc_%s' % name
            for key in rtcconf.keys():
                if key.find('config_file') > 0:
                    rtcconf.pop(key)
            targetconf = os.path.join(package.get_confpath(fullpath=False), 'rtc_' + name + '.conf')
            targetconf = targetconf.replace('\\', '/')
        else: # not standalone
            if len(rtcconf_filename) == 0:
                rtcconf = admin.rtcconf.RTCConf(package.rtcconf[rtc.rtcprofile.language.kind])
            else:
                rtcconf = admin.rtcconf.RTCConf(rtcconf_filename)
            
                
        targetfile = copy_binary_from_rtc(package, rtc, verbose=verbose, standalone=standalone)

        if len(targetfile) == 0:
            targetfile = os.path.join(package.get_binpath(fullpath=False), rtc.get_rtc_file_path())
            pass

        rtc_count = 0
        if standalone:
            backup_dir = os.path.join(package.path, 'backup')
            if not os.path.isdir(backup_dir):
                os.mkdir(backup_dir)
            setting_filename = os.path.join(package.path, 'setting.yaml')
            backup_filename = os.path.join(backup_dir, 'setting.yaml'+wasanbon.timestampstr())
            shutil.copy(setting_filename, backup_filename)
            import yaml
            dic = yaml.load(open(backup_filename, 'r'))

            cmd_list = [cmd for cmd in dic['application'].get('standalone', []) if cmd.startswith(targetfile)]
            if len(cmd_list) == 0:
                dic['application']['standalone'] = dic['application'].get('standalone', []) + [targetfile + ' -f ' + targetconf]
            open(setting_filename, 'w').write(yaml.dump(dic, default_flow_style=False))
            pass

        else: # If not standalone
            if verbose: sys.stdout.write('### Setting manager.modules.load_path:\n')
            rtcconf.append('manager.modules.load_path', os.path.dirname(targetfile))
            if verbose: sys.stdout.write('### OK.\n')
            if preload:
                if verbose: sys.stdout.write('### Setting manager.modules.preload:\n')
                rtcconf.append('manager.modules.preload', os.path.basename(targetfile))
                if verbose: sys.stdout.write('### OK.\n')
            if precreate:
                if verbose: sys.stdout.write('### Setting manager.components.precreate:\n')
                rtc_count = rtcconf.append('manager.components.precreate', rtc.rtcprofile.basicInfo.name, verbose=verbose, allow_duplicate=allow_duplication) 
                if rtc_count > 0:
                    if verbose: sys.stdout.write('### OK.\n')
                else:
                    if verbose: sys.stdout.write('### Failed.\n')
                    return -1

        if conffile == None:
            confpath = copy_conf_from_rtc(package, rtc, verbose=verbose, force=copy_conf, rtc_count=rtc_count-1)
        else:
            confpath = conffile
        if confpath:
            key = rtc.rtcprofile.basicInfo.category + '.' + rtc.rtcprofile.basicInfo.name + '%s.config_file' % (rtc_count-1)
            if verbose:
                sys.stdout.write('## Configuring System. Set (%s) to %s\n' % (key, confpath))
            rtcconf.append(key, confpath)

        rtcconf.sync()

        return 0

    def uninstall_rtc_from_package(self, package, rtc, rtcconf_filename=None, verbose=False):
        if self.is_installed(package, rtc, standalone=True):
            return self.uninstall_standalone_rtc_from_package(package, rtc, verbose=verbose)
            
        if verbose: sys.stdout.write('## Uninstall RTC (%s) from package\n' % rtc.rtcprofile.basicInfo.name)
        if rtcconf_filename:
            rtcconf = admin.rtcconf.RTCConf(rtcconf_filename)
        else:
            rtcconf = admin.rtcconf.RTCConf(package.rtcconf[rtc.rtcprofile.language.kind])

        name = rtc.rtcprofile.basicInfo.name 
        targetfile = os.path.join(package.get_binpath(), os.path.basename(rtc.get_rtc_file_path()))
        language = rtc.rtcprofile.language.kind
        if language == 'C++':
            filename = name + wasanbon.get_bin_file_ext()
        elif language == 'Java':
            filename = name + '.jar'
        elif language == 'Python':
            filename = name + '.py'
        else:
            raise wasanbon.UnsupportedSystemException()

        rtcconf.remove('manager.components.precreate', name, verbose=verbose)
        if len(rtcconf['manager.components.precreate'].strip()) == 0:
            rtcconf.remove('manager.components.precreate')

        rtcconf.remove('manager.modules.preload', filename, verbose=verbose)
        if len(rtcconf['manager.modules.preload'].strip()) == 0:
            rtcconf.remove('manager.modules.preload')
            rtcconf.remove('manager.modules.load_path')

        keys = [rtc.rtcprofile.basicInfo.category + '.' + rtc.rtcprofile.basicInfo.name + '.config_file']
        for i in range(0, 16):
            keys.append(rtc.rtcprofile.basicInfo.category + '.' + rtc.rtcprofile.basicInfo.name + str(i) + '.config_file')

        for k in keys:
            rtcconf.remove(k)

        rtcconf.sync()

    def uninstall_all_rtc_from_package(self, package, rtcconf_filename=None, verbose=False):
        if verbose: sys.stdout.write('## Uninstall All RTC from conf in package\n')
        if rtcconf_filename:
            rtcconf = admin.rtcconf.RTCConf(rtcconf_filename)
        else:
            rtcconf = admin.rtcconf.RTCConf(package.rtcconf[rtc.rtcprofile.language.kind])

        rtcconf.remove('manager.components.precreate')
        rtcconf.remove('manager.modules.preload')
        rtcconf.remove('manager.modules.load_path')
        """
        keys = [rtc.rtcprofile.basicInfo.category + '.' + rtc.rtcprofile.basicInfo.name + '.config_file']
        for i in range(0, 16):
            keys.append(rtc.rtcprofile.basicInfo.category + '.' + rtc.rtcprofile.basicInfo.name + str(i) + '.config_file')
        for k in keys:
            rtcconf.remove(k)
        """
        rtcconf.sync()

    def uninstall_standalone_rtc_from_package(self, package, rtc, verbose=False):
        rtcs = []
        cmds = setting = package.setting.get('standalone', [])
        uninstall_cmd = None
        for cmd in cmds:
            if self.__get_rtc_name_from_standalone_command(package, cmd) == rtc.rtcprofile.basicInfo.name:
                if verbose: sys.stdout.write('## Uninstalling RTC (%s) from package (--standalone mode)\n' % rtc.rtcprofile.basicInfo.name)
                uninstall_cmd = cmd

        backup_dir = os.path.join(package.path, 'backup')
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)
            pass
        setting_filename = os.path.join(package.path, 'setting.yaml')
        backup_filename = os.path.join(backup_dir, 'setting.yaml'+wasanbon.timestampstr())
        shutil.copy(setting_filename, backup_filename)
        import yaml
        dic = yaml.load(open(backup_filename, 'r'))
        cmd_list = [cmd for cmd in dic['application'].get('standalone', []) if cmd != uninstall_cmd]
        if len(cmd_list) == 0 and 'standalone' in dic['application'].keys():
            del dic['application']['standalone']
        open(setting_filename, 'w').write(yaml.dump(dic, default_flow_style=False))
        return 0

def copy_binary_from_rtc(package, rtc, verbose=False, standalone=False):
    if standalone:
        filepath = rtc.get_rtc_executable_file_path(verbose=verbose)
    else:
        filepath = rtc.get_rtc_file_path(verbose=verbose)

    if verbose: sys.stdout.write('## Copying RTC Binary File from %s to %s\n' % (filepath, 'bin'))

    if len(filepath) == 0:
        sys.stdout.write("    - Can not find RTC file in RTC's directory\n")
        return ""
    

    if verbose: sys.stdout.write('## Detect RTC binary %s\n' % filepath)

    if rtc.rtcprofile.language.kind == 'Python':
        norm_path = os.path.normcase(os.path.normpath(os.path.split(filepath)[0]))
        prefix = os.path.commonprefix([package.path, norm_path])
        bin_dir_rel = norm_path[len(package.path)+1:]
        targetfile = os.path.join(bin_dir_rel, os.path.basename(filepath))
    else:
        bin_dir = package.get_binpath()
        bin_dir_rel = package.get_binpath(fullpath=False)
        if not os.path.isdir(bin_dir):
            os.mkdir(bin_dir)
            pass

        if standalone:
            target = os.path.join(bin_dir, os.path.basename(filepath))
            shutil.copy(filepath, target)
            pass
        else:

            if sys.platform == 'darwin':
                ext = 'dylib'
            elif sys.platform == 'win32':
                ext = 'dll'
            elif sys.platform == 'linux2':
                ext = 'so'
                pass
                
            files = [filepath]
                # dlls in the same directry must be copied with rtc's binary.
            for file in os.listdir(os.path.dirname(filepath)):
                if file.endswith(ext):
                    files.append(os.path.join(os.path.dirname(filepath), file))
                    pass
                pass

            for file in files:
                target = os.path.join(bin_dir, os.path.basename(file))
                shutil.copy(filepath, target)
                pass

        targetfile = os.path.join(bin_dir_rel, os.path.basename(filepath))
    targetfile = targetfile.replace('\\', '/')
    return targetfile


def copy_conf_from_rtc(package, rtc, verbose=False, force=False, rtc_count=0):
    conffile = rtc.get_rtc_conf_path(verbose=verbose)
    if len(conffile) == 0:
        sys.stdout.write('## No configuration file for RTC (%s) is found.\n' % rtc.rtcprofile.basicInfo.name)
        return []
    targetconf = os.path.join(package.path, 'conf', os.path.basename(conffile))
    targetconf = targetconf[:-5] + '%s' % rtc_count + '.conf'
    if os.path.isfile(targetconf):
        if verbose:  sys.stdout.write('## Found %s.\n' % targetconf)
        if force:
            if verbose: sys.stdout.write('## Force Copying Config (%s -> %s)\n' % (conffile, targetconf))
            shutil.copy(conffile, targetconf)
        else:
            if verbose:  sys.stdout.write('## Do not copy.\n')
            pass
    else:
        if verbose: sys.stdout.write('# Copying Config (%s -> %s)\n' % (conffile, targetconf))
        shutil.copy(conffile, targetconf)
    confpath = 'conf' + '/' + os.path.basename(targetconf)
    if sys.platform == 'win32':
        confpath.replace('\\', '\\\\')
    return confpath
