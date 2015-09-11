from ..logging_helper import *

from ..downloader.cacher import *

class cmd_cache(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'cache',
            'args': '[download_type|download_all|clear_type|clear_all|rebuild|setup]',
            'desc': 'performs an action on the cache of a particular release type'
        };
    
    @classmethod
    def validValues(cls, release_type=None, version=None):
        return ['download_type', 'download_all', 'clear_type', 'clear_all', 'rebuild', 'setup'];
    
    @classmethod
    def query(cls, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(), input);
        else:
            return (False, None);
    
    @classmethod
    def action(cls, args):
        cache_action = args['cache'];
        
        release_type = None;
        if 'type' in args.keys():
            release_type = args['type'];
        if cache_action == 'download_type' or cache_action == 'download_all':
            if cache_action == 'download_type':
                cacher.fetch(release_type, None);
            if cache_action == 'download_all':
                cacher.fetch(None, None);
            logging_helper.getLogger().info(': Download complete, please run the "cache rebuild" command to update the index');
        if cache_action == 'clear_type':
            cacher.flush(release_type, None);
        if cache_action == 'clear_all':
            cacher.flush(None, None);
        if cache_action == 'rebuild':
            cacher.rebuild();
        if cache_action == 'setup':
            cacher.flush(None, None);
            cacher.fetch(None, None);
            cacher.rebuild();
        print '====================';