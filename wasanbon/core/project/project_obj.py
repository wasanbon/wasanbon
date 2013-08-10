import os, sys, yaml, subprocess, shutil, types, time
import wasanbon
from wasanbon.core import rtc
from wasanbon.util import git
from wasanbon.util import github_ref

class InvalidProjectPathError(Exception):
    def __init__(self):
        pass

class RTCNotFoundException(Exception):
    def __init__(self):
        pass

class Project():

    def __init__(self, path):
        self._path = path
        if not os.path.isfile(os.path.join(path, 'setting.yaml')):
            raise InvalidProjectPathError()
        self._rtcs = []
        self._name = os.path.basename(path)
        self._process = {}
        pass

    @property
    def name(self):
        return self._name

    @property
    def bin_path(self):
        return os.path.join(self.path, self.setting['BIN_DIR'])
    
    @property
    def rtc_path(self):
        return os.path.join(self.path, self.setting['RTC_DIR'])

    @property
    def rtc_repositories(self):
        repos = []
        dic = yaml.load(open(os.path.join(self.path, self.setting['RTC_DIR'], 'repository.yaml'), 'r'))
        for name, value in dic.items():
            repos.append(rtc.RtcRepository(name=name, url=value['git'], desc=value['description'], hash=value.get('hash', "")))
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
        if True:
            for dir in os.listdir(os.path.join(self.path, self.setting['RTC_DIR'])):
                if dir.startswith('.') or dir == 'repository.yaml':
                    pass
                else:
                    try:
                        rtc_obj = rtc.RtcObject(os.path.join(self.path, self.setting['RTC_DIR'], dir))
                        self._rtcs.append(rtc_obj)
                    except rtc.RTCProfileNotFoundException, ex:
                        pass
                    except Exception, ex:
                        print ex
                        pass
        return self._rtcs

    def rtc(self, name):
        for rtc_ in self.rtcs:
            if rtc_.name == name:
                return rtc_
        raise RTCNotFoundException()

    def delete_rtc(self, rtc_, verbose=False):
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
    

    def rtcconf(self, language):
        return rtc.RTCConf(self.setting['conf.' + language])

    def uninstall(self, rtc_, verbose=False):
        if type(rtc_) == types.ListType:
            for rtc__ in rtc_:
                self.uninstall(rtc__, verbose=verbose)
                return

        rtcconf = self.rtcconf(rtc_.rtcprofile.language.kind)

        
        name = rtc_.rtcprofile.basicInfo.name 
        filename = name + wasanbon.get_bin_file_ext()
        rtcconf.remove('manager.components.precreate', name)
        rtcconf.remove('manager.modules.preload', filename)
        rtcconf.sync()

    def install(self, rtc_, verbose=False, preload=True, precreate=True):
        if type(rtc_) == types.ListType:
            for rtc__ in rtc_:
                self.install(rtc__, verbose=verbose, preload=preload, precreate=precreate)
                return

        rtcconf = self.rtcconf(rtc_.rtcprofile.language.kind)
        filepath = rtc_.packageprofile.getRTCFilePath()

        bin_dir = os.path.join(self.path, self.setting['BIN_DIR'])
        if not os.path.isdir(bin_dir):
            os.mkdir(bin_dir)
            pass

        targetfile = os.path.join(bin_dir, os.path.basename(filepath))
        shutil.copy(filepath, targetfile)

        rtcconf.append('manager.modules.load_path', self.setting['BIN_DIR'])
        if preload:
            rtcconf.append('manager.modules.preload', os.path.basename(targetfile))
        if precreate:
            rtcconf.append('manager.components.precreate', rtc_.rtcprofile.basicInfo.name)

        conffile = rtc_.packageprofile.getConfFilePath()
        if len(conffile) == 0:
            sys.stdout.write(' - No configuration file for RTC (%s) is found.\n' % rtc_.rtcprofile.basicInfo.name)

        else:
            targetconf = os.path.join(self.path, 'conf', os.path.basename(conffile))
            targetconf = targetconf[:-5] + '0' + '.conf'
            shutil.copy(conffile, targetconf)
            rtcconf.append(rtc_.rtcprofile.basicInfo.category, '.' + rtc_.rtcprofile.basicInfo.name + '0.config_file:' + os.path.join('conf', os.path.basename(targetconf)))
            pass
        rtcconf.sync()
        pass
        
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
            ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
            if not os.path.isfile(ws_file_name):
                if verbose:
                    print ' - workspace.yaml can not be found in RTM_HOME'
                return False
    
        y = self._open_workspace()
        proj_dir = y[self.name]
        if clean:
            if verbose:
                print ' - Removing Directory'
            shutil.rmtree(proj_dir, onerror = remShut)
        y.pop(self.name)

        self._save_workspace(y)
        if verbose:
            print ' - Finished.'
        return True

    def _open_workspace(self):
        ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
        if not os.path.isfile(ws_file_name):
            fout = open(ws_file_name, "w")
            fout.close()
            pass

        y = yaml.load(open(ws_file_name, "r"))
        if not y:
            y = {}
        return y

    def _save_workspace(self, dic):
        ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
        yaml.dump(dic, open(ws_file_name, "w"), encoding='utf8', allow_unicode=True, default_flow_style=False)
        pass

    def git_init(self, verbose=False):
        git_obj = wasanbon.util.git.GitRepository(self.path, init=True, verbose=verbose)
        files = ['.gitignore', 'setting.yaml', 'conf/*.conf', 'rtc/repository.yaml', 'system/*.xml', 'README.txt']
        self.add(files, verbose=verbose)
        self.commit('Append Initial Files.\n', verbose=verbose)

    def add(self, files, verbose=False):
        git_obj = wasanbon.util.git.GitRepository(self.path, verbose=verbose)
        git_obj.add(files, verbose=verbose)
        pass

    def commit(self, comment, verbose=False):
        git_obj = wasanbon.util.git.GitRepository(self.path, verbose=verbose)
        git_obj.commit(comment, verbose=verbose)
        pass
               

    def github_init(self, user, passwd, verbose=False):
        github_obj = github_ref.GithubReference(user, passwd)
        repo = github_obj.create_repo(self.name)
        git.git_command(['remote', 'add', 'origin', 'git@github.com:' + user + '/' + self.name + '.git'], verbose=verbose, path=self.path)
        git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose, path=self.path)

    def get_nameservers():
        nss = []
        languages = ['C++', 'Python', 'Java']
        for lang in languages:
            ns = self.rtcconf(lang)['corba.nameservers']
            if not ':' in ns:
                ns = ns + ':2809'
            nss.append(ns)
        return nss

    def launch_all_rtcd(self, verbose=False):
        if not os.path.isdir('log'):
            os.mkdir('log')

        self._process['C++']    = run.start_cpp_rtcd()
        self._process['Python'] = run.start_python_rtcd()
        self._process['Java']   = run.start_java_rtcd()
        pass

    def connect_and_configure(self, try_count=5, verbose=False):
        if verbose:
            sys.stdout.write(' - Connect And Configure System\n')
        for i in range(0, try_count):
            if run.exe_rtresurrect():
                return True
            time.sleep(1)
        return False

    def activate(self, try_count=5, verbose=False):
        if verbose:
            sys.stdout.write(' - Activate all RTCs\n')
        for i in range(0, try_count):
            if run.exe_rtstart():
                return True
            time.sleep(1)
        return False

    def is_process_terminated(self, verbose=False):
        flags = []
        for key, value in self._process:
            if value.returncode:
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

    def terminate_all_process(self, verbose=False):
        for key, value in self._process:
            value.poll()
            if not value.returncode:
                if verbose:
                    sys.stdoutwrite(' - Terminating rtcd(%s)\n' % key)
                value.kill()

        
def remShut(*args):
    func, path, _ = args 
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)
