# coding: utf-8
"""
en_US :
 brief : |
  Check you wasanbon platform status.
 description : |
  This command will show the setup status of wasanbon.
 subcommands : []

ja_JP :
 brief : |
  wasanbonのプラットフォームの状態を表示します．
 description : |
  wasanbonのプラットフォームの状態を表示します．
  依存するモジュールの状態を表示します．
 subcommands : []
"""

import sys, os
import wasanbon

def alternative(argv=None):
    return []

def execute_with_argv(argv, force=False, verbose=False, clean=False):
    wasanbon.arg_check(argv, 2)
    #platform.init_rtm_home(force=False, verbose=verbose, update=False)
    sys.stdout.write(' - Checking Platform Status.\n')
    sys.stdout.write('    - wasanbon.platform : %s\n' % wasanbon.platform() )
    
    try:
        __import__('yaml')


    except ImportError, e:
        sys.stdout.write(' - Your System does not have PyYAML package.\n')
        return 

    try:
        yaml = sys.modules['yaml']
        __import__('wasanbon.core.platform.path')
        path = sys.modules['wasanbon.core.platform.path']
        sys.stdout.write(' - Checking Platform installation.\n')
        path.init_tools_path(verbose=verbose)
        y = yaml.load(open(os.path.join(wasanbon.rtm_home(), 'setting.yaml'), 'r'))
        for cmd, stat in y.items():
            if len(stat.strip()) == 0:
                stat = 'Not Installed'
                pass
            sys.stdout.write('    - ' + cmd + ' ' * (12-len(cmd)) + ': ' + stat + '\n')
            pass
    except ImportError, e:
        sys.stdout.write(' - Your System does not have PyYAML package.\n')
        return 


        
    from wasanbon.core import tools
    from wasanbon.core.rtm import cpp, python, java

    sys.stdout.write(' - Checking OpenRTM-aist installation\n')
    sys.stdout.write('    - rtm_c++    (OpenRTM-aist C++)    : %s\n' % cpp.is_installed())
    sys.stdout.write('    - rtm_python (OpenRTM-aist Python) : %s\n' % python.is_installed())
    sys.stdout.write('    - rtm_java   (OpenRTM-aist Java)   : %s\n' % java.is_installed())
    sys.stdout.write(' - Checking tools intallation\n')
    sys.stdout.write('    - rtshell : %s\n' % tools.is_installed_rtshell())
    sys.stdout.write('    - eclipse : %s\n' % tools.is_installed_eclipse())
    sys.stdout.write('    - arduino : %s\n' % tools.is_installed_arduino())
    

        
