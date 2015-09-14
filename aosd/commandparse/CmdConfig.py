"""
imports
"""
from .RootCmd import RootCmd
from ..logging_helper import logging_helper
from ..downloader.config import config

class CmdConfig(RootCmd):
    """
    command to modify the configuration of the `aosd` utility
    """

    @classmethod
    def usage(cls):
        """
        usage info for the command
        """
        return {
            'name': 'config',
            'args': '[display|set <key> <value>|defaults]',
            'desc': 'allows for a the configuration file to be updated '
        }

    @classmethod
    def valid_values(cls):
        """
        arguments that this command takes
        """
        return ['display', 'set', 'defaults']

    @classmethod
    def query(cls, args):
        """
        validates the argument passed to this command
        """
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(), args)
        else:
            return (False, None)

    @classmethod
    def action(cls, args):
        """
        modify the config file
        """
        if args[0] == 'display':
            settings = config.read()
            logging_helper.getLogger().info('Current Configuration:')
            for key in settings:
                print('"'+key+'": "'+str(settings[key])+'"')
        if args[0] == 'set':
            if len(args) == 3:
                if args[1] == 'core_url':
                    config.setUpdateURL(args[2])
                elif args[1] == 'download_directory':
                    config.setDownloadDir(args[2])
                elif args[1] == 'verbose_logging':
                    config.setVerboseLogging(args[2])
                elif args[1] == 'requests_via_https':
                    config.setUseHTTPS(args[2])
                elif args[1] == 'first_run':
                    logging_helper.getLogger().info('If you want to reset to original state, please use the "config defaults" command.')
                else:
                    logging_helper.getLogger().error('Attempting to set unrecognized key "'+args[1]+'".')
        if args[0] == 'defaults':
            config.defaults()
            logging_helper.getLogger().info('Default configuration has been restored.')
        print('====================')
