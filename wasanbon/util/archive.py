import os, sys
if sys.platform == 'linux2' or sys.platform == 'darwin':
    import pwd, grp
import zipfile
import subprocess

def unpack_tgz(filepath, distpath, force=False):
    old_dir = os.getcwd()
    dir, file = os.path.split(filepath)
    os.chdir(dir)
    cmd = ['tar', 'zxfv', filepath, '-C', distpath]
    res = subprocess.call(cmd)
    #cmd = ['chown', '-R',  pwd.getpwuid(os.getuid())[0] + ':' +  grp.getgrgid(os.getgid())[0], distpath]
    #print cmd
    #subprocess.call(cmd)
    os.chdir(old_dir)
    pass

def unpack_zip(filepath, distpath, force=False):
    path, file = os.path.split(filepath)

    if sys.platform == 'linux2' or sys.platform == 'darwin':
        home_stat = os.stat(os.environ['HOME'])
        uid = home_stat.st_uid
        gid = home_stat.st_gid

    if not os.path.isdir(distpath):
        os.mkdir(distpath)
        if sys.platform == 'linux2' or sys.platform == 'darwin':
            os.chown(distpath, uid, gid)

    sys.stdout.write('Unpacking %s\n'% filepath)
    zf = zipfile.ZipFile(filepath)
    for filepath in zf.namelist():
        sys.stdout.write(" - %s\n" % filepath)
        fullpath = os.path.join(distpath, filepath)
        path, filename = os.path.split(fullpath)
        if not os.path.isdir(path) and len(path) > 0:
            os.makedirs(path)
            if sys.platform == 'linux2' or sys.platform == 'darwin':
                os.chown(path, uid, gid)

        if not os.path.isfile(fullpath) and len(filename) > 0:
            fout = open(fullpath, 'wb')
            fout.write(zf.read(filepath))
            fout.close()

            if sys.platform == 'linux2' or sys.platform == 'darwin':
                os.chown(fullpath, uid, gid)

    zf.close()
    pass

