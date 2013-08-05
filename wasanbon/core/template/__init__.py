import os, sys, yaml, shutil, subprocess, stat, time
import github
import wasanbon



def command(commands, verbose = False):
    gitenv = os.environ.copy()
    if not 'HOME' in gitenv.keys():
        gitenv['HOME'] = wasanbon.get_home_path()
        print 'Environmental Value HOME (%s) is added.' % gitenv['HOME']

    if verbose:
        sys.stdout.write(" - GIT command %s in repository\n" % (repr(commands)))

    cmd = [wasanbon.setting['local']['git']] + commands
    stdout = None if verbose else subprocess.PIPE

    if verbose:
        sys.stdout.write(' - COMMAND:')
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')

    subprocess.call(cmd, env=gitenv, stdout=stdout)

def clone_project(prjname, url, verbose):
    projs = get_projects(verbose)
    if projs:
        if prjname in projs.keys():
            if verbose:
                print ' - There is %s project in workspace.yaml\n' % prjname
                print ' - Please unregister the project\n' 
            return False

    appdir = os.path.join(os.getcwd(), prjname)
    if os.path.isdir(appdir) or os.path.isfile(appdir):
        if verbose:
            print ' - There seems to be %s here. Please change application name.' % psjname
        return False

    command(['clone', url, appdir], verbose)
    curdir = os.getcwd()
    os.chdir(appdir)

    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    if verbose:
        sys.stdout.write(" - copying from %s to %s\n" % (tempdir, appdir))
        
    for root, dirs, files in os.walk(tempdir):
        distdir = os.path.join(appdir, root[len(tempdir)+1:])
        print distdir
        if not os.path.isdir(distdir):
            os.mkdir(distdir)
        for file in files:
            if not os.path.isfile(os.path.join(distdir, file)):
                if verbose:
                    sys.stdout.write("    - file: %s\n" % file)
                fin = open(os.path.join(root, file), "r")
                fout = open(os.path.join(distdir, file), "w")
                for line in fin:
                    index = line.find('$APP')
                    if index >= 0:
                        line = line[:index] + prjname + line[index + len('$APP'):]
                    fout.write(line)
            fin.close()
            fout.close()
 
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        cmd = ['chmod', '755', ('mgr.py')]
        subprocess.call(cmd)

    register_project(prjname, appdir, verbose=verbose)    
    os.chdir(curdir)
    pass

def fork_project(prjname, user, passwd, url, verbose):
    projs = get_projects(verbose)
    if projs:
        if prjname in projs.keys():
            if verbose:
                print ' - There is %s project in workspace.yaml\n' % prjname
                print ' - Please unregister the project\n' 
            return False

    appdir = os.path.join(os.getcwd(), prjname)
    if os.path.isdir(appdir) or os.path.isfile(appdir):
        if verbose:
            print ' - There seems to be %s here. Please change application name.' % psjname
        return False

    sys.stdout.write(' - Forking URL:: %s\n' % url)
    github_obj = github.Github(user, passwd)
    git_user = github_obj.get_user()
    try:
        git_user.login
    except:
        print ' - Login Error.'
        return None

    target_user, target_repo = url.split('/')[-2:]
    try:
        my_repo = github_obj.get_user().get_repo(target_repo[:-4])
        print ' - Your repository already has the %s repository' % target_repo[:-4]
        print ' - This will be cloned into your space.'
        return 'git@github.com:' + user + '/' + target_repo
    except:
        print ' - Your repository does not have the %s repository' % target_repo[:-4]

        
    repo = github_obj.get_user(target_user).get_repo(target_repo[:-4])

    print ' - Now creating fork of the %s repository' % target_repo[:-4]
    github_obj.get_user().create_fork(repo)
    sys.stdout.write(' - Please wait for 5 seconds to fork...\n')
    time.sleep(5)
    for i in range(0, 5):
        try:
            r = github_obj.get_user().get_repo(target_repo[:-4])
            sys.stdout.write(' - Success\n')
            my_url = 'git@github.com:' + user + '/' + target_repo
            return my_url
        except:
            sys.stdout.write(' - Please wait for 1 more seconds to fork...\n')
            time.sleep(1)
            pass
    sys.stdout.write(' - Failed to create fork.\n')
    return None









