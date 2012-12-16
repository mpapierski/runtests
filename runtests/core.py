# -*- encoding: utf-8 -*-
"""
runtests.core
~~~~~~~~~

This module implements the core functionality of runtests.
"""
import os
import sys
import time

import yaml

from runtests.shell import Shell

def execute(filename):
    '''
    Load ``filename`` and execute defined script in a matrix.
    '''
    config = yaml.load(open(filename))
    start = time.time()
    yep = nope = 0
    for env in config.get('env', []):
        shell = Shell()
        shell.execute('export ' + env)
        try:
            for before_script in config.get('before_script', []):
                shell.execute(before_script)
            for script in config.get('script', []):
                shell.execute(script)
        finally:
            # Cleanup
            w = shell.wait()
            del shell
            # Cleanup is done in fresh shell.
            cleanup_shell = Shell()
            cleanup_shell.execute('export ' + env)
            try:
                for after_script in config.get('after_script', []):
                    cleanup_shell.execute(after_script)
            finally:
                cleanup_shell.wait()
                del cleanup_shell

            if w > 0:
                nope += 1
                print '✖ failure'
            else:
                yep += 1
                print '✔ success' 
    print
    print 'summary'
    print 'passes: %d' % (yep, )
    print 'failures: %d' % (nope, )
    print 'duration: %.2fs' % (time.time() - start, )
    return nope == 0