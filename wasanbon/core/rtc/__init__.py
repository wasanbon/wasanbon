import os, sys, shutil, time, subprocess, shutil
import wasanbon
from rtcconf import *
from repository import *
from rtc_object import *
from wasanbon.core import repositories


def get_repositories(verbose=False, all_platform=False):
    rtcs, packs = repositories.load_repositories(verbose=verbose, all_platform=all_platform)
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
    if verbose: sys.stdout.write(' - Initializing github.com repository.\n')
    github_obj = github_api.GithubReference(user, passwd)
    repo = github_obj.create_repo(rtc_.name)
    git.git_command(['remote', 'add', 'origin', 'https://github.com/' + user + '/' + rtc_.name + '.git'], verbose=verbose, path=rtc_.path, interactive=True)
    
    #git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose, path=rtc_.path, interactive=True)
    rtc_.push(verbose=verbose, username=user, password=passwd)
    return rtc_


def github_delete(user, passwd, rtc_, verbose=False):
    from wasanbon.core.repositories import github_api
    if verbose: sys.stdout.write(' - Removing github.com repository.\n')
    github_obj = github_api.GithubReference(user, passwd)
    try:
        repo = github_obj.delete_repo(rtc_.name)
    except:
        sys.stdout.write(' @ Failed to remove remote repository.\n')
        sys.stdout.write(' @ Proceed to remove local config of origin.\n')
        pass
    git.git_command(['remote', 'del', 'origin', 'https://github.com/' + user + '/' + rtc_.name + '.git'], verbose=verbose, path=rtc_.path, interactive=True)
    #rtc_.push(verbose=verbose, username=user, password=passwd)
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
    if rtcp.configurationSet:
        sys.stdout.write('ConfigurationSet:\n')
        cs = rtcp.configurationSet
        for c in cs.configurations:
            sys.stdout.write('  ' + c.name + ':\n')
            sys.stdout.write('    type         : ' + c.type + '\n')
            sys.stdout.write('    defaultValue : ' + c.defaultValue + '\n')


    from wasanbon.core.rtc import rtcprofile
    rtcprofile.save_rtcprofile(rtcp, "test.xml")


def verify_rtcprofile(rtc, verbose=False):
    rtcp = rtc.rtcprofile
    rtcp_real = create_rtcprofile(rtc, verbose=verbose)
    rtcp_new = compare_rtcprofile(rtcp, rtcp_real, verbose=verbose)
    print_rtcprofile(rtcp_new)

def compare_rtcprofile(rtcp, rtcp_real, verbose=False):
    from wasanbon.core.rtc import rtcprofile
    b = rtcprofile.RTCProfileBuilder(rtcp)
    # compare dataports
    if verbose: sys.stdout.write(' - Comparing RTC.xml with Running RTC(%s)\n' % (rtcp.name))
    for dp in rtcp.dataports:
        match_flag = False
        if verbose:
            sys.stdout.write(' Searching DataPort %s : %s... ' % (dp['rtc:name'], dp['rtc:type']))
        for dp_real in rtcp_real.dataports:
            #if verbose:
                #sys.stdout.write(' Testing %s : %s...\n' % (dp_real['rtc:name'], dp_real['rtc:type']))
            if dp.equals(dp_real):
                match_flag = True
                break
        
        if not match_flag: # RTC.xml does not have dp
            if verbose: sys.stdout.write('Not Found in the running RTC\n')
            b.removeDataPort(dp)
        else:
            if verbose: sys.stdout.write('Match.\n')
            
    return b.buildRTCProfile()

def create_rtcprofile(rtc, verbose=False):
    import rtcprofile
    rtcb = rtcprofile.RTCProfileBuilder()
    
    import rtctree.path
    full_path = rtc.get_full_path_in_ns()
    #print full_path
    path, port = rtctree.path.parse_path(full_path) 
    if not path[-1]:
        # There was a trailing slash
        trailing_slash = True
        path = path[:-1]
    filter = []
    tree = rtctree.tree.RTCTree(paths=path, filter=filter)
    comp = tree.get_node(path)    
    if not comp.is_component:
        sys.stdout.write(' Object is not component\n')
        return None
    
    rtcb.setBasicInfo(comp.type_name, comp.category, comp.vendor, comp.version, comp.description)
    rtcb.setLanguage(comp.properties['language'])
    keys = [key for key in comp.properties.keys() if key.startswith('conf.default')]
    for key in keys:
        type = 'string'
        rtcb.appendConfiguration(type, key.split('.')[-1], comp.properties[key])

    for p in comp.ports:
        if p.porttype == 'DataOutPort':
            data_type = p.properties['dataport.data_type'].split(':')[1].replace('/', '::')
            rtcb.appendDataPort('DataOutPort', data_type, p.name)
        elif p.porttype == 'DataInPort':
            data_type = p.properties['dataport.data_type'].split(':')[1].replace('/', '::')
            rtcb.appendDataPort('DataInPort', data_type, p.name)
        elif p.porttype == 'CorbaPort':
            rtcb.appendServicePort(p.name)
            for i in p.interfaces:
                path = ""
                idlFile = ""
                rtcb.appendServiceInterfaceToServicePort(p.name, path, idlFile, i.type_name,
                                                         i.polarity_as_string(),
                                                         i.instance_name)

    return rtcb.buildRTCProfile()


def create_python_rtc(_package, module_name, module_description="Module Description", vendor_name="Vendor Name", category="Category", verbose=False):
    dist_dir = os.path.join(_package.rtc_path, module_name)
    template_dir = os.path.join(wasanbon.__path__[0], 'core', 'rtc', 'template', 'python')
    def copytree(src, dst, copyfunc):
        if not os.path.isdir(dst): os.mkdir(dst)
        for f in os.listdir(src):
            srcfullpath = os.path.join(src, f)
            dstfullpath = os.path.join(dst, f)
            if os.path.isdir(srcfullpath):
                if not os.path.isdir(dstfullpath): os.mkdir(dstfullpath)
                copytree(srcfullpath, dstfullpath, copyfunc)
            else:
                copyfunc(srcfullpath, dstfullpath)

    def copyfunc(src, dst):
        dst = os.path.join(os.path.dirname(dst), os.path.basename(src).replace('ModuleName', module_name))
        fin = open(src, 'r')
        fout = open(dst, 'w')
        for line in fin:
            line = line.replace('$ModuleName', module_name)
            line = line.replace('$ModuleDescription', module_description)
            line = line.replace('$VendorName', vendor_name)
            line = line.replace('$Category', category)
            line = line.replace('$Date', '$Date')
            fout.write(line)

    copytree(template_dir, dist_dir, copyfunc)
    #for root, dirs, files in os.walk(dist_dir):
    #    print 'root:%s' % root
    #    print 'dirs:%s' % dirs
    #    print 'files:%s' % files

    pass
