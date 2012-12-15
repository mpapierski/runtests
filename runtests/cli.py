"""
runtests.cli
~~~~~~~~~

This module povides the CLI interface to runtests.
"""
import sys
import logging
from optparse import OptionParser

from runtests.core import execute

logging.basicConfig(level=logging.DEBUG)

def main():
    '''Main entry point executed from your shell.'''
    parser = OptionParser()
    parser.add_option('-c', '--config', dest='config',
        help='configuration file')
    (options, args) = parser.parse_args()
    if not execute(options.config):
        sys.exit(1)
