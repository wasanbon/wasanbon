import os, sys, subprocess, shutil
import wasanbon
from packageprofile import *
from rtcprofile import *


def command(rtcp, commands, verbose = False):
    gitenv = os.environ.copy()
    if not 'HOME' in gitenv.keys():
        gitenv['HOME'] = wasanbon.get_home_path()
        print 'Environmental Value HOME (%s) is added.' % gitenv['HOME']

    rtc_dir = os.path.split(rtcp.getRTCProfileFileName())[0]
    if verbose:
        sys.stdout.write(" - GIT command %s in repository in %s\n" % (repr(commands), rtc_dir))
    #pp = PackageProfile(rtcp)
    current_dir = os.getcwd()
    if verbose:
        sys.stdout.write(' - Changing Current Directory to %s\n' % rtc_dir)
    os.chdir(rtc_dir)
    cmd = [wasanbon.setting['local']['git']] + commands
    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE

    if verbose:
        sys.stdout.write(' - COMMAND:')
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')

    subprocess.call(cmd, env=gitenv, stdout=stdout, stderr=stderr)
    os.chdir(current_dir)

def git_init(rtcp, verbose=False):
    command(rtcp, ['init'], verbose=verbose)


    
def commit(rtcp, comment, verbose = False):
    if verbose:
        print ' - GIT commit changes to my local repository'
    command(rtcp, ['commit', '-a', '-m', comment], verbose=verbose)

def push(rtcp, verbose=False):
    if verbose:
        print ' - GIT push my repository to upstream'
    command(rtcp, ['push'], verbose=True) 
    # In push mode, always should be verbose because password input is needed

def pull(rtcp, verbose=False):
    if verbose:
        print ' - GIT pull upstream repository'
    command(rtcp, ['pull'], verbose=verbose)

def checkout(rtcp, hash="", verbose=False):
    if verbose:
        print ' - GIT checkout and overwrite master branch'
    if len(hash)==0:
        command(rtcp, ['checkout', 'master', '--force'], verbose=verbose)
    else:
        command(rtcp, ['checkout', hash], verbose=verbose)

def clone(url, verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - GIT cloning : %s\n' % url)
    distpath = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], os.path.basename(url))
    if distpath.endswith('.git'):
        distpath = distpath[:-4]

    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE
    gitenv = os.environ.copy()
    if not 'HOME' in gitenv.keys():
        gitenv['HOME'] = wasanbon.get_home_path()
        sys.stdout.write(' - Environment Param HOME (%s) is added.\n' % gitenv['HOME'])

    if os.path.isdir(distpath):
        sys.stdout.write(' - Your Project already has the repository (%s)\n' % distpath)
        if not force:
            if util.yes_no(' - Do you want to change the origin to %s?\n' % url) == 'yes':
                filename = os.path.join(distpath, '.git', 'config')
                tempfilename = filename + ".bak"
                if os.path.isfile(tempfilename):
                    os.remove(tempfilename)
                    pass
                os.rename(filename, tempfilename)
                # os.remove(tempfilename)
                git_config = open(filename, 'w')
                git_config_bak = open(tempfilename, 'r')
                for line in git_config_bak:
                    if line.strip() == '[remote "origin"]':
                        line = '[remote "upstream"]\n'
                        pass
                    git_config.write(line)
                    pass
                git_config.write('[remote "origin"]\n')
                git_config.write('       url = %s\n' % url)
                git_config.write('       fetch = +refs/heads/*:refs/remotes/origin/*\n')
                
                git_config.close()
                git_config_bak.close()
                pass
            for root, dirs, files in os.walk(distpath):
                if 'RTC.xml' in files:
                    return RTCProfile(os.path.join(root, 'RTC.xml'))

        # Already Cloned?
        pass

    cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath]
    if verbose:
        sys.stdout.write(' - COMMAND:')
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')
    subprocess.call(cmd, env=gitenv, stdout=stdout, stderr=stderr)

    curdir = os.getcwd()
    os.chdir(distpath)
    cmd = [wasanbon.setting['local']['git'], 'submodule', 'init']
    if verbose:
        sys.stdout.write(' - COMMAND:')
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')
    subprocess.call(cmd, env=gitenv, stdout=stdout, stderr=stderr)

    cmd = [wasanbon.setting['local']['git'], 'submodule', 'update']
    if verbose:
        sys.stdout.write(' - COMMAND:')
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')
    subprocess.call(cmd, env=gitenv, stdout=stdout, stderr=stderr)
    os.chdir(curdir)
    for root, dirs, files in os.walk(distpath):
        if  'RTC.xml' in files:
            return RTCProfile(os.path.join(root, 'RTC.xml'))

    return None
    
def get_hash(rtcp, verbose=False):
    gitenv = os.environ.copy()
    if not 'HOME' in gitenv.keys():
        gitenv['HOME'] = wasanbon.get_home_path()
        print 'Environmental Value HOME (%s) is added.' % gitenv['HOME']

    rtc_dir = os.path.split(rtcp.getRTCProfileFileName())[0]
    if verbose:
        sys.stdout.write(" - GIT command (git log) in repository in %s\n" % rtc_dir)
    pp = PackageProfile(rtcp)
    current_dir = os.getcwd()
    if verbose:
        sys.stdout.write(' - Changing Current Directory to %s\n' % rtc_dir)
    os.chdir(rtc_dir)
    cmd = [wasanbon.setting['local']['git'], 'log', '--pretty=format:"%H"', '-1']
    stdout = subprocess.PIPE
    if verbose:
        sys.stdout.write(' - COMMAND:')
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')
    p = subprocess.Popen(cmd, env=gitenv, stdout=stdout)
    os.chdir(current_dir)
    
    p.wait()
    
    retval = p.stdout.readline().strip()[1:-1]
    return retval
