import wasanbon
import rtsprofile.rts_profile
import os, sys, shutil

class SystemObject:
    def __init__(self, filename):
        self._filename = filename
        stri = open(filename, "r").read()
        self._rtsprofile = rtsprofile.rts_profile.RtsProfile(xml_spec=stri)

    @property
    def rtcs(self):
        return [str(comp.path_uri) for comp in self._rtsprofile.components]

    def _rtc(self, rtc_name):
        for comp in self._rtsprofile.components:
            if rtc_name == str(comp.path_uri):
                return comp
        raise wasanbon.RTCNotFoundException()

    def active_conf_set(self, rtc_name):
        return self._rtc(rtc_name).active_configuration_set
        
        
    def active_conf_data(self, rtc_name):

        for conf in self._rtc(rtc_name).configuration_sets:
            if conf.id == self._rtc(rtc_name).active_configuration_set:
                return conf.configuration_data
        #        for d in conf.configuration_data:
        #            ret_dict[str(d.name)] = str(d.data)

        return []

    def set_active_conf_data(self, rtc_name, key, value):
        for conf in self._rtc(rtc_name).configuration_sets:
            if conf.id == self._rtc(rtc_name).active_configuration_set:
                for conf_data in conf.configuration_data:
                    if conf_data.name == key:
                        conf_data.data = value
        

    def update(self):
        bakfile = self._filename + wasanbon.timestampstr()
        if os.path.isfile(bakfile):
            os.remove(bakfile)
        os.rename(self._filename, bakfile)
        fout = open(self._filename, "w")
        fout.write(self._rtsprofile.save_to_xml())
        fout.close()
