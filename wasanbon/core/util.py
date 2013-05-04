
import urllib, subprocess
from wasanbon.core.management import *


def unpack_zip(filepath):
    path, file = os.path.split(filepath)
    distpath = os.path.join(path, file[len(file)-4:])
    if not os.path.isdir(distpath):
        os.mkdir(distdir)
    zf = zipfile.ZipFile(filepath)
    for filepath in zf.namelist():
        fullpath = os.path.join(distdir, filepath)
        path, filename = os.path.split(fullpath)
        if not os.path.isdir(path) and len(path) > 0:
            os.makedirs(path)
        if not os.path.isfile(fullpath) and len(filename) > 0:
            fout = file(fullpath, 'wb')
            fout.write(zf.read(filepath))
            fout.close()
    zf.close()
    pass

def download_and_unpack(url):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    filename = os.path.basename(url)
    distpath = os.path.join(rtm_temp, filename)

    # try to download
    download(url, distpath)

    if filename.endswith(".zip"):
        unpack_zip(filepath)

    pass

def download(url, dist):
    if not os.path.isfile(dist):
        urllib.urlretrieve(url, dist)
    pass

def download_and_install(url):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    filename = os.path.basename(url)
    distpath = os.path.join(rtm_temp, filename)

    # try to download
    download(url, distpath)

    if filename.endswith(".zip"):
        unpack_zip(filepath)

    if filename.endswith(".dmg"):
        install_dmg(distpath)
        
    pass


def install_dmg(dmg):
    cmd = ['hdiutil', 'mount', dmg]
    ret = subprocess.check_output(cmd)
    mountedVolume = [x.strip() for x in ret.split('\t') if x.startswith("/Volumes/")]
    if len(mountedVolume) != 1:
        print 'Error mounting %s' % dmg
    pkgfiles = [x for x in os.listdir(mountedVolume[0]) if x.endswith('.pkg')]
    print pkgfiles
    cmd = ['sudo', 'apachectl', 'installer', '-package', pkgfiles[0], '-target', '/Volumes/Macintosh HD']
    try:
        ret = subprocess.check_output(cmd)
        print 'Installing %s is successful. Message is below' % dmg
        print ret

    except:
        print 'Installing %s is failed. Maybe this process must have done by super user.' % dmg

