"""
@author Yuki Suga (Sugar Sweet Robotics)
@email ysuga@sugarsweetrobotics.com
@copyright SugarSweetRobotics Co. LTD. 2014
"""

import os, sys, yaml, subprocess, shutil, types, threading
import wasanbon
from wasanbon.util import git
from connection import *
from package_obj import *
from repository import *
from diff import *
from wasanbon.core import repositories


def run_nameservers(obj, verbose=False, force=False):
    nss = obj.get_nameservers(verbose=verbose)
    interval = 1.0
    def callback():
        
    wdt = threading.Timer(interval, callback)
    for ns in nss:
        if not ns.check_and_launch(verbose=verbose, force=force):
            if verbose:
                sys.stdout.write(' @ Nameserver %s is not running\n' % ns.path)
            return False

    return True


def kill_nameservers(obj, verbose=False):
    nss = obj.get_nameservers(verbose=verbose)
    for ns in nss:
        ns.kill()
    return True

"""
"""
def run_system(obj, verbose=False):
    obj.launch_all_rtcd(verbose=verbose)
    obj.launch_standalone_rtcs(verbose=verbose)
    return True


def build_system(obj, verbose=False):
    obj.connect_and_configure(verbose=verbose)
    return True


def activate_system(obj, verbose=False):
    obj.activate(verbose=verbose)
    return True

def deactivate_system(obj, verbose=False):
    obj.deactivate(verbose=verbose)
"""
"""
def stop_system(obj, verbose=False):
    obj.deactivate(verbose=verbose)
    obj.terminate_standalone_rtcs(verbose=verbose)
    obj.terminate_all_rtcd(verbose=verbose)


"""
package : wasanbon.core.package.Package class object
rtc : string - name of rtc / wasanbon.core.rtc.Rtc class object

option
verbose : message on/off
overwrite_conf : overwrite configuration file on/off
"""
def install_rtc(package, rtc, verbose=False, overwrite_conf=False, standalone=False):
    if type(rtc) == types.ListType:
        return [install_rtc(package, r, verbose=verbose, overwrite_conf=overwrite_conf, standalone=standalone) for r in rtc]
    else:
        if type(rtc) == types.StringType:
            rtc = package.rtc(rtc)
        return package.install(rtc, verbose=verbose, copy_conf=overwrite_conf, standalone=standalone)

def git_push(package, verbose=False):
    git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose, path=package.path)

def github_init(package, user, passwd, verbose=False):
    from wasanbon.core.repositories import github_api
    github_obj = github_api.GithubReference(user, passwd)
    repo = github_obj.create_repo(package.name)
    git.git_command(['remote', 'add', 'origin', 'git@github.com:' + user + '/' + package.name + '.git'], verbose=verbose, path=package.path)
    git_push(package, verbose=verbose)

def bitbucket_init(package, user, passwd, verbose=False):
    from wasanbon.core.repositories import bitbucket_api
    _obj = bitbucket_api.BitbucketReference(user, passwd)
    repo = _obj.create_repo(package.name)
    git.git_command(['remote', 'add', 'origin', 'https://bitbucket.org/' + user + '/' + package.name + '.git'], verbose=verbose, path=package.path)
    git_push(package, verbose=verbose)

############### legacy codes #################

def get_repositories(verbose=False):
    rtcs, packs = repositories.load_repositories(verbose=verbose)
    repos = []
    for key, value in packs.items():
        repos.append(PackageRepository(key, value['description'], value['url']))
    return repos


def get_repository(name, verbose=False):
    repos = get_repositories(verbose)
    for repo in repos:
        if repo.name == name:
            return repo
    raise wasanbon.RepositoryNotFoundException()

def update_repositories(verbose=False, force=False, url=None):
    repo_path = os.path.join(wasanbon.rtm_home(), 'repositories')
    for dir in os.listdir(repo_path):
        if dir.startswith('.'):
            continue
        if dir.endswith(repositories.owner_sign):
            user = dir[:-len(repositories.owner_sign)]
        else:
            user = dir
        for repo_name in os.listdir(os.path.join(repo_path, dir)):
            url = 'https://github.com/' + user + '/' + repo_name
            repositories.download_repositories(verbose=verbose, force=force, url=url)
    pass



def get_packages(verbose=False, force=True):
    ws_file_name = os.path.join(wasanbon.rtm_home(), "workspace.yaml")
    if not os.path.isfile(ws_file_name):
        if verbose:
            sys.stdout.write(' - Can not find workspace.yaml: %s\n' % ws_file_name)
            sys.stdout.write(' - Creating workspace.yaml\n')
        fout = open(ws_file_name, "w")
        fout.close()
        return []
    else:
        if verbose:
            sys.stdout.write(' - Opening workspace.yaml.\n')
        y= yaml.load(open(ws_file_name, "r"))
        projs = []
        if type(y) != types.NoneType:
            for key, value in y.items():
                try:
                    projs.append(Package(value))
                except wasanbon.InvalidPackagePathError, ex:
                    if force:
                        if verbose:
                            sys.stdout.write(' - Invalid Package Path (%s:%s)\n' % (key,value))
                        pass
                    else:
                        raise ex
        return projs

def get_package(prjname, verbose=False):
    target = None
    projs = get_packages(verbose)
    for proj in projs:
        if proj.name == prjname:
            return proj
    raise wasanbon.PackageNotFoundException()

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

def create_package(prjname, verbose=False, overwrite=False, force_create=False):
    projs = get_packages(verbose)
    proj_names = [prj.name for prj in projs]
    if prjname in proj_names:
        if verbose:
            print ' - There is %s package in workspace.yaml already\n' % prjname
        raise wasanbon.PackageAlreadyExistsException()

    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    appdir = os.path.join(os.getcwd(), prjname)
    if not force_create:
        if os.path.isdir(appdir) or os.path.isfile(appdir):
            if verbose:
                print ' - There seems to be %s here. Please change application name.' % prjname
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

    proj = Package(appdir)
    proj.register(verbose)
    return proj



def clone_package(prjname, verbose=False):
    try:
        projs = get_packages(verbose)
        if verbose:
            print ' - There is %s package in workspace.yaml\n' % prjname
            print ' - Please unregister the package\n' 
        raise wasanbon.PackageAlreadyExistsException()
    except wasanbon.PackageNotFoundExeption, ex:
        pass

    appdir = os.path.join(os.getcwd(), prjname)
    if os.path.isdir(appdir) or os.path.isfile(appdir):
        if verbose:
            print ' - There seems to be %s here. Please change application name.' % prjname
        raise wasanbonDirectoryAlreadyExistsException()
    
    repo = get_repository(projname)
    git.git_command(['clone', repo.url, appdir], verbose)
    return package.create_package(self.name, verbose=verbose)


def diff(repo1, repo2):
    return PackageDiff(repo1, repo2)
