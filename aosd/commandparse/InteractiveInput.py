import cmd

from ..logging_helper import logging_helper

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

from ..downloader.releases import releases

class InteractiveInput(cmd.Cmd):
    prompt = ':> '
    display_info = {}

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

    # Quit
    def help_quit(self):
        self.DisplayUsage(CmdQuit.usage())

    def do_quit(self, line):
        result = CmdQuit.query(self.get_arguments(line))
        if result[0] == True:
            CmdQuit.action(self.display_info)
        else:
            logging_helper.getLogger().error('Fatal error, cannot quit!')

    # Release type
    def help_type(self):
        self.DisplayUsage(CmdType.usage())

    def do_type(self, line):
        result = CmdType.query(self.get_arguments(line))
        if result[0] == True:
            self.display_info = {}
            self.display_info['type'] = result[1]
            CmdType.action(self.display_info)
        else:
            logging_helper.getLogger().error('Invalid release type!')

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
                logging_helper.getLogger().error('Invalid package name!')
        else:
            logging_helper.getLogger().info('Please select a release type before using the "package" command.')

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
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type']
            result = CmdVersion.query(release_type, self.get_arguments(line))
            if result[0] == True:
                self.display_info['version'] = result[1]
                if 'build' in self.display_info.keys():
                    del self.display_info['build']
                if 'package' in self.display_info.keys():
                    package_result = CmdPackage.query(release_type, result[1], self.display_info['package'])
                    if package_result[0] == True:
                        self.display_info['build'] = package_result[1][1]
                CmdVersion.action(self.display_info)
            else:
                logging_helper.getLogger().error('Invalid version name!')
        else:
            logging_helper.getLogger().info('Please select a release type before using the "version" command.')

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
        result = CmdCache.query(self.get_arguments(line))
        if result[0] == True:
            self.display_info['cache'] = result[1]
            CmdCache.action(self.display_info)
        else:
            logging_helper.getLogger().error('Invalid cache command!')

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
        result = CmdUpdate.query(self.get_arguments(line))
        if result[0] == True:
            CmdUpdate.action(self.display_info)
        else:
            logging_helper.getLogger().error('Fatal error, cannot update!')

    # Download
    def help_download(self):
        self.DisplayUsage(CmdDownload.usage())

    def do_download(self, line):
        result = CmdDownload.query(self.get_arguments(line))
        if result[0] == True:
            CmdDownload.action(self.display_info)
        else:
            logging_helper.getLogger().error('Fatal error, cannot download!')

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
                logging_helper.getLogger().error('Invalid build number!')
        else:
            logging_helper.getLogger().info('Please select a release type and package before using the "build" command.')

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
        result = CmdConfig.query(self.get_arguments(line))
        if result[0] == True:
            CmdConfig.action(result[1])
        else:
            logging_helper.getLogger().error('Invalid config command argument!')

    # diff
    def help_diff(self):
        self.DisplayUsage(CmdDiff.usage())

    def do_diff(self, line):
        if 'type' in self.display_info.keys() and 'package' in self.display_info.keys():
            release_type = self.display_info['type']
            package_name = self.display_info['package']
            result = CmdDiff.query(release_type, package_name, self.get_arguments(line))
            if result[0] == True:
                self.display_info['diff'] = result[1]
                CmdDiff.action(self.display_info)
            else:
                logging_helper.getLogger().error('Invalid build numbers!')
        else:
            logging_helper.getLogger().info('Please select a release type and package before using the "diff" command.')
        
    # hashes
    def help_hash(self):
        self.DisplayUsage(CmdHash.usage())
    
    def do_hash(self, line):
        if 'type' in self.display_info.keys() and 'version' in self.display_info.keys():
            result = CmdHash.query(self.get_arguments(line))
            if result[0] == True:
                CmdHash.action(self.display_info)
            else:
                logging_helper.getLogger().error('Fatal error, cannot process hashes!')
        else:
            logging_helper.getLogger().info('Please select a release type and package before using the "diff" command.')
