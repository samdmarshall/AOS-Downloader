class cmd_version(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'version',
            'args': '<version name>',
            'desc': 'selects the current release version'
        };
    
    @classmethod
    def validValues(cls, aosd_instance):
        return [];
    
    @classmethod
    def action(cls, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(), input);
        else:
            return (False, None);