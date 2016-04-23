import os, sys, subprocess, traceback


def call_subprocess(cmds, verbose=False, env=None, unrestricted=False):
    out = None if verbose else subprocess.PIPE
    _in = None if verbose else subprocess.PIPE
    if env == None:
        env = os.environ
    if sys.platform == 'win32' and unrestricted:
        cmd_str = ''
        for c in cmds:
            cmd_str = c + ' '
        cmd_str = cmd_str.strip()
        admin_cmd = ['@powershell', '-NoProfile', '-ExecutionPolicy', 'unrestricted', '-Command', cmd_str]
        
        p = subprocess.Popen(admin_cmd, shell=True, stdout=out, stderr=out, env=env)

    else:
        p = subprocess.Popen(cmds, stdout=out, stdin=out, env=env)
    return p.wait()

def install_exe(file, verbose=False, path='downloads'):
    if verbose: sys.stdout.write('# Launching %s\n' % file)
    cmds = [ os.path.join(os.getcwd(), path, file) ]
    return call_subprocess(cmds, verbose, unrestricted=True)

def install_py(file, verbose=False, path='downloads'):
    if verbose: sys.stdout.write('# Launching %s\n' % file)
    cmds = ['python', os.path.join(os.getcwd(), path, file) ]
    return call_subprocess(cmds, verbose)

def install_easy_install(cmd, verbose=False):
    cmds = cmd.split()
    env = os.environ
    if sys.platform == 'darwin':
        env['ARCHFLAGS'] = '-Wno-error=unused-command-line-argument-hard-error-in-future'
    return call_subprocess(cmds, verbose, env)

def install_pip(cmd, verbose=False):
    cmds = cmd.split()
    env = os.environ
    if sys.platform == 'darwin':
        env['ARCHFLAGS'] = '-Wno-error=unused-command-line-argument-hard-error-in-future'
    return call_subprocess(cmds, verbose, env)

def install_apt(cmd, verbose=False):
    cmds = cmd.split()
    return call_subprocess(cmds)

def install_svn(cmd, path, verbose=False, path_svn='svn'):
    url = cmd.split(' ')[1].strip()
    stdout = None if verbose else subprocess.PIPE
    old_dir = os.getcwd()
    os.chdir(path)
    cmd = ['svn', 'co', url]
    ret = subprocess.call(cmd, stdout=stdout)
    if url.endswith('/'):
        url = url[:-1]
    dirname = os.path.basename(url)
    os.chdir(dirname)

    if dirname.startswith('OpenRTM'):
        install_pyrtm(stdout=stdout)
    else:
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file == 'setup.py':
                    install_setup_py(root, verbose=verbose)
                    
    os.chdir(old_dir)

def install_pyrtm(stdout=None):
    cmd = ['python', 'setup.py', 'build_core']
    ret = subprocess.call(cmd, stdout=stdout)
    cmd = ['python', 'setup.py', 'install']
    ret = subprocess.call(cmd, stdout=stdout)
    cmd = ['python', 'setup.py', 'install_example']
    ret = subprocess.call(cmd, stdout=stdout)
    

def install_setup_py(dirname, args=[['install']], verbose=False):
    if verbose: sys.stdout.write('# Installing Python Module in "%s" with distutil.\n' % dirname)
    cwd = os.getcwd()
    os.chdir(dirname)
    out = None if verbose else subprocess.PIPE
    if os.path.isfile('setup.py'):
        for arg in args:
            cmds = ['python', 'setup.py'] + arg
            if sys.platform == 'linux' or sys.platform == 'darwin':
                cmds = ['sudo'] + cmds
            env = os.environ
            if sys.platform == 'darwin':
                env['ARCHFLAGS'] = '-Wno-error=unused-command-line-argument-hard-error-in-future'
            ret = call_subprocess(cmds, verbose, env=env)
            #ret = subprocess.call(cmd, stdout=out, stdin=out, env=env)
    os.chdir(cwd)
    return ret



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
        if verbose: sys.stdout.write('## Unsuppoted file type: %s\n' % file)
        return False

    if verbose: sys.stdout.write(' - Executing %s\n' % str(cmd))

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
                sys.stdout.write(' - Parsing Directory %s\n' % os.path.join(root, dir))
            if install(os.path.join(root, dir), verbose=verbose): # .pkg and .app is directory but installable.
                break
        for file in files:
            if verbose:
                sys.stdout.write(' - Parsing File %s\n' % os.path.join(root, file))
            if install(os.path.join(root, file), verbose=verbose):
                break
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
        if ret != 0:
            sys.stdout.write(' - Installing %s failed. Return value is %d\n' % (app, ret))
            return False
        if verbose:
            sys.stdout.write(' - Installing %s is successful. Message is below\n' % app)
        return True
    except Exception, e:
        sys.stdout.write(' @ Error. Installing %s is failed. Maybe this process must have done by super user.\n' % app)
        if verbose:
            sys.stdout.write(' - Exception:\n')
            sys.stdout.write(str(e))
        
        return False

    return False
