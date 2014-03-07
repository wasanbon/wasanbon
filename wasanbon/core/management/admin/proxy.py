"""
en_US :
 brief : |
  This command simply set the proxy setting for git command

 description : |
  This command simply set the proxy setting for git command

 subcommands: []
"""


import wasanbon
from wasanbon import util

def alternative(argv=None):
    return []

def execute_with_argv(argv, verbose=False, clean=False):
    if len(argv) >= 3:
        host, port = argv[2].split(':')
        util.set_proxy(host, port, verbose=True)
        return
    else:
        util.omit_proxy(verbose=True)
        return

