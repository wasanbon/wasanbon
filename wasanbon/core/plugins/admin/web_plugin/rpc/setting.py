import os, sys, traceback
import WSB
from plugin import *


class SettingPlugin(PluginObject):
    
    def __init__(self):
        PluginObject.__init__(self, 'setting')
    
    def echo(self, msg):
        self.debug('echo(%s)' % msg)
        return self.return_value(True, '', msg)

    def selfupdate(self):
        self.debug('selfupdate')
        p = call('selfupdate', 'run', '-f')
        stdout, stderr = p.communicate()
        return self.return_value(p.returncode==0, '', (stdout, stderr))

    def ready_packages(self):
        self.debug('ready_packages')
        stdout = check_output('web', 'packages')
        import yaml
        d = yaml.load(stdout)
        return self.return_value(True, '', d)

    def upload_package(self, filename, content):
        substr = content[content.find('base64,') + len('base64,'):]
        content = substr
        substr = content[6:] if len(content) > 10 else content

        self.debug('upload_package(%s, %s)' % (filename, substr))
        try:
            package_dir = check_output('web', 'package_dir').strip()
            cwd = os.getcwd()
            os.chdir(package_dir)
            
            #open(filename + '.zip', 'wb').write(content)

            import base64
            open(filename + '.zip', 'wb').write(base64.urlsafe_b64decode(content))
            
            os.chdir(cwd)
            return self.return_value(True, '', True)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception occured %s' % str(ex), '')


    def remove_package(self, filename):
        self.debug('upload_package(%s)' % filename)
        try:
            package_dir = check_output('web', 'package_dir').strip()
            cwd = os.getcwd()
            os.chdir(package_dir)
            
            if os.path.isfile(filename + '.zip'):
                os.remove(filename + '.zip')
                os.chdir(cwd)
                return self.return_value(True, '', True)
            
            os.chdir(cwd)
            return self.return_value(True, '', False)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception occured %s' % str(ex), '')

    def applications(self):
        self.debug('applicatione()')
        try:
            cmd = ['web', 'applications']
            stdout = check_output(*cmd).strip()
            import yaml
            d = yaml.load(stdout)
            if not d:
                d = []
            return self.return_value(True, '', d)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception occured %s' % str(ex), '')
        
    def install_package(self, packageName, force, version):
        self.debug('install_package(%s, %s, %s)' % (packageName, force, version))
        try:
            cmd = ['web', 'install', packageName]
            if force:
                cmd = cmd + ['-f']
            if len(version) > 0:
                cmd = cmd + ['-s', version]
            stdout = check_output(*cmd).strip()
            return self.return_value(True, '', True)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception occured %s' % str(ex), '')

    def uninstall_application(self, appName):
        self.debug('install_package(%s)' % (appName))
        try:
            cmd = ['web', 'uninstall', appName]
            stdout = check_output(*cmd).strip()
            return self.return_value(True, '', True)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception occured %s' % str(ex), '')

    def status(self):
        self.debug('status')
        stdout = check_output('status')
        dic = {}
        for line in stdout.split('\n'):
            if len(line.strip()) == 0:
                continue
            if line.strip().startswith('- Checking'):
                continue
            name = line.split()[1]
            status = line.split()[-1]
            dic[name] = status
        return self.return_value(True, '', dic)

    def restart(self):
        self.debug('restart()')
        try:
            cwd = os.getcwd()
            if sys.platform == 'win32':
                pass
            else:
                script = """sleep 4;
wasanbon-admin.py web restart """
                print 'saving script..'
                filename = os.path.join(cwd, 'restart_script.sh')
                with open(filename, 'w') as f:
                    f.write(script)
                    f.close()
                
                time.sleep(1)
            if not os.path.isfile(filename):
                print 'File not found!!!'
            cmd = ['/bin/sh', filename]
            import subprocess
            p = subprocess.Popen(cmd)
            #os.remove(filename)

            return self.return_value(True, '', True)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception occured %s' % str(ex), '')

    def stop(self):
        self.debug('stop()')
        try:
            if sys.platform == 'win32':
                pass
            else:
                script = """sleep 5;
wasanbon-admin.py web stop """
                print 'saving script..'
                with open('stop_script.sh', 'w') as f:
                    f.write(script)
                    f.close()
            cmd = ['sh', 'stopt_script.sh']
            import subprocess
            p = subprocess.Popen(cmd)
            os.remove('stop_script.sh')
            return self.return_value(True, '', True)
        except Exception, ex:
            traceback.print_exc()
            return self.return_value(False, 'Exception occured %s' % str(ex), '')
