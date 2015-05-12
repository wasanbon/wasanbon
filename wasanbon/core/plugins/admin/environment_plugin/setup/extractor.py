import os, sys, subprocess

def extract_tar(filename, verbose=False, distpath=None):
    if verbose: sys.stdout.write('# Extracting %s\n' % filename)
    cur_dir = os.getcwd()
    os.chdir(os.path.dirname(filename))
    if filename.endswith('.tar.gz'):
        dirname = filename[:-7]
    elif filename.endswith('.tgz'):
        dirname = filename[:-4]
    else:
        return (-1, "")

    cmd = ['tar', 'zxf', filename]
    if distpath:
        sys.stdout.write('## distpath=%s\n' % distpath)
        cmd = cmd + ['-C', distpath]
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen(cmd, stdout=out, stdin=out)
    ret = p.wait()
    os.chdir(cur_dir)
    return (ret, dirname)
