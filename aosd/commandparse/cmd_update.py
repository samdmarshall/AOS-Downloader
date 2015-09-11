from ..downloader.update import *

class cmd_update(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'update',
            'args': '',
            'desc': 'updates the current open source manifests'
        };
    
    @classmethod
    def query(cls, args):
        return (True, None);
    
    @classmethod
    def action(cls, args):
        update.fetch();
        print '====================';