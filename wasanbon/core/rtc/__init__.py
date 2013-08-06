import os, sys


import wasanbon
from repository import *


class RTCProfileNotFoundError(Exception):
    def __init__(self):
        pass

class RTC():
    
    def __init__(self, path):
        self._profile = None
        pass

    def build(self):
        pass
    
    @property
    def profile(self):
        return self._profile
