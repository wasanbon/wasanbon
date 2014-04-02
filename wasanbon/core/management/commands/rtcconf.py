"""
en_US : 
 brief : |
  Configure rtc.conf files for RTC-daemon. Use like...
 description : |
  Set/Get rtc.conf files setting.
  
 subcommands:
  set : |
   set configuration value
   $ mgr.py rtcconf set KEY VALUE
   ex., $ mgr.py rtcconf set corba.endpoint 127.0.0.1:2809
   You can specify the laungage of RTC daemon with -b option
   ex., $ mgr.py rtcconf set -b [cxx|python|java] logger.enable TRUE
  get : |
   get configuration value
   $ mgr.py rtcconf get KEY
   You can specify the laungage of RTC daemon with -b option
   ex., $ mgr.py rtcconf get -b [cxx|python|java] logger.enable 
  status : |
   view all configuration value
   ex., $ mgr.py rtcconf status

ja_JP : 
 brief : |
  Configure rtc.conf files for RTC-daemon. Use like...
 description : |
  Set/Get rtc.conf files setting.
  
 subcommands:
  set : |
   set configuration value
   $ mgr.py rtcconf set KEY VALUE
   ex., $ mgr.py rtcconf set corba.endpoint 127.0.0.1:2809
   You can specify the laungage of RTC daemon with -b option
   ex., $ mgr.py rtcconf set -b [cxx|python|java] logger.enable TRUE
  get : |
   get configuration value
   $ mgr.py rtcconf get KEY
   You can specify the laungage of RTC daemon with -b option
   ex., $ mgr.py rtcconf get -b [cxx|python|java] logger.enable 
  status : |
   view all configuration value
   ex., $ mgr.py rtcconf status
"""
import sys, os, yaml, optparse
import wasanbon
from wasanbon.core import rtc, package

rtcconf_keys = ['config.version',
             'openrtm.version',
             'manager.name',
             'manager.naming_formats',
             'manager.is_master',
             'manager.corba_servant',
             'corba.master_manager',
             'manager.shutdown_on_nortcs',
             'manager.shutdown_auto',
             'manager.auto_shutdown_duration',
             'corba.args',
             'corba.endpoint',
             'corba.endpoints',
             'corba.nameservers',
             'corba.nameservice.replace_endpoint',
             'corba.alternate_iiop_addresses',
             'naming.enable',
             'naming.type',
             'naming.formats',
             'naming.update.enable',
             'naming.update.interval',
             'naming.update.rebind',
             'manager.modules.load_path',
             'manager.modules.preload',
             'manager.modules.abs_path_allowed',
             ## 'manager.modules.config_ext',
             ## 'manager.modules.config_path',
             ## 'manager.modules.detect_loadable',
             ## 'manager.modules.init_func_suffix',
             ## 'manager.modules.init_func_prefix',
             ## 'manager.modules.download_allowed',
             ## 'manager.modules.download_dir',
             ## 'manager.modules.download_cleanup',
             'manager.components.precreate',
             'logger.enable',
             'logger.file_name',
             'logger.date_format',
             'logger.log_level',
             'timer.enable',
             'timer.tick',
             'exec_cxt.periodic.type',
             'exec_cxt.periodic.rate',
             'sdo.service.provider.available_services',
             'sdo.service.provider.enabled_services',
             'sdo.service.provider.providing_services',
             'sdo.service.consumer.available_services',
             'sdo.service.consumer.enabled_services',
             ]


def alternative(argv=None):
    key_return_cmd = ['set', 'get']
    if len(argv) == 3:
        if argv[2] in key_return_cmd:
            return rtcconf_keys

    return ['status'] + key_return_cmd

def execute_with_argv(args, force=False, verbose=False, clean=False):
    usage = "mgr.py rtcconf [subcommand] ...\n"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-b', '--backend', help='Language of RTC daemon', default='all', dest='backend')
    try:
        options, argv = parser.parse_args(args[:])
    except:
        raise wasanbon.InvalidUsageException()


    if options.backend == 'java':
        lang = 'Java'
    elif options.backend == 'cxx':
        lang = 'C++'
    elif options.backend == 'python':
        lang = 'Python'
    elif options.backend == 'all':
        lang = 'all'
    else:
        raise wasanbon.InvalidUsageException()

    wasanbon.arg_check(argv, 3)
    _package = package.Package(os.getcwd())
    rtcconf_cpp = _package.rtcconf('C++')
    rtcconf_py  = _package.rtcconf('Python')
    rtcconf_java= _package.rtcconf('Java')
    
    if argv[2] == 'set':
        wasanbon.arg_check(argv, 5)
        key = argv[3]
        value = argv[4]
        print value
        value = value.replace('\\', '')
        print value
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

    elif argv[2] == 'get':
        wasanbon.arg_check(argv, 4)
        key = argv[3]
        sys.stdout.write(' - ' + key + '\n')
        if not len(rtcconf_cpp[key]) == 0:
            sys.stdout.write('    - C++   : ' + rtcconf_cpp[key] + '\n')
        if not len(rtcconf_py[key]) == 0:
            sys.stdout.write('    - Python: ' + rtcconf_py[key] + '\n')
        if not len(rtcconf_java[key]) == 0:
            sys.stdout.write('    - Java  : ' + rtcconf_java[key] + '\n')

    elif argv[2] == 'status':
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
                printed_key.append(key)

        for key, value in rtcconf_java.items():
            if not key in printed_key:
                sys.stdout.write(' - ' +  key + '\n')
                if not len(rtcconf_cpp[key]) == 0:
                    sys.stdout.write('    - C++   : ' + rtcconf_cpp[key] + '\n')
                if not len(rtcconf_py[key]) == 0:
                    sys.stdout.write('    - Python: ' + rtcconf_py[key] + '\n')
                if not len(rtcconf_java[key]) == 0:
                    sys.stdout.write('    - Java  : ' + rtcconf_java[key] + '\n')

    else:
        raise wasanbon.InvalidUsageException()
