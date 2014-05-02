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
    git.git_command(['remote', 'add', 'origin', 'https://github.com/' + user + '/' + rtc_.name + '.git'], verbose=verbose, path=rtc_.path, interactive=True)
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

def print_rtcprofile(rtcp):
    sys.stdout.write('basicInfo : \n')
    sys.stdout.write('  name        : ' + rtcp.basicInfo.name + '\n')
    sys.stdout.write('  description : ' + rtcp.basicInfo.description + '\n')
    sys.stdout.write('  category    : ' + rtcp.basicInfo.category + '\n')
    sys.stdout.write('  version     : ' + rtcp.basicInfo.version + '\n')
    sys.stdout.write('Language : \n')
    sys.stdout.write('  kind : ' + rtcp.language.kind + '\n')
    filename = rtcp.getRTCProfileFileName()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    #sys.stdout.write('RTC.xml    : ' + filename + '\n')
    if len(rtcp.dataports) > 0:
        sys.stdout.write('DataPort:\n')
        for dp in rtcp.dataports:
            sys.stdout.write('  ' +dp.name + ':\n')
            sys.stdout.write('    type     : "' +dp.type + '"\n')
            sys.stdout.write('    portType : "' +dp.portType + '"\n')
    if len(rtcp.serviceports) > 0:
        sys.stdout.write('ServicePort:\n')
        for sp in rtcp.serviceports:
            sys.stdout.write('  ' +sp.name + ':\n')
            sys.stdout.write('    Interface :\n')
            for si in sp.serviceInterfaces:
                sys.stdout.write('      ' +si.name + ':\n')
                sys.stdout.write('        type      : "' +si.type + '"\n')
                sys.stdout.write('        direction : ' +si.direction + '\n')
    if len(rtcp.configurationSets) > 0:
        sys.stdout.write('ConfigurationSet:\n')
        for cs in rtcp.configurationSets:
            for c in cs.configurations:
                sys.stdout.write('  ' + c.name + ':\n')
                sys.stdout.write('    type         : ' + c.type + '\n')
                sys.stdout.write('    defaultValue : ' + c.defaultValue + '\n')


    from wasanbon.core.rtc import rtcprofile
    rtcprofile.save_rtcprofile(rtcp, "test.xml")
