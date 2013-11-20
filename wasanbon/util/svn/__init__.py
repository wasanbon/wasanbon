import os, sys, datetime
import wasanbon

def input_setting(file, addr, port):
    file.write('http-proxy-host = %s\n' % addr)
    file.write('http-proxy-port = %s\n' % port)
    pass

def set_proxy(addr, port, verbose=False):
    if verbose:
        sys.stdout.write(' - setting svn proxy\n')
        pass

    svn_home_path = os.path.join(wasanbon.get_home_path(), '.subversion')
    if not os.path.isdir(svn_home_path):
        os.mkdir(svn_home_path)
        pass
    svn_server_file = os.path.join(svn_home_path, 'servers')
    if not os.path.isfile(svn_server_file):
        file = open(svn_server_file, 'w')
        file.write('[global]\n')
        input_setting(file, addr, port)
    else:
        today = datetime.datetime.today()
        datestr = '%s%s%s%s%s' % (today.year, today.month, today.day, today.hour, today.minute)
        os.rename(svn_server_file, svn_server_file + '.bak' + datestr)
        file = open(svn_server_file, 'w')
        old_file = open(svn_server_file + '.bak' + datestr, 'r')
        block_found = False
        for line in old_file:
            if line.strip().startswith('[global]'):
                if verbose:
                    sys.stdout.write(' -- Found global seting area\n')
                    pass

                file.write('### ' + line)
                for line in old_file:
                    if line.strip().startswith('['):
                        # another block
                        #block_found = True
                        #input_setting(file, addr, port)
                        file.write(line)
                        break
                    elif not line.strip().startswith('#'):
                        line = '### ' + line
                        pass
                    if verbose:
                        sys.stdout.write(line)
                    file.write(line)
            else:
                file.write(line)
        if not block_found:
            file.write('[global]\n')            
            input_setting(file, addr, port)
        pass
    


def omit_proxy(verbose=False):
    if verbose:
        sys.stdout.write(' - removing the setting svn proxy\n')
        pass

    svn_home_path = os.path.join(wasanbon.get_home_path(), '.subversion')
    if not os.path.isdir(svn_home_path):
        sys.stdout.write(' - setting file not found.\n')
        return 
    svn_server_file = os.path.join(svn_home_path, 'servers')
    if not os.path.isfile(svn_server_file):
        sys.stdout.write(' - setting file not found.\n')
        return 
    else:
        today = datetime.datetime.today()
        datestr = '%s%s%s%s%s' % (today.year, today.month, today.day, today.hour, today.minute)
        os.rename(svn_server_file, svn_server_file + '.bak' + datestr)
        file = open(svn_server_file, 'w')
        old_file = open(svn_server_file + '.bak' + datestr, 'r')
        block_found = False
        for line in old_file:
            if line.strip().startswith('[global]'):
                if verbose:
                    sys.stdout.write(' -- Found global seting area\n')
                    pass

                file.write(line)
                for line in old_file:
                    if line.strip().startswith('['):
                        # another block
                        #block_found = True
                        #input_setting(file, addr, port)
                        file.write(line)
                        break
                    elif not line.strip().startswith('#'):
                        line = '### ' + line
                        pass
                    if verbose:
                        sys.stdout.write(line)
                    file.write(line)
            else:
                file.write(line)
        pass
    

        
