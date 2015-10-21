"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.Builds import Builds

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper


class CmdBuild(RootCmd):
    """
    command to select a build number of a package
    """

    @classmethod
    def usage(cls):
        """
        command usage information
        """
        return {
            'name': 'build',
            'args': '<build version>',
            'desc': 'selects a build version for the currently selected package'
        }

    @classmethod
    def valid_values(cls, release_type, package_name):
        """
        fetches the builds for a specific package
        """
        return Builds.get(release_type, package_name)

    @classmethod
    def query(cls, release_type, package_name, args):
        """
        validate the value passed to the command
        """
        # only use the first value
        if len(args) > 0:
            return (args[0] in cls.valid_values(release_type, package_name), args[0])
        else:
            return (False, None)

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        if context.has_key('type') and context.has_key('package'):
            release_type = context.get('type', None)
            package_name = context.get('package', None)
            arguments = argument_helper.parse(line_text)
            result = cls.query(release_type, package_name, arguments)
            if result[0] == True:
                if context.has_key('version'):
                    del context['version']
                context['build'] = result[1]
                cls.action(context)
            else:
                ret_val = 'Invalid build number!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type and package before using the "build" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val