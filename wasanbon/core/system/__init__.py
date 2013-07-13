# encoding: UTF-8
import os, sys, time, signal, traceback, yaml, subprocess

import rtctree
import omniORB

import wasanbon
from wasanbon import util
from wasanbon.core.system import run
from wasanbon.core import rtc
from wasanbon.core.rtc import rtcprofile
from wasanbon.core.system import rtsprofile
from wasanbon.core.rtc import rtcconf

process = {}
endflag = False

#import rtctree
from rtshell import rtcryo

def signal_action(num, frame):
    print 'SIGINT captured'
    global endflag
    endflag = True
    pass

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


def get_nameserver():
    y = yaml.load(open('setting.yaml', 'r'))
    cppconf = rtcconf.RTCConf(y['application']['conf.C++'])
    pyconf = rtcconf.RTCConf(y['application']['conf.Python'])
    javaconf = rtcconf.RTCConf(y['application']['conf.Java'])
    ns = cppconf['corba.nameservers']
    if ns == pyconf['corba.nameservers'] and ns == javaconf['corba.nameservers']:
        return ns
    return None

def launch_nameserver(ns, verbose=False):
    sys.stdout.write(' - Starting Nameserver %s\n' % ns)
    if ns.startswith('/'):
        ns = ns[1:]
    token = ns.split(':')
    if len(token) == 1:
        addr = token[0].strip()
        port = 2809
    else:
        addr = token[0].strip()
        port = token[1].strip()
        
    if addr == 'localhost' or addr == '127.0.0.1':
        pstdout = None if verbose else subprocess.PIPE 
        pstdin = None if verbose else subprocess.PIPE

        if sys.platform == 'win32':
            path = os.path.join(os.environ['RTM_ROOT'], 'bin', 'rtm-naming.bat')
            cmd = [path, port]
            creationflag = 512

        else:
            cmd = ['rtm-naming', port]
            creationflag = 0

        if verbose:
            print 'Command = %s' % cmd
        p = subprocess.Popen(cmd, creationflags=creationflag, stdout=pstdout, stdin=pstdin)
        for i in range(0,5):
            time.sleep(1)
        print ' - Starting Nameservice okay.'
        return p
    return None

def run_system(nobuild, nowait=False, verbose=False):
    sys.stdout.write('Ctrl+C to stop system.\n')
    signal.signal(signal.SIGINT, signal_action)
    
    ns_process = []
    no_ns = False
    ns = get_nameserver()
    if not ns.startswith('/'):
        ns = '/' + ns.strip()
    if verbose:
        print " - System's NameServer = %s" % ns
    for i in range(0, 3):
        try:
            path, port = rtctree.path.parse_path(ns)
            tree = rtctree.tree.RTCTree(paths=path, filter=[path])
            dir_node = tree.get_node(path)
            no_ns = False
            break
        except rtctree.exceptions.InvalidServiceError, e:
            no_ns = True
        except omniORB.CORBA.OBJECT_NOT_EXIST, e:
            no_ns = True
            pass


    if no_ns:
        if verbose:
            sys.stdout.write('Can not find Name Service (%s)\n' % ns)
        ns_process = launch_nameserver(ns)


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

    if ns_process and ns_process.returncode == None:
        ns_process.kill()


def terminate_all_process():
    global process
    for key in process.keys():
        process[key].poll()
        if process[key].returncode == None:
            sys.stdout.write(' - Terminating RTC-Daemon(%s)\n' % key)
            process[key].kill()
            

    pass


def list_rtcs_by_dataport():
    pass


def comp_full_path(comp):
    str = ""
    for p in comp.full_path:
        str = str + p
        if not str.endswith('/') and not str.endswith('.rtc'):
            str = str + '/'
    return str

def port_full_path(port):
    str = ""
    for p in port.owner.full_path:
        str = str + p
        if not str.endswith('/') and not str.endswith('.rtc'):
            str = str + '/'
    str = str+':'+port.name
    return str

def get_port_list(tree, dir_node):
    types = {}
    def func(node, types):
        for dataport in node.inports + node.outports:
            type = dataport.properties['dataport.data_type']
            if not type in types.keys():
                types[type] = {'DataInPort':[],'DataOutPort':[], 'CorbaPort':[] }
            types[type][dataport.porttype].append(dataport)

    def filt_func(node):
        if node.is_component and not node.parent.is_manager:
            return True
        return False

    dir_node.iterate(func, types, [filt_func])
    return types

        
def list_available_connections():
    for i in range(0, 3):
        try:
            path, port = rtctree.path.parse_path('/localhost')
            tree = rtctree.tree.RTCTree(paths=path, filter=[path])
            dir_node = tree.get_node(path)
            types = get_port_list(tree, dir_node)
            for type in types.keys():
                for outport in types[type]['DataOutPort']:
                    for inport in types[type]['DataInPort']:
                        msg = ' - Connect   [%s]  ->  [%s]' % (port_full_path(outport), port_full_path(inport))
                        if util.no_yes(msg) == 'yes':
                            sys.stdout.write(' - connecting...')
                            outport.connect([inport])
                            sys.stdout.write(' connected.\n')
            return True
        except omniORB.CORBA.UNKNOWN, e:
            pass
        except Exception, e:
            traceback.print_exc()
            return False
            
    return False

def list_available_configurations():
    for i in range(0, 3):
        try:
            path, port = rtctree.path.parse_path('/localhost')
            tree = rtctree.tree.RTCTree(paths=path, filter=[path])
            dir_node = tree.get_node(path)

            nodes = []
            def func(node, types):
                nodes.append(node)
                pass
            def filt_func(node):
                if node.is_component and not node.parent.is_manager:
                    return True
                return False
            dir_node.iterate(func, nodes, [filt_func])

            while True:
                choices = []
                for i in range(0, len(nodes)):
                    choices.append(comp_full_path(nodes[i]))
                choices.append('quit')
                answer = util.choice(choices, msg='Select RTC to configure')
                if answer == len(nodes):
                    break
                
                while True:
                    sys.stdout.write(comp_full_path(nodes[answer]))
                    sys.stdout.write('\n  ' + nodes[answer].active_conf_set_name + '\n')
                    choices = []
                    active_conf_set = nodes[answer].active_conf_set
                    for key, value in active_conf_set.data.items():
                        choices.append(key + ':' + value)
                    choices.append('quit')
                    answer2 = util.choice(choices, msg='Select Configuration to set')
                    if answer2 == len(choices)-1:
                        break

                    key = active_conf_set.data.keys()[answer2]
                    old_val = active_conf_set.data[key]
                    sys.stdout.write(key + ':')
                    val = raw_input()
                    if util.yes_no('%s: %s ==> %s' % (key, old_val, val)) == 'yes':
                        active_conf_set.set_param(key, val)
                        print 'Updated.'
                    else:
                        print 'Aborted.'

            return True
            
        except omniORB.CORBA.UNKNOWN, e:
            traceback.print_exc()
            pass
        except Exception, e:
            traceback.print_exc()
            return False
    return False

def save_all_system(nameservers):
    sys.stdout.write("Updating system/DefaultSystem.xml\n")
    try:
        argv = ['--verbose', '-n', 'DefaultSystem01', '-v', '1.0', '-e', 'Sugar Sweet Robotics',  '-o', 'system/DefaultSystem.xml']
        argv = argv + nameservers
        print argv
        rtcryo.main(argv=argv)
        print "rtcryo updated. ok."
    except omniORB.CORBA.UNKNOWN, e:
        traceback.print_exc()
        print e
        pass
    except Exception, e:
        traceback.print_exc()
        return False



def list_rtsp():
    
    pass


def list_installed_rtcs():
    for language in ['C++', 'Python', 'Java']:
        rtcc = rtcconf.RTCConf(wasanbon.setting['application']['conf.' + language])
        print '    - %s' % language
        try:
            installed = rtcc['manager.components.precreate'].split(',')
            for rtc in installed:
                if rtc.strip() != '':
                    print '      - %s' % rtc
        except KeyError, e:
            pass
    pass
