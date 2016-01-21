import os, sys

def search_command(cmd, path, hints, verbose=False):
    if verbose:
        sys.stdout.write('## Searching Command (%s)\n' % cmd)
        for h in hints:
            sys.stdout.write('### Hint: %s\n' % h)
    if cmd.startswith('python_'):
        module_name = cmd[7:]
        try:
            __import__(module_name)
            return sys.modules[module_name].__path__[0]
        except ImportError, e:
            return ""

    if sys.platform == 'win32':
        path_splitter = ';'
        if not cmd.endswith(cmd):
            cmd = cmd + '.exe'
    elif sys.platform == 'darwin':
        path_splitter = ':'        
    elif sys.platform == 'linux2':
        path_splitter = ':'
    else:
        return ""


    if sys.platform == 'darwin' and (cmd == 'java' or cmd == 'javac'):
        return check_java_path_in_darwin(cmd, verbose=verbose)

    if verbose:
        sys.stdout.write('## Searching %s ... ' % (cmd))
    if not path is None:
        if path.endswith(cmd) and os.path.isfile(path):
            if verbose: sys.stdout.write(' Found in %s\n' % path)
            return path

    paths = [os.path.join(p,cmd) for p in os.environ['PATH'].split(path_splitter) \
                 if os.path.isfile(os.path.join(p,cmd))]
    if len(paths) == 0:
        paths = [hint for hint in hints if os.path.isfile(hint)]
        if len(paths) == 0:
            if verbose:
                sys.stdout.write(' Not found.\n')
            return ""

    if verbose: sys.stdout.write('  Found in %s. \n' % paths[0])
    return paths[0]
    

def check_java_path_in_darwin(cmd, verbose=False):
    if verbose: sys.stdout.write('## Searching %s ... ' % (cmd))
    import subprocess

    p = subprocess.Popen([cmd, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret = p.wait()
    if p.stderr.read().startswith(' No Java runtime present'):
        if verbose:
            sys.stdout.write(' No Java runtime present\n')
        return ""
    else:
        if verbose:
            sys.stdout.write(' Java runtime found.\n')

        return "/usr/bin/" + cmd
    

def check_command(cmd_key, cmd_path, verbose=False):
    if verbose: sys.stdout.write('# Checking Command [%s%s] ...' % (cmd_key, " "*(10-len(cmd_key))))
    if verbose: sys.stdout.write('#  Checking Path : %s\n' % cmd_path)
    if os.path.isfile(cmd_path):
        if verbose: sys.stdout.write('installed in %s\n' % cmd_path)
        return True

    if verbose: sys.stdout.write('not installed.\n')
    return False

def install_command(cmd, verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Installing command [%s]\n' % cmd)

    if cmd == 'java':
        return False

    if sys.platform == 'darwin':
        return util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages'][cmd],
                                  verbose=verbose, force=force)
    elif sys.platform == 'win32':
        if cmd == 'emacs':
            return util.download_and_unpack(wasanbon.setting()[wasanbon.platform()]['packages'][cmd],
                                     dist_path=wasanbon.setting()['common']['path']['RTM_HOME'],
                                     verbose=verbose, force=force)
        else:
            return util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages'][cmd], 
                                      verbose=verbose, force=force)
    elif sys.platform == 'linux2':
        return util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages'][cmd],
                                  verbose=verbose, force=force)
    raise wasanbon.UnsupportedPlatformError()


