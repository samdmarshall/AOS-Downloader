"""
imports
"""
from ..logging_helper import logging_helper

from ..downloader.diff import diff
from ..downloader.builds import builds

class CmdDiff(object):
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
        return builds.get(release_type, package_name)

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
                logging_helper.getLogger().error(': Cannot download package without a release type set. Use the "type" command.')

            if has_package == False:
                logging_helper.getLogger().error(': Cannot download package without a package set. Use the "package" command.')
        print('====================')
