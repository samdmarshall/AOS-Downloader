from ..downloader.versions import *

class cmd_version(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'version',
            'args': '<version name>',
            'desc': 'selects the current release version'
        };
    
    @classmethod
    def validValues(cls, release_type):
        return versions.get(release_type);
    
    @classmethod
    def query(cls, release_type, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(release_type), input);
        else:
            return (False, None);
    
    @classmethod
    def action(cls, args):
        return;