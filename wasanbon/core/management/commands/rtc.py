"""
en_US:
 brief : |
  RTC administration
 description : |
  This command provides RTC administration functions.
  You can get installed RTC list.
  You can clone/fork RTC from internet.
  You can build/clean RTC source code.  
 subcommands:
  list : |
   Display RTCs list which are placed in the current packages rtc directory.
  clone  : |
   Clone RTC source code from RTC repository.
   ex., $ mgr.py rtc clone YOUR_RTC_REPOSITORY
   This command allows to clone from specific url as well.
   ex., $ mgr.py rtc clone YOUR_RTC_URL
  fork   : |
   Fork RTC source code from RTC repository to your remote repository.
   ex., $ mgr.py rtc fork YOUR_RTC_REPOSITORY
   You will asked your remote repository address (Currently github only).
  build : |
   Build RTC from Source code.
   This command will create rtc/YOUR_RTC/build-YOUR_SYSTEM directory and then, build binary.
   If RTC is written in C++, cmake and build (make or msbuild) will be called.
   If Python, idl compile is done.
   If Java, javac will compile .java codes and then, jar command will create archive file.
   After build, this function will install the binary and config files into your bin direcotry.
   The place of the bin directory is defined by YOUR_PACKAGE_PATH/setting.yaml.
   The files to be copied will be compiled binary *.dll|*.dylib|*.so, and YOUR_RTC_NAME.conf file.
   If you add -s (--standalone) option, you will include the RTC into system with Stand Alone Version.
   Stand Alone Version will be launched as a standalone process.
   This subcommand recognises -n (--noinstall) option which will change the post-build behavior.
   WITH -n option, build process does not copy the binary file to your bin directory, 
   so you are not able to use the newly built binary for system administration.
  clean : |
   Cleanup build directory.
  run : |
   This command will run the specified RTC only.
   ex., $ mgr.py rtc run YOUR_RTC_NAME
  edit : |
   This command will launch editor (emacs) to edit RTC source code.
   In default, open RTC source code.
  delete : |
   This command delete RTC directory
  configure : |
   This command will configure YOUR_RTC_NAME.conf file in conf directory.
   This configuration will be updated if the RT System Profile has the default configuration values.
   However, if your RTC needs to have default configuration such as log_level, endpoints, naming_formats, and so on, 
   This function is very useful.

ja_JP:
 brief : |
  RTC administration
 description : |
  This command provides RTC administration functions.
  You can get installed RTC list.
  You can clone/fork RTC from internet.
  You can build/clean RTC source code.  
 subcommands:
  list : |
   Display RTCs list which are placed in the current packages rtc directory.
  clone  : |
   Clone RTC source code from RTC repository.
   ex., $ mgr.py rtc clone YOUR_RTC_REPOSITORY
   This command allows to clone from specific url as well.
   ex., $ mgr.py rtc clone YOUR_RTC_URL
  fork   : |
   Fork RTC source code from RTC repository to your remote repository.
   ex., $ mgr.py rtc fork YOUR_RTC_REPOSITORY
   You will asked your remote repository address (Currently github only).
  build : |
   Build RTC from Source code.
   This command will create rtc/YOUR_RTC/build-YOUR_SYSTEM directory and then, build binary.
   If RTC is written in C++, cmake and build (make or msbuild) will be called.
   If Python, idl compile is done.
   If Java, javac will compile .java codes and then, jar command will create archive file.
   After build, this function will install the binary and config files into your bin direcotry.
   The place of the bin directory is defined by YOUR_PACKAGE_PATH/setting.yaml.
   The files to be copied will be compiled binary *.dll|*.dylib|*.so, and YOUR_RTC_NAME.conf file.
   If you add -s (--standalone) option, you will include the RTC into system with Stand Alone Version.
   Stand Alone Version will be launched as a standalone process.
   This subcommand recognises -n (--noinstall) option which will change the post-build behavior.
   WITH -n option, build process does not copy the binary file to your bin directory, 
   so you are not able to use the newly built binary for system administration.
  clean : |
   Cleanup build directory.
  run : |
   This command will run the specified RTC only.
   ex., $ mgr.py rtc run YOUR_RTC_NAME
  edit : |
   This command will launch editor (emacs) to edit RTC source code.
   In default, open RTC source code.
  delete : |
   This command delete RTC directory
  configure : |
   This command will configure YOUR_RTC_NAME.conf file in conf directory.
   This configuration will be updated if the RT System Profile has the default configuration values.
   However, if your RTC needs to have default configuration such as log_level, endpoints, naming_formats, and so on, 
   This function is very useful.
"""

import os, sys, optparse, yaml, types, traceback, signal, threading
import wasanbon
from wasanbon.core import package as pack
from wasanbon.core import rtc, tools, repositories
from wasanbon.util import editor
from wasanbon import util

ev = threading.Event()

def alternative(argv=None):
    return_rtcs = ['clean', 'build', 'delete', 'run', 'edit', 'configure']
    return_rtc_repos = ['clone']
    all_rtcs = ['list'] + return_rtcs + return_rtc_repos
    if argv:
        if len(argv) <= 2:
            return all_rtcs
        if argv[2] in return_rtcs:
            rtcs = pack.Package(os.getcwd()).rtcs
            return [rtc.name for rtc in rtcs]
        elif argv[2] in return_rtc_repos:
            repos = wasanbon.core.rtc.get_repositories()
            return [repo.name for repo in repos]

    return []

def get_rtc_rtno( _package, name, verbose=False):
    try:
        return _package.rtc(name)
    except wasanbon.RTCNotFoundException, e:
        return tools.get_rtno_package(_package, name, verbose=verbose)

def is_url(argv):
    return argv[3].startswith('git@') or argv[3].startswith('http')

def _clone_from_url(_package, url, verbose=False):
    name = os.path.basename(url)
    if name.endswith('.git'):
        name = name[:-4]
    sys.stdout.write(' @ Cloning RTC %s\n' % argv[3])
    try:
        repo_ = wasanbon.core.rtc.RtcRepository(name=name, url=url, desc="")
        rtc_ = repo_.clone(verbose=verbose, path=_package.rtc_path)
    except wasanbon.RTCProfileNotFoundException, e:
        rtc_ = get_rtc_rtno(_package, name, verbose=verbose)
        



def execute_with_argv(args, verbose, force=False, clean=False):
    usage = "mgr.py rtc [subcommand] ...\n"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-l', '--long', help='show status in long format', action='store_true', default=False, dest='long_flag')
    parser.add_option('-n', '--noinstall', help='Build without installing the RTC', action='store_true', default=False, dest='noinstall_flag')
    parser.add_option('-s', '--standalone', help='Installing RTC with standalone version (mostly YOUR_RTC_NAMEComp.exe', action='store_true', default=False, dest='standalone_flag')
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
    elif argv[2] == 'create':
        wasanbon.arg_check(argv, 4)
        if not options.back_end == 'rtno':
            raise wasanbon.InvalidUsageException()
        rtc_name = argv[3]
        tools.generate_rtno_temprate(_package, rtc_name, verbose=True)
        
    elif argv[2] == 'clone':
        wasanbon.arg_check(argv, 4)
        # if argument is url, then, clone by git command
        if is_url(argv[3]):
            _clone_from_url(_package, argv[3], verbose=verbose)

        else:
            for name in argv[3:]:
                sys.stdout.write(' @ Cloning RTC %s\n' % name)
                try:
                    rtc_ = wasanbon.core.rtc.get_repository(name).clone(verbose=verbose, path=_package.rtc_path)
                except wasanbon.RTCProfileNotFoundException, e:
                    rtc_ = get_rtc_rtno(_package, name, verbose=verbose)

        _package.update_rtc_repository(rtc_.repository, verbose=verbose)

    elif argv[2] == 'fork':
        wasanbon.arg_check(argv, 4)
        sys.stdout.write(' @ Forking GITHUB repository in %s\n' % argv[3])
        user, passwd = wasanbon.user_pass()
        original_repo = wasanbon.core.rtc.get_repository(argv[3])
        try:
            repo = original_repo.fork(user, passwd, verbose=verbose, path=_package.rtc_path)
        except wasanbon.RepositoryAlreadyExistsException, ex:
            sys.stdout.write(' - Repository is already exists. Trying to clone it....\n')
            from wasanbon.core.rtc import repository
            url = 'https://github.com/' + user + '/' + original_repo.name + '.git'
            repo = repository.RtcRepository(name=original_repo.name, 
                                            url=url,
                                            desc=original_repo.description)

        sys.stdout.write(' @ Cloning GITHUB repository in %s\n' % argv[3])            
        rtc_ = repo.clone(verbose=verbose, path=_package.rtc_path)
        _package.update_rtc_repository(repo, verbose=verbose)
        owner_add(_package, argv[3])

    elif argv[2] == 'build':
        build_all = True if 'all' in argv else False
        found_flag = False
        if sys.platform == 'win32':
            verbose=True
            pass
            
        for rtc in _package.rtcs:
            if build_all or rtc.name in argv:
                sys.stdout.write(' - Building RTC (%s)\n' % rtc.name)
                ret = rtc.build(verbose=verbose)
                if ret[0]:
                    sys.stdout.write('  - Success\n')
                    if not options.noinstall_flag: # Installing RTC 
                        sys.stdout.write(' - Installing RTC (%s)\n' % rtc.name)
                        try:
                            pack.install_rtc(_package, rtc, standalone=options.standalone_flag, verbose=verbose)
                            sys.stdout.write('  - Success.\n')
                        except Exception ,ex:
                            sys.stdout.write('  @ Installing RTC %s failed.\n' % rtc.name)
                            if verbose:
                                traceback.print_exc()
                else:
                    sys.stdout.write('  @ Failed\n')
                    if util.yes_no('  @ Do you want to watch error message?') == 'yes':
                        print ret[1]
                found_flag = True
                pass
            pass
        if not found_flag:
            raise wasanbon.RTCNotFoundException()

    elif argv[2] == 'clean':
        build_all = True if 'all' in argv else False
        found_flag = False
        if sys.platform == 'win32':
            verbose=True
            pass
        for rtc in _package.rtcs:
            if build_all or rtc.name in argv:
                sys.stdout.write(' - Cleanup RTC %s\n' % rtc.name)
                ret = rtc.clean(verbose=verbose)
                found_flag = True
                pass
            pass
        if not found_flag:
            raise wasanbon.RTCNotFoundException()

    elif argv[2] == 'run':
        endflag = False
        def signal_action(num, frame):
            print ' - SIGINT captured'
            ev.set()
            #global endflag
            endflag = True
            pass

        signal.signal(signal.SIGINT, signal_action)

        if sys.platform == 'win32':
            sys.stdout.write(' - Escaping SIGBREAK...\n')
            signal.signal(signal.SIGBREAK, signal_action)
            pass

        sys.stdout.write(' @ Executing RTC %s\n' % argv[3])
        rtc_ = _package.rtc(argv[3])
        rtcconf = _package.rtcconf(rtc_.language)
        rtc_temp = os.path.join("conf", "rtc_temp.conf")
        if os.path.isfile(rtc_temp):
            os.remove(rtc_temp)
            pass
        rtcconf.sync(verbose=True, outfilename=rtc_temp)
        _package.uninstall(_package.rtcs, rtcconf_filename=rtc_temp, verbose=True)
        _package.install(rtc_, rtcconf_filename=rtc_temp, copy_conf=False)
        
        if not pack.run_nameservers(_package, verbose=verbose, force=force):
            raise wasanbon.BuildSystemException()

        try:
            from wasanbon.core.package import run
            _package.launch_rtcd(rtc_.language, rtcconf=rtc_temp, verbose=True)
            """
            if rtc_.language == 'C++':
                p = run.start_cpp_rtcd(rtc_temp, verbose=True)
            elif rtc_.language == 'Python':
                p = run.start_python_rtcd(rtc_temp, verbose=True)
            elif rtc_.language == 'Java':
                p = run.start_java_rtcd(rtc_temp, verbose=True)
            """
            while not endflag:
                if _package._process[rtc_.language].poll() != None:
                    sys.stdout.write(' - rtcd terminated.\n')
                    break
                pass

            #_package._process[rtc_.language].wait()
            #p.wait()
        except KeyboardInterrupt, e:
            sys.stdout.write(' -- Aborted.\n')
        _package.terminate_rtcd(rtc_.language, verbose=True)
        pack.kill_nameservers(_package, verbose=verbose)            

    elif argv[2] == 'delete':
        wasanbon.arg_check(argv, 4)
        sys.stdout.write(' @ Deleting RTC %s\n' % argv[3])
        for rtcname in argv[3:]:
            _rtc = _package.rtc(rtcname)
            _package.delete_rtc(_rtc, verbose=verbose)

            
    elif argv[2] == 'edit':
        try:
            rtc_ = _package.rtc(argv[3])
                
            if rtc_.is_git_repo():
                if rtc_.git_branch() != 'master':
                    sys.stdout.write(' @ You are not in master branch.\n')
                    if util.yes_no(' @ Do you want to checkout master first?') == 'yes':
                        rtc_.checkout(verbose=verbose)
            editor.edit_rtc(_package.rtc(argv[3]), verbose=verbose)
        except wasanbon.RTCNotFoundException, ex:
            rtnos = tools.get_rtno_packages(_package)
            for rtno in rtnos:
                if rtno.name == argv[3]:
                    tools.launch_arduino(rtno.file, verbose=verbose)
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



