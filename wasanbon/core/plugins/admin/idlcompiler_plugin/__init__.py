import os, sys, types

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.idl']

    @manifest
    def dart(self, argv):
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option

        admin.idl.parse()

        import dart_converter as dc
        dc.generate_converter(admin.idl.get_idl_parser(), verbose=verbose)
            
        return 0





