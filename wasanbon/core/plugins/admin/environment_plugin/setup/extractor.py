import os, sys, subprocess

def extract_tar(filename, verbose=False):
    if verbose: sys.stdout.write('# Extracting %s\n' % filename)
    cur_dir = os.getcwd()
    os.chdir(os.path.dirname(filename))
    if filename.endswith('.tar.gz'):
        dirname = filename[:-7]
    elif filename.endswith('.tgz'):
        dirname = filename[:-4]
    else:
        return (-1, "")

    cmd = ['tar', 'zxfv', filename]
    out = None if verbose else subprocess.PIPE
    p = subprocess.Popen(cmd, stdout=out, stdin=out)
    ret = p.wait()
    os.chdir(cur_dir)
    return (ret, dirname)
