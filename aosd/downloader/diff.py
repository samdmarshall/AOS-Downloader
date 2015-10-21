from __future__ import absolute_import

from ..helpers.logging_helper import logging_helper
from ..helpers.subprocess_helper import subprocess_helper

from .manager import manager
from .config import config

import os

class diff(object):

    @classmethod
    def perform(cls, release_type, package_name, diff_numbers):
        ancestor_build = manager.ValidateAndDownload(release_type, package_name, diff_numbers[0])
        child_build = manager.ValidateAndDownload(release_type, package_name, diff_numbers[1])
        if ancestor_build != None and child_build != None:
            if os.path.exists(ancestor_build) == True and os.path.exists(child_build) == True:
                # download was successful
                diff_path = os.path.join(config.getDownloadDir(), package_name+'.diff')
                logging_helper.getLogger().info('Creating source diff...')
                cls.make(ancestor_build, child_build, diff_path)
                logging_helper.getLogger().info('Package diff written to "'+diff_path+'"!')
            else:
                logging_helper.getLogger().error('There was an error with finding the downloaded packages!')
        else:
            logging_helper.getLogger().error('One or more of the build numbers supplied was not valid. Please use the "--list" command to see available build numebrs.')

    @classmethod
    def make(cls, ancestor_build, child_build, diff_path):
        output = subprocess_helper.make_call(('diff', '-r', ancestor_build, child_build))
        diff_file = open(diff_path, 'w')
        diff_file.write(output)
        diff_file.close()
