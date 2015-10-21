"""
imports
"""
from .RootCmd import RootCmd
from ..downloader.manager import manager

from ..helpers.logging_helper import logging_helper
from ..helpers.argument_helper import argument_helper

class CmdDownload(RootCmd):
    """
    command to download a specific tarball based on package name and build number
    """
    @classmethod
    def usage(cls):
        return {
            'name': 'download',
            'args': '',
            'desc': 'downloads a selected version of a package'
        }

    @classmethod
    def action(cls, args):
        has_type = 'type' in args.keys()
        has_package = 'package' in args.keys()
        has_build = 'build' in args.keys()
        has_version = 'version' in args.keys()

        build_number = None

        if has_build == True:
            build_number = args['build']

        if has_build == False and has_version == True:
            logging_helper.getLogger().error('Could not resolve the build number from the version!')

        if has_type == True and has_package == True and has_build == True:
            release_type = args['type']
            package_name = args['package']
            manager.DownloadPackageTarball(release_type, package_name, build_number)
        else:
            if has_type == False:
                logging_helper.getLogger().error('Cannot download package without a release type set. Use the "type" command.')

            if has_package == False:
                logging_helper.getLogger().error('Cannot download package without a package set. Use the "package" command.')

            if has_build == False:
                logging_helper.getLogger().error('Cannot download package without a version set. Use the "version" command or the "build" command.')
        print('====================')

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        arguments = argument_helper.parse(line_text)
        result = cls.query(arguments)
        if result[0] == True:
            cls.action(context)
        else:
            ret_val = 'Fatal error, cannot download!'
            logging_helper.getLogger().error(ret_val)
        return ret_val