import os, sys
import wasanbon
from wasanbon.util import git
import rtc_object

class RtcRepository():

    def __init__(self, name, url, desc, platform="", hash="", protocol='git'):
        self._name = name
        self._url = url
        self._desc = desc
        self._hash = hash
        self._protocol = protocol
        self._platform = platform

    @property
    def name(self):
        return self._name

    @property
    def user(self):
        return self.url.split('/')[-2]

    @property
    def platform(self):
        return self._platform

    @property
    def repo_name(self):
        repo_name = os.path.basename(self._url)
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        return repo_name

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

    def fork(self, user, passwd, verbose=False, path='.'):
        from wasanbon.core.repositories import github_api
        if verbose:
            sys.stdout.write(' - Forking RtcRepository %s\n' % self.name)
        github_obj = github_api.GithubReference(user, passwd)
        repo = github_obj.fork_repo(self.user, self.repo_name, self.repo_name, verbose=verbose)
        url = 'https://github.com/%s/%s.git' % (user, self.repo_name)
        return RtcRepository(name=self.name, url=url, desc=self.description, hash=self.hash)

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
                return rtc_object.RtcObject(os.path.join(path, distpath))
            except:# git.GitRepositoryNotFoundException, ex:
                sys.stdout.write(' - Directory is not git repository\n')
                return None
        
        git.git_command(['clone', self.url, distpath], verbose=verbose)
        distpath_full = os.path.join(os.getcwd(), distpath)
        if not os.path.isdir(distpath_full):
            return None
        os.chdir(os.path.join(os.getcwd(), distpath))

        #if len(self.hash) != 0:
        #    git.git_command(['checkout', '-b', 'temp_branch', self.hash], verbose=verbose)
        if verbose:
            sys.stdout.write(' - Updating Submodules.....\n')
        git.git_command(['submodule', 'init'], verbose=verbose)
        git.git_command(['submodule', 'update'], verbose=verbose)
        os.chdir(curdir)
        return rtc_object.RtcObject(os.path.join(path, distpath))

    def hg_clone(self, verbose=False):
        pass
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

    def get_readme(self, verbose=False, service='github', force_download=False):
        prof_dir = os.path.join(wasanbon.rtm_temp(), 'rtcprofile', self.repo_name)
        readme_path = os.path.join(prof_dir, 'README.' + self.repo_name)
        readme_text = ''
        if os.path.isfile(readme_path): 
            if verbose and (not force_download): sys.stdout.write(' - Use Cached File (%s).\n' % readme_path)
            f = open(readme_path, 'r')
            readme_text = f.read()
            f.close()

        if force_download or len(readme_text) == 0:
            if verbose: sys.stdout.write(' - Downloading RTC README from web.\n')
                
            from wasanbon.core.repositories import github_api
            if service == 'github':
                github_obj = github_api.GithubReference() # user, passwd)

                readme_text = github_obj.get_file_contents(self.user, self.repo_name, 'README.'+self.repo_name, verbose=verbose)
                if os.path.isfile(readme_path):
                    os.rename(readme_path, readme_path+wasanbon.timestampstr())
                f = open(readme_path, 'w')
                f.write(readme_text)
                f.close()
            
        if readme_text == 'Not Found':
            return None
        return readme_text
        
    def get_rtcprofile(self, verbose=False, service='github', force_download=False):
        prof_text = ''
        prof_root_dir =  os.path.join(wasanbon.rtm_temp(), 'rtcprofile')
        if not os.path.isdir(prof_root_dir):
            os.mkdir(prof_root_dir)

        prof_dir =  os.path.join(wasanbon.rtm_temp(), 'rtcprofile', self.repo_name)
        if not os.path.isdir(prof_dir):
            os.mkdir(prof_dir)
        fullpath = os.path.join(prof_dir, self.repo_name + '.xml')
        if os.path.isfile(fullpath):
            if verbose and (not force_download): sys.stdout.write(' - Use Cached File (%s).\n' % fullpath)
            f = open(fullpath, 'r')
            prof_text = f.read()
            f.close()

        if force_download or len(prof_text) == 0:
            if verbose: sys.stdout.write(' - Downloading RTC Profile from web.\n')
                
            from wasanbon.core.repositories import github_api
            if service == 'github':
                github_obj = github_api.GithubReference() # user, passwd)
                prof_text = github_obj.get_file_contents(self.user, self.repo_name, 'RTC.xml', verbose=verbose)
                if os.path.isfile(fullpath):
                    os.rename(fullpath, fullpath + wasanbon.timestampstr())

                f = open(fullpath, 'w')
                f.write(prof_text)
                f.close()

        setting_fullpath = os.path.join(prof_dir, self.repo_name + '.yaml')
        if not os.path.isfile(setting_fullpath) or force_download:
            if os.path.isfile(setting_fullpath):
                os.rename(setting_fullpath, setting_fullpath + wasanbon.timestampstr())
            f = open(setting_fullpath, 'w')
            f.write('name : %s\n' % self.repo_name)
            f.write('url : %s\n' % self.url)
            f.write('platform : %s\n' % self.platform)
            f.close()
            
        if prof_text == 'Not Found':
            return None
        from wasanbon.core.rtc import rtcprofile
        return rtcprofile.RTCProfile(str=prof_text)
