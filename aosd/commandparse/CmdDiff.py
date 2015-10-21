"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.diff import diff
from ..downloader.Builds import Builds

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdDiff(RootCmd):
    """
    command to create a diff of a package given two build numbers
    """

    @classmethod
    def usage(cls):
        """
        usage info for this command
        """
        return {
            'name': 'diff',
            'args': '<ancestor version> <child version>',
            'desc': 'selects a build version for the currently selected package'
        }

    @classmethod
    def valid_values(cls, release_type, package_name):
        """
        TODO: look into auto-complete for both arguments
        """
        return Builds.get(release_type, package_name)

    @classmethod
    def query(cls, release_type, package_name, args):
        """
        validate both values passed are build numbers that exist for the selected package
        """
        # only use the first value
        if len(args) == 2:
            valid_values = cls.valid_values(release_type, package_name)
            ancestor_valid = args[0] in valid_values
            child_valid = args[1] in valid_values
            return (ancestor_valid == True and child_valid == True, args)
        else:
            return (False, None)

    @classmethod
    def action(cls, args):
        """
        download both and perform the diff
        """
        has_type = 'type' in args.keys()
        has_package = 'package' in args.keys()

        build_numbers = args['diff']

        if has_type == True and has_package == True:
            release_type = args['type']
            package_name = args['package']
            diff.perform(release_type, package_name, build_numbers)
        else:
            if has_type == False:
                logging_helper.getLogger().error('Cannot download package without a release type set. Use the "type" command.')

            if has_package == False:
                logging_helper.getLogger().error('Cannot download package without a package set. Use the "package" command.')
        print('====================')

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        if context.has_key('type') and context.has_key('package'):
            release_type = context.get('type', None)
            package_name = context.get('package', None)
            arguments = argument_helper.parse(line_text)
            result = cls.query(release_type, package_name, arguments)
            if result[0] == True:
                context['diff'] = result[1]
                cls.action(context)
            else:
                ret_val = 'Invalid build numbers!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type and package before using the "diff" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val