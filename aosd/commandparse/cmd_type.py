class cmd_type(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'type',
            'args': '[mac|ios|dev|server]',
            'desc': 'selects the current release type'
        };
    
    @classmethod
    def validValues(cls):
        return ['mac', 'ios', 'dev', 'server'];
    
    @classmethod
    def action(cls, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(), input);
        else:
            return (False, None);