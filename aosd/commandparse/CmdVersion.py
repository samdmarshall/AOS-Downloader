"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.versions import versions
from ..downloader.cacher import cacher

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdVersion(RootCmd):
    """
    command to assign a release version
    """

    @classmethod
    def usage(cls):
        """
        usage for this command
        """
        return {
            'name': 'version',
            'args': '<version name>',
            'desc': 'selects the current release version'
        }

    @classmethod
    def valid_values(cls, release_type):
        """
        returns the versions available for this release type
        """
        return versions.get(release_type)

    @classmethod
    def query(cls, release_type, args):
        """
        Validate that what was passed to the command
        """
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(release_type), args[0])
        else:
            return (False, None)

    @classmethod
    def action(cls, args):
        """
        pre-fetch the manifest for this version
        """
        cacher.fetch(args['type'], args['version'])
        print('====================')

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        if context.has_key('type'):
            release_type = context.get('type', None)
            arguments = argument_helper.parse(line_text)
            result = cls.query(release_type, arguments)
            if result[0] == True:
                context['version'] = result[1]
                if context.has_key('build'):
                    del context['build']
                if context.has_key('package'):
                    package_result = CmdPackage.query(release_type, result[1], [context['package']])
                    if package_result[0] == True:
                        context['build'] = package_result[1][1]
                cls.action(context)
            else:
                ret_val = 'Invalid version name!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type before using the "version" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val