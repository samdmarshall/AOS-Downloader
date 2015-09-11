from ..logging_helper import *

from ..downloader.config import *


class cmd_config(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'config',
            'args': '[display|set <key> <value>|defaults]',
            'desc': 'allows for a the configuration file to be updated '
        };
    
    @classmethod
    def validValues(cls):
        return ['display', 'set', 'defaults'];
    
    @classmethod
    def query(cls, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(), args);
        else:
            return (False, None);
    
    @classmethod
    def action(cls, args):
        if args[0] == 'display':
            settings = config.read();
            logging_helper.getLogger().info(': Current Configuration');
            for key in settings:
                print '"'+key+'": "'+str(settings[key])+'"';
        if args[0] == 'set':
            if len(args) == 3:
                if args[1] == 'core_url':
                    config.setUpdateURL(args[2]);
                elif args[1] == 'download_directory':
                    config.setDownloadDir(args[2]);
                elif args[1] == 'first_run':
                    logging_helper.getLogger().info(': If you want to reset to original state, please use the "config defaults" command.');
                else:
                    logging_helper.getLogger().error(': Attempting to set unrecognized key "'+args[1]+'".')
        if args[0] == 'defaults':
            config.defaults();
            logging_helper.getLogger().info(': Default configuration has been restored.');