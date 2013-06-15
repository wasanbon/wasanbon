import os, sys, time, subprocess, signal, yaml
import wasanbon
from wasanbon.core import rtc
from wasanbon.core import system
from wasanbon.core.system import run



class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv):
        if len(argv) < 3 or argv[2] == 'help':
            wasanbon.show_help_description('system')
            return

        rtcps = rtc.parse_rtcs()
        if(argv[2] == 'install'):
            if len(argv) < 4:
                wasanbon.show_help_description('system')
                return

            if argv[3] == 'all':
                for rtcp in rtcps:
                    print 'Installing RTC %s' % rtcp.getName()
                    rtc.install(rtcp)
                return

            for rtcp in rtcps:
                if rtcp.getName() == argv[3]:
                    print 'Installing RTC %s' % argv[3]
                    rtc.install(rtcp)
                    return
            print 'RTC(%s) can not found.' % argv[3]

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
            if len(argv) >= 4 and argv[3] == '--nobuild':
                sys.stdout.write('\n - Launch System without System Build.\n\n')
                nobuild=True
            else:
                nobuild=False

            system.run_system(nobuild=nobuild)
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
