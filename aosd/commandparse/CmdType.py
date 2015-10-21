"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.releases import releases

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdType(RootCmd):

    @classmethod
    def usage(cls):
        return {
            'name': 'type',
            'args': '['+'|'.join(releases.get())+']',
            'desc': 'selects the current release type'
        }

    @classmethod
    def valid_values(cls):
        return releases.get()

    @classmethod
    def query(cls, args):
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(), args[0])
        else:
            return (False, None)

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        arguments = argument_helper.parse(line_text)
        result = cls.query(arguments)
        if result[0] == True:
            context.clear()
            context['type'] = result[1]
            cls.action(context)
        else:
            ret_val = 'Invalid release type!' 
            logging_helper.getLogger().error(ret_val)
        return ret_val