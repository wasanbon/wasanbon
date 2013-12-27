import sys, os, yaml
import wasanbon
from wasanbon.core import rtc, package

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        wasanbon.arg_check(argv, 3)
        _package = package.Package(os.getcwd())
        rtcconf_cpp = _package.rtcconf('C++')
        rtcconf_py  = _package.rtcconf('Python')
        rtcconf_java= _package.rtcconf('Java')

        if argv[2] == 'set':
            wasanbon.arg_check(argv, 6)
            lang = argv[3]
            key = argv[4]
            value = argv[5]
            if lang == 'all':
                rtcconf_cpp[key] = value
                rtcconf_py[key] = value
                rtcconf_java[key] = value
                rtcconf_cpp.sync()
                rtcconf_py.sync()
                rtcconf_java.sync()
            else:
                _package.rtcconf(lang)[key] = value
                _package.rtcconf(lang).sync()

        elif argv[2] == 'status':

            if len(argv) >= 4:
                key = argv[3]
                sys.stdout.write(' - ' + key + '\n')
                if not len(rtcconf_cpp[key]) == 0:
                    sys.stdout.write('    - C++   : ' + rtcconf_cpp[key] + '\n')
                if not len(rtcconf_py[key]) == 0:
                    sys.stdout.write('    - Python: ' + rtcconf_py[key] + '\n')
                if not len(rtcconf_java[key]) == 0:
                    sys.stdout.write('    - Java  : ' + rtcconf_java[key] + '\n')
                
            else:
                
                printed_key = []
                for key, value in rtcconf_cpp.items():
                    if value == rtcconf_py[key] and value == rtcconf_java[key]:
                        sys.stdout.write(' - ' +  key + ' ' * (20-len(key))
                                         + ' : ' + value + '\n')
                    else:
                        sys.stdout.write(' - ' +  key + '\n')
                        if not len(rtcconf_cpp[key]) == 0:
                            sys.stdout.write('    - C++   : ' + rtcconf_cpp[key] + '\n')
                        if not len(rtcconf_py[key]) == 0:
                            sys.stdout.write('    - Python: ' + rtcconf_py[key] + '\n')
                        if not len(rtcconf_java[key]) == 0:
                            sys.stdout.write('    - Java  : ' + rtcconf_java[key] + '\n')
                        
                    printed_key.append(key)

                for key, value in rtcconf_py.items():
                    if not key in printed_key:
                        sys.stdout.write(' - ' +  key + '\n')
                        if not len(rtcconf_cpp[key]) == 0:
                            sys.stdout.write('    - C++   : ' + rtcconf_cpp[key] + '\n')
                        if not len(rtcconf_py[key]) == 0:
                            sys.stdout.write('    - Python: ' + rtcconf_py[key] + '\n')
                        if not len(rtcconf_java[key]) == 0:
                            sys.stdout.write('    - Java  : ' + rtcconf_java[key] + '\n')

                            
