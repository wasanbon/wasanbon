import sys
import wasanbon
import wasanbon.core
from wasanbon.core.project import *


class ProjectAlreadyExistsException(Exception):
    def __init__(self):
        pass


class ProjectDirectoryExistsException(Exception):
    def __init__(self):
        pass

class ProjectRepository():

    def __init__(self, name, desc, url):
        self._name = name
        self._url = url
        self._desc = desc
        pass


    def clone(self, verbose=False):
        try:
            proj = wasanbon.core.project.get_project(self.name, verbose)
            if verbose:
                print ' - There is %s project in workspace.yaml\n' % prjname
                print ' - Please unregister the project\n' 
            raise ProjectAlreadyExistsException()
        except wasanbon.ProjectNotFoundException, ex:
            pass
        
        appdir = os.path.join(os.getcwd(), self.name)
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose:
                print ' - There seems to be %s here. Please change application name.' % prjname
            raise ProjectDirectoryExistsException()
            #return False

        git.git_command(['clone', self.url, appdir], verbose=verbose)
        proj = wasanbon.core.project.create_project(self.name, verbose=verbose, force_create=True, overwrite=False)
        for repo in proj.rtc_repositories:
            if verbose:
                sys.stdout.write(' - Cloning RTC %s\n' % repo.name)
            rtc = repo.clone(path=os.path.join(appdir, proj.setting['RTC_DIR']), verbose=verbose)
            rtc.build(verbose=verbose)
            proj.install(rtc, precreate=False, preload=True)
        return Project(appdir)


    def fork(self, user, passwd, verbose=False):
        proj = wasanbon.core.project.get_project(self.name, verbose)
        if proj:
            if verbose:
                print ' - There is %s project in workspace.yaml\n' % prjname
                print ' - Please unregister the project\n' 
            #return None
            raise ProjectAlreadyExistsException()
        
        appdir = os.path.join(os.getcwd(), self.name)
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose:
                print ' - There seems to be %s here. Please change application name.' % prjname
            raise ProjectDirectoryExistsException()

            #return False
        sys.stdout.write(' - Forking URL:: %s\n' % url)
        github_obj = wasanbon.util.github.GithubReference(user, passwd)
        repo = github_obj.fork(self.user, self.repo_name, verbose=verbose)
        
        url = 'https://github.com/%s/%s.git' % (user, self.repo_name)
        return ProjectRepository(user=user, name=self.name, url=url, desc=self.description)
        

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._desc

    @property
    def url(self):
        return self._url

    @property
    def user(self):
        return os.path.split('/')[-2]

    @property
    def repo_name(self):
        repo_name = os.path.basename(self._url)
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        return repo_name
        

