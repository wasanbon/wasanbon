import os, sys, yaml, types, subprocess

import wasanbon
from package_obj import  PackageObject

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

def load_workspace(verbose=False):
    ws_file_name = os.path.join(wasanbon.home_path, "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        if verbose:
            sys.stdout.write(' - Can not find workspace.yaml: %s\n' % ws_file_name)
            sys.stdout.write(' - Creating workspace.yaml\n')
        open(ws_file_name, "w").close()
        return {}
    else:
        if verbose: sys.stdout.write(' - Opening workspace.yaml.\n')
        y= yaml.load(open(ws_file_name, "r"))
        if not y: y = {}
        return y

def save_workspace(dic):
    ws_file_name = os.path.join(wasanbon.home_path, 'workspace.yaml')
    yaml.dump(dic, open(ws_file_name, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)


def create_package(prjname, verbose=False, overwrite=False, force_create=False):
    projs = get_packages(verbose)
    proj_names = [prj.name for prj in projs]
    if prjname in proj_names:
        if verbose: sys.stdout.write(' - There is %s package in workspace.yaml already\n' % prjname)
        raise wasanbon.PackageAlreadyExistsException()

    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    appdir = os.path.join(os.getcwd(), prjname)
    if not force_create:
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose: sys.stdout.write(' - There seems to be %s here. Please change application name.\n' % prjname)
            raise wasanbon.DirectoryAlreadyExistsException()

    for root, dirs, files in os.walk(tempdir):
        distdir = os.path.join(appdir, root[len(tempdir)+1:])
        if not os.path.isdir(distdir):
            os.mkdir(distdir)
        for file in files:
            if os.path.isfile(os.path.join(distdir, file)) and not overwrite:
                pass
            else:
                if verbose:
                    sys.stdout.write(" - copy file: %s\n" % file)
                parse_and_copy(os.path.join(root, file), os.path.join(distdir, file), {'$APP' : prjname})
            
    #y = yaml.load(open(os.path.join(appdir, 'setting.yaml'), 'r'))
    #file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'repository.yaml')
    #shutil.copy(file, os.path.join(appdir, y['application']['RTC_DIR'], 'repository.yaml'))
    
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        cmd = ['chmod', '755', os.path.join(prjname, 'mgr.py')]
        subprocess.call(cmd)

    register_package(prjname, appdir)
    return 0

def register_package(prjname, appdir):
    y = load_workspace()
    y[prjname] = appdir
    save_workspace(y)
    return 0
def delete_package(name, deletepath=False, verbose=False):
    p = get_package(name)
    
    dic = load_workspace()
    dic.pop(p.name)
    save_workspace(dic)

    if deletepath:
        import shutil
        def remShut(*args):
            func, path, _ = args 
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        shutil.rmtree(p.path, onerror = remShut)
    return 0
        

def validate_package(package, verbose=False, autofix=False, interactive=False, ext_only=False):
    for lang in ['C++', 'Java', 'Python']:
        rtcc = package.rtcconf[lang]
        if lang == 'C++':
            rtcc.ext_check(verbose=verbose, autofix=autofix, interactive=interactive)
        if not ext_only:
            rtcc.validate(verbose=verbose, autofix=autofix, interactive=interactive)
        rtcc.sync()
    
def get_packages(verbose=False, force=True):
    y = load_workspace()
    projs = []
    if type(y) != types.NoneType:
        for key, value in y.items():
            try:
                projs.append(PackageObject(name=key, path=value))
            except wasanbon.InvalidPackagePathError, ex:
                if force:
                    if verbose:
                        sys.stdout.write(' - Invalid Package Path (%s:%s)\n' % (key,value))
                        pass
                else:
                    raise wasanbon.PackageNotFoundException()
    return projs


def get_package(name, verbose=False):
    y = load_workspace()
    if not name in y.keys():
        raise wasanbon.PackageNotFoundException()
    return PackageObject(name, y[name])


def get_package_from_path(path, verbose=False):
    y = load_workspace()
    for key, value in y.items():
        if value == path:
            return PackageObject(key, value)
    

    raise wasanbon.PackageNotFoundException()

