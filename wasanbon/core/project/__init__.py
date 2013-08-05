import os, sys, yaml, subprocess, shutil
import wasanbon

def get_projects(verbose):
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        sys.stdout.write(' - Can not find workspace.yaml: %s\n' % ws_file_name)
        fout = open(ws_file_name, "w")
        fout.close()
        return {}
    else:
        if verbose:
            sys.stdout.write(' - Opening workspace.yaml.\n')
        return yaml.load(open(ws_file_name, "r"))

def parse_and_copy(src, dist, dic, verbose=False):
    fin = open(src, "r")
    fout = open(dist, "w")
    for line in fin:
        for key, value in dic.items():
            index = line.find(key)
            if index >= 0:
                line = line[:index] + value + line[index + len(key):]
        fout.write(line)
    fin.close()
    fout.close()

def create_project(prjname, verbose=False):
    projs = get_projects(verbose)
    if prjname in projs.keys():
        if verbose:
            print ' - There is %s project in workspace.yaml already\n' % prjname
        return None

    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    appdir = os.path.join(os.getcwd(), prjname)
    if os.path.isdir(appdir) or os.path.isfile(appdir):
        if verbose:
            print ' - There seems to be %s here. Please change application name.' % prjname
        return None

    for root, dirs, files in os.walk(tempdir):
        distdir = os.path.join(appdir, root[len(tempdir)+1:])
        os.mkdir(distdir)
        for file in files:
            if verbose:
                sys.stdout.write(" - copy file: %s\n" % file)
            parse_and_copy(os.path.join(root, file), os.path.join(distdir, file), {'$APP' : prjname})
            
    #y = yaml.load(open(os.path.join(appdir, 'setting.yaml'), 'r'))
    #file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'repository.yaml')
    #shutil.copy(file, os.path.join(appdir, y['application']['RTC_DIR'], 'repository.yaml'))
    
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        cmd = ['chmod', '755', os.path.join(prjname, 'mgr.py')]
        subprocess.call(cmd)

    proj = Project(appdir)
    proj.register(verbose)
    return proj



class Project():

    def __init__(self, path):
        self._path = path
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
    def rtcs(self):
        return self._rtcs
        pass

    def run(self):
        pass

        
    def register(self, verbose=False):
        if verbose:
            print ' - Registering workspace:'
            pass

        y = self._open_workspace()
        y[self._name] = self._path
        self._save_workspace(y)

        #fout = open(ws_file_name, "w")
        #if verbose:
        #    for key, item in y.items():
        #        print '  ' + key + ' '*(10-len(key)) + ':' + item
        #    pass
        #
        #yaml.dump(y, fout,  encoding='utf8', allow_unicode=True, default_flow_style=False)

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
                return
    
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
