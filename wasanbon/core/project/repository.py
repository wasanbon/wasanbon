import sys
import wasanbon
import wasanbon.core
from wasanbon.core.project import *



class ProjectRepository():

    def __init__(self, name, desc, url):
        self._name = name
        self._url = url
        self._desc = desc
        pass


    def clone(self, verbose=False):
        proj = wasanbon.core.project.get_project(self.name, verbose)
        if proj:
            print ' - There is %s project in workspace.yaml\n' % prjname
            print ' - Please unregister the project\n' 
            return None
        
        appdir = os.path.join(os.getcwd(), self.name)
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose:
                print ' - There seems to be %s here. Please change application name.' % prjname
            return False

        git.git_command(['clone', self.url, appdir], verbose=verbose)
        proj = wasanbon.core.project.create_project(self.name, verbose=verbose, force_create=True, overwrite=False)
        for repo in proj.rtc_repositories:
            if verbose:
                sys.stdout.write(' - Cloning RTC %s\n' % repo.name)
            rtc = repo.clone(path=os.path.join(appdir, proj.setting['RTC_DIR']), verbose=verbose)
            rtc.build(verbose=verbose)
        return Project(appdir)

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._desc

    @property
    def url(self):
        return self._url
        

