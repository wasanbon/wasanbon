import os, sys, shutil, time, subprocess
import wasanbon
from rtcconf import *
from repository import *
from rtc_object import *
import github
import wasanbon.util.github

def get_repositories(verbose=False):
    repos = []
    for name, value in wasanbon.repositories.items():
        if 'git' in value.keys():
            protocol = 'git'
        elif 'hg' in value.keys():
            protocol = 'hg'
        repos.append(RtcRepository(name=name, url=value[protocol], desc=value['description'], hash="", protocol=protocol))
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
    
    github_obj = wasanbon.util.github(user, passwd)
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

