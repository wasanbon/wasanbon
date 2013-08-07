import os, sys
import wasanbon

from repository import *
from rtc_object import *


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

