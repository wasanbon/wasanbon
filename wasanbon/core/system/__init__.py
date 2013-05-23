# encoding: UTF-8

import os, sys, time, signal, traceback

import omniORB

import wasanbon
from wasanbon.core.system import run
from wasanbon.core import rtc
from wasanbon.core.rtc import rtcprofile
from wasanbon.core.system import rtsprofile
process = {}

import rtctree

def signal_action(num, frame):
    print 'SIGINT captured'
    global endflag
    endflag = True
    pass

endflag = False

def is_all_process_terminated():
    flags = []
    global process
    for key in process.keys():
        if process[key].returncode != None:
            flags.append(False)
        else:
            process[key].poll()
            if process[key].returncode == None:
                flags.append(False)
            else:
                flags.append(True)
    if len(flags) != 0:
        return all(flags)
    else:
        return False


def start_process():
    if not os.path.isdir('log'):
        os.mkdir('log')

    global process
    process['cpp']    = run.start_cpp_rtcd()
    process['python'] = run.start_python_rtcd()
    process['java']   = run.start_java_rtcd()


def run_system(nobuild, nowait=False):
    sys.stdout.write('Ctrl+C to stop system.\n')
    signal.signal(signal.SIGINT, signal_action)

    sys.stdout.write('Starting RTC-Daemons\n')
    
    start_process()

    global endflag
    
    if not nobuild:
        interval = 3
        for i in range(0, interval):
            sys.stdout.write('\rwaiting %s seconds to rebuild RTSystem.' % (interval-i))
            sys.stdout.flush()
            time.sleep(1)
            
        while not endflag:
            sys.stdout.write('\n rtresurrect.\n')                    
            if run.exe_rtresurrect():
                time.sleep(1)
                break
        while not endflag:
            sys.stdout.write(' rtstart.\n')
            if run.exe_rtstart():
                time.sleep(1)
                break
    sys.stdout.write('System successfully started.\n')
    
    while not endflag:
        try :
            time.sleep(2)
            list_online_rtcs()
            break
        except omniORB.CORBA.UNKNOWN, e:
            print e
        except Exception, e:
            traceback.print_exc()
                        


    if nowait:
        return
    while not endflag:
        try:
            time.sleep(0.1)
            if is_all_process_terminated():
                break
        except Exception, e:
            print 'Exception Occurred: %s' % repr(e)
            endflag = True
            pass


    print 'Terminating All Process....'        
    terminate_all_process()
    print 'All rtcd process terminated.'


def terminate_all_process():
    global process
    for key in process.keys():
        process[key].poll()
        if process[key].returncode == None:
            sys.stdout.write(' - Terminating RTC-Daemon(%s)\n' % key)
            process[key].kill()
            

    pass


def list_rtcs_by_dataport():
    types = {}
    rtcps = rtc.parse_rtcs()
    for rtcp in rtcps:
        dataports = rtcp.getDataPorts()
        for port in dataports:
            if not port.type in types.keys():
                types[port.type] = [rtcp.getName() + '.' + port.name + '.' + port.portType]
            else:
                types[port.type].append(rtcp.getName() + '.' + port.name + '.' + port.portType)

    for key in types.keys():
        print key
        for v in types[key]:
            if v.endswith('.DataInPort'):
                print ' In : ' + v
            else:
                print ' Out: ' + v
                
def list_online_rtcs():
    types = {}
    path, port = rtctree.path.parse_path('/localhost')
    tree = rtctree.tree.RTCTree(paths=path, filter=[path])
    dir_node = tree.get_node(path)
    def func(node, types):
        for dport in node.inports + node.outports:
            type = dport.properties['dataport.data_type']
            if not type in types.keys():
                types[type] = [ dport ]
            else:
                types[type].append(dport)
    def filt_func(node):
        if node.is_component:
            return True
        return False

    dir_node.iterate(func, types, [filt_func])


    #for key in types.keys():
     #   print ' - ' + key
      #  for p in types[key]:
       #     print '    - ' + str(p.owner.full_path) + '.' + p.name

    pass

def list_rtsp():
    
    pass
