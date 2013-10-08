import os, sys, shutil, time, subprocess
import wasanbon
from rtcconf import *
from repository import *
from rtc_object import *
from wasanbon.core import repositories
import github
import wasanbon.util.github_ref

def get_repositories(verbose=False):
    rtcs, packs = repositories.load_repositories(verbose=verbose)
    repos = []
    for key, value in rtcs.items():
        try:
            repos.append(RtcRepository(name=key, desc=value['description'], url=value['url'], hash="", protocol=value['type']))
        except KeyError:
            sys.stdout.write(' - Repository %s is invalid.\n' % key)
    return repos

def get_repository(name, verbose=False):
    repos = get_repositories(verbose=verbose)
    for repo in repos:
        if repo.name == name:
            return repo
    return None

def github_init(user, passwd, rtc_, verbose=False):
    curdir = os.getcwd()
    os.chdir(rtc_.path)
    
    github_obj = github_ref.GithubReference(user, passwd)
    repo_name = os.path.split(rtc_.rtcprofile.filename)[0]
    if not github_obj.create_repo(repo_name):
        sys.stdout.write(' - failed.\n')
        os.chdir(curdir)
        return False

    git.git_command(['remote', 'add', 'origin', 'https://github.com/' + user + '/' + repo_name + '.git'], verbose=verbose)
    git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose)

    os.chdir(cur_dir)

    url = 'git@github.com:' + user + '/' + repo_name + '.git'
    return rtc.RtcRepository(rtc_.name, url=url, desc='', hash=rtc_.git.hash)

