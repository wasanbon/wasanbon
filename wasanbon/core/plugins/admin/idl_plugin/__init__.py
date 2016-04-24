import sys, os
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

from idl_parser import *

class Plugin(PluginFunction):

    def __init__(self):
        super(Plugin, self).__init__()
        self._parser = None
        pass

    def depends(self):
        return ['admin.environment']

    def _print_alternatives(self, args):
        print 'hoo'
        print 'foo'
        print 'hoge'
        print 'yah'


    def get_global_module(self):
        return self._parser.global_module

    def is_primitive(self, name):
        return self._parser.is_primitive(name)

    def forEachIDL(self, func, idls=[], idl_dirs=[], except_files=[]):
        """ Apply func function to each IDLs.
        """
        default_idl_dirs = [os.path.join(wasanbon.get_rtm_root(), 'rtm', 'idl'),
                            os.path.join(wasanbon.home_path, 'idl')]

        default_except_files = ['RTM.idl', 'RTC.idl', 'OpenRTM.idl', 'DataPort.idl', 'Manager.idl', 'SDOPackage.idl']

        if self._parser is None:
            self._parser = parser.IDLParser()

        except_files = except_files + default_except_files
        self._parser.forEachIDL(func, idl_dirs=idl_dirs + default_idl_dirs, except_files=except_files)
        
    def parse(self, idls=[], idl_dirs=[], except_files=[]):
        self._parser = parser.IDLParser()
        self.forEachIDL(self._parser.parse_idl, idls=idls, idl_dirs=idl_dirs, except_files=except_files)

    def get_idl_parser(self):
        return self._parser
        
    @manifest
    def list(self, argv):
        """ List IDL files in default directories (RTM_ROOT and ~/.wasanbon/idl)
        """
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option

        self.forEachIDL(lambda x: sys.stdout.write(x + '\n'))
        return 0


    @manifest
    def to_dic(self, argv):
        """ Convert IDL contents to Dictionary.
        $ wasanbon-admin.py idl to_dic
        """
        self.parser.add_option('-l', '--long', help='Long format option (default=False)', default=False, action='store_true', dest='long_flag')
        self.parser.add_option('-d', '--detail', help='Detail information option. This shows the converted dictionary completely. A bit difficult to read. (default=False)', default=False, action='store_true', dest='detail_flag')

        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        long = options.long_flag
        detail = options.detail_flag

        self.parse()

        import yaml
        if detail:
            print yaml.dump(self._parser.global_module.to_dic(), default_flow_style=False)
        else:
            print yaml.dump(self._parser.global_module.to_simple_dic(not long), default_flow_style=False)

    @manifest
    def show(self, argv):
        """ Show datatype (struct, enum, typedef, and interface) information.
        """
        self.parser.add_option('-l', '--long', help='Long format option (default=False)', default=False, action='store_true', dest='long_flag')
        self.parser.add_option('-r', '--recursive', help='Recursive Type Parse. Show each members in inner structs. (default=False)', default=False, action='store_true', dest='recursive_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        long = options.long_flag
        recursive = options.recursive_flag

        wasanbon.arg_check(argv, 4)

        self.parse()

        full_typename = argv[3]
        typs = self._parser.global_module.find_types(full_typename)
        if len(typs) == 0:
            sys.stdout.write('Not Found.\n')
            return 0

        for t in typs:
            import yaml
            print yaml.dump(t.to_simple_dic(full_path=True, recursive=recursive), default_flow_style=False)

        return 0
        
    @manifest
    def gen_constructor(self, argv):
        """ Generate Constructor Code """
        self.parser.add_option('-l', '--language', help='Language option (default=python)', default='python', action='store', dest='language')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option
        language = options.language
        recursive = True

        wasanbon.arg_check(argv, 4)
        self.parse()

        full_typename = argv[3]
        codes = self.generate_constructor_python(full_typename, verbose=verbose)
        for code in codes:
            print code

        return 0

    def generate_constructor_python(self, full_typename, verbose=False):
        codes = []
        typs = self._parser.global_module.find_types(full_typename)
        if len(typs) == 0:
            sys.stdout.write('Not Found.\n')
            return 0

        for t in typs:
            import yaml
            if verbose: print yaml.dump(t.to_simple_dic(full_path=True, recursive=recursive), default_flow_style=False)
            
            code = self._parser.generate_constructor_python(t)
            codes.append(code)

        return codes



        
            
        
