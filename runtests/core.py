# -*- encoding: utf-8 -*-
"""
runtests.core
~~~~~~~~~

This module implements the core functionality of runtests.
"""
import os
import sys

import yaml

from runtests.shell import Shell

def handle_commands(shell, cmds, env=None):
    '''
    Execute commands in ``cmds`` list.
    ``env`` dict is passed to each command.
    Each of the command is sent to the ``shell``.

    The execution loop breaks when one of the commands exits with non-zero.
    '''
    for cmd in cmds:
        shell.execute(cmd)

def execute(filename):
    '''
    Load ``filename`` and execute defined script in a matrix.
    '''
    config = yaml.load(open(filename))
    yep = nope = 0
    for env in config.get('env', []):
        shell = Shell()
        print '$ export ' + env
        shell.execute('export ' + env)
        try:
            for before_script in config.get('before_script', []):
                shell.execute(before_script)
            for script in config.get('script', []):
                shell.execute(script)
        finally:
            # Cleanup
            w = shell.wait()
            # Cleanup is done in fresh shell.
            cleanup_shell = Shell()
            for after_script in config.get('after_script', []):
                cleanup_shell.execute(after_script)
            if w > 0:
                nope += 1
            else:
                yep += 1
    print 'success:', yep
    print 'failure:', nope
    return nope == 0