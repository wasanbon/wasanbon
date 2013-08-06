#from wasanbon.util import git
import os
import wasanbon.util.git

class GitRepositoryNotFoundException(Exception):
    def __init__(self):
        pass


class GitRepository():

    def __init__(self, path):
        self._path = path
        if not os.path.isdir(os.path.join(path, '.git')):
            raise GitRepositoryNotFoundException()

    @property
    def path(self):
        return self._path

    @property
    def hash(self):
        popen = wasanbon.util.git.git_command(['log', '--pretty=format:"%H"', '-1'], pipe=True)
        popen.wait()
        return popen.stdout.readline().strip()[1:-1]

    def change_upstream_pointer(url, verbose=False):
        curdir = os.getcwd()
        os.chdir(self.path)
        filename = os.path.join(distpath, '.git', 'config')
        tempfilename = filename + ".bak"
        if os.path.isfile(tempfilename):
            os.remove(tempfilename)
            pass
        os.rename(filename, tempfilename)

        git_config = open(filename, 'w')
        git_config_bak = open(tempfilename, 'r')
        for line in git_config_bak:
            if line.strip() == '[remote "origin"]':
                line = '[remote "upstream"]\n'
                pass
            git_config.write(line)
            pass
        git_config.write('[remote "origin"]\n')
        git_config.write('       url = %s\n' % url)
        git_config.write('       fetch = +refs/heads/*:refs/remotes/origin/*\n')
        
        git_config.close()
        git_config_bak.close()

        os.chdir(curdir)
