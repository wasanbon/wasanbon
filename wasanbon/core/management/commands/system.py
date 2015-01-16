# coding: utf-8
"""
en_US:
 brief : |
  RT-System administration
 description : |

 subcommands : 
  list : |
   List all RTCs which are installed into the System.
  install : |
   Install RTC binary into bin directory.
   This command will update conf/rtc_{your_language}.conf file.
   By this modification, RTC will be automatically launched by RTC-daemon
  uninstall : |
   Uninstall RTC binary from bin directory.
   This command also remove the preload and precreate setting.
  build : |
   Build RT-system.
   This command will launch RTC-daemon, and list the available connections.
   You will be asked if the ports must be connected or not.
   After the listing connections, you will get the RTCs list for the configuration. 
   You can change the default configuration in the step.
   Finally, you will get the DefaultSystem.xml (RT-System-profile) in your system directory.
  configure : |
   This command modifies the RT-system profile interactively.
  run : |
   Launch RT-system.
   This will launch RTC-daemon of C++, Python, and Java.
   All load rtc.conf in conf directory, and precreate RTCs if necessary.
   Then, process load RT-System profile (in default, system/DefaultSystem.xml), and
   build / activate RT-system.
   Before launching RTC-daemon, the naming service will be initiated if necessary.
   To stop the system, press Ctrl+C
  terminate : |
   Terminate RT-system.

ja_JP :
 brief : |
  RTシステムの管理
 description : |
  RTシステムの管理を行います．
  パッケージはRTCの集まりですが，複数の言語で作られたRTCを個別に実行するのでは，分散システム化した結果，開発効率が悪くなります．
  wasanbonでは，RTCを一度に複数起動することが可能です．
  また，standalone版のRTCを実行することもできるので，柔軟なシステム設計が可能です．
  
 subcommands : 
  list : |
   RTシステムにインストールされているRTCをリスト表示します．
  install : |
   RTCのバイナリをインストールします．
   この時，conf/rtc_{開発言語}.confファイルを編集します．C++版ならrtc_cpp.confです．
   これにより，runコマンド時には，RTC-DaemonからRTCが読み込まれ，自動的にRTCが起動します．
  uninstall : |
   RTCのバイナリをシステムからアンインストールします．
  build : |
   RTシステムをビルドします．
   このコマンドでは，runと同様にRTC-daemonを起動します．
   そして，ネームサーバー上の可能なコネクションを表示しますので，接続するときにはyを押します．
   また，コンフィグレーションについても変更を行います．
   最後に，システム構築の結果をsystem/DefaultSystem.xmlファイルに保存します．
   Finally, you will get the DefaultSystem.xml (RT-System-profile) in your system directory.
  configure : |
   RT System Profile (デフォルトではsystem/DefaultSystem.xml) を編集して，RTCのコンフィグレーションを変更できます．
   このコマンドは，パッケージを展開したマシンによって，シリアルポートなどが変更になった場合に，簡易的に編集する場合に使います．
  run : |
   RTシステムを起動します．
   このコマンドはC++, Python, JavaのRTC-daemonを同時に起動します．
   この時，confディレクトリのrtc_cpp.conf, rtc_py.conf, rtc_java.confを読み込みます．
   また，RT System Profile (デフォルトでは，system/DefaultSystem.xml) を読み込んで，
   RTシステムの構築とアクティブ化を行います．
   また，setting.yamlに書かれているスクリプトを読み込んで，standalone版のRTCを起動します．
   standalone版のRTCとは，独自にスレーブマネージャを起動するRTCで，通常は**Comp.exeなどの実行形式で与えられます．
   終了するためには，Ctrl+Cを押してください．
  terminate : |
   RTシステムを終了します．
   パッケージ内のRTシステムが起動中であれば終了を試みます．pidファイル内にあるプロセスIDを読み込んでkillを送ります．
"""
import os, sys, time, subprocess, signal, yaml, getpass, threading, traceback, optparse
import wasanbon
from wasanbon.core import package, nameserver
from wasanbon import util

import rtctree
import omniORB
from rtshell import rtcryo

ev = threading.Event()

endflag = False


def alternative(argv=None):

    rtcname_return_commands = ['install', 'uninstall']
    system_file_name_return_commands = ['configure']
    all_commands = rtcname_return_commands + system_file_name_return_commands + ['build', 'run', 'datalist', 'list', 'nameserver', 'terminate']
    if len(argv) >= 3:
        if argv[2] in rtcname_return_commands:
            pack = package.Package(os.getcwd())
            return [rtc.name for rtc in pack.rtcs]
        elif argv[2] in system_file_name_return_commands:
            pack = package.Package(os.getcwd())
            return [f for f in os.listdir(pack.system_path) if f.endswith('.xml')]
    return all_commands

def execute_with_argv(args, verbose, force=False, clean=False):

    usage = 'mgr.py system [subcommand]'
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-l', '--long', help='long format information', action='store_true', default=False, dest='long_flag')
    parser.add_option('-i', '--interactive', help='interactive launch', action='store_true', default=False, dest='interactive_flag')
    parser.add_option('-f', '--force', help='Force relaunch nameserver', action='store_true', default=False, dest='force_flag')
    parser.add_option('-s', '--standalone', help='Install RTC with standalone version', action='store_true', default=False, dest='standalone_flag')
    try:
        options, argv = parser.parse_args(args[:])
    except:
        return
    wasanbon.arg_check(argv, 3)

    force = options.force_flag
    interactive = options.interactive_flag
    _package = package.Package(os.getcwd())

    if argv[2] == 'install':
        if 'all' in argv[3:]:
            rtc_names = [rtc.name for rtc in _package.rtcs]
        else:
            rtc_names = [arg for arg in argv[3:] if not arg.startswith('-')]

        for name in rtc_names:
            sys.stdout.write(' @ Installing RTC (%s).\n' % name)
            try:
                #_package.install(_package.rtc(name), verbose=verbose)
                rtc = _package.rtc(name)
                package.install_rtc(_package, rtc, verbose=verbose, overwrite_conf=force, standalone=options.standalone_flag)
                
            except Exception, ex:
                sys.stdout.write(' - Installing RTC %s failed.\n' % name)
                print ex
        
    elif argv[2] == 'uninstall':
        wasanbon.arg_check(argv, 4)
        sys.stdout.write(' @ Uninstalling RTC.\n')
        if 'all' in argv[3:]:
            _package.uninstall(_package.rtcs, verbose=verbose)
            pass
        for name in argv[3:]:
            try:
                _package.uninstall(_package.rtc(name), verbose=verbose)
            except:
                if verbose:
                    traceback.print_exc()
                sys.stdout.write(' - Unnstalling RTC %s failed.\n' % name)


    elif(argv[2] == 'list'):
        # sys.stdout.write(' @ Listing installed RTCs.\n')
        rtcs_map = _package.installed_rtcs()
        rtcs_stand = _package.installed_standalone_rtcs()
        for lang, rtcs in rtcs_map.items():
            sys.stdout.write('  %s :\n' % lang)
            for rtc_ in rtcs:
                sys.stdout.write('   - %s\n' % rtc_.name) 
        sys.stdout.write('  Standalone :\n')
        for rtc in rtcs_stand:
            sys.stdout.write('   - %s\n' % rtc.name)
                
    elif(argv[2] == 'build'):
        print ' @ Building RTC System in Wasanbon'

        package.run_nameservers(_package, verbose=verbose, force=force)
        package.run_system(_package, verbose=verbose)

        print_delay(_package.get_build_delay())

        interactive_connection(_package, verbose=verbose)
        interactive_configuration(_package, verbose=verbose)

        save_all_system(['localhost'], verbose=verbose)
        package.stop_system(_package, verbose=verbose)
        package.kill_nameservers(_package, verbose=verbose)


    elif(argv[2] == 'run'):
        _run(_package, verbose=verbose, force=force, interactive=interactive)


    elif(argv[2] == 'terminate'):
        _terminate(_package, verbose=verbose)
        
    elif(argv[2] == 'datalist'):
        package.list_rtcs_by_dataport()
                 
        pass

    elif(argv[2] == 'nameserver'):
        y = yaml.load(open('setting.yaml', 'r'))
        
        rtcconf_cpp = rtc.RTCConf(y['application']['conf.C++'])
        rtcconf_py = rtc.RTCConf(y['application']['conf.Python'])
        rtcconf_java = rtc.RTCConf(y['application']['conf.Java'])
        
        if len(argv) == 3:
            sys.stdout.write(' - Listing Nameservers\n')
            sys.stdout.write('rtcd(C++)    : "%s"\n' % rtcconf_cpp['corba.nameservers'])
            sys.stdout.write('rtcd(Python) : "%s"\n' % rtcconf_py['corba.nameservers'])
            sys.stdout.write('rtcd(Java)   : "%s"\n' % rtcconf_java['corba.nameservers'])
        elif len(argv) == 4:
            sys.stdout.write(' - Adding Nameservers\n')
            rtcconf_cpp['corba.nameservers'] = argv[3]
            rtcconf_py['corba.nameservers'] = argv[3]
            rtcconf_java['corba.nameservers'] = argv[3]
            rtcconf_cpp.sync()
            rtcconf_py.sync()
            rtcconf_java.sync()
                
            pass
    elif argv[2] == 'validate':
        _package.validate(verbose=verbose, autofix=force, interactive=True)
        pass

    elif argv[2] == 'configure':
        interactive_systemfile_configure(_package, argv, verbose=verbose)
    else:
        raise wasanbon.InvalidUsageException

def interactive_configuration(_package, verbose):
    nss = _package.get_nameservers(verbose=verbose)
    rtcs = []
    for ns in nss:
        rtcs = rtcs + ns.rtcs
        
    rtc_choices = [comp_full_path(rtc) for rtc in rtcs]

    def on_rtc_selected(rtc_num):
        rtcs = []
        for ns in nss:
            ns.refresh()
            rtcs = rtcs + ns.rtcs
                
        sys.stdout.write(' @ RTC(%s) is chosen.\n' % rtc_choices[rtc_num])
        set_name = rtcs[rtc_num].active_conf_set_name
        if len(set_name) == 0:
            sys.stdout.write(' @ There is NO ACTIVE CONFIGURATION SET.\n')
            sys.stdout.write(' @ Quit.\n')
            return False
        sys.stdout.write(' @ Active Configuration Set = %s\n' % set_name)
        conf_choices = [key + ':' + value for key, value in rtcs[rtc_num].active_conf_set.data.items()]

        def on_conf_selected(conf_num):
            sys.stdout.write(conf_choices[conf_num] +' is chosen.\n')
            key = conf_choices[conf_num].split(':')[0].strip()
            old_val = rtcs[rtc_num].active_conf_set.data[key]
            sys.stdout.write(' %s :' % key)
            val = raw_input()
            if util.yes_no(' - %s:%s : %s ==> %s' % (set_name, key, old_val, val)) == 'yes':
                #rtcs[rtc_num].active_conf_set.set_param(key, val)
                rtcs[rtc_num].set_conf_set_value(set_name, key, val)
                rtcs[rtc_num].activate_conf_set(set_name)
                sys.stdout.write(' @ Updated.\n')
                return True
            return False
        util.choice(conf_choices, callback=on_conf_selected, msg=' @ Select Configuration to modify.')
        return False

    util.choice(rtc_choices, callback=on_rtc_selected, msg=' @ Select RTC to configure')

    pass

def interactive_connection(_package, verbose):
    nss = _package.get_nameservers(verbose=verbose)
    for ns in nss:
        ns.refresh(verbose=verbose, force=True)

    pairs = _package.available_connection_pairs(nameservers=nss, verbose=verbose)
    for outport, inport in pairs:
        msg = ' @ Connect? %s -> %s' % (port_full_path(outport), port_full_path(inport))
        if util.no_yes(msg) == 'yes':
            sys.stdout.write(' @ Connecting...')
            try:
                inport.connect([outport])
                sys.stdout.write(' OK.\n')
            except Exception, ex:
                sys.stdout.write(' Failed.\n')

    return True



def interactive_systemfile_configure(_package, argv, verbose):
    __import__('wasanbon.core.system.system_obj')
    system_obj = sys.modules['wasanbon.core.system.system_obj'] 
    sysobj = system_obj.SystemObject(_package.system_file)
    def select_rtc(ans):
        confs = sysobj.active_conf_data(sysobj.rtcs[ans])
        conf_names = [conf.name +':' + conf.data for conf in confs]
        
        def select_conf(ans2):
            key = confs[ans2].name
            sys.stdout.write(' INPUT (%s):' % key)
            val = raw_input()
            if util.yes_no('%s = %s. Okay?' % (key, val)) == 'yes':
                sysobj.set_active_conf_data(sysobj.rtcs[ans], key, val)
                return True
            return False
        util.choice(conf_names, select_conf, msg='Select Configuration')
        return False

    util.choice(sysobj.rtcs, select_rtc, msg='Select RTC')
    sysobj.update()

def signal_action(num, frame):
    print ' - SIGINT captured'
    ev.set()
    global endflag
    endflag = True
    pass

def print_delay(dt):
    times = dt * 10
    sys.stdout.write(' - Waiting approx. %s seconds\n' % dt)
    for t in range(times):
        percent = float(t) / times
        width = 30
        progress = (int(width*percent)+1)
        sys.stdout.write('\r  [' + '#'*progress + ' '*(width-progress-1) + ']')
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write('\n')

def save_all_system(nameservers, filepath='system/DefaultSystem.xml', verbose=False):
    if verbose:
        sys.stdout.write(" - Saving System on %s to %s\n" % (str(nameservers), filepath))
    try:
        argv = ['--verbose', '-n', 'DefaultSystem01', '-v', '1.0', '-e', 'Sugar Sweet Robotics',  '-o', filepath]
        argv = argv + nameservers
        rtcryo.main(argv=argv)
    except omniORB.CORBA.UNKNOWN, e:
        traceback.print_exc()
        pass
    except Exception, e:
        traceback.print_exc()
        return False


def comp_full_path(comp):
    str = ""
    for p in comp.full_path:
        str = str + p
        if not str.endswith('/') and not str.endswith('.rtc'):
            str = str + '/'
    return str

def port_full_path(port):
    return comp_full_path(port.owner) + ':' + port.name


def _terminate(_package, verbose=False):
    package.stop_system(_package, verbose=verbose)
    package.kill_nameservers(_package, verbose=verbose)

def _run(_package, verbose=False, force=False, interactive=False):
    signal.signal(signal.SIGINT, signal_action)
    if sys.platform == 'win32':
        sys.stdout.write(' - Escaping SIGBREAK...\n')
        signal.signal(signal.SIGBREAK, signal_action)
        pass
    sys.stdout.write(' @ Starting RTC-daemons...\n')

    global endflag
    nss = []
    try:
        nss = package.run_nameservers(_package, verbose=verbose, force=force)
        if not nss:
            raise wasanbon.BuildSystemException()

        if interactive:
            raw_input(' - Nameserver Checked. Press Enter.\n')

        if not package.run_system(_package, verbose=verbose):
            raise wasanbon.BuildSystemException()

        if interactive:
            raw_input(' - rtcd launched. Press Enter.\n')
        else:
            print_delay(_package.get_build_delay())

        if not package.build_system(_package, verbose=verbose):
            raise wasanbon.BuildSystemException()
            
        if interactive:
            raw_input(' - connection okay. Press Enter.\n')

        if not package.activate_system(_package, verbose=verbose):
            raise wasanbon.BuildSystemException()


        while not endflag:
            try:
                time.sleep(0.1)
                if package.is_shutdown(_package):
                    break
            except IOError, e:
                pass
            pass
    except wasanbon.BuildSystemException, ex:
        traceback.print_exc()
        pass
    if not package.is_shutdown(_package):
        package.deactivate_system(_package, verbose=verbose)
        package.exit_all_rtcs(_package, verbose=verbose)
        package.stop_system(_package, verbose=verbose)

    
    package.kill_nameservers(_package, verbose=verbose)

