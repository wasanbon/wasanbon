# coding: utf-8
"""
en_US :
 brief : |
  This command simply show the version of wasanbon
 description : |
  This command simply show the version of wasanbon
 subcommands: []

ja_JP :
 brief : |
  wasanbonのバージョンを表示します．
 description : |
  wasanbonのバージョンを表示します．
 subcommands: []
"""


import sys
import wasanbon

def alternative(argv=None):
    return []

def execute_with_argv(argv, force=False, verbose=False, clean=False):
    sys.stdout.write(' - Platform = %s\n' % wasanbon.platform())
    sys.stdout.write(' - Version  = %s\n' % wasanbon.get_version())

