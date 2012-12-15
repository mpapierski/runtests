# -*- encoding: utf-8 -*-
"""
runtests.shell
~~~~~~~~~

This module encapsulates a shell in a class.
"""
import os
import sys
import subprocess
import threading

from StringIO import StringIO

class Shell(object):
    '''
    Spawns new $SHELL piped to stdout.
    '''
    def __init__(self):
        self.shell = os.getenv('SHELL')
        self.process = subprocess.Popen(self.shell,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=sys.stderr,
            stderr=sys.stdout)
        # This causes shell to exit when any of the commands returns non-zero.
        self.execute('set -e')

    def wait(self):
        self.execute('exit 0')
        self.process.poll()
        self.process.wait()
        return self.process.returncode

    def execute(self, command):
        '''
        Send a command to the shell.
        '''
        self.process.stdin.write(command + '\n')
        self.process.poll()
