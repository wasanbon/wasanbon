import os, sys, yaml, subprocess, shutil
import wasanbon

from project_obj import *

def get_projects(verbose=False):
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        sys.stdout.write(' - Can not find workspace.yaml: %s\n' % ws_file_name)
        fout = open(ws_file_name, "w")
        fout.close()
        return {}
    else:
        if verbose:
            sys.stdout.write(' - Opening workspace.yaml.\n')
        y= yaml.load(open(ws_file_name, "r"))
        projs = []
        for key, value in y.items():
            projs.append(Project(value))
        return projs

def get_project(prjname, verbose=False):
    target = None
    projs = get_projects(verbose)
    for proj in projs:
        if proj.name == prjname:
            target = proj

    return target

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
    proj_names = [prj.name for prj in projs]
    if prjname in proj_names:
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



