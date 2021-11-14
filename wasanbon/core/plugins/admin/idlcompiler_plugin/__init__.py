import os
import sys
import types

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

from .dart_converter import *
# import .dart_converter


class Plugin(PluginFunction):
    """ IDL dart file compiler Plugin."""

    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.idl']

    @manifest
    def dart(self, argv):
        """ Convert IDL files to dart files.
        $ wasanbon-admin.py idlcompiler dart
        """
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag  # This is default option

        admin.idl.parse()

        generate_converter(admin.idl.get_idl_parser(), verbose=verbose)

        return 0
