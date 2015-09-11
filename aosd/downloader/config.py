from ..logging_helper import *

import plistlib
import urlparse

from .utilities import *

class config(object):
    
    @classmethod
    def read(cls):
        config_contents = {};
        config_plist_path = utilities.GetConfigurationPlistPath();
        if os.path.exists(config_plist_path) == False:
            logging_helper.getLogger().error(': Fatal error, cannot locate the configuration plist. Use the "config defaults" command to restore defaults.');
        else:
            config_contents = plistlib.readPlist(config_plist_path);
        return config_contents;
    
    @classmethod
    def write(cls, new_settings):
        config_plist_path = utilities.GetConfigurationPlistPath();
        plistlib.writePlist(new_settings, config_plist_path);
    
    @classmethod
    def getUpdateURL(cls):
        settings = cls.read();
        return settings['core_url'];
    
    @classmethod
    def setUpdateURL(cls, url):
        settings = cls.read();
        new_url = urlparse.urlparse(url);
        if bool(new_url.scheme) == True:
            settings['core_url'] = url;
            cls.write(settings);
        else:
            logging_helper.getLogger().error(': The supplied URL is not valid (lacks a scheme).');
        
    @classmethod
    def toggleFirstRun(cls):
        settings = cls.read();
        value = settings['first_run'];
        if value == True:
            settings['first_run'] = False;
            cls.write(settings);
    
    @classmethod
    def getFirstRun(cls):
        settings = cls.read();
        return settings['first_run'];
    
    @classmethod
    def defaults(cls):
        default_values = {
            'core_url': 'https://raw.githubusercontent.com/samdmarshall/AOS-Downloader/refactor/aosd/data/',
            'first_run': True,
            'requests_via_https': True,
        };
        cls.write(default_values);