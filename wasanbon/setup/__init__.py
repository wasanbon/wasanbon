import os, sys, urllib

_urls = {
    'pyyaml': {'win32' : "http://pyyaml.org/download/pyyaml/PyYAML-3.10.win32-py2.6.exe",
               'darwin' : 'http://sugarsweetrobotics.com/pub/Darwin/libs/PyYAML-3.10.tar.gz',
               'linux' : 'http://sugarsweetrobotics.com/pub/Darwin/libs/PyYAML-3.10.tar.gz'}

    }

def _get_url(tag):
    global _urls
    return _urls[tag][sys.platform]


def _download_url(url, verbose=False):
    out = None if verbose else subprocess.PIPE
    cur_dir = os.getcwd()
    file = os.path.join(cur_dir, 'thirdparty', os.path.basename(url))
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
        if verobse:
            sys.stdout.write(' - Saved to %s\n' % file)

    return file

def _install_exe(file, verbose=False):
    if verbose:
        sys.stdout.write(' - Launching %s\n' % file)
    cur_dir = os.getcwd()
    os.chdir(os.path.join(cur_dir, 'thirdparty'))
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen([file], stdout=out, stdin=out)
    ret = p.wait()
    os.chdir(cur_dir)
    return ret

def extract_tar(filename, verbose=False):
    cur_dir = os.getcwd()
    os.chdir(os.path.dirname(filename))
    if filename.endswith('.tar.gz'):
        dirname = filename[:-7]
    elif filename.endswith('.tgz'):
        dirname = filename[:-4]
    else:
        return (False, "")

    cmd = ['tar', 'zxfv', filename, dirname]
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen(cmd, stdout=out, stdin=out)
    ret = p.wait()
    os.chdir(cur_dir)
    return (ret, dirname)

def _extract_tar_and_install(filename, verobse=False):
    ret, dirname = extract_tar(filename, verbose=verbose)
    if ret:
        setup_py(dirname, verbose=verbose)


def setup_py(dirname, args=[['install']], verbose=False):
    cwd = os.getcwd()
    os.chdir(dirname)
    out = None if verbose else subprocess.PIPE
    if os.path.isfile('setup.py'):
        for arg in args:
            cmd = ['python', 'setup.py'] + arg
            p = subprocess.Popen(cmd, stdout=out, stdin=out)
            ret = p.wait()

    os.chdir(cwd)
    return ret

def download_and_install(tag, verbose=False):
    if verbose:
        sys.stdout.write(' - Download and Intall [%s]\n' % tag)
    url = _get_url(tag)
    filename = download_url(url, verbose=verbose)
    if filename.endswith('.exe'):
        return _install_exe(filename, verbose=verbose)
    elif filename.endswith('.tar.gz'):
        return _extract_tar_and_install(filename, verbose=verbose)
