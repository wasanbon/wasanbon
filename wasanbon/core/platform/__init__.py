import os, sys, subprocess
import wasanbon

def init_rtm_home(force=False, verbose=False, update=True):
    module_name = 'wasanbon.core.platform.directory'
    __import__(module_name)
    directory = sys.modules[module_name]

    directory.create_rtm_home(force=force, verbose=verbose)
    directory.copy_setting_file(verbose=verbose, force=True)
    directory.copy_repository_file(verbose=verbose, force=force)
    
    if sys.platform == 'darwin':
        init_bashrc('.bash_profile', verbose=verbose)
    elif sys.platform == 'linux2':
        init_bashrc('.bashrc', verbose=verbose)

    create_dot_emacs()
    return True #all(retval)

def init_bashrc(filename, verbose=False):
    start_str = '#-- Starting Setup Script of wasanbon --#'
    stop_str  = '#-- Ending Setup Script of wasanbon --#'
    target = os.path.join(wasanbon.get_home_path(), filename)
    script = open(os.path.join(wasanbon.__path__[0], "settings", wasanbon.platform(), "bashrc"), "r").read()
    
    if verbose:
        sys.stdout.write(' - Initializing $HOME/%s\n' % filename)

    if os.path.isfile(target):
        erase = False
        file = open(target, "r")
        fout = open(target + '.bak', "w")
        for line in file:
            if line.strip() == start_str:
                erase = True
                continue

            elif line.strip() == stop_str:
                erase = False
                continue

            if not erase:
                fout.write(line)
        
        file.close()
        fout.close()

        os.remove(target)
        os.rename(target + ".bak" , target)

        fout = open(target, "a")
    else:
        fout = open(target, "w")

    fout.write("\n\n" + start_str + "\n")
    fout.write(script)
    fout.write("\n" + stop_str + "\n\n")
            

    fout.close()
    pass


    

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


