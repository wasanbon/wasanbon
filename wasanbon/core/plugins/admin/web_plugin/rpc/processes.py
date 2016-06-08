import os, sys, time
import WSB
from plugin import *


class ProcessesPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'processes')
        self._processes = []

    def run(self, filename, args):
        self.debug('run(%s, %s)' % (filename, str(args)))
        import subprocess
        shell = False
        if filename.endswith('.py'):
            cmd = ['python', filename]
            try:
                p = subprocess.Popen(cmd, shell=shell)
                time.sleep(2)
                self._processes.append(p)
                return self.return_value(True, '', ('python', p.pid))
            except Exception, ex:
                traceback.print_exc()
                return self.return_value(False, 'Exception: %s' % str(ex), [])

        return self.return_value(False, 'Unknown File Extension.', [])

    def kill(self, pid):
        self.debug('kill(%s)' % (str(pid)))
        #import subprocess
        import psutil
        for p in psutil.process_iter():
            try:
                if p.pid() == pid:
                    sys.stdout.write('%s kill.\n' % p)
                    p.kill()
                    return self.return_value(True, '', (pid))
            except Exception, ex:
                traceback.print_exc()
        return self.return_value(False, 'Exception: %s' % str(ex), [])

