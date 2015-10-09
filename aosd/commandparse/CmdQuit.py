"""
imports
"""
from .RootCmd import RootCmd
import sys

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
