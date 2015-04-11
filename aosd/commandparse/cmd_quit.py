import sys

class cmd_quit(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'quit',
            'args': 'None',
            'desc': 'Quits aosd'
        };
    
    @classmethod
    def action(cls, args):
        print 'Quitting!';
        sys.exit();