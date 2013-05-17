import os, sys
import zipfile
import subprocess

def unpack_tgz(filepath, distpath, force=False):
    old_dir = os.getcwd()
    dir, file = os.path.split(filepath)
    os.chdir(dir)
    cmd = ['tar', 'zxfv', filepath, '-C', distpath]
    subprocess.call(cmd)
    os.chdir(old_dir)
    pass

def unpack_zip(filepath, distpath, force=False):
    path, file = os.path.split(filepath)
    if not os.path.isdir(distpath):
        os.mkdir(distpath)
    sys.stdout.write('Unpacking %s\n'% filepath)
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
    pass

