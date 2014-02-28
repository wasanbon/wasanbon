#!/usr/bin/env python

import os, sys, optparse, yaml, types
import wasanbon
from wasanbon.core import package as pack
from wasanbon.core import rtc, tools, repositories
from wasanbon.util import editor
from wasanbon import util


def alternative():
    return ['repository', 'git_init', 'github_init', 'github_fork',
            'github_pullrequest', 'clone',
            'configure', 'release']

def get_rtc_rtno( _package, name, verbose=False):
    try:
        return _package.rtc(name)
    except wasanbon.RTCNotFoundException, e:
        return tools.get_rtno_package(_package, name, verbose=verbose)

def execute_with_argv(args, verbose, force=False, clean=False):
    if True:
        usages  = wasanbon.get_help_text(['help', 'command', 'description', 'rtc'])
        usage = "mgr.py rtc [subcommand] ...\n\n"
        for line in usages:
            usage = usage + line + '\n'

        parser = optparse.OptionParser(usage=usage, add_help_option=False)
        parser.add_option('-l', '--long', help=wasanbon.get_help_text(['help', 'longformat']), action='store_true', default=False, dest='long_flag')
        try:
            options, argv = parser.parse_args(args[:])
        except:
            return


        wasanbon.arg_check(argv, 3)
        _package = pack.Package(os.getcwd())

        if argv[2] == 'list':
            sys.stdout.write(' @ Listing RTCs in current package\n')
            for rtc in _package.rtcs:
                print_rtc(rtc, long=options.long_flag)

            for rtno in tools.get_rtno_packages(_package, verbose=verbose):
                print_rtno(rtno, long=options.long_flag)

        elif argv[2] == 'repository':
            sys.stdout.write(' @ Listing RTC Repository\n')
            for repo in wasanbon.core.rtc.get_repositories(verbose):
                print_repository(repo, long=options.long_flag)

        elif argv[2] == 'git_init':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Initializing RTC %s as GIT repository\n' % argv[3])
            rtc_ = get_rtc_rtno(_package, argv[3], verbose=verbose)
            rtc_.git_init(verbose=verbose)

        elif argv[2] == 'github_init':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Initializing github.com repository in %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            rtc_ = get_rtc_rtno(_package, argv[3], verbose=verbose)
            rtc_.github_init(user, passwd, verbose=verbose)
            sys.stdout.write(' @ Updating repository infomation\n')
            _package.append_rtc_repository(rtc_.repository)

        elif argv[2] == 'github_fork':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Forking GITHUB repository in %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            original_repo = wasanbon.core.rtc.get_repository(argv[3])
            repo = original_repo.fork(user, passwd, verbose=verbose, path=_package.rtc_path)
            sys.stdout.write(' @ Cloning GITHUB repository in %s\n' % argv[3])            
            rtc_ = repo.clone(verbose=verbose, path=_package.rtc_path)
            _package.update_rtc_repository(repo, verbose=verbose)

        elif argv[2] == 'github_pullrequest':
            wasanbon.arg_check(argv, 6)
            sys.stdout.write(' @ Sending Pullrequest.\n')
            user, passwd = wasanbon.user_pass()
            rtc_ = _package.rtc(argv[3])
            rtc_.github_pullrequest(user, passwd, argv[4], argv[5], verbose=verbose)
            
        elif argv[2] == 'clone':
            wasanbon.arg_check(argv, 4)

            # if argument is url, then, clone by git command
            if argv[3].startswith('git@') or argv[3].startswith('http'):
                url = argv[3]
                name = os.path.basename(url)
                if name.endswith('.git'):
                    name = name[:-4]
                sys.stdout.write(' @ Cloning RTC %s\n' % argv[3])
                try:
                    rtc_ = wasanbon.core.rtc.RtcRepository(name=name, url=url, desc="").clone(verbose=verbose, path=_package.rtc_path)
                except wasanbon.RTCProfileNotFoundException, e:
                    rtc_ = get_rtc_rtno(_package, name, verbose=verbose)
                    
                _package.update_rtc_repository(rtc_.repository, verbose=verbose)
                return
                
            #for i in range(3, len(argv)):
            for name in argv[3:]:
                sys.stdout.write(' @ Cloning RTC %s\n' % name)
                try:
                    rtc_ = wasanbon.core.rtc.get_repository(name).clone(verbose=verbose, path=_package.rtc_path)
                except wasanbon.RTCProfileNotFoundException, e:
                    rtc_ = get_rtc_rtno(_package, name, verbose=verbose)

                _package.update_rtc_repository(rtc_.repository, verbose=verbose)

        elif argv[2] == 'delete':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Deleting RTC %s\n' % argv[3])
            for rtcname in argv[3:]:
                _package.delete_rtc(_package.rtc(rtcname), verbose=verbose)
            
        elif argv[2] == 'checkout':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Checkout and overwrite  RTC %s\n' % argv[3])
            get_rtc_rtno(_package, argv[3], verbose=verbose).checkout(verbose=verbose)

        elif argv[2] == 'clean':
            sys.stdout.write('now build option is duplicated\n')
            raise wasanbon.InvalidUsageException()
            
        elif argv[2] == 'build':
            sys.stdout.write('now build option is duplicated\n')
            raise wasanbon.InvalidUsageException()

        elif argv[2] == 'edit':
            sys.stdout.write(' This funciton is currently deplicated.')
            raise wasanbon.InvalidUsageException()

        elif argv[2] == 'configure':
            wasanbon.arg_check(argv, 4)
            rtc_name = argv[3]
            targets = []
            for i in range(0, 16):
                if rtc_name.endswith(str(i)):
                    target_file = os.path.join(_package.conf_path, rtc_name + '.conf')
                    targets.append(target_file)
                    
            if len(targets) == 0: # all files
                for i in range(0, 16):
                    target_file = os.path.join(_package.conf_path, rtc_name + str(i) + '.conf')
                    if os.path.isfile(target_file):
                        targets.append(target_file)

            for target in targets:
                sys.stdout.write(' @ Configuring %s\n' % os.path.basename(target))
                rtcc = wasanbon.core.rtc.RTCConf(target)
                
                choice1 = ['add'] + [key + ':' + rtcc[key] for key in rtcc.keys()]
                msg = ' @ Choice configuration'
                def callback1(ans1):
                    if ans1 == 0: # add
                        sys.stdout.write(' -- Input keyname (ex., conf.default.param1) : ')
                        key = raw_input()
                    else:
                        key = rtcc.keys()[ans1-1]

                    sys.stdout.write(' -- Input value of %s (ex., 1) : ' % key)
                    val = raw_input()
                    msg = ' - Update Configuration (%s:%s)?' % (key, val)
                    if util.yes_no(msg) == 'yes':
                        sys.stdout.write(' - Configuring (key=%s, value=%s).\n' % (key, val))
                        rtcc[key] = val
                        choice1 = ['add'] + [key + ':' + rtcc[key] for key in rtcc.keys()]
                        return [False, choice1]
                    else:
                        sys.stdout.write(' - Aborted.\n')
                        return False

                util.choice(choice1, callback1, msg)
                rtcc.sync(verbose=verbose)
                # del(rtcc)
                print target
                rtcc = wasanbon.core.rtc.RTCConf(target)
                for key in rtcc.keys():
                    print ' -- %s:%s' % (key, rtcc[key])

        elif argv[2] == 'release':
            wasanbon.arg_check(argv,4)
            rtc_ = get_rtc_rtno(_package, argv[3], verbose=verbose)
            name = rtc_.name
            url = rtc_.repository.url
            repo_type = 'git'
            description = raw_input(" - Input explanation of your RTC :")
            sys.stdout.write(' - Your current platform is %s.\n' % wasanbon.platform)
            platform_str = raw_input(" - Input your RTC's platform:")
            platform = yaml.safe_load(platform_str)
            if not type(platform) is types.ListType:
                platform = [platform]

            sys.stdout.write(' - Checking out the RTC repository %s\n' % name)

            paths = repositories.parse_rtc_repo_dir()
            for path in paths:
                owner_name = os.path.basename(os.path.dirname(path))
                if owner_name.endswith(repositories.owner_sign):
                    file_list = [f for f in os.listdir(os.path.join(path, 'rtcs')) if f.endswith('.yaml')]
                    file_list.append('Create New Repository File:')
                    def function01(num):
                        if num == len(file_list)-2:
                            while True:
                                sys.stdout.write(' @ Input Filename:')
                                filename = raw_input()
                                if not filename.endswith('.yaml'):
                                    sys.stdout.write(' @@ Filename must be ended with .yaml\n')
                                    continue
                                break
                            file = os.path.join(path, 'rtcs', filename)
                            open(file, 'w').close()
                            git.git_command(['add', filename], path=os.path.join(path, 'rtcs'), verbose=verbose)
                        else:
                            file = os.path.join(path, 'rtcs', file_list[num])
                        y = yaml.safe_load(open(file, 'r'))
                        if name in y.keys():
                            sys.stdout.write(' @ Error. RTC(%s) is already released.\n' % name)
                            return True
                        f = open(file, 'a')
                        f.write('\n%s :\n' % name)
                        f.write('  type : %s\n' % repo_type)
                        f.write('  url  : %s\n' % url)
                        f.write('  description : %s\n' % description)
                        f.write('  platform : %s\n' % platform)
                        f.close()
                        sys.stdout.write(' - Updated.\n')
                        sys.stdout.write(' - If you want to confirm the update, use "wasanbon-admin.py repository status"\n')
                        return True
                    util.choice(file_list, function01, ' - Select RTC repository file')
            
            

        else:
            raise wasanbon.InvalidUsageException()

def print_rtno(rtno, long=False):
    str = ' - ' + rtno.name
    if long:
        str = str + ':\n'
        str = str + '    - name       : ' + rtno.name + '\n'
        str = str + '    - language   : ' + 'arduino' + '\n'
        filename = rtno.file
        if filename.startswith(os.getcwd()):
            filename = filename[len(os.getcwd()) + 1:]
            str = str + '    - file       : ' + filename
    str = str + '\n'
    sys.stdout.write(str)

def print_rtc_profile(rtcp, long=False):
    str = ' - ' + rtcp.basicInfo.name

    if long:
        str = str + ':\n'
        str = str + '    - name       : ' + rtcp.basicInfo.name + '\n'
        str = str + '    - language   : ' + rtcp.getLanguage() + '\n'
        str = str + '    - category   : ' + rtcp.getCategory() + '\n'
        filename = rtcp.getRTCProfileFileName()
        if filename.startswith(os.getcwd()):
            filename = filename[len(os.getcwd()) + 1:]
        str = str + '    - RTC.xml    : ' + filename 
    str = str + '\n'
    sys.stdout.write(str)

def print_package_profile(pp, long=False):
    if not long:
        return
    filename = pp.getConfFilePath()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = '    - config     : ' + filename + '\n'
    sys.stdout.write(str)

    filename = pp.getRTCFilePath()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = '    - binary     : ' + filename + '\n'
    sys.stdout.write(str)

    filename = pp.getRTCExecutableFilePath()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = '    - executable : ' + filename + '\n'
    sys.stdout.write(str)


def print_rtc(rtc, long=False):
    print_rtc_profile(rtc.rtcprofile, long=long)
    print_package_profile(rtc.packageprofile, long=long)
    pass



def print_repository(repo, long=False):
    sys.stdout.write(' - %s\n' % repo.name)
    if long:
        sys.stdout.write('    description : %s\n' % repo.description)
        sys.stdout.write('    protocol    : %s\n' % repo.protocol)
        sys.stdout.write('    url         : %s\n' % repo.url)
    pass
