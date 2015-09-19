from __future__ import absolute_import

from ..logging_helper import logging_helper
from ..subprocess_helper import subprocess_helper

from .utilities import utilities

import os
import plistlib

class Hashes(object):
    
    @classmethod
    def manifest(cls):
        hashes_manifest_path = utilities.getlookupplistpath('hashes')
        hashes_manifest = plistlib.readPlist(hashes_manifest_path)
        return hashes_manifest
    
    @classmethod
    def add(cls, release_type, package_name, build_number, hash_string):
        if cls.get(release_type, package_name, build_number) == '':
            hashes_manifest = cls.manifest()
            check_release = hashes_manifest.get(release_type, None)
            if check_release != None:
                check_package = check_release.get(package_name, None)
                if check_package != None:
                    check_package[build_number] = {'sha256': hash_string}
                    plistlib.writePlist(hashes_manifest, utilities.getlookupplistpath('hashes'))
                    logging_helper.getLogger().info('Added hash for "'+package_name+'-'+build_number+'"')
    
    @classmethod
    def get(cls, release_type, package_name, build_number):
        hashes_manifest = cls.manifest()
        recorded_hash = ''
        check_release = hashes_manifest.get(release_type, None)
        if check_release != None:
            check_package = check_release.get(package_name, None)
            if check_package != None:
                check_build = check_package.get(build_number, None)
                if check_build != None:
                    recorded_hash = check_build.get('sha256', '')
        return recorded_hash
    
    @classmethod
    def calculate(cls, output_file, remove_after=True):
        output = subprocess_helper.make_call(('shasum', '-a', '256', output_file))
        file_hash = output.split()[0]
        if remove_after == True:
            os.remove(output_file)
        return file_hash
    
    @classmethod
    def ValidateDownloadedFileByHash(cls, output_file, release_type, package_name, build_number, remove_after=True):
        # get the file hash of what we downloaded
        file_hash = cls.calculate(output_file, remove_after)
        # look up any existing hash
        recorded_hash = cls.get(release_type, package_name, build_number)
        matching_hash = False
        if recorded_hash != '':
            matching_hash = recorded_hash == file_hash
        else:
            logging_helper.getLogger().error('There is no hash on record for "'+package_name+'-'+build_number+'". If you were able to download a tarball, then please submit a pull request to update "https://github.com/samdmarshall/AOS-Downloader/blob/master/aosd/data/hashes.plist" to reflect the correct hash.')
        return (matching_hash, file_hash, recorded_hash)