import os, sys
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


def download_and_install(url, force=False):
    filename = os.path.basename(url)
    dist_file = os.path.join(wasanbon.rtm_temp, filename)
    download.download(url, dist_file, force=force)
    install.install(dist_file)
    pass



