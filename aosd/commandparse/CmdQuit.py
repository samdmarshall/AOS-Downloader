import sys

class CmdQuit(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'quit',
            'args': '',
            'desc': 'Quits aosd'
        }
    
    @classmethod
    def valid_values(cls):
        return []
    
    @classmethod
    def query(cls, args):
        return (True, None)
    
    @classmethod
    def action(cls, args):
        print('Quitting!')
        sys.exit()