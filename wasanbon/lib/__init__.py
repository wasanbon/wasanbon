import os, sys, shutil, time, subprocess
import wasanbon
#from rtcconf import *
from repository import *
#from rtc_object import *
import github
#import wasanbon.util.github_ref

def get_repositories(verbose=False):
    repos = []
    for name, value in wasanbon.setting()[wasanbon.platform()]['libraries'].items():
        if 'git' in value.keys():
            protocol = 'git'
        elif 'hg' in value.keys():
            protocol = 'hg'
        elif 'dmg' in value.keys():
            protocol = 'dmg'
        repos.append(LibRepository(name=name, url=value[protocol], desc=value['description'], hash="", protocol=protocol))
    return repos

def get_repository(name, verbose=False):
    repos = get_repositories(verbose=verbose)
    for repo in repos:
        if repo.name == name:
            return repo

    return None
