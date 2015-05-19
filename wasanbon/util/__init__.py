import os, sys, subprocess, types, time, threading
import wasanbon
#from . import download, install, archive, svn#, git


def choice(alts, callback, msg='Choice', choice_msg='Choice?:', noquit=False):
    if not noquit:
        alts.append('Quit(Q)')
    while True:
        print msg
        for i in range(0, len(alts)):
            sys.stdout.write(' - %s:%s\n' % (i+1, alts[i]))
        i = raw_input(choice_msg) # Input 
        try:
            if i == 'q' or i == 'Q': # if chice is 'q', quit.
                sys.stdout.write('Quit.\n')
                break
            ans = int(i)
        except ValueError, e:
            sys.stdout.write(' - ValueError.\n') 
            continue
        if ans < 1 or ans > len(alts):
            sys.stdout.write(' - RangeError.\n')
            continue
        if ans == len(alts):
            sys.stdout.write(' - Quit.\n')
            break
        # Callback Function
        retval = callback(ans-1)
        if type(retval) == types.ListType:
            ans = retval[0]
            alts = retval[1]
            alts.append('Quit(Q)')
        else:
            ans = retval

        # if callback function returns True, quit.
        if ans:
            sys.stdout.write(' - Quit.\n')
            break
        

def yes_no(msg):
    sys.stdout.write('%s (Y/n)' % msg)
    while True:
        c = raw_input()
        if len(c) == 0:
            return 'yes'
        if c[0] == 'y':
            return 'yes'
        else:
            return 'no'


def no_yes(msg):
    sys.stdout.write('%s (y/N)' % msg)
    while True:
        c = raw_input()
        if len(c) == 0:
            return 'no'
        if c[0] == 'y':
            return 'yes'
        else:
            return 'no'
    
"""
def download_and_unpack(url, dist_path, force=False, verbose=False):
    filename = os.path.basename(url)
    dist_file = os.path.join(wasanbon.rtm_temp(), filename)
    download.download(url, dist_file, force=force, verbose=verbose)
    if filename.endswith(".zip"):
        archive.unpack_zip(dist_file, dist_path)
    elif filename.endswith(".tar.gz"):
        archive.unpack_tgz(dist_file, dist_path)
    pass

def apt_get(url, verbose=False):
    cmd = [e for e in url.split(' ') if not e == '']
    if verbose:
        sys.stdout.write(' - Executing apt-get : %s\n' % cmd)
    subprocess.call(cmd)

def download_and_install(url, force=False, temp="", verbose=False, open_only=False):
    if url.startswith("apt-get") or url.startswith("aptitude"):
        apt_get(url)
        return

    if verbose:
        sys.stdout.write(' - Download and Install from %s\n' % url)

    filename = os.path.basename(url)
    if len(temp)==0:
        temp = wasanbon.rtm_temp()

    dist_file = os.path.join(temp, filename)
    download.download(url, dist_file, force=force, verbose=verbose)

    if dist_file.endswith(".zip"):
        dist_path = dist_file[:-4]
        archive.unpack_zip(dist_file, dist_path, verbose=verbose)
        for root, dirs, files in os.walk(dist_path):
            for dir in dirs:
                if dir.endswith('.mpkg'):
                    install.install(os.path.join(root, dir), verbose=verbose)
    else:
        install.install(dist_file, open_only=open_only, verbose=verbose)
    pass
"""

def search_file(rootdir, filename):
    found_files_ = []
    if type(filename) is list:
        for file_ in filename:
            found_files_ = found_files_ + search_file(rootdir, file_)
        return found_files_

    files = os.listdir(rootdir)

    for file_ in files:
        fullpath_ = os.path.join(rootdir, file_)
        if os.path.isdir(fullpath_):
            found_files_ = found_files_ + search_file(fullpath_, filename)
        else:
            if file_ == filename:
                found_files_.append(fullpath_)
    return found_files_

def set_proxy(addr, port, verbose=False):
    if verbose:
        sys.stdout.write(' - Set Proxy Server:(%s:%s)\n' % (addr, port))
        pass
    svn.set_proxy(addr, port, verbose=verbose)
    import git
    git.set_proxy(addr, port, verbose=verbose)

    pass


def omit_proxy(verbose=False):
    if verbose:
        sys.stdout.write(' - Omitting Proxy Server setting.\n')
        pass
    svn.omit_proxy(verbose=verbose)
    git.omit_proxy(verbose=verbose)
    pass
