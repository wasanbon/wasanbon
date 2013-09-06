#!/usr/bin/env python

import os, sys, optparse
import wasanbon
from wasanbon.core import project as prj
from wasanbon.core import rtc, tools
from wasanbon.util import editor
from wasanbon import util


class Command(object):
    def __init__(self):
        pass

    def get_rtc_rtno(self, proj, name, verbose=False):
        try:
            return proj.rtc(name)
        except wasanbon.RTCNotFoundException, e:
            return tools.get_rtno_project(proj, name, verbose=verbose)

    def execute_with_argv(self, args, verbose, force, clean):
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
        proj = prj.Project(os.getcwd())

        if argv[2] == 'list':
            sys.stdout.write(' @ Listing RTCs in current project\n')
            for rtc in proj.rtcs:
                print_rtc(rtc, long=options.long_flag)

            for rtno in tools.get_rtno_projects(proj, verbose=verbose):
                print_rtno(rtno)

        elif argv[2] == 'repository':
            sys.stdout.write(' @ Listing RTC Repository\n')
            for repo in wasanbon.core.rtc.get_repositories(verbose):
                print_repository(repo, long=options.long_flag)

        elif argv[2] == 'git_init':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Initializing RTC %s as GIT repository\n' % argv[3])
            rtc_ = self.get_rtc_rtno(proj, argv[3], verbose=verbose)
            rtc_.git_init(verbose=verbose)

        elif argv[2] == 'github_init':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Initializing github.com repository in %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            rtc_ = self.get_rtc_rtno(proj, argv[3], verbose=verbose)
            rtc_.github_init(user, passwd, verbose=verbose)
            sys.stdout.write(' @ Updating repository infomation\n')
            proj.append_rtc_repository(rtc_.repository)

        elif argv[2] == 'github_fork':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Forking GITHUB repository in %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            original_repo = wasanbon.core.rtc.get_repository(argv[3])
            repo = original_repo.fork(user, passwd, verbose=verbose, path=proj.rtc_path)
            sys.stdout.write(' @ Cloning GITHUB repository in %s\n' % argv[3])            
            rtc_ = repo.clone(verbose=verbose, path=proj.rtc_path)
            proj.update_rtc_repository(repo, verbose=verbose)

        elif argv[2] == 'github_pullrequest':
            wasanbon.arg_check(argv, 6)
            sys.stdout.write(' @ Sending Pullrequest.\n')
            user, passwd = wasanbon.user_pass()
            rtc_ = proj.rtc(argv[3])
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
                    rtc_ = wasanbon.core.rtc.RtcRepository(name=name, url=url, desc="").clone(verbose=verbose, path=proj.rtc_path)
                except wasanbon.RTCProfileNotFoundException, e:
                    rtc_ = self.get_rtc_rtno(proj, name, verbose=verbose)
                    
                proj.update_rtc_repository(rtc_.repository, verbose=verbose)
                return
                
            #for i in range(3, len(argv)):
            for name in argv[3:]:
                sys.stdout.write(' @ Cloning RTC %s\n' % name)
                try:
                    rtc_ = wasanbon.core.rtc.get_repository(name).clone(verbose=verbose, path=proj.rtc_path)
                except wasanbon.RTCProfileNotFoundException, e:
                    rtc_ = self.get_rtc_rtno(proj, name, verbose=verbose)

                proj.update_rtc_repository(rtc_.repository, verbose=verbose)

        elif argv[2] == 'delete':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Deleting RTC %s\n' % argv[3])
            for rtcname in argv[3:]:
                proj.delete_rtc(proj.rtc(rtcname), verbose=verbose)
            
        elif argv[2] == 'commit':
            wasanbon.arg_check(argv, 5)
            sys.stdout.write(' @ Commiting Changes of RTC %s\n' % argv[3])
            rtc_ = self.get_rtc_rtno(proj, argv[3], verbose=verbose)
            rtc_.commit(comment=argv[4], verbose=verbose)
            proj.update_rtc_repository(rtc_.repository, verbose=verbose)

        elif argv[2] == 'pull':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Pulling the changing upstream RTC repository %s\n' % argv[3])
            rtc_ = self.get_rtc_rtno(proj, argv[3], verbose=verbose)
            rtc_.pull(verbose=verbose)
            proj.update_rtc_repository(rtc_.repository, verbose=verbose)

        elif argv[2] == 'checkout':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Checkout and overwrite  RTC %s\n' % argv[3])
            self.get_rtc_rtno(proj, argv[3], verbose=verbose).checkout(verbose=verbose)

        elif argv[2] == 'push':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Pushing RTC repository  %s to upstream.\n' % argv[3])
            self.get_rtc_rtno(proj, argv[3], verbose=verbose).push(verbose=True) # when pushing always must be verbose 

        elif argv[2] == 'clean':
            wasanbon.arg_check(argv, 4)
            build_all = True if 'all' in argv else False
            for rtc in proj.rtcs:
                if build_all or rtc.name in argv:
                    sys.stdout.write(' @ Cleaning Up RTC %s\n' % rtc.name)
                    rtc.clean(verbose=verbose)

        elif argv[2] == 'build':
            wasanbon.arg_check(argv, 4)
            build_all = True if 'all' in argv else False

            if sys.platform == 'win32':
                verbose=True

            for rtc in proj.rtcs:
                if build_all or rtc.name in argv:
                    sys.stdout.write(' @ Building RTC %s\n' % rtc.name)
                    rtc.build(verbose=verbose)

        elif argv[2] == 'edit':
            wasanbon.arg_check(argv, 4)
            try:
                rtc_ = proj.rtc(argv[3])
                
                if rtc_.is_git_repo():
                    if rtc_.git_branch() != 'master':
                        sys.stdout.write(' @ You are not in master branch.\n')
                        if util.yes_no(' @ Do you want to checkout master first?') == 'yes':
                            rtc_.checkout(verbose=verbose)
                editor.edit_rtc(proj.rtc(argv[3]), verbose=verbose)
            except wasanbon.RTCNotFoundException, ex:
                rtnos = tools.get_rtno_projects(proj)
                for rtno in rtnos:
                    if rtno.name == argv[3]:
                        tools.launch_arduino(rtno.file, verbose=verbose)
                        return
                raise wasanbon.RTCNotFoundException()
            


        elif argv[2] == 'configure':
            wasanbon.arg_check(argv, 4)
            rtc_name = argv[3]
            targets = []
            for i in range(0, 16):
                if rtc_name.endswith(str(i)):
                    target_file = os.path.join(proj.conf_path, rtc_name + '.conf')
                    targets.append(target_file)
                    
            if len(targets) == 0: # all files
                for i in range(0, 16):
                    target_file = os.path.join(proj.conf_path, rtc_name + str(i) + '.conf')
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
                        sys.stdout.write(' - Updated.\n')
                        rtcc[key] = val
                        return False
                    else:
                        sys.stdout.write(' - Aborted.\n')
                        return False

                util.choice(choice1, callback1, msg)
            
                rtcc.sync(verbose=verbose)

                rtcc = wasanbon.core.rtc.RTCConf(target)
                for key in rtcc.keys():
                    print ' -- %s:%s' % (key, rtcc[key])
        elif argv[2] == 'run':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Executing RTC %s\n' % argv[3])
            rtc_ = self.get_rtc_rtno(proj, argv[3], verbose=verbose)
            conf_file = os.path.join(proj.conf_path, rtc_.name + '0.conf')
            if os.path.isfile(conf_file):
                sys.stdout.write(' - with rtc.conf %s\n' % os.path.basename(conf_file))
                arg = ['-f', conf_file]
            else:
                arg = []
            rtc_.execute_standalone(arg, verbose=True)
            

        else:
            raise wasanbon.InvalidUsageException()

def print_rtno(rtno):
    str = rtno.name + ' : \n'
    str = str + '    name       : ' + rtno.name + '\n'
    str = str + '    language   : ' + 'arduino' + '\n'
    filename = rtno.file
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = str + '    file       : ' + filename + '\n'
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
