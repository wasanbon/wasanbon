#!/usr/bin/env python
import os, sys
import wasanbon

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, clean, force, verbose):
        sys.stdout.write(' This funciton is currently deplicated.')
        raise wasanbon.InvalidUsageException()
