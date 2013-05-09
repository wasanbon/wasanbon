import os, sys, subprocess
import wasanbon
from . import download, install, archive

def yes_no(msg):
    sys.stdout.write('%s (y/n)' % msg)
    while True:
        c = raw_input()
        if c[0] == 'y':
            return 'yes'
        else:
            return 'no'

def download_and_unpack(url, dist_path, force=False):
    filename = os.path.basename(url)
    dist_file = os.path.join(wasanbon.rtm_temp, filename)
    download.download(url, dist_file, force=force)
    if filename.endswith(".zip"):
        archive.unpack_zip(dist_file, dist_path)
    elif filename.endswith(".tar.gz"):
        archive.unpack_tgz(dist_file, dist_path)
    pass

def apt_get(url):
    cmd = url.split(' ')
    subprocess.call(cmd)

def download_and_install(url, force=False, temp=""):
    if url.startswith("apt-get"):
        apt_get(url)
        return
    filename = os.path.basename(url)
    if len(temp)==0:
        temp = wasanbon.rtm_temp
    dist_file = os.path.join(temp, filename)
    download.download(url, dist_file, force=force)
    install.install(dist_file)
    pass


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

