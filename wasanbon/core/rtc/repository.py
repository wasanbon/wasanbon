import os, sys
import wasanbon
from wasanbon.util import git
import rtc_object

class RtcRepository():

    def __init__(self, name, url, desc, hash="", protocol='git'):
        self._name = name
        self._url = url
        self._desc = desc
        self._hash = hash
        self._protocol = protocol

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url
    
    @property
    def description(self):
        return self._desc
    
    @property
    def protocol(self):
        return self._protocol

    @property
    def hash(self):
        return self._hash

    def clone(self, path='.', verbose=False):
        if self._protocol == 'git':
            return self.git_clone(path=path, verbose=verbose)
        if self._protocol == 'hg':
            return self.hg_clone(path=path, verbose=verbose)

    def git_clone(self, path='.', verbose=False):
        curdir = os.getcwd()
        os.chdir(path)
        distpath = os.path.basename(self.url)
        if distpath.endswith('.git'):
            distpath = distpath[:-4]
        if os.path.isdir(os.path.join(os.getcwd(), distpath)):
            sys.stdout.write(' - Directory already exists.\n')
            try:
                git_obj = git.GitRepository(os.path.join(os.getcwd(), distpath))
                git_obj.change_upstream_pointer(self.url, verbose=verbose)
            except git.GitRepositoryNotFoundException, ex:
                sys.stdout.write(' - Directory is not git repository\n')
                return False
            return
        
        git.git_command(['clone', self.url, distpath], verbose=verbose)
        os.chdir(os.path.join(os.getcwd(), distpath))

        if len(hash) != 0:
            git.git_command(['checkout', self.hash], verbose=verbose)

        git.git_command(['submodule', 'init'], verbose=verbose)
        git.git_command(['submodule', 'update'], verbose=verbose)
        os.chdir(curdir)
        return rtc_object.RtcObject(os.path.join(path, distpath))

    def hg_clone(self, verbose=False):
                    #if 'hg' in repo.keys():
                    #    gitenv = os.environ.copy()
                    #    if not 'HOME' in gitenv.keys():
                    #        gitenv['HOME'] = wasanbon.get_home_path()
                    #        print 'HOME is %s' % gitenv['HOME']
                    #    url = repo['hg']
                    #    print ' - Mercurial cloning : %s' % url
                    #    distpath = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], rtcname)
                    #    cmd = [wasanbon.setting['local']['hg'], 'clone', url, distpath]
                    #    subprocess.call(cmd, env=gitenv)
                    #    #return
        pass
