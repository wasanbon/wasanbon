import os, sys, yaml, subprocess, shutil, types, time, stat, psutil
import wasanbon
#from wasanbon.core import rtc
import wasanbon.core.rtc

from wasanbon.util import git
#from wasanbon.util import github_ref
from wasanbon.core import nameserver
from wasanbon.core.package import run
from wasanbon.core.package import workspace, repository



class Package():

    def __init__(self, path):
        self._path = path
        if not os.path.isfile(os.path.join(path, 'setting.yaml')):
            raise wasanbon.InvalidPackagePathError()
        self._rtcs = []
        self._name = os.path.basename(path)
        self._process = {'standalone':[]}
        self._languages = ['C++', 'Python', 'Java']
        self._setting = []
        self._nameservers = []
        pass

    @property
    def name(self):
        return self._name

    @property
    def pid_path(self):
        return os.path.join(self.path, self.pid_rel_path)

    @property
    def pid_rel_path(self):
        return 'pid'

    @property
    def bin_path(self):
        return os.path.join(self.path, self.bin_rel_path)

    @property
    def bin_rel_path(self):
        return self.setting['BIN_DIR']
    
    @property
    def rtc_path(self):
        return os.path.join(self.path, self.setting['RTC_DIR'])

    @property
    def conf_path(self):
        return os.path.join(self.path, self.conf_rel_path)

    @property
    def conf_rel_path(self):
        stg = self.setting
        return stg.get('CONF_DIR', 'conf')

    @property
    def repository(self):
        git_obj = wasanbon.util.git.GitRepository(self.path)
        return repository.PackageRepository(self.name, url=git_obj.url, desc="")

    @property
    def system_path(self):
        return os.path.join(self.path, self.setting['RTS_DIR'])

    @property
    def system_file(self):
        return os.path.join(self.path, self.setting['system'])

    def get_build_delay(self):
        stg = self.setting
        if 'build_delay' in stg.keys():
            return int(stg['build_delay'])
        else:
            return 5

    @property
    def rtc_repositories(self):
        repos = []
        dic = yaml.load(open(os.path.join(self.path, self.setting['RTC_DIR'], 'repository.yaml'), 'r'))
        #print os.path.join(self.path, self.setting['RTC_DIR'], 'repository.yaml')
        for name, value in dic.items():
            repos.append(wasanbon.core.rtc.RtcRepository(name=name, url=value['git'], desc=value['description'], hash=value.get('hash', "")))
        return repos

    def append_rtc_repository(self, repo, verbose=False):
        repo_file = os.path.join(self.path, self.setting['RTC_DIR'], 'repository.yaml')
        bak_file = repo_file + '.bak'
        if os.path.isfile(bak_file):
            os.remove(bak_file)
        shutil.copy(repo_file, bak_file)
        dic = yaml.load(open(bak_file, 'r'))
        if not dic:
            dic = {}
        dic[repo.name] = {'git': repo.url, 'description':repo.description, 'hash':repo.hash}
        yaml.dump(dic, open(repo_file, 'w'), encoding='utf8', allow_unicode=True)
        pass

    def update_rtc_repository(self, repo, verbose=False):
        repo_file = os.path.join(self.path, self.setting['RTC_DIR'], 'repository.yaml')
        bak_file = repo_file + '.bak'
        if os.path.isfile(bak_file):
            os.remove(bak_file)
        shutil.copy(repo_file, bak_file)
        dic = yaml.load(open(bak_file, 'r'))
        if not dic:
            dic = {}
        dic[repo.name] = {'git': repo.url, 'description':repo.description, 'hash':repo.hash}
        yaml.dump(dic, open(repo_file, 'w'), encoding='utf8', allow_unicode=True)
        pass

    def remove_rtc_repository(self, name, verbose=False):
        repo_file = os.path.join(self.path, self.setting['RTC_DIR'], 'repository.yaml')
        bak_file = repo_file + '.bak'
        if os.path.isfile(bak_file):
            os.remove(bak_file)
        shutil.copy(repo_file, bak_file)
        dic = yaml.load(open(bak_file, 'r'))
        #dic[repo.name] = {'git': repo.url, 'description':repo.description, 'hash':repo.hash}
        if not dic:
            dic = {}
        if name in dic.keys():
            dic.pop(name)
        yaml.dump(dic, open(repo_file, 'w'), encoding='utf8', allow_unicode=True)
        pass
        

    @property
    def rtcs(self):
        if not self._rtcs:
            for dir in os.listdir(os.path.join(self.path, self.setting['RTC_DIR'])):
                if dir.startswith('.') or dir == 'repository.yaml':
                    pass
                else:
                    try:
                        rtc_obj = wasanbon.core.rtc.RtcObject(os.path.join(self.path, self.setting['RTC_DIR'], dir))
                        self._rtcs.append(rtc_obj)
                    except wasanbon.RTCProfileNotFoundException, ex:
                        pass
                    except Exception, ex:
                        print ex
                        pass
        return self._rtcs

    def rtc(self, name, verbose=True, suppress_exception=False):
        for rtc_ in self.rtcs:
            if rtc_.name == name:
                return rtc_
        if verbose:
            sys.stdout.write(' - Can not find RTC %s\n' % name)
        if suppress_exception: return None
        raise wasanbon.RTCNotFoundException()

    def delete_rtc(self, rtc_, verbose=False):
        self.uninstall(rtc_, verbose=verbose)
        if verbose:
            sys.stdout.write(' - Deleting RTC directory %s\n' % rtc_.name)
        shutil.rmtree(rtc_.path, ignore_errors=True)
        self.remove_rtc_repository(rtc_.name)
        pass

    @property
    def path(self):
        return self._path

    @property
    def setting(self):
        if not self._setting:
            self._setting = yaml.load(open(os.path.join(self.path, 'setting.yaml'), 'r'))['application']
        return self._setting

    @property
    def standalone_rtcs_commands(self):
        stg = self.setting
        if 'standalone' in stg.keys():
            return stg['standalone']
        return []

    def rtcconf(self, language, verbose=False):
        return wasanbon.core.rtc.RTCConf(os.path.join(self.path, self.setting['conf.' + language]), verbose=verbose)

    @property
    def console_bind(self):
        if not 'console_bind' in self.setting.keys():
            bind_languages = ['C++', 'Python', 'Java']
        else:
            bind_languages = self.setting['console_bind']
            if type(bind_languages) != types.ListType:
                bind_languages = [bind_languages]
                
        return bind_languages

    def uninstall(self, rtc_, verbose=False, rtcconf_filename=""):
        if type(rtc_) == types.ListType:
            for rtc__ in rtc_:
                self.uninstall(rtc__, verbose=verbose, rtcconf_filename=rtcconf_filename)
            return
        if verbose:
            sys.stdout.write(' - Uninstaliling RTC (%s)\n' % rtc_.name)
        
        if len(rtcconf_filename) == 0:
            rtcconf = self.rtcconf(rtc_.rtcprofile.language.kind)
        else:
            if verbose:
                sys.stdout.write('    - Opening rtc.conf (%s)\n' % rtcconf_filename)
            rtcconf = wasanbon.core.rtc.RTCConf(rtcconf_filename)
        
        name = rtc_.rtcprofile.basicInfo.name 
        targetfile = os.path.join(self.bin_rel_path, os.path.basename(rtc_.packageprofile.getRTCExecutableFilePath()))
        if rtc_.language == 'C++':
            filename = name + wasanbon.get_bin_file_ext()
        elif rtc_.language == 'Java':
            filename = name + '.jar'
        elif rtc_.language == 'Python':
            filename = name + '.py'
        else:
            raise wasanbon.UnsupportedSystemException()

        rtcconf.remove('manager.components.precreate', name, verbose=verbose)
        rtcconf.remove('manager.modules.preload', filename, verbose=verbose)
        rtcconf.sync()

        setting_filename = os.path.join(self.path, 'setting.yaml')
        shutil.copy(setting_filename, setting_filename + '.bak')

        dic = yaml.load(open(setting_filename + '.bak', 'r'))
        all_cmd_list = dic.get('standalone', [])
        cmd_list = [cmd for cmd in all_cmd_list if cmd.startswith(targetfile)]
        if len(cmd_list) > 0:
            for cmd in cmd_list:
                all_cmd_list.remove(cmd)
            dic['standalone'] = all_cmd_list
        open(setting_filename, 'w').write(yaml.dump(dic, default_flow_style=False))
        pass


    def copy_binary_from_rtc(self, rtc_, verbose=False, standalone=False):
        if standalone:
            filepath = rtc_.packageprofile.getRTCExecutableFilePath()
        else:
            filepath = rtc_.packageprofile.getRTCFilePath(verbose=verbose)

        if verbose:
            sys.stdout.write('    - Copying RTC Binary File from %s to %s\n' % (filepath, 'bin'))

        if len(filepath) == 0:
            sys.stdout.write("    - Can not find RTC file in RTC's directory\n")
            return ""
        
        if verbose:
            sys.stdout.write('    - Detect RTC binary %s\n' % filepath)
        if rtc_.language == 'Python':
            norm_path = os.path.normcase(os.path.normpath(os.path.split(filepath)[0]))
            prefix = os.path.commonprefix([self.path, norm_path])
            bin_dir_rel = norm_path[len(self.path)+1:]
            targetfile = os.path.join(bin_dir_rel, os.path.basename(filepath))
        else:
            bin_dir = os.path.join(self.path, self.setting['BIN_DIR'])
            bin_dir_rel = self.setting['BIN_DIR']
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
                
                files = [filepath]
                # dlls in the same directry must be copied with rtc's binary.
                for file in os.listdir(os.path.dirname(filepath)):
                    if file.endswith(ext):
                        files.append(os.path.join(os.path.dirname(filepath), file))

                for file in files:
                    target = os.path.join(bin_dir, os.path.basename(file))
                    shutil.copy(filepath, target)

            targetfile = os.path.join(bin_dir_rel, os.path.basename(filepath))
        
        return targetfile

    def is_installed(self, rtc_, verbose=False, standalone=False):
        rtcs = self.installed_standalone_rtcs()
        for r in rtcs:
            if r.name == rtc_.name:
                return True
        return False

    def install(self, rtc_, verbose=False, preload=True, precreate=True, copy_conf=True, rtcconf_filename="", copy_bin=True, standalone=False):

        if verbose:
            sys.stdout.write(' - Installing RTC in package %s\n' % self.name)
            pass

        if not standalone and  self.is_installed(rtc_, standalone=True, verbose=verbose):
            if verbose:
                sys.stdout.write('    - RTC (%s) is already installed as standalone.\n' % rtc_.name)
                sys.stdout.write('    - Install standalone again.\n')
            standalone = True
        
        if standalone:
            targetconf = os.path.join(self.conf_path, 'rtc_' + rtc_.name + '.conf')
            #print self.rtcconf(rtc_.rtcprofile.language.kind).filename, targetconf
            shutil.copy(self.rtcconf(rtc_.rtcprofile.language.kind).filename, targetconf)
            rtcconf = wasanbon.core.rtc.RTCConf(targetconf)
            rtcconf['manager.modules.load_path'] = ''
            rtcconf['manager.modules.preload'] = ''
            rtcconf['manager.components.precreate'] = ''
            rtcconf['manager.is_master'] = 'NO'
            rtcconf['logger.file_name'] = './log/standalonertc_%s' % rtc_.name
            for key in rtcconf.keys():
                if key.find('config_file') > 0:
                    rtcconf.pop(key)
            targetconf = os.path.join(self.conf_rel_path, 'rtc_' + rtc_.name + '.conf')
        else:
            if len(rtcconf_filename) == 0:
                rtcconf = self.rtcconf(rtc_.rtcprofile.language.kind, verbose=verbose)
            else:
                rtcconf = wasanbon.core.rtc.RTCConf(rtcconf_filename)
            

        targetfile = self.copy_binary_from_rtc(rtc_, verbose=verbose, standalone=standalone)
        if len(targetfile) == 0:
            targetfile = os.path.join(self.setting['BIN_DIR'], rtc_.packageprofile.get_rtc_bin_filename())
            pass

        if standalone:
            setting_filename = os.path.join(self.path, 'setting.yaml')
            shutil.copy(setting_filename, setting_filename + '.bak')
            dic = yaml.load(open(setting_filename + '.bak', 'r'))

            cmd_list = [cmd for cmd in dic['application'].get('standalone', []) if cmd.startswith(targetfile)]
            if len(cmd_list) == 0:
                dic['application']['standalone'] = dic['application'].get('standalone', []) + [targetfile + ' -f ' + targetconf]
            open(setting_filename, 'w').write(yaml.dump(dic, default_flow_style=False))
            pass

        else:
            rtcconf.append('manager.modules.load_path', os.path.dirname(targetfile))
            if preload:
                rtcconf.append('manager.modules.preload', os.path.basename(targetfile))
            if precreate:
                rtcconf.append('manager.components.precreate', rtc_.rtcprofile.basicInfo.name)

        confpath = self.copy_conf_from_rtc(rtc_, verbose=verbose, force=copy_conf)
        if confpath:
            key = rtc_.rtcprofile.basicInfo.category + '.' + rtc_.rtcprofile.basicInfo.name + '0.config_file'
            if verbose:
                sys.stdout.write('    - Configuring System. Set (%s) to %s\n' % (key, confpath))
            rtcconf.append(key, confpath)

        rtcconf.sync()

        return True


    def copy_conf_from_rtc(self, rtc_, verbose=False, force=False):
        conffile = rtc_.packageprofile.getConfFilePath()
        if len(conffile) == 0:
            sys.stdout.write('    - No configuration file for RTC (%s) is found.\n' % rtc_.rtcprofile.basicInfo.name)
            return []
        targetconf = os.path.join(self.path, 'conf', os.path.basename(conffile))
        targetconf = targetconf[:-5] + '0' + '.conf'
        if os.path.isfile(targetconf):
            if verbose:
                sys.stdout.write('    - Found %s.\n' % targetconf)
            if force:
                if verbose:
                    sys.stdout.write('    - Force Copying Config (%s -> %s)\n' % (conffile, targetconf))
                shutil.copy(conffile, targetconf)
            else:
                if verbose:
                    sys.stdout.write('    - Do not copy.\n')
        else:
            if verbose:
                sys.stdout.write(' - Copying Config (%s -> %s)\n' % (conffile, targetconf))
            shutil.copy(conffile, targetconf)
        confpath = 'conf' + '/' + os.path.basename(targetconf)
        if sys.platform == 'win32':
            confpath.replace('\\', '\\\\')
        return confpath

        
    def register(self, verbose=False):
        if verbose:
            print ' - Registering workspace:'
            pass

        y = self._open_workspace()
        y[self._name] = self._path
        self._save_workspace(y)
        if verbose:
            print ' - Finished.'
        return True

    def unregister(self, verbose=False, clean=False):
        if verbose:
            print ' - Unregistering workspace:'
            ws_file_name = os.path.join(wasanbon.rtm_home(), "workspace.yaml")
            if not os.path.isfile(ws_file_name):
                if verbose:
                    print ' - workspace.yaml can not be found in RTM_HOME'
                return False
    
        y = self._open_workspace()
        _package_dir = y[self.name]
        if clean:
            if verbose:
                print ' - Removing Directory'
            shutil.rmtree(_package_dir, onerror = remShut)
        y.pop(self.name)

        self._save_workspace(y)
        if verbose:
            print ' - Finished.'
        return True

    def _open_workspace(self):
        return workspace.load_workspace()

    def _save_workspace(self, dic):
        workspace.save_workspace(dic)

    def git_init(self, verbose=False):
        git_obj = wasanbon.util.git.GitRepository(self.path, init=True, verbose=verbose,
                                                  ignore=['system/.metadata/*', 'rtc/*', 'mgr.py'])
        files = ['.gitignore', 'setting.yaml', 'conf/*.conf', 'rtc/repository.yaml', 'system/*.xml', 'README.txt']
        self.add(files, verbose=verbose, force=True)
        self.commit('Append Initial Files.\n', verbose=verbose)

    def add(self, files, verbose=False, force=False):
        git_obj = wasanbon.util.git.GitRepository(self.path, verbose=verbose)
        git_obj.add(files, verbose=verbose, force=force)
        pass

    def commit(self, comment, verbose=False):
        git_obj = wasanbon.util.git.GitRepository(self.path, verbose=verbose)
        files = ['.gitignore', 'setting.yaml', 'conf/*.conf', 'rtc/repository.yaml', 'system/*.xml', 'README.txt']
        self.add(files, verbose=verbose)
        git_obj.commit(comment, verbose=verbose)
        pass
               

    def push(self, verbose=False):
        git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose, path=self.path)
        pass

    def github_init(self, user, passwd, verbose=False):
        github_obj = github_ref.GithubReference(user, passwd)
        repo = github_obj.create_repo(self.name)
        git.git_command(['remote', 'add', 'origin', 'git@github.com:' + user + '/' + self.name + '.git'], verbose=verbose, path=self.path)
        self.push(verbose=verbose)

    def get_nameservers(self, verbose=False, force=False):
        if not force and self._nameservers:
            return self._nameservers

        nss = []
        for lang in self._languages:
            ns = self.rtcconf(lang)['corba.nameservers']
            if not ':' in ns:
                ns = ns + ':2809'
            if verbose:
                sys.stdout.write(' - Nameserver for rtcd_%s is %s\n' % (lang, ns))
            if not ns in nss:
                nss.append(ns)
        self._nameservers =  [nameserver.NameService(ns) for ns in nss]
        return self._nameservers

    def launch_standalone_rtcs(self, verbose=False):
        console_bind = self.console_bind
        if not os.path.isdir('pid'):
            os.mkdir('pid')

        if os.path.isdir('pid'):
            for file in os.listdir('pid'):
                if file.startswith('standalonertc_'):
                    pid = file[len('standalonertc_'):]
                else:
                    continue
                for proc in psutil.process_iter():
                    if str(proc.pid) == pid:
                        proc.kill()
                os.remove(os.path.join('pid', file))

        if verbose:
            sys.stdout.write(' - Launching standalone rtcs\n')

        cmds = self.standalone_rtcs_commands
        self._process['standalone'] = []
        for cmd in cmds:
            if verbose:
                sys.stdout.write(' - Launching command: %s' % cmd.split())
            rtc_name = self.__get_rtc_name_from_standalone_command(cmd)
            out = None if rtc_name in console_bind else subprocess.PIPE
            process = subprocess.Popen(cmd.split(), stdout=out, stderr=out)
            open(os.path.join('pid', 'standalonertc_' + str(process.pid)), 'w').close()
            self._process['standalone'].append(process)

        return True

    def launch_rtcd(self, language, rtcconf="", verbose=False):
        piddir = 'pid'
        logdir = 'log'
        if not os.path.isdir(logdir):
            os.mkdir(logdir)
        if not os.path.isdir(piddir):
            os.mkdir(piddir)

        if len(rtcconf) == 0:
            rtcconf = self.rtcconf(language).filename

        self.terminate_rtcd(language, verbose=verbose)

        if len(self.installed_rtcs(language=language, verbose=verbose)) > 0:
            if verbose:
                sys.stdout.write(' -Starting RTC-Daemon %s version.\n' % language)
            self._process[language]    = run.start_rtcd(language, rtcconf, 
                                                        language in self.console_bind)
            if verbose:
                sys.stdout.write('    - Save rtcd_'+language+'_' + str(self._process[language].pid) + '\n')
            open(os.path.join(piddir, 'rtcd_'+language+'_' + str(self._process[language].pid)), 'w').close()
        return True

    def launch_all_rtcd(self, verbose=False):
        if verbose:
            sys.stdout.write(' - Launching All RTCDaemon\n')

        self.launch_rtcd('C++', verbose=verbose)
        self.launch_rtcd('Python', verbose=verbose)
        self.launch_rtcd('Java', verbose=verbose)
        pass

    def getpid(self, language):
        return self._process[language].pid

    def connect_and_configure(self, try_count=5, verbose=False):
        if verbose:
            sys.stdout.write(' - Connect And Configure System\n')
        for i in range(0, try_count):
            if run.exe_rtresurrect():
                return True
            time.sleep(1)
        raise wasanbon.BuildSystemException()

    def activate(self, try_count=5, verbose=False):
        if verbose:
            sys.stdout.write(' - Activate all RTCs\n')
        for i in range(0, try_count):
            if run.exe_rtstart():
                return True
            time.sleep(1)
        raise wasanbon.BuildSystemException()

    def deactivate(self, try_count=5, verbose=False):
        if verbose:
            sys.stdout.write(' - Deactivate all RTCs\n')
        for i in range(0, try_count):
            if run.exe_rtstop():
                return True
            time.sleep(1)
        raise wasanbon.BuildSystemException()
    
    def terminate_rtcd(self, language, verbose=False):
        piddir = 'pid'
        if language in self._process.keys():
            if self._process[language].poll() == None:
                if verbose:
                    sys.stdout.write(' - Terminating rtcd (%s) ...' % language)
                try:
                    self._process[language].kill()
                except OSError, e:
                    sys.stdout.write('    @ OSError: process seems to be killed already.\n')

        for file in os.listdir(piddir):
            if file.startswith('rtcd_'+language+'_'):
                pid = int(file[len('rtcd_'+language+'_'):])
                for proc in psutil.process_iter():
                    if proc.pid == pid:
                        proc.kill()
                    if os.path.isfile(os.path.join(piddir, file)):
                        if verbose:
                            sys.stdout.write('     - Removing File(%s)\n' % os.path.join(piddir, file))
                        os.remove(os.path.join(piddir, file))
                    
    """
    def is_process_terminated(self, verbose=False):
        if verbose:
            sys.stdout.write(' - Checking RTCDaemon process is dead.\n')
        flags = []
        for key, value in self._process:
            if value.returncode: # Process is killed.
                print 'Process is killed.'
                pid = self._process[key].pid
                if os.path.isdir(os.path.join(self.path, 'pid')):
                    for file in os.listdir('pid'):
                        if file.startswith('rtcd_cpp_'):
                            _process = file[len('rtcd_cpp_'):]
                        elif file.startswith('rtcd_py_'):
                            _process = file[len('rtcd_py_'):]
                        elif file.startswith('rtcd_java_'):
                            _process = file[len('rtcd_java_'):]
                        else:
                            continue

                        print ' - package_obj.py checking process :', file
                        if _process == str(pid):
                            os.remove(os.path.join('pid', file))
                flags.append(True)
            else:
                value.polll()
                if value.returncode:
                    flags.append(False)
                else:
                    flags.append(True)
        if len(flags) != 0:
            return all(flags)
        else:
            return False
    """
    def terminate_standalone_rtcs(self, verbose=False):
        for p in self._process['standalone']:
            if p.poll() == None:
                if verbose:
                    sys.stdout.write(' - Terminating standalone RTC ()\n')
                try:
                    p.kill()
                except OSError, e:
                    sys.stdout.write(' - OSError: process seems to be killed already.\n')

            if os.path.isdir('pid'):
                sys.stdout.write(' - checking pid directory\n')
                for file in os.listdir('pid'):
                    if file.startswith('standalonertc_'):
                        _process = file[len('standalonertc_'):]
                    else:
                        continue
                    if _process == str(p.pid):
                        if verbose:
                            sys.stdout.write(' - removing file %s\n' % file)
                        os.remove(os.path.join('pid', file))
        pass

    def terminate_all_rtcd(self, verbose=False):
        self.terminate_rtcd('C++', verbose=verbose)
        self.terminate_rtcd('Python', verbose=verbose)
        self.terminate_rtcd('Java', verbose=verbose)

        return True

    """
        for key, value in self._process.items():
            # ignore standalone rtcs
            if key == 'standalone':
                continue

            if value.poll() == None:
                if verbose:
                    sys.stdout.write(' - Terminating rtcd(%s)\n' % key)
                try:
                    value.kill()

                except OSError, e:
                    sys.stdout.write(' - OSError: process seems to be killed already.\n')
            if os.path.isdir('pid'):
                sys.stdout.write(' - checking pid directory\n')
                for file in os.listdir('pid'):
                    if file.startswith('rtcd_cpp_'):
                        _process = file[len('rtcd_cpp_'):]
                    elif file.startswith('rtcd_py_'):
                        _process = file[len('rtcd_py_'):]
                    elif file.startswith('rtcd_java_'):
                        _process = file[len('rtcd_java_'):]
                    else:
                        continue
                    if _process == str(value.pid):
                        sys.stdout.write(' - removing file %s\n' % file)
                        os.remove(os.path.join('pid', file))

    """
    def installed_rtcs(self, language='all', verbose=False):
        rtcs_ = {}
        for lang in self._languages:
            rtcs_[lang] = [self.rtc(rtc_.strip()) for rtc_ in self.rtcconf(lang)['manager.components.precreate'].split(',') if len(rtc_.strip()) != 0]
            
        if language == 'all':
            return rtcs_

        return rtcs_[language]

    def __get_rtc_name_from_standalone_command(self, cmd):
        rtc_launch_cmd = cmd.split()[0]
        post_fix = 'Comp'
        if sys.platform == 'win32':
            post_fix = 'Comp.exe'
        if rtc_launch_cmd.startswith(self.bin_rel_path) and rtc_launch_cmd.endswith(post_fix):
            return rtc_launch_cmd[len(self.bin_rel_path)+1:-(len(post_fix))]
        else:
            return ""
    def installed_standalone_rtcs(self, verbose=False):
        rtcs_ = []
        stg = self.setting
        cmds = stg.get('standalone', [])
        for cmd in cmds:
                rtc_name = self.__get_rtc_name_from_standalone_command(cmd)
                try:
                    rtc_ = self.rtc(rtc_name)
                    rtcs_.append(rtc_)
                except wasanbon.RTCNotFoundExpcetion, e:
                    if verbose:
                        sys.stdout.write(' - Searching %s RTC in package but not found.\n')
                    
            #sys.stdout.write(' - package_obj.installed_standalone_rtcs not implemented.\n')
        return rtcs_
        

    def available_connection_pairs(self, verbose=False, nameservers=None):
        pairs = []

        if not nameservers:
            nameservers = self.get_nameservers(verbose=verbose)
        # For DataPorts
        outports = []
        for ns in nameservers:
            outports = outports + ns.dataports(port_type='DataOutPort')
        for outport in outports:
            inports = []
            for ns in nameservers:
                inports = inports + ns.dataports(port_type='DataInPort', data_type=outport.properties['dataport.data_type'])
            for inport in inports:
                pairs.append([outport, inport])

        # For ServicePorts
        provports = []
        for ns in nameservers:
            provports = provports + ns.svcports(polarity='Provided')
        for provport in provports:
            reqports = []
            for interface in provport.interfaces:
                if interface.polarity_as_string(False) == 'Provided':
                    interface_type = interface.type_name
                    for ns in nameservers:
                        reqports = reqports + ns.svcports(polarity='Required', interface_type=interface_type)
                    for reqport in reqports:
                        pairs.append([provport, reqport])
        return pairs

    def validate(self, verbose=False, autofix=False, interactive=False, ext_only=False):
        for lang in self._languages:
            
            rtcc = self.rtcconf(lang)
            if lang == 'C++':
                rtcc.ext_check(verbose=verbose, autofix=autofix, interactive=interactive)
            if not ext_only:
                rtcc.validate(verbose=verbose, autofix=autofix, interactive=interactive)
            rtcc.sync()

        pass


    def is_running(self):
        if not os.path.isdir(self.pid_path):
            return False
        for p_file in os.listdir(self.pid_path):
            if p_file.startswith("nameserver"):
                continue
            pid = int(p_file.split('_')[-1])
            for p in psutil.process_iter():
                if p.pid == pid:
                    return True
        return False
        
def remShut(*args):
    func, path, _ = args 
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)
