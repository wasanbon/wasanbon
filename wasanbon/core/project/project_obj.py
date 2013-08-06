import os, sys, yaml, subprocess, shutil, yaml
import wasanbon
from wasanbon.core import rtc

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
        print str(dic)
        for name, value in dic.items():
            repos.append(rtc.RtcRepository(value['git'], value['description'], value.get('hash', "")))
        return repos

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


    @property
    def path(self):
        return self._path

    @property
    def setting(self):
        return yaml.load(open(os.path.join(self.path, 'setting.yaml'), 'r'))['application']
    
    def run(self):
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
