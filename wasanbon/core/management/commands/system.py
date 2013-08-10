import os, sys, time, subprocess, signal, yaml, getpass
import wasanbon
from wasanbon.core import rtc
from wasanbon.core import system
from wasanbon.core.system import run
from wasanbon.core import project

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv, clean, verbose, force):

        proj = project.Project(os.getcwd())

        if(argv[2] == 'install'):
            wasanbon.arg_check(argv, 4)

            if 'all' in argv[3:]:
                proj.install(proj.rtcs)

            for name in argv[3:]:
                try:
                    proj.install(proj.rtc(name))
                except:
                    sys.stdout.write(' - Installing RTC %s failed.\n' % name)


        elif(argv[2] == 'uninstall'):
            wasanbon.arg_check(argv, 4)
            if 'all' in argv[3:]:
                proj.uninstall(proj.rtcs)

            for name in argv[3:]:
                try:
                    proj.uninstall(proj.rtc(name))
                except:
                    sys.stdout.write(' - Unnstalling RTC %s failed.\n' % name)


        elif(argv[2] == 'list'):
            print ' - Listing installed RTCs.'
            retval = system.list_installed_rtcs()
            for key, value in retval.items():
                print ' - Language:', key
                for v in value:
                    print '    ', v
            pass

        elif(argv[2] == 'build'):
            print 'Building RTC System in Wasanbon'
            system.run_system(nobuild=True, nowait=True)
            
            for i in range(0, 5):
                sys.stdout.write('\r - Waiting (%s/%s)\n' % (i+1, 5))
                sys.stdout.flush()
                time.sleep(1)
            system.list_available_connections()
            system.list_available_configurations()
            system.save_all_system(['localhost'])

            system.terminate_all_process()
            return

        elif(argv[2] == 'run'):
            sys.stdout.write(' @ Starting RTC-daemons...\n')
            nameservers = proj.get_nameservers()
            if verbose:
                sys.stdout.write(' @ Listing Nameservers:\n')
                for ns in nameservers:
                    sys.stdout.write('    - %s\n' % ns)
            
            nameserver.is_nameserver_running('localhost')
            pass

        elif(argv[2] == 'datalist'):
            system.list_rtcs_by_dataport()
                 
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
            
