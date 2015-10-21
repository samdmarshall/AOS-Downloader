"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.cacher import cacher

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper


class CmdCache(RootCmd):
    """
    command to operate on the manifest cache files
    """

    @classmethod
    def usage(cls):
        """
        usage info for the command
        """
        return {
            'name': 'cache',
            'args': '[download_type|download_all|clear_type|clear_all|rebuild|setup]',
            'desc': 'performs an action on the cache of a particular release type'
        }

    @classmethod
    def valid_values(cls, release_type=None, version=None):
        """
        arguments that this command takes
        """
        return ['download_type', 'download_all', 'clear_type', 'clear_all', 'rebuild', 'setup']

    @classmethod
    def query(cls, args):
        """
        validate the arguments passed to this command
        """
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(), args[0])
        else:
            return (False, None)

    @classmethod
    def action(cls, args):
        """
        performs the selected cache operation
        """
        cache_action = args['cache']

        release_type = None
        if 'type' in args.keys():
            release_type = args['type']
        if cache_action == 'download_type' or cache_action == 'download_all':
            if cache_action == 'download_type':
                cacher.fetch(release_type, None)
            if cache_action == 'download_all':
                cacher.fetch(None, None)
            logging_helper.getLogger().info('Download complete, please run the "cache rebuild" command to update the index')
        if cache_action == 'clear_type':
            cacher.flush(release_type, None)
        if cache_action == 'clear_all':
            cacher.flush(None, None)
        if cache_action == 'rebuild':
            cacher.rebuild()
        if cache_action == 'setup':
            cacher.clean()
        print('====================')

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        arguments = argument_helper.parse(line_text)
        result = cls.query(arguments)
        if result[0] == True:
            context['cache'] = result[1]
            cls.action(context)
        else:
            ret_val = 'Invalid cache command!'
            logging_helper.getLogger().error(ret_val)
        return ret_val