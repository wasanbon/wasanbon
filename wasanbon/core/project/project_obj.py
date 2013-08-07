import os, sys, yaml, subprocess, shutil, yaml
import wasanbon
from wasanbon.core import rtc
from wasanbon.util import git

class InvalidProjectPathError(Exception):
    def __init__(self):
        pass

class Project():

    def __init__(self, path):
        self._path = path
        if not os.path.isfile(os.path.join(path, 'setting.yaml')):
            raise InvalidProjectPathError()
        self._rtcs = []
        self._name = os.path.basename(path)
        
        pass

    def install(self, rtc):
        pass

    def uninstall(self, rtc):
        pass

    @property
    def name(self):
        return self._name
    
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
        dic.pop(name)
        yaml.dump(dic, open(repo_file, 'w'), encoding='utf8', allow_unicode=True)
        pass
        

    @property
    def rtcs(self):
        if len(self._rtcs) == 0:
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
        return None
    
    def clone_rtc(self, url, verbose=False):
        current_dir = os.getcwd()
        os.chdir(os.path.join(self.path, self.setting['RTC_DIR']))
        distdir = os.path.join(os.getcwd(), os.path.basename(url))
        sys.stdout.write(' - Cloning RTC into %s\n' % distdir)
        if distdir.endswith('.git'):
            distdir = distdir[:-4]
        if os.path.isdir(distdir):
            sys.stdout.write(' - Directory already exists.\n')
            sys.stdout.write(' - Now changing the upstream pointer [master].\n')
            try:
                git_obj = git.GitRepository(distdir)
                git_obj.change_ustream_pointer(url, verbose=verbose)
            except git.GitRepositoryNotFoundException, ex:
                sys.stdout.write(' - Directory is not git repository\n')
                sys.stdout.write(' - This error can not be fixed in this version.\n')
                return 
        else:
            git.git_command(['clone', url, distdir], verbose=verbose)
            pass
        os.chdir(distdir)

        git.git_command(['submodule', 'init'], verbose=verbose)
        git.git_command(['submodule', 'update'], verbose=verbose)
        os.chdir(current_dir)
        rtc_obj = rtc.RtcObject(distdir)
        self.rtcs.append(rtc_obj)
        
        repo = rtc.RtcRepository(name=rtc_obj.name, url=url, desc="", hash=rtc_obj.git.hash)
        self.append_rtc_repository(repo)

        return rtc_obj

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
        return yaml.load(open(os.path.join(self.path, 'setting.yaml'), 'r'))['application']
    
    def run(self):
        pass

    def rtcconf(self, language):
        return rtc.RTCConf(self.setting['conf.' + language])

    def install(self, rtc_, verbose=False, preload=True, precreate=True):
        rtcconf = self.rtcconf(rtc_.rtcprofile.language.kind)
        filepath = rtc_.packageprofile.getRTCFilePath()
        if len(filepath) == 0:
            sys.stdout.write(' - Executable of RTC (%s) is not found.\n' % rtc_.name)
            return None

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

def remShut(*args):
    func, path, _ = args 
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)
