import os, sys, time, subprocess, signal, yaml, getpass, threading
import wasanbon
from wasanbon.core import rtc
from wasanbon import util
#from wasanbon.core import system
#from wasanbon.core.system import run
from wasanbon.core import project, nameserver

ev = threading.Event()

endflag = False

def signal_action(num, frame):
    print ' - SIGINT captured'
    ev.set()
    global endflag
    endflag = True
    pass


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
                proj.install(proj.rtcs, verbose=verbose)

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


            #project.list_available_connections()
            
            outports = []
            for ns in nss:
                ns.refresh(force=True)
                outports = outports + ns.dataports(port_type='DataOutPort')
            print outports
            for outport in outports:
                inports = []
                for ns in nss:
                    inports = inports + ns.dataports(port_type='DataInPort', data_type=outport.properties['dataport.data_type'])

                for inport in inports:
                    msg = ' @ Connect? %s -> %s' % (port_full_path(outport), port_full_path(inport))
                    if util.no_yes(msg) == 'yes':
                        sys.stdout.write(' @ Connecting...')
                        for i in range(0, 3):
                            try:
                                inport.connect([outport])
                                sys.stdout.write(' OK.\n')
                            except Exception, ex:
                                print ex
                                sys.stdout.write(' Failed.\n')
                                pass



                    
            project.list_available_configurations()
            project.save_all_system(['localhost'])
            proj.terminate_all_rtcd(verbose=verbose)

            for ns in nss:
                ns.kill()



        elif(argv[2] == 'run'):
            signal.signal(signal.SIGINT, signal_action)
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

            if sys.platform == 'win32':
                global endflag
                while not endflag:
                    time.sleep(0.1)
            else:
                signal.pause()

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
            
