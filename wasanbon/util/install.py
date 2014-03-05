import os, sys, traceback
import subprocess


def install(file, open_only=False, verbose=False):
    if verbose:
        sys.stdout.write(' - Installing %s\n' % file)

    if file.endswith(".dmg"):
        return install_dmg(file, open_only=open_only, verbose=verbose)
    elif file.endswith(".app"):
        return install_app(file, verbose=verbose)
    elif file.endswith(".egg"):
        cmd = ['sh', file]
    elif file.endswith(".pkg"):
        cmd = ['installer', '-package', file, '-target', '/Volumes/Macintosh HD']
    elif file.endswith(".mpkg"):
        cmd = ['installer', '-pkg', file, '-target', '/']
    elif file.endswith(".msi"):
        cmd = ['msiexec', '/i', file]
    elif file.endswith(".exe"):
        cmd = [file]
    else:
        #if verbose:
        #    sys.stdout.write(' @ Unsuppoted file type: %s\n' % file)
        return

    if verbose:
        sys.stdout.write(' - Executing %s\n' % str(cmd))

    try:
        if sys.platform == 'win32':
            ret = subprocess.Popen(cmd, creationflags=512, env=os.environ)
            ret.wait()
            
        else:
            ret = subprocess.check_output(cmd)
        if verbose:
            sys.stdout.write('Installing %s is successful.\n' % file)
        return True
        #sys.stdout.write(ret)
    except:
        if verbose:
            traceback.print_exc()
            sys.stdout.write('Installing %s is failed. Maybe this process must have done by super user.\n' % file)
        return False


def install_dmg(dmg, open_only=False, verbose=False):
    if verbose:
        sys.stdout.write(' - Installing DMG file : %s\n' % dmg)

    cmd = ['hdiutil', 'mount', dmg]
    if verbose:
        sys.stdout.write(' - Executing %s\n' % str(cmd))
    ret = subprocess.check_output(cmd)

    mountedVolume = [x.strip() for x in ret.split('\t') if x.startswith("/Volumes/")]
    if verbose:
        sys.stdout.write(' - Mounted Volume is %s\n' % str(mountedVolume))

    if len(mountedVolume) != 1:
        if verbose:
            sys.stdout.write(' @ Error mounting %s\n' % dmg)
        return False

    if open_only:
        cur=os.getcwd()
        os.chdir(mountedVolume[0])
        subprocess.call(['open', '.'])
        os.chdir(cur)
        return False

    for root, dirs, files in os.walk(mountedVolume[0]):

        if not all([not d.startswith('.') for d in os.path.split(root)]):
            continue

        for dir in dirs:
            if verbose:
                sys.stdout.write(' - Parsing Directory %s\n' % os.path.join(root, dir), verbose=verbose)
            install(os.path.join(root, dir)) # .pkg and .app is directory but installable.
        for file in files:
            if verbose:
                sys.stdout.write(' - Parsing File %s\n' % os.path.join(root, file), verbose=verbose)

            install(os.path.join(root, file))
    cmd = ['hdiutil', 'unmount', mountedVolume[0]]
    if verbose:
        sys.stdout.write(' - Executing %s\n' % str(cmd))
    ret = subprocess.check_output(cmd)
    return True

def install_app(app, verbose=False):
    if app.endswith('/'):
        app = app[len(app)-1:]

    cmd = ['cp', '-R', app, '/Applications/']
    if verbose:
        sys.stdout.write(' - Executing %s\n' % str(cmd))

    try:
        ret = subprocess.check_output(cmd)
        if verbose:
            sys.stdout.write(' - Installing %s is successful. Message is below\n' % app)
        return True
    except:
        if verobse:
            sys.stdout.write(' @ Error. Installing %s is failed. Maybe this process must have done by super user.\n' % app)
        return False

