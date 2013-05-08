
import os, sys
import wasanbon
from wasanbon import util
from search_rtc import *
from build_rtc import *
from packageprofile import *
from rtcprofile import *
import github

def parse_rtcs():
    rtc_dir = os.path.join(os.getcwd(), 
                           wasanbon.setting['application']['RTC_DIR'])
    rtcprofiles = util.search_file(rtc_dir, 'RTC.xml')
    rtcps = []
    for fullpath in rtcprofiles:
        try:
            rtcp = RTCProfile(fullpath)
            rtcps.append(rtcp)
        except Exception, e:
            print str(e)
            print '-Error Invalid RTCProfile file[%s]' % fullpath
    return rtcps

def github_init(user, passwd, rtcp):
    rtc_dir = os.path.split(rtcp.getRTCProfileFileName())[0]
    if rtc_dir.endswith('/'): 
        rtc_dir = rtc_dir[:-1]
    repo_name = os.path.basename(rtc_dir)

    github_obj = github.Github(user, passwd)
    github_obj.get_user().create_repo(repo_name)

    rtc_dir = os.path.split(rtcp.getRTCProfileFileName())[0]
    sys.stdout.write("Connect to GITHUB repository of %s\n" % repo_name)
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    cmd = [wasanbon.setting['local']['git'], 'remote', 'add', 'origin', 'git@github.com:' + user + '/' + repo_name + '.git']
    subprocess.call(cmd)
    cmd = [wasanbon.setting['local']['git'], 'push', '-u', 'origin', 'master']
    subprocess.call(cmd)
    os.chdir(current_dir)

