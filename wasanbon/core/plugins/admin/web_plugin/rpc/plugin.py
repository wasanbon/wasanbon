import os, subprocess, yaml, types, time, sys
import wasanbon

class PluginObject:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def debug(self, msg):
        sys.stdout.write('Plugin(%s) %s\n' % (self._name, str(msg)))
        pass

    def return_value(self, success_flag, msg, return_value):
        self.debug('return_value is (%s, %s, %s)' % (success_flag, msg, return_value))
        return (success_flag, msg, return_value)


def call(*args, **kwargs):
    cmd = ['wasanbon-admin.py']
    shell = False
    for arg in args:
        cmd.append(arg)
    if sys.platform == 'win32':
        shell = True
    sys.stdout.write('call: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    #p.wait()
    #return p.stdout
    #std_out_data, std_err_data = p.communicate()
    return p #std_out_data


def check_output(*args, **kwargs):
    
    cmd = ['wasanbon-admin.py']
    shell = False
    for arg in args:
        cmd.append(arg)
    if sys.platform == 'win32':
        shell = True
    sys.stdout.write('check_output: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    #p.wait()
    #return p.stdout
    std_out_data, std_err_data = p.communicate()
    return std_out_data

def check_mgr_output(*args, **kwargs):
    cmd = ['./mgr.py']
    shell = False
    if sys.platform == 'win32':
        cmd = ['mgr.py']
        shell = True
    for arg in args:
        cmd.append(arg)
    sys.stdout.write('check_mgr_output: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    #p.wait()
    std_out_data, std_err_data = p.communicate()
    return std_out_data

def mgr_call(*args, **kwargs):
    cmd = ['./mgr.py']
    shell = False
    if sys.platform == 'win32':
        cmd = ['mgr.py']
        shell = True
    for arg in args:
        cmd.append(arg)
    sys.stdout.write('mgr_call: %s\n' % str(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    return p

