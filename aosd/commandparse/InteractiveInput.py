import sys
import platform
if sys.platform == 'darwin' and not 'ppc' in platform.machine():
     from .readline_unsorted.cmd import *
else:
    from cmd import Cmd

from ..logging_helper import logging_helper
from ..subprocess_helper import subprocess_helper

from .CmdQuit import CmdQuit
from .CmdType import CmdType
from .CmdPackage import CmdPackage
from .CmdVersion import CmdVersion
from .CmdCache import CmdCache
from .CmdUpdate import CmdUpdate
from .CmdDownload import CmdDownload
from .CmdBuild import CmdBuild
from .CmdConfig import CmdConfig
from .CmdDiff import CmdDiff
from .CmdHash import CmdHash
from .CmdList import CmdList

from ..downloader.releases import releases
from ..version import __version__ as AOSD_VERSION

class InteractiveInput(Cmd):
    prompt = ':> '
    display_info = {}
    quitOnError = True

    def get_arguments(self, arguments_str):
        arguments_str = str(arguments_str)
        arg_words = []
        input_split = arguments_str.split(' ')
        offset = 0
        counter = 0
        current_word = ''
        while counter < len(input_split):
            word = input_split[counter]
            current_word += word
            if len(current_word) == 0:
                offset += 1
            else:
                if offset >= 0:
                    curr = offset + len(word)
                    prev = curr - 1
                    if arguments_str[prev:curr] != '\\':
                        arg_words.append(current_word)
                        current_word = ''
                    else:
                        current_word += ' '
                    offset += len(word) + 1
            counter += 1
        return arg_words

    def DisplayUsage(self, cmd_usage):
        print('Command: ')
        print('%10s %s\n%10s %s\n' % (cmd_usage['name'], cmd_usage['args'], '-', cmd_usage['desc']))

    def GenerateInfo(self):
        info = []
        if 'type' in self.display_info.keys():
            info.append('Type: %s' % releases.get_display_name(self.display_info['type']))
        if 'version' in self.display_info.keys():
            info.append('Version: %s' % self.display_info['version'])
        if 'package' in self.display_info.keys():
            info.append('Package: %s' % self.display_info['package'])
        if 'build' in self.display_info.keys():
            info.append('Build: %s' % self.display_info['build'])
        return '\n'.join(info)

    def postcmd(self, stop, line):
        info_string = self.GenerateInfo()
        if len(info_string) > 0:
            print('\n'+info_string)
        return stop
        
    def emptyline(self):
        # do nothing as repeating the last command can be dangerous
        return None
    
    # Quit
    def help_quit(self):
        self.DisplayUsage(CmdQuit.usage())

    def do_quit(self, line):
        ret_val = None
        result = CmdQuit.query(self.get_arguments(line))
        if result[0] == True:
            CmdQuit.action(self.display_info)
        else:
            ret_val = 'Fatal error, cannot quit!'
            logging_helper.getLogger().error(ret_val)
        return ret_val if self.quitOnError == True else None

    # Release type
    def help_type(self):
        self.DisplayUsage(CmdType.usage())

    def do_type(self, line):
        ret_val = None
        result = CmdType.query(self.get_arguments(line))
        if result[0] == True:
            self.display_info = {}
            self.display_info['type'] = result[1]
            CmdType.action(self.display_info)
        else:
            ret_val = 'Invalid release type!' 
            logging_helper.getLogger().error(ret_val)
        return ret_val

    def complete_type(self, text, line, begidx, endidx):
        completions = []
        release_types = CmdType.valid_values()
        if not text:
            completions = release_types[:]
        else:
            completions = [item for item in release_types if item.startswith(text)]
        return completions

    # Package
    def help_package(self):
        self.DisplayUsage(CmdPackage.usage())

    def do_package(self, line):
        ret_val = None
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type']
            release_version = None
            if 'version' in self.display_info.keys():
                release_version = self.display_info['version']
            result = CmdPackage.query(release_type, release_version, self.get_arguments(line))
            if result[0] == True:
                self.display_info['package'] = result[1][0]
                if 'version' in self.display_info.keys():
                    self.display_info['build'] = result[1][1]
                CmdPackage.action(self.display_info)
            else:
                ret_val = 'Invalid package name!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type before using the "package" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val if self.quitOnError == True else None

    def complete_package(self, text, line, begidx, endidx):
        completions = []
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type']
            release_version = None
            if 'version' in self.display_info.keys():
                release_version = self.display_info['version']
            package_names = CmdPackage.valid_values(release_type, release_version)
            if not text:
                completions = package_names[:]
            else:
                completions = [item for item in package_names if item.startswith(text)]
        return completions

    # Release Version
    def help_version(self):
        self.DisplayUsage(CmdVersion.usage())

    def do_version(self, line):
        ret_val = None
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type']
            result = CmdVersion.query(release_type, self.get_arguments(line))
            if result[0] == True:
                self.display_info['version'] = result[1]
                if 'build' in self.display_info.keys():
                    del self.display_info['build']
                if 'package' in self.display_info.keys():
                    package_result = CmdPackage.query(release_type, result[1], [self.display_info['package']])
                    if package_result[0] == True:
                        self.display_info['build'] = package_result[1][1]
                CmdVersion.action(self.display_info)
            else:
                ret_val = 'Invalid version name!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type before using the "version" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val if self.quitOnError == True else None

    def complete_version(self, text, line, begidx, endidx):
        completions = []
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type']
            release_versions = CmdVersion.valid_values(release_type)
            if not text:
                completions = release_versions[:]
            else:
                completions = [item for item in release_versions if item.startswith(text)]
        return completions

    # Cache Control
    def help_cache(self):
        self.DisplayUsage(CmdCache.usage())

    def do_cache(self, line):
        ret_val = None
        result = CmdCache.query(self.get_arguments(line))
        if result[0] == True:
            self.display_info['cache'] = result[1]
            CmdCache.action(self.display_info)
        else:
            ret_val = 'Invalid cache command!'
            logging_helper.getLogger().error(ret_val)
        return ret_val if self.quitOnError == True else None

    def complete_cache(self, text, line, begidx, endidx):
        completions = []
        cache_completions = CmdCache.valid_values()
        if not text:
            completions = cache_completions[:]
        else:
            completions = [item for item in cache_completions if item.startswith(text)]
        return completions

    # Update
    def help_update(self):
        self.DisplayUsage(CmdUpdate.usage())

    def do_update(self, line):
        ret_val = None
        result = CmdUpdate.query(self.get_arguments(line))
        if result[0] == True:
            CmdUpdate.action(self.display_info)
        else:
            ret_val = 'Fatal error, cannot update!'
            logging_helper.getLogger().error(ret_val)
        return ret_val if self.quitOnError == True else None

    # Download
    def help_download(self):
        self.DisplayUsage(CmdDownload.usage())

    def do_download(self, line):
        ret_val = None
        result = CmdDownload.query(self.get_arguments(line))
        if result[0] == True:
            CmdDownload.action(self.display_info)
        else:
            ret_val = 'Fatal error, cannot download!'
            logging_helper.getLogger().error(ret_val)
        return ret_val if self.quitOnError == True else None

    # Build
    def help_build(self):
        self.DisplayUsage(CmdBuild.usage())

    def complete_build(self, text, line, begidx, endidx):
        completions = []
        if 'type' in self.display_info.keys() and 'package' in self.display_info.keys():
            release_type = self.display_info['type']
            package_name = self.display_info['package']
            build_numbers = CmdBuild.valid_values(release_type, package_name)
            if not text:
                completions = build_numbers[:]
            else:
                completions = [item for item in build_numbers if item.startswith(text)]
        return completions

    def do_build(self, line):
        ret_val = None
        if 'type' in self.display_info.keys() and 'package' in self.display_info.keys():
            release_type = self.display_info['type']
            package_name = self.display_info['package']
            result = CmdBuild.query(release_type, package_name, self.get_arguments(line))
            if result[0] == True:
                if 'version' in self.display_info.keys():
                    del self.display_info['version']
                self.display_info['build'] = result[1]
                CmdBuild.action(self.display_info)
            else:
                ret_val = 'Invalid build number!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type and package before using the "build" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val if self.quitOnError == True else None

    # Config
    def help_config(self):
        self.DisplayUsage(CmdConfig.usage())

    def complete_config(self, text, line, begidx, endidx):
        completions = []
        config_completions = CmdConfig.valid_values()
        if not text:
            completions = config_completions[:]
        else:
            completions = [item for item in config_completions if item.startswith(text)]
        return completions

    def do_config(self, line):
        ret_val = None
        result = CmdConfig.query(self.get_arguments(line))
        if result[0] == True:
            CmdConfig.action(result[1])
        else:
            ret_val = 'Invalid config command argument!'
            logging_helper.getLogger().error(ret_val)
        return ret_val if self.quitOnError == True else None

    # diff
    def help_diff(self):
        self.DisplayUsage(CmdDiff.usage())

    def do_diff(self, line):
        ret_val = None
        if 'type' in self.display_info.keys() and 'package' in self.display_info.keys():
            release_type = self.display_info['type']
            package_name = self.display_info['package']
            result = CmdDiff.query(release_type, package_name, self.get_arguments(line))
            if result[0] == True:
                self.display_info['diff'] = result[1]
                CmdDiff.action(self.display_info)
            else:
                ret_val = 'Invalid build numbers!'
                logging_helper.getLogger().error(ret_val)
        else:
            ret_val = 'Please select a release type and package before using the "diff" command.'
            logging_helper.getLogger().info(ret_val)
        return ret_val if self.quitOnError == True else None
        
    # hashes
    def help_hash(self):
        self.DisplayUsage(CmdHash.usage())
    
    def do_hash(self, line):
        ret_val = None
        result = CmdHash.query(self.get_arguments(line))
        if result[0] == True:
            CmdHash.action((result[1], self.display_info))
        else:
            ret_val = 'Fatal error, cannot process hashes!'
            logging_helper.getLogger().error(ret_val)
        return ret_val if self.quitOnError == True else None
    
    # list
    def help_list(self):
        self.DisplayUsage(CmdList.usage())
    
    def do_list(self, line):
        ret_val = None
        result = CmdList.query(self.get_arguments(line))
        if result[0] == True:
            CmdList.action(self.display_info)
        else:
            ret_val = 'Fatal error, could not list!'
            logging_helper.getLogger().error(ret_val)
        return ret_val if self.quitOnError == True else None
    
    # info
    def do_info(self, line):
        print('AOSD Version: '+AOSD_VERSION)