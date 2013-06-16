import os, sys, yaml, shutil, subprocess

import wasanbon


def create_project(prjname, verbose):
    projs = get_projects(verbose)
    if projs:
        if prjname in projs.keys():
            if verbose:
                print 'There is %s project in workspace.yaml\n' % prjname
            return False

    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    appdir = os.path.join(os.getcwd(), prjname)

    if os.path.isdir(appdir) or os.path.isfile(appdir):
        if verbose:
            print 'There seems to be %s here. Please change application name.' % psjname
        return False

    if verbose:
        sys.stdout.write(" - copying from %s to %s\n" % (tempdir, appdir))
        
    for root, dirs, files in os.walk(tempdir):
        distdir = os.path.join(appdir, root[len(tempdir)+1:])
        os.mkdir(distdir)
        for file in files:
            if verbose:
                sys.stdout.write("    - file: %s\n" % file)
            fin = open(os.path.join(root, file), "r")
            fout = open(os.path.join(distdir, file), "w")
            for line in fin:
                index = line.find('$APP')
                if index >= 0:
                    line = line[:index] + prjname + line[index + len('$APP'):]
                fout.write(line)
            fin.close()
            fout.close()
            
    y = yaml.load(open(os.path.join(appdir, 'setting.yaml'), 'r'))
    file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'repository.yaml')
    shutil.copy(file, os.path.join(appdir, y['application']['RTC_DIR'], 'repository.yaml'))
    
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        cmd = ['chmod', '755', os.path.join(prjname, 'mgr.py')]
        subprocess.call(cmd)

    register_project(prjname, appdir, verbose=verbose)    
    pass

def register_project(appname, appdir, verbose):
    if verbose:
        print ' - Registering workspace:'
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        fout = open(ws_file_name, "w")
        fout.close()

    y = yaml.load(open(ws_file_name, "r"))
    if not y:
        y = {}

    y[appname] = appdir

    fout = open(ws_file_name, "w")

    if verbose:
        for key, item in y.items():
            print '  ' + key + ' '*(10-len(key)) + ':' + item

    yaml.dump(y, fout,  encoding='utf8', allow_unicode=True, default_flow_style=False)

    if verbose:
        print ' - Finished.'
    return True


def unregister_project(appname, verbose):
    if verbose:
        print ' - Unregistering workspace:'
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        if verbose:
            print ' - workspace.yaml can not be found in RTM_HOME'
        return
    
    if verbose:
        print ' - Opening workspace.yaml and writing workspace data.'

    y = yaml.load(open(ws_file_name, "r"))

    if appname in y.keys():
        if verbose:
            print '    - %s found. Deleting workspace.' % appname
        del(y[appname])

    if verbose:
        print ' - Saving workspace.yaml'
    yaml.dump(y, open(ws_file_name, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)
    if verbose:
        print ' - Finished.'
    return True



def get_projects(verbose):
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        sys.stdout.write(' - Can not find workspace.yaml: %s\n' % ws_file_name)
        fout = open(ws_file_name, "w")
        return False
    else:
        if verbose:
            sys.stdout.write(' - Opening workspace.yaml.\n')
        return yaml.load(open(ws_file_name, "r"))

