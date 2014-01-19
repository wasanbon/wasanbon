import os, sys, yaml, subprocess
import wasanbon

from wasanbon import util

from wasanbon.core.template import *

from . import directory, path, install


def init_rtm_home(force=False, verbose=False, update=True):
    directory.create_rtm_home(force=force, verbose=verbose)
    directory.copy_initial_setting(verbose=verbose, force=force)
    create_dot_emacs()
    return True #all(retval)


def create_dot_emacs():
    dot_e_file = os.path.join(wasanbon.get_home_path(), '.emacs')
    dot_e_temp = os.path.join(wasanbon.__path__[0], 'settings', 'common', 'dot.emacs')
    flag = 'w'
    if os.path.isfile(dot_e_file):
        fin = open(dot_e_file, 'r')
        tempin = open(dot_e_temp, 'r')
        if fin.read().count(tempin.read()) > 0:
            return
        fin.close()
        tempin.close()

        flag = 'a'
    fout = open(dot_e_file, flag)
    fin = open(dot_e_temp, 'r')
    fout.write(fin.read())
    fout.close()
    fin.close()


