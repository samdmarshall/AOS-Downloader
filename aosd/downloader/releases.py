from __future__ import absolute_import

from ..logging_helper import logging_helper

import os
import plistlib
from .utilities import utilities

class releases(object):

    @classmethod
    def get(cls):
        releases = []
        releases_dict_path = utilities.getreleaseplistpath()
        if os.path.exists(releases_dict_path) == True:
            releases_dict = plistlib.readPlist(releases_dict_path)
            releases_results = list(map(lambda release: release['package_name'], releases_dict))
            if len(releases_results) > 0:
                releases = releases_results
            else:
                logging_helper.getLogger().error('Could not find any release types in the releases manifest file. Please run the "update" command.')
        else:
            logging_helper.getLogger().error('Could not find the releases manifest file. Please run the "update" command.')
        return releases

    @classmethod
    def get_display_name(cls, release_type):
        release_display_name = ''
        releases_dict_path = utilities.getreleaseplistpath()
        if os.path.exists(releases_dict_path) == True:
            releases_dict = plistlib.readPlist(releases_dict_path)
            type_results = list((item for item in releases_dict if item['package_name'] == release_type))
            if len(type_results) > 0:
                release_display_name = type_results[0]['display_name']
            else:
                logging_helper.getLogger().error('Could not find a version in the releases manifest file matching type "'+release_type+'". Please run the "update" command.')
        else:
            logging_helper.getLogger().error('Could not find the releases manifest file. Please run the "update" command.')
        return release_display_name

    @classmethod
    def getInfo(cls, release_type, version):
        info_dict = {}
        if release_type != None:
            if version != None:
                type_plist_path = utilities.getlookupplistpath(release_type)
                if os.path.exists(type_plist_path) == True:
                    versions_dict = plistlib.readPlist(type_plist_path)
                    version_results = list((item for item in versions_dict if item['name'] == version))
                    if len(version_results) > 0:
                        info_dict = version_results[0]
                    else:
                        logging_helper.getLogger().error('Could not find version "'+version+'" for release type "'+release_type+'". If you think this is an error, run the "update" command.')
                else:
                    logging_helper.getLogger().error('Could not find a versions manifest for release type "'+release_type+'". If you think this is an error, run the "update" command.')
            else:
                logging_helper.getLogger().error('Must supply a version number!')
        return info_dict
