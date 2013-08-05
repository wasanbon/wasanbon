import os, sys


import wasanbon



class RTCProfileNotFoundError(exception):
    def __init__(self):
        pass

class RTC():
    
    def __init__(self, path):
        self._profile = None
        pass

    def build(self):
        pass
    
    @parameter
    def profile(self):
        return self._profile
