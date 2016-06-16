import os, sys, traceback
import WSB
from plugin import *

class NameServicePlugin(PluginObject):
    def __init__(self):
        PluginObject.__init__(self, 'nameservice')

    def activate_rtc(self, fullpath):
        """ Activate RT-component
        """
        self.debug('activate_rtc(%s)' % fullpath)
        try:
            stdout = check_output('nameserver', 'activate_rtc', fullpath)
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def deactivate_rtc(self, fullpath):
        """ Deactivate RT-component
        """
        self.debug('deactivate_rtc(%s)' % fullpath)
        try:
            stdout = check_output('nameserver', 'deactivate_rtc', fullpath)
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def reset_rtc(self, fullpath):
        """ Reset RT-component
        """
        self.debug('reset_rtc(%s)' % fullpath)
        try:
            stdout = check_output('nameserver', 'reset_rtc', fullpath)
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def exit_rtc(self, fullpath):
        """ Exit RT-component
        """
        self.debug('exit_rtc(%s)' % fullpath)
        try:
            stdout = check_output('nameserver', 'exit_rtc', fullpath)
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass


    def configure_rtc(self, rtc, confset, confname, confvalue):
        self.debug('configure_rtc(%s, %s, %s, %s)' % (rtc, confset, confname, confvalue))
        try:
            stdout = check_output('nameserver', 'configure', rtc, '-s', confset, confname, confvalue)
            if stdout.find('Success') >= 0:
                return self.return_value(True, '', True)
            else:
                return self.return_value(True, '', False)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def list_connectable_pairs(self, nss):
        self.debug('list_connectable_pairs(%s)' % nss)
        try:
            stdout = check_output('nameserver', 'list_connectable_pair', '-n', nss) 
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass
        
    def connect_ports(self, port0, port1, param):
        self.debug('connect_ports(%s, %s, %s)' % (port0, port1, param))
        try:
            params = param.split(',')
            cmd = ['nameserver', 'connect', port0, port1]
            for p in params:
                if len(p) > 0:
                    cmd = cmd + ['-p', p]
                    pass
                pass
            stdout = check_output(*cmd)
            if stdout.find('Success') >= 0:
                return self.return_value(True, '', True)                
            else:
                return self.return_value(True, '', False)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def disconnect_ports(self, port0, port1):
        self.debug('disconnect_ports(%s, %s)' % (port0, port1))
        try:
            cmd = ['nameserver', 'disconnect', port0, port1]
            stdout = check_output(*cmd)
            if stdout.find('Success') >= 0:
                return self.return_value(True, '', True)                
            else:
                return self.return_value(True, '', False)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def start(self, port):
        self.debug('start(%s)' % str(port))
        try:
            sub = ['nameserver', 'start', '-p', str(port)] 
            #process = call(*sub)
            #return self.return_value(True, '', process.pid)
            stdout = check_output(*sub)
            return self.return_value(True, '', stdout)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def check_running(self, port):
        self.debug('check_running')
        try:
            sub = ['nameserver', 'check_running', '-p', str(port)]
            stdout = check_output(*sub)
            retval = True
            if stdout.find('Not Running') >= 0:
                retval = False
            return self.return_value(True, '', retval)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass


    def stop(self, port):
        self.debug('stop(%s)' % str(port))
        try:
            sub = ['nameserver', 'stop', '-p', str(port)] 
            stdout = check_output(*sub)
            return self.return_value(True, '', stdout)
            #process = call(*sub)
            #return self.return_value(True, '', process.pid)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass

    def tree(self, host, port):
        self.debug('tree(%s, %s)' % (host, str(port)))
        try:
            sub = ['nameserver', 'tree', '-d', '-p', str(port), '-u', host]
            stdout = check_output(*sub)
            return self.return_value(True, '', stdout.strip())
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception: %s' % str(ex), [])
        pass
        
 
