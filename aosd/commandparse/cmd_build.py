from ..downloader.builds import *

class cmd_build(object):
    @classmethod
    def usage(cls):
        return {
            'name': 'build',
            'args': '<build version>',
            'desc': 'selects a build version for the currently selected package'
        };
    
    @classmethod
    def validValues(cls, release_type, package_name):
        return builds.get(release_type, package_name);

    @classmethod
    def query(cls, release_type, package_name, args):
        # only use the first value;
        if len(args) > 0:
            input = args[0];
            return (input in cls.validValues(release_type, package_name), input);
        else:
            return (False, None);

    @classmethod
    def action(cls, args):
        return;