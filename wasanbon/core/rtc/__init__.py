import os, sys, shutil, time, subprocess
import wasanbon
from rtcconf import *
from repository import *
from rtc_object import *
from wasanbon.core import repositories


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
    """
    Add upsatream
    """
    from wasanbon.core.repositories import github_api
    github_obj = github_api.GithubReference(user, passwd)
    repo = github_obj.create_repo(rtc_.name)
    git.git_command(['remote', 'add', 'origin', 'git@github.com:' + user + '/' + rtc_.name + '.git'], verbose=verbose, path=rtc_.path, interactive=True)
    git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose, path=rtc_.path, interactive=True)
    return rtc_

def bitbucket_init(user, passwd, rtc_, verbose=False):
    """
    """
    from wasanbon.core.repositories import bitbucket_api
    bb_obj = bitbucket_api.BitbucketReference(user, passwd)
    repo = bb_obj.create_repo(rtc_.name)
    git.git_command(['remote', 'add', 'origin', 'https://bitbucket.org/' + user + '/' + rtc_.name + '.git'], verbose=verbose, path=rtc_.path, interactive=True)
    git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose, path=rtc_.path, interactive=True)
    return rtc_
