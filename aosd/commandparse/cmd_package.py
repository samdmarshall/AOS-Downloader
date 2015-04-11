class cmd_package(object):
    
    @classmethod
    def usage(cls):
        return {
            'name': 'package',
            'args': '<package name>',
            'desc': 'selects a package by name from the current release type'
        };
    
    @classmethod
    def validValues(cls, release_type=None, version=None):
        return [];
    
    @classmethod
    def action(cls, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(), input);
        else:
            return (False, None);