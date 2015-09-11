import sys

class cmd_quit(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'quit',
            'args': '',
            'desc': 'Quits aosd'
        };
    
    @classmethod
    def validValues(cls):
        return [];
    
    @classmethod
    def query(cls, args):
        return (True, None);
    
    @classmethod
    def action(cls, args):
        print('Quitting!');
        sys.exit();