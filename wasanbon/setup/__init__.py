import os, sys, urllib, subprocess

# This data can not be exported to yaml file because this setup can be launched without yaml library.
_urls = {
    'yaml': {'win32' : "http://pyyaml.org/download/pyyaml/PyYAML-3.10.win32-py2.6.exe",
             'darwin' : 'http://sugarsweetrobotics.com/pub/Darwin/libs/PyYAML-3.10.tar.gz',
             'linux2' : 'http://sugarsweetrobotics.com/pub/Darwin/libs/PyYAML-3.10.tar.gz'},
    'github' : {'darwin' : 'https://pypi.python.org/packages/source/P/PyGithub/PyGithub-1.23.0.tar.gz',
                'win32'  : 'https://pypi.python.org/packages/source/P/PyGithub/PyGithub-1.23.0.tar.gz',
                'linux2'  : 'https://pypi.python.org/packages/source/P/PyGithub/PyGithub-1.23.0.tar.gz'},
    'setuptools': {'darwin' : 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py',
                   'win32' : 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py',
                   'linux2' : 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py'},
    'psutil' : {'darwin' : 'https://pypi.python.org/packages/source/p/psutil/psutil-1.2.1.tar.gz',
                'linux2' : 'https://pypi.python.org/packages/source/p/psutil/psutil-1.2.1.tar.gz',
                'win32' : 'https://pypi.python.org/packages/2.6/p/psutil/psutil-1.2.1.win32-py2.6.exe'},
    'pip' : {'darwin' : 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py',
             'linux2' : 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py',
             'win32' : 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'},
    'bitbucket' : {'darwin' : 'pip install bitbucket-api',
                   'linux2' : 'pip install bitbucket-api',
                   'win32' : 'pip install bitbucket-api'}
    }

def _get_url(tag):
    global _urls
    return _urls[tag][sys.platform]

def _download_url(url, verbose=False, force=False, path='downloads'):
    out = None if verbose else subprocess.PIPE
    cur_dir = os.getcwd()
    dir = os.path.join(cur_dir, path)
    if os.path.isdir(dir):
        if force:
            pass
        else:
            return False
    else:
        os.mkdir(dir)
    file = os.path.join(dir, os.path.basename(url))

    if not os.path.isfile(file):
        class DownloadReport(object):
            def __init__(self):
                pass

            def __call__(self, read_blocks, block_size, total_bytes):
                end = read_blocks * block_size / float(total_bytes) * 100.0
                sys.stdout.write('\rProgress %3.2f [percent] ended' % end)
                sys.stdout.flush()
            pass
        if verbose:
            sys.stdout.write(' - Downloading url:%s\n' % url)
        urllib.urlretrieve(url, file+'.part', DownloadReport())
        os.rename(file+'.part', file)
        if verbose:
            sys.stdout.write(' - Saved to %s\n' % file)

    return file

def _install_exe(file, verbose=False, path='downloads'):
    if verbose:
        sys.stdout.write(' - Launching %s\n' % file)
    cur_dir = os.getcwd()
    os.chdir(os.path.join(cur_dir, path))
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen([file], stdout=out, stdin=out)
    ret = p.wait()
    os.chdir(cur_dir)
    return ret

def _install_py(file, verbose=False, path='downloads'):
    if verbose:
        sys.stdout.write(' - Launching %s\n' % file)
    cur_dir = os.getcwd()
    os.chdir(os.path.join(cur_dir, path))
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen(['python', file], stdout=out, stdin=out)
    ret = p.wait()
    os.chdir(cur_dir)
    return ret

def _install_pip(cmd, verbose=False):
    cmds = cmd.split()
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen(cmds, stdout=out, stdin=out)
    ret = p.wait()
    return ret

def _extract_tar(filename, verbose=False):
    if verbose:
        sys.stdout.write(' - Extracting %s\n' % filename)
    cur_dir = os.getcwd()
    os.chdir(os.path.dirname(filename))
    if filename.endswith('.tar.gz'):
        dirname = filename[:-7]
    elif filename.endswith('.tgz'):
        dirname = filename[:-4]
    else:
        return (False, "")

    cmd = ['tar', 'zxfv', filename]
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen(cmd, stdout=out, stdin=out)
    ret = p.wait()
    os.chdir(cur_dir)
    return (ret, dirname)

def _extract_tar_and_install(filename, verbose=False):
    ret, dirname = _extract_tar(filename, verbose=verbose)
    if ret == 0:
        _setup_py(dirname, verbose=verbose)
        return True

def _setup_py(dirname, args=[['install']], verbose=False):
    if verbose:
        sys.stdout.write(' - Installing Python Module in "%s" with distutil.\n' % dirname)
    cwd = os.getcwd()
    os.chdir(dirname)
    out = None if verbose else subprocess.PIPE
    if os.path.isfile('setup.py'):
        for arg in args:
            cmd = ['python', 'setup.py'] + arg
            if sys.platform == 'linux' or sys.platform == 'darwin':
                cmd = ['sudo'] + cmd
            ret = subprocess.call(cmd, stdout=out, stdin=out)
    os.chdir(cwd)
    return ret

def download_and_install(tag, verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Download and Intall [%s]\n' % tag)
    url = _get_url(tag)
    
    if url.startswith('pip'):
        return _install_pip(url, verbose=verbose)
    
    filename = _download_url(url, verbose=verbose, force=force)
    if not filename:
        return False
    if filename.endswith('.exe'):
        return _install_exe(filename, verbose=verbose)
    elif filename.endswith('.py'):
        return _install_py(filename, verbose=verbose)
    elif filename.endswith('.tar.gz'):
        return _extract_tar_and_install(filename, verbose=verbose)
