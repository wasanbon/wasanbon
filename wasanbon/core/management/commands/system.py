import os, sys, time, subprocess, signal, yaml, getpass, threading, traceback
import wasanbon
from wasanbon.core import rtc
from wasanbon import util
#from wasanbon.core import system
#from wasanbon.core.system import run
from wasanbon.core import project, nameserver


import rtctree
import omniORB
from rtshell import rtcryo
ev = threading.Event()

endflag = False

def signal_action(num, frame):
    print ' - SIGINT captured'
    ev.set()
    global endflag
    endflag = True
    pass


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

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, clean, verbose, force):

        proj = project.Project(os.getcwd())

        if(argv[2] == 'install'):
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Installing RTC.\n')
            if 'all' in argv[3:]:
                for rtc in proj.rtcs:
                    sys.stdout.write(' @ Installing %s\n' % rtc.name)
                    proj.install(rtc, verbose=verbose)
                return

            for name in argv[3:]:
                try:
                    proj.install(proj.rtc(name), verbose=verbose)
                except Exception, ex:
                    print ex
                    sys.stdout.write(' - Installing RTC %s failed.\n' % name)


        elif(argv[2] == 'uninstall'):
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Uninstalling RTC.\n')
            if 'all' in argv[3:]:
                proj.uninstall(proj.rtcs)

            for name in argv[3:]:
                try:
                    proj.uninstall(proj.rtc(name))
                except:
                    sys.stdout.write(' - Unnstalling RTC %s failed.\n' % name)


        elif(argv[2] == 'list'):
            sys.stdout.write(' @ Listing installed RTCs.\n')
            rtcs_map = proj.installed_rtcs()
            for lang, rtcs in rtcs_map.items():
                sys.stdout.write(' @ %s:\n' % lang)
                for rtc_ in rtcs:
                    sys.stdout.write('    @ %s\n' % rtc_.name) 

        elif(argv[2] == 'build'):
            print ' @ Building RTC System in Wasanbon'
            nss = proj.get_nameservers(verbose=verbose)
            ns_process = None
            for ns in nss:
                if not ns.check_and_launch(verbose=verbose, force=force):
                    sys.stdout.write(' @ Nameserver %s is not running\n' % ns.path)
                    return

            proj.launch_all_rtcd(verbose=verbose)

            for i in range(0, 5):
                sys.stdout.write('\r - Waiting (%s/%s)\n' % (i+1, 5))
                sys.stdout.flush()
                time.sleep(1)

            for ns in nss:
                ns.refresh(verbose=verbose, force=True)

            pairs = proj.available_connection_pairs(nameservers=nss, verbose=verbose)
            for outport, inport in pairs:
                msg = ' @ Connect? %s -> %s' % (port_full_path(outport), port_full_path(inport))
                if util.no_yes(msg) == 'yes':
                    sys.stdout.write(' @ Connecting...')
                    try:
                        inport.connect([outport])
                        sys.stdout.write(' OK.\n')
                    except Exception, ex:
                        sys.stdout.write(' Failed.\n')

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
            
            save_all_system(['localhost'])
            proj.terminate_all_rtcd(verbose=verbose)

            for ns in nss:
                ns.kill()



        elif(argv[2] == 'run'):
            signal.signal(signal.SIGINT, signal_action)
            if sys.platform == 'win32':
                print 'SIGBREAK..'
                signal.signal(signal.SIGBREAK, signal_action)
            sys.stdout.write(' @ Starting RTC-daemons...\n')

            nss = proj.get_nameservers(verbose=verbose)
            ns_process = None
            for ns in nss:
                if not ns.check_and_launch(verbose=verbose, force=force):
                    sys.stdout.write(' @ Nameserver %s is not running\n' % ns.path)
                    return

            proj.launch_all_rtcd(verbose=verbose)
            proj.connect_and_configure(verbose=verbose)
            proj.activate(verbose=verbose)

            global endflag
            while not endflag:
                try:
                    time.sleep(0.1)
                except IOError, e:
                    pass


            proj.deactivate(verbose=verbose)
            proj.terminate_all_rtcd(verbose=verbose)

            for ns in nss:
                ns.kill()
                

        elif(argv[2] == 'datalist'):
            project.list_rtcs_by_dataport()
                 
            pass

        elif(argv[2] == 'nameserver'):
            
            y = yaml.load(open('setting.yaml', 'r'))
            
            rtcconf_cpp = rtc.rtcconf.RTCConf(y['application']['conf.C++'])
            rtcconf_py = rtc.rtcconf.RTCConf(y['application']['conf.Python'])
            rtcconf_java = rtc.rtcconf.RTCConf(y['application']['conf.Java'])
            
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
            proj.validate(verbose=verbose, autofix=force, interactive=True)
            pass
            
        else:
            raise wansanbon.InvalidUsageException


