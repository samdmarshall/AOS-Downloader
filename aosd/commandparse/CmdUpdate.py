"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.update import update

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdUpdate(RootCmd):
    """
    command for fetching updates to the releases plist
    """

    @classmethod
    def usage(cls):
        """
        command usage
        """
        return {
            'name': 'update',
            'args': '',
            'desc': 'updates the current open source manifests'
        }

    @classmethod
    def action(cls, args):
        """
        calls to perform the update
        """
        update.fetch()
        print('====================')

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        arguments = argument_helper.parse(line_text)
        result = cls.query(arguments)
        if result[0] == True:
            cls.action(context)
        else:
            ret_val = 'Fatal error, cannot update!'
            logging_helper.getLogger().error(ret_val)
        return ret_val