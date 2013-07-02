import os, sys, time, subprocess, signal, yaml
import wasanbon
from wasanbon.core import rtc
from wasanbon.core import system
from wasanbon.core.system import run



class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, verbose, force, clean):
        if len(argv) < 3:
            print 'To read help, input "mgr.py nameserver help"'
            return

        if argv[2] == 'list':
            show_nameserver_list(verbose)
            return

        if argv[2] == 'add':
            add_nameserver(argv, verbose=verbose)
            return

        if argv[2] == 'remove':
            remove_nameserver(argv, verbose=verbose)
            return

def remove_nameserver(argv, verbose):
    sys.stdout.write('Name Server Remove:\n')
    y = yaml.load(open('setting.yaml', 'r'))
    if not y:
        return
    if not 'application' in y.keys():
        sys.stdout.write('Invalid setting.yaml file.\n')
        return
    if not 'nameservers' in y['application'].keys():
        sys.stdout.write('setting.yaml does not include nameservers key.\n')
        y['application']['nameservers'] = ['localhost:2809']

    y['application']['nameservers'].remove(argv[3])
    yaml.dump(y, open('setting.yaml', 'w'), default_flow_style=False)
    sys.stdout.write(' - Removed.\n')
    pass


def add_nameserver(argv, verbose):
    sys.stdout.write('Name Server Add:\n')
    y = yaml.load(open('setting.yaml', 'r'))
    if not y:
        return
    if not 'application' in y.keys():
        sys.stdout.write('Invalid setting.yaml file.\n')
        return
    if not 'nameservers' in y['application'].keys():
        sys.stdout.write('setting.yaml does not include nameservers key.\n')
        y['application']['nameservers'] = ['localhost:2809']

    for host in argv[3:]:
        if not host in y['application']['nameservers']:
            y['application']['nameservers'].append(host)

    yaml.dump(y, open('setting.yaml', 'w'), default_flow_style=False)
    
    pass

def show_nameserver_list(verbose):
    sys.stdout.write('Name Server List:\n')
    
    if verbose:
        print ' - Opening %s...' % os.path.join(os.getcwd(), 'setting.yaml')
    y = yaml.load(open('setting.yaml', 'r'))
    if not y:
        print ' - Invalid Yaml file (setting.yaml)'
        return

    if not 'application' in y.keys():
        sys.stdout.write('Invalid setting.yaml file.\n')
        return

    if not 'nameservers' in y['application'].keys():
        sys.stdout.write('setting.yaml does not include nameservers key.\n')
        y['application']['nameservers'] = ['localhost:2809']
        yaml.dump(y, open('setting.yaml', 'w'), default_flow_style=False)
        return
    
    nameservers = y['application']['nameservers']
    print nameservers
        
            
    pass
