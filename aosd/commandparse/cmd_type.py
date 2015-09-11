from ..downloader.releases import *

def FormatForArgumentDisplay():
    return '['+'|'.join(releases.GetReleases())+']';

class cmd_type(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'type',
            'args': FormatForArgumentDisplay(),
            'desc': 'selects the current release type'
        };
    
    @classmethod
    def validValues(cls):
        return releases.GetReleases();
    
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
        return;