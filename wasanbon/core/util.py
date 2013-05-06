import zipfile
import urllib, subprocess
from wasanbon.core.management import *

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



def download_and_unpack(url, dist="", force=False):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    filename = os.path.basename(url)
    distpath = os.path.join(rtm_temp, filename)

    if len(dist) == 0:
        dist = rtm_temp

    # try to download
    download(url, distpath, force=force)

    if filename.endswith(".zip"):
        unpack_zip(distpath, dist, noinstall=(unpackonly))
    elif filename.endswith(".tar.gz"):
        unpack_tgz(distpath, dist, noinstall=(unpackonly))

    pass

class DownloadReport(object):
    def __init__(self):
        pass

    def __call__(self, read_blocks, block_size, total_bytes):
        end = read_blocks * block_size / float(total_bytes) * 100.0
        sys.stdout.write('\rProgress %3.2f [percent] ended' % end)
        sys.stdout.flush()


def download(url, dist, force=False):
    if force and os.path.isfile(dist):
        os.remove(dist)
    if not os.path.isfile(dist):
        sys.stdout.write("Downloading from URL: %s\n" % url)
        urllib.urlretrieve(url, dist+'.part', DownloadReport())
        sys.stdout.write("Saved in Directory  :%s\n" % dist)
        os.rename(dist+'.part', dist)
    pass

def download_and_install(url):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    filename = os.path.basename(url)
    distpath = os.path.join(rtm_temp, filename)

    # try to download
    download(url, distpath)

    parse_package(distpath)
        
    pass

def install_msi(msi):
    cmd = ('msiexec', '/i', msi)
    try:
        ret = subprocess.check_output(cmd)
        print 'Installing %s is successful. Message is below' % msi
        print ret
    except:
        print 'Installing %s is failed.' % msi
    pass

def install_exe(exe):
    cmd = [exe]
    try:
        ret = subprocess.check_output(cmd)
        print 'Installing %s is successful. Message is below' % exe
        print ret
    except:
        print 'Installing %s is failed.' % exe

def install_pkg(pkg):
    cmd = ['installer', '-package', pkg, '-target', '/Volumes/Macintosh HD']
    try:
        ret = subprocess.check_output(cmd)
        print 'Installing %s is successful. Message is below' % pkg
        print ret
    except:
        print 'Installing %s is failed. Maybe this process must have done by super user.' % pkg

def install_app(app):
    if app.endswith('/'):
        app = app[len(app)-1:]

    cmd = ['cp', '-R', app, '/Applications/']
    try:
        ret = subprocess.check_output(cmd)
        print 'Installing %s is successful. Message is below' % app
        print ret
    except:
        print 'Installing %s is failed. Maybe this process must have done by super user.' % app

def parse_package(file, nounpack=False, noinstall=False):
    if file.startswith('.'):
        pass
    elif file.endswith(".pkg") and not noinstall:
        install_pkg(file)
    elif file.endswith(".app") and not noinstall:
        install_app(file)
    elif file.endswith(".exe") and not noinstall:
        install_exe(file)
    elif file.endswith(".msi") and not noinstall:
        install_msi(file)
    elif file.endswith(".zip") and not nounpack:
        unpack_zip(file)
    elif file.endswith(".dmg") and not nounpack:
        unpack_dmg(file)


def unpack_dmg(dmg):
    cmd = ['hdiutil', 'mount', dmg]
    ret = subprocess.check_output(cmd)
    mountedVolume = [x.strip() for x in ret.split('\t') if x.startswith("/Volumes/")]
    if len(mountedVolume) != 1:
        print 'Error mounting %s' % dmg

    for root, dirs, files in os.walk(mountedVolume[0]):
        for dir in dirs:
            parse_package(os.path.join(root, dir), nounpack=True)
        for file in files:
            parse_package(os.path.join(root, file), nounpack=True)

    cmd = ['hdiutil', 'unmount', mountedVolume[0]]
    ret = subprocess.check_output(cmd)

def unpack_tgz(filepath, distpath, noinstall=False):
    old_dir = os.getcwd()
    dir, file = os.path.split(filepath)
    os.chdir(dir)
    cmd = ['tar', 'zxfv', filepath, '-C', distpath]
    #subprocess.check_output(cmd)
    subprocess.call(cmd)

    os.chdir(old_dir)
    pass

def unpack_zip(filepath, distpath = "", noinstall=False):
    sys.stdout.write("Unpacking %s\n" % filepath)
    path, file = os.path.split(filepath)
    if len(distpath) == 0:
        distpath = os.path.join(path, file[len(file)-4:])
    if not os.path.isdir(distpath):
        os.mkdir(distpath)
    zf = zipfile.ZipFile(filepath)
    for filepath in zf.namelist():
        sys.stdout.write(" - %s\n" % filepath)
        fullpath = os.path.join(distpath, filepath)
        path, filename = os.path.split(fullpath)
        if not os.path.isdir(path) and len(path) > 0:
            os.makedirs(path)
        if not os.path.isfile(fullpath) and len(filename) > 0:
            fout = open(fullpath, 'wb')
            fout.write(zf.read(filepath))
            fout.close()
    zf.close()

    for root, dirs, files in os.walk(distpath):
        for file in files:
            parse_package(os.path.join(root, file), nounpack=True, noinstall=noinstall)

    pass
