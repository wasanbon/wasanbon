"""
en_US:
 brief : |
  Name Service Administration
 description : | 
  Change setting of Name Service for current package.
  Add/Del nameservice for this package.

 subcommands : 
  list : |
   Show all nameservice of current package
  add : |
   Add nameserver address 
   ex., $ mgr.py nameserver add 192.168.1.1:2809
  del : |
   Delete nameserver address
   ex., $ mgr.py nameserver del 192.168.1.1:2809

ja_JP:
 brief : |
  Name Service Administration
 description : | 
  Change setting of Name Service for current package.
  Add/Del nameservice for this package.

 subcommands : 
  list : |
   Show all nameservice of current package
  add : |
   Add nameserver address 
   ex., $ mgr.py nameserver add 192.168.1.1:2809
  del : |
   Delete nameserver address
   ex., $ mgr.py nameserver del 192.168.1.1:2809
"""

import os, sys, time, subprocess, signal, yaml
import wasanbon
from wasanbon.core import rtc
from wasanbon.core import system, package

def alternative(argv=None):
    if len(argv) == 3:
        if argv[2] == 'del':
            y = yaml.load(open('setting.yaml', 'r'))
            if 'nameservers' in y['application'].keys():
                return ['\\"'+n+'\\"' for n in  y['application']['nameservers']]
        
    return ['list', 'add', 'del']

def execute_with_argv(argv, verbose):
    wasanbon.arg_check(argv, 3)
    _package = package.Package(os.getcwd())

    if argv[2] == 'list':
        show_nameserver_list(verbose)
        return

    elif argv[2] == 'add':
        add_nameserver(argv, verbose=verbose)
        return

    if argv[2] == 'del':
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
