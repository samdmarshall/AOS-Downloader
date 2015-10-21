"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.Packages import Packages

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdPackage(RootCmd):

    @classmethod
    def usage(cls):
        return {
            'name': 'package',
            'args': '<package name>',
            'desc': 'selects a package by name from the current release type'
        }

    @classmethod
    def valid_values(cls, release_type, release_version):
        return Packages.get(release_type, release_version)

    @classmethod
    def query(cls, release_type, version, args):
        # only use the first value
        if len(args) > 0:
            build_number = None
            if version != None:
                build_number = Packages.resolveNumberFromVersion(release_type, version, args[0])
            return (args[0] in cls.valid_values(release_type, version), [args[0], build_number])
        else:
            return (False, None)

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        if context.has_key('type'):
            release_type = context.get('type', None)
            release_version = None
            if context.has_key('version'):
                release_version = context.get('version', None)
            arguments = argument_helper.parse(line_text)
            result = cls.query(release_type, release_version, arguments)
            if result[0] == True:
                context['package'] = result[1][0]
                if context.has_key('version'):
                    context['build'] = result[1][1]
                cls.action(context)
            else:
                ret_val = 'Invalid package name!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type before using the "package" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val