"""
en_US:
 brief: |
  Install the modules that are required with wasanbon.


 description : |
  Install the modules which are required with wasanbon.
  This command will install RT-middleware.
  To install the modules, use : $ wasanbon-admin.py install [modules]
  If you want to get alternatives of modules, use: $ wasanbon-admin.py install -a
  If you want to check if it's installed or not, use: $ wasanbon-admin.py status


 subcommands : []
"""

import sys, os,yaml
import wasanbon
from wasanbon.core import rtm, tools
from wasanbon.core.rtm import cpp, python, java
from wasanbon.core.platform import install


def alternative(argv=None):
    y = yaml.load(open(os.path.join(wasanbon.rtm_home(), 'setting.yaml'), 'r'))
    return ['rtm_c++', 'rtm_python', 'rtm_java', 'eclipse', 'arduino'] + y.keys()

def execute_with_argv(argv, force=False, verbose=False, clean=False):
    wasanbon.arg_check(argv, 3)

    y = yaml.load(open(os.path.join(wasanbon.rtm_home(), 'setting.yaml'), 'r'))    
    
    if 'all' in argv:
        argv = ['rtm_c++', 'rtm_python', 'rtm_java', 'eclipse', 'arduino'] + y.keys()
    else:
        argv = argv[2:]
        
    for arg in argv:
        if arg.startswith("rtm_"):
            sys.stdout.write(' - Installing OpenRTM-aist %s\n' % arg)
        else:
            sys.stdout.write(' - Installing %s\n' % arg)
            pass
        if arg in y.keys():
            install.check_command(arg, y[arg], verbose=True, install=True, force=force)
        elif arg == 'rtm_c++':
            cpp.install(force=force, verbose=True)
        elif arg == 'rtm_python':
            python.install(force=force, verbose=True)
        elif arg == 'rtm_java':
            java.install(force=force, verbose=True)
        elif arg == 'rtshell':
            tools.install_rtshell(verbose=True, force=force)
        elif arg == 'eclipse':
            tools.install_eclipse(force=force, verbose=True)
        elif arg == 'arduino':
            tools.install_rtno(force=force, verbose=True)

        
