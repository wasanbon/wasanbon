import os, sys, urllib, subprocess, types, shutil
from installer import *
from downloader import *
from extractor import *
from path import *
from archive import *

# This data can not be exported to yaml file because this setup can be launched without yaml library.
_urls = {
    'yaml': { 'win32' : 'pip install pyyaml',
        #'win32' : 'https://pypi.python.org/packages/2.6/P/PyYAML/PyYAML-3.11.win32-py2.6.exe',
        'darwin' : 'pip install pyyaml',
        'linux2' : 'http://sugarsweetrobotics.com/pub/Darwin/libs/PyYAML-3.10.tar.gz'},
    
    'github' : {'darwin' : 'pip install pygithub',
                'win32'  : 'pip install pygithub',
                'linux2'  : 'pip install pygithub'},
    'setuptools': {'darwin' : 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py',
                   'win32' : 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py',
                   'linux2' : 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py'},

    'psutil' : {'darwin' : 'pip install psutil',
                'linux2' : 'apt-get install python-psutil',
                #'win32' : 'https://pypi.python.org/packages/2.6/p/psutil/psutil-2.0.0.win32-py2.6.exe'
                'win32' : 'pip install psutil'
                },

    'pip' : {'darwin' : 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py',
             'linux2' : 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py',
             'win32' : 'easy_install pip'
             },
    'requests' : {'darwin' : 'pip install requests',
                  'linux2' : 'pip install requests',
                  'win32' : 'pip install requests'},
    'requests_oauthlib' : {'darwin' : 'pip install requests-oauthlib',
                  'linux2' : 'pip install requests-oauthlib',
                  'win32' : 'pip install requests-oauthlib'},
    'bitbucket' : {'darwin' : 'pip install bitbucket-api --pre',
                   'linux2' : 'pip install bitbucket-api --pre',
                   'win32' : 'pip install bitbucket-api --pre',},

    'freetype' : {'darwin' : 'http://download.savannah.gnu.org/releases/freetype/freetype-2.4.10.tar.gz'
                  },

    #'lxml' : {'darwin' : 'pip install lxml',
    #          'linux2' : 'pip install lxml',
    #          'win32' : 'pip install lxml'},

    #'pillow' : {'darwin' : 'pip install pillow',
    #          'linux2' : 'pip install pillow',
    #          'win32' : 'pip install pillow'},

    'jinja2' : {'darwin' : 'pip install jinja2',
              'linux2' : 'pip install jinja2',
              'win32' : 'pip install jinja2'},
    }

def _get_url(tag):
    global _urls
    if not tag in _urls.keys():
        return None
    return _urls[tag][sys.platform]

def import_check(pack):
    try:
        __import__(pack)
        return True
    except ImportError, ex:
        return False

def extract_zip_and_install(filename, verbose=False, distpath='.', force=False):
    if verbose: sys.stdout.write('# Extracting %s\n' % filename)
    dist_path = filename[:-4]
    
    if os.path.isdir(dist_path):
        if force:
            original_dist_path  = dist_path
            i = 2
            while os.path.isdir(dist_path):
                dist_path = original_dist_path + str(i)
                i = i + 1
            unpack_zip(filename, dist_path, verbose=verbose)
    else:
        unpack_zip(filename, dist_path, verbose=verbose)        

    for root, dirs, files in os.walk(dist_path):
        for dir in dirs:
            if dir.endswith('.mpkg'):
                return install(os.path.join(root, dir), verbose=verbose)
        for file in files:
            if file == 'setup.py':
                return install_setup_py(root, verbose=verbose)
            if file.endswith('.jar'):
                if distpath:
                    src = os.path.join(root, file)
                    dst = os.path.join(distpath, 'jar')
                    dstfile = os.path.join(dst, os.path.basename(src))
                    if not os.path.isdir(dst):
                        os.mkdir(dst)
                    if not os.path.isfile(dstfile):
                        shutil.move(src, dst)
                

def extract_tar_and_install(filename, verbose=False, distpath=None):
    if verbose: sys.stdout.write('# Extracting tar file and installing ....\n')
    ret, dirname = extract_tar(filename, verbose=verbose, distpath=distpath)
    if ret == 0:
        if os.path.isfile(os.path.join(dirname, 'setup.py')):
            install_setup_py(dirname, verbose=verbose)
        return True

def try_import_and_install(pack, verbose=False, force=False, workpath='downloads'):
    if verbose: sys.stdout.write('# Trying to import %s module.\n' % pack)
    if import_check(pack):
        if verbose: sys.stdout.write('## Package %s is successfully imported.\n')
        if not force: return 0
    else: sys.stdout.write('## Import Error. You need to install python-%s module.\n' % pack)

    sys.stdout.write('# AUTOMATIC INSTALL\n')
    sys.stdout.write('# You will may need to invoke the command with superuser privileges to install.\n')
    if not force:
        ret = raw_input('#? Do you want to install python-%s automatically?(Y/n):' % pack)
        if ret == '' or ret.startswith('Y') or ret.startswith('y'):
            pass
        else:
            return -1
    if not download_and_install(pack, force=force, verbose=verbose, temppath=workpath):
        sys.stdout.write('# Error. There may be "download" directory in the current path.\n')
        return -1
    return 0


def download_and_install(tag, verbose=False, force=False, temppath='downloads', installpath='.'):
    if verbose: sys.stdout.write('# Download and Intall [%s]\n' % tag)
    url = _get_url(tag)
    if url is None:
        url = tag

    if type(url) != types.ListType:
        url = [url]
        
    for u in url:
        _download_and_install_url(u, verbose=verbose, force=force, temppath=temppath, installpath=installpath)
        if import_check(tag):
            return True
    return False


def _download_and_install_url(url, verbose=False, force=False, temppath='downloads', installpath='.'):    
    if not os.path.isdir(temppath):
        os.mkdir(temppath)
    if url.startswith('easy_install'):
        return install_easy_install(url, verbose=verbose)

    if url.startswith('pip'):
        return install_pip(url, verbose=verbose)

    if url.startswith('apt-get'):
        return install_apt(url, verbose=verbose)

    if url.startswith('svn'):
        return install_svn(url, path=temppath, verbose=verbose)

    if url.startswith('aptitude'):
        return install_apt(url, verbose=verbose)
    
    filename = download_url(url, verbose=verbose, force=force, path=temppath)
    if not filename:
        return False
    if filename.endswith('.exe'):
        return install_exe(filename, verbose=verbose)
    elif filename.endswith('.py'):
        return install_py(filename, verbose=verbose)
    elif filename.endswith('.tar.gz'):
        return extract_tar_and_install(filename, verbose=verbose, distpath=installpath)
    elif filename.endswith('.zip'):
        return extract_zip_and_install(filename, verbose=verbose, distpath=installpath)
    elif filename.endswith('.dmg'):
        return install_dmg(filename, verbose=verbose)
    elif filename.endswith('.msi'):
        return install(filename, verbose=verbose)
    else:
        sys.stdout.write(' ## Error. Unsupported Format File %s\n' % filename)

