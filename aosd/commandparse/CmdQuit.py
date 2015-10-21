"""
imports
"""
from .RootCmd import RootCmd
import sys

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdQuit(RootCmd):

    @classmethod
    def usage(cls):
        return {
            'name': 'quit',
            'args': '',
            'desc': 'Quits aosd'
        }

    @classmethod
    def action(cls, args):
        sys.exit()

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        arguments = argument_helper.parse(line_text)
        result = cls.query(arguments)
        if result[0] == True:
            cls.action(context)
        else:
            ret_val = 'Fatal error, cannot quit!'
            logging_helper.getLogger().error(ret_val)
        return ret_val