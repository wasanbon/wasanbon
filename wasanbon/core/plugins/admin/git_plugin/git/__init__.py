
import os, sys, subprocess

plugin_obj = None
def git_command(commands, path='.', verbose = False, pipe=False, interactive=False):
    cur_dir = os.getcwd()
    os.chdir(path)
    gitenv = os.environ.copy()
    import wasanbon
    if not 'HOME' in gitenv.keys():
        gitenv['HOME'] = wasanbon.get_home_path()
        if verbose:
            sys.stdout.write(' - Environmental Variable  HOME (%s) is added.\n' % gitenv['HOME'])

    setting = plugin_obj.admin.environment.path
    if len(setting['git']) == 0:
        sys.stdout.write(' @ GIT COMMAND NOT FOUND.....\n')
        return False

    cmd = [setting['git']] + commands
    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE

    if interactive:
        stdout = None
        stderr = None
    if verbose:
        sys.stdout.write(' - wasanbon.git command = %s' % setting['git'])
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')

    if not pipe:
        #p = subprocess.call(cmd, env=gitenv, stdout=stdout, stderr=stderr)
        p = subprocess.Popen(cmd, env=gitenv, stdout=stdout, stderr=stderr)
        p.wait()
    else:
        p = subprocess.Popen(cmd, env=gitenv, stdout=stdout, stderr=stderr)
    os.chdir(cur_dir)
    return p
