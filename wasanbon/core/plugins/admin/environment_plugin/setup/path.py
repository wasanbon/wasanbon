import os
import sys


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
        except ImportError as e:
            return ""

    if sys.platform == 'win32':
        path_splitter = ';'
        if not cmd.endswith(cmd):
            cmd = cmd + '.exe'
    elif sys.platform == 'darwin':
        path_splitter = ':'
    elif sys.platform == 'linux':
        path_splitter = ':'
    else:
        return ""

    if sys.platform == 'darwin' and (cmd == 'java' or cmd == 'javac'):
        return check_java_path_in_darwin(cmd, verbose=verbose)

    if verbose:
        sys.stdout.write('## Searching %s ... ' % (cmd))
    if not path is None:
        if path.endswith(cmd) and os.path.isfile(path):
            if verbose:
                sys.stdout.write(' Found in %s\n' % path)
            return path

    paths = [os.path.join(p, cmd) for p in os.environ['PATH'].split(path_splitter)
             if os.path.isfile(os.path.join(p, cmd))]
    if len(paths) == 0:
        paths = [hint for hint in hints if os.path.isfile(os.path.expandvars(hint))]
        if len(paths) == 0:
            if verbose:
                sys.stdout.write(' Not found.\n')
            return ""

    if verbose:
        sys.stdout.write('  Found in %s. \n' % paths[0])
    return os.path.expandvars(paths[0])


def check_java_path_in_darwin(cmd, verbose=False):
    if verbose:
        sys.stdout.write('## Searching %s ... ' % (cmd))
    import subprocess

    p = subprocess.Popen([cmd, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret = p.wait()
    stdout_data, stderr_data = p.communicate()
    if str(stderr_data).startswith(' No Java runtime present'):
        if verbose:
            sys.stdout.write(' No Java runtime present\n')
        return ""
    else:
        if verbose:
            sys.stdout.write(' Java runtime found.\n')

        return "/usr/bin/" + cmd
