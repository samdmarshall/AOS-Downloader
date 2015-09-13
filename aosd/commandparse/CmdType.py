from ..downloader.releases import releases

def FormatForArgumentDisplay():
    return '['+'|'.join(releases.get())+']'

class CmdType(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'type',
            'args': FormatForArgumentDisplay(),
            'desc': 'selects the current release type'
        }
    
    @classmethod
    def valid_values(cls):
        return releases.get()
    
    @classmethod
    def query(cls, args):
        # only use the first value
        if len(args) > 0:
            input = args[0]
            return (input in cls.valid_values(), input)
        else:
            return (False, None)
    
    @classmethod
    def action(cls, args):
        return