import os, sys

#plugin_obj = None


class PackageObject(object):

    def __init__(self, name=None, path=None):

        self._path = path
        self._setting_file_path = os.path.join(path, 'setting.yaml')
        if not os.path.isfile( self._setting_file_path):
            import wasanbon
            raise wasanbon.InvalidPackagePathError()
        self._setting = None
        self._rtcconf = None

        if name:
            self._name = name
        else:
            self._name = self.setting['name']
    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def setting(self):
        if self._setting is None:
            import yaml
            self._setting = yaml.load(open(self._setting_file_path, 'r'))
        return self._setting['application']

    def get_binpath(self, fullpath=True):
        dir = self.setting['BIN_DIR']
        if fullpath:
            return os.path.join(self.path, dir)
        return dir

    def get_systempath(self, fullpath=True):
        dir = self.setting['RTS_DIR']
        if fullpath:
            return os.path.join(self.path, dir)
        return dir

    def get_confpath(self, fullpath=True):
        dir = self.setting.get('CONF_DIR', 'conf')
        if fullpath:
            return os.path.join(self.path, dir)
        return dir

    def get_rtcpath(self, fullpath=True):
        dir = self.setting.get('RTC_DIR', 'rtc')
        if fullpath:
            return os.path.join(self.path, dir)
        return dir

    @property
    def rtc_repository_file(self):
        return os.path.join(self.get_rtcpath(), 'repository.yaml')

        

    def __repr__(self):
        return self.name + '(' + self.path + ')'
    
    @property
    def rtcconf(self):
        #from . import plugin_obj
        if self._rtcconf is None:
            self._rtcconf = {}
            #import wasanbon
            for lang in ['C++', 'Java', 'Python']:
                path = os.path.join(self.path, self.setting['conf.'+lang])
                if os.path.isfile(path):
                    sys.stdout.write('# setting.yaml is written in old manner.\n')
                    sys.stdout.write('# conf.%s must be filename, and path of conffile must be writtein in CONF_DIR\n'%lang)
                else:
                    path = os.path.join(self.get_confpath(), self.setting['conf.'+lang])
                if not os.path.isfile(path):
                    sys.stdout.write('# Config file %s is not found.\n' % path)
                    continue
                #self._rtcconf[lang] = plugin_obj.admin.rtcconf.rtcconf.RTCConf(path) #wasanbon.plugins.admin.rtcconf.rtcconf.RTCConf(path)
                self._rtcconf[lang] = path
        return self._rtcconf
