# -*- encoding: utf-8 -*-
"""
runtests.core
~~~~~~~~~

This module implements the core functionality of runtests.
"""
import os
import subprocess
import sys

import yaml


def command(cmd, env=None):
    '''
    Execute ``cmd`` and return (code, stdout, and stderr).
    The actual environment is updated with ``env`` dict,
    and the command is run.
    '''
    environ = dict(os.environ)
    environ.update(env or {})
    process = subprocess.Popen(cmd,
        universal_newlines=True,
        shell=True,
        env=environ,
        stdin=subprocess.PIPE,
        stdout=sys.stdout,
        stderr=sys.stdout,
        bufsize=0,
        cwd=None,
    )
    out, err = process.communicate()
    return process.returncode

def handle_commands(cmds, env=None):
    '''
    Execute commands in ``cmds`` list.
    ``env`` dict is passed to each command.

    The execution loop breaks when one of the commands exits with non-zero.
    '''
    for cmd in cmds:
        print cmd
        code = command(cmd, env=env)
        if code > 0:
            return False
    return True

def execute(filename):
    '''
    Load ``filename`` and execute defined script in a matrix.
    '''
    config = yaml.load(open(filename))
    yep = nope = 0
    for env in config.get('env', []):
        print 'running test... %r' % (env, )
        if not handle_commands(config.get('before_script', []), env=env):
            nope += 1
            continue
        try:
            if not handle_commands(config.get('script', []), env=env):
                nope += 1
                continue
            yep += 1
        finally:
            # Cleanup
            handle_commands(config.get('after_script', []), env=env)
            print 'test finished...'
    print 'TOTAL', yep + nope
    print 'SUCCESS', yep
    print 'FAILURE', nope
    return yep
