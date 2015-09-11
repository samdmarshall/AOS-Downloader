import cmd

from ..logging_helper import *

from .cmd_quit import *
from .cmd_type import *
from .cmd_package import *
from .cmd_version import *
from .cmd_cache import *
from .cmd_update import *
from .cmd_download import *
from .cmd_build import *

class input(cmd.Cmd):
    prompt = ':> ';
    display_info = {};
    
    def GetArguments(self, arguments_str):
        arguments_str = str(arguments_str);
        arg_words = [];
        input_split = arguments_str.split(' ');
        offset = 0;
        counter = 0;
        current_word = '';
        while counter < len(input_split):
            word = input_split[counter];
            current_word += word;
            if len(current_word) == 0:
                offset += 1;
            else:
                if offset >= 0:
                    curr = offset + len(word);
                    prev = curr - 1
                    if arguments_str[prev:curr] != '\\':
                        arg_words.append(current_word);
                        current_word = '';
                    else:
                        current_word += ' ';
                    offset += len(word) + 1;
            counter += 1;
        return arg_words;
    
    def DisplayUsage(self, cmd_usage):
        print 'Command: ';
        print '%10s %s\n%10s %s\n' % (cmd_usage['name'], cmd_usage['args'], '-', cmd_usage['desc']);
    
    def GenerateInfo(self):
        info = [];
        if 'type' in self.display_info.keys():
            info.append('Type: %s' % releases.GetReleaseDisplayName(self.display_info['type']));
        if 'version' in self.display_info.keys():
            info.append('Version: %s' % self.display_info['version']);
        if 'package' in self.display_info.keys():
            info.append('Package: %s' % self.display_info['package']);
        if 'build' in self.display_info.keys():
            info.append('Build: %s' % self.display_info['build']);
        return '\n'.join(info);
    
    def postcmd(self, stop, line):
        info_string = self.GenerateInfo();
        if len(info_string) > 0:
            print '\n'+info_string;
        return stop;
    
    # Quit
    def help_quit(self):
        self.DisplayUsage(cmd_quit.usage());
    
    def do_quit(self, line):
        result = cmd_quit.query(self.GetArguments(line));
        if result[0] == True:
            cmd_quit.action(self.display_info);
        else:
            logging_helper.getLogger().error(': Fatal error, cannot quit!');
    
    # Release type
    def help_type(self):
        self.DisplayUsage(cmd_type.usage());
    
    def do_type(self, line):
        result = cmd_type.query(self.GetArguments(line));
        if result[0] == True:
            self.display_info = {};
            self.display_info['type'] = result[1];
            cmd_type.action(self.display_info);
        else:
            logging_helper.getLogger().error(': Invalid release type!');
    
    def complete_type(self, text, line, begidx, endidx):
        release_types = cmd_type.validValues();
        if not text:
            completions = release_types[:];
        else:
            completions = [ item for item in release_types if item.startswith(text) ];
        return completions;
    
    # Package
    def help_package(self):
        self.DisplayUsage(cmd_package.usage());
    
    def do_package(self, line):
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type'];
            release_version = None;
            if 'version' in self.display_info.keys():
                release_version = self.display_info['version'];
            result = cmd_package.query(release_type, release_version, self.GetArguments(line));
            if result[0] == True:
                self.display_info['package'] = result[1];
                cmd_package.action(self.display_info);
            else:
                logging_helper.getLogger().error(': Invalid package name!');
        else:
            logging_helper.getLogger().info(': Please select a release type before using the "package" command.');
    
    def complete_package(self, text, line, begidx, endidx):
        completions = [];
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type'];
            release_version = None;
            if 'version' in self.display_info.keys():
                release_version = self.display_info['version'];
            package_names = cmd_package.validValues(release_type, release_version);
            if not text:
                completions = package_names[:];
            else:
                completions = [ item for item in package_names if item.startswith(text) ];
        return completions;
        
    # Release Version
    def help_version(self):
        self.DisplayUsage(cmd_version.usage());
    
    def do_version(self, line):
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type'];
            result = cmd_version.query(release_type, self.GetArguments(line));
            if result[0] == True:
                self.display_info['version'] = result[1];
                if 'build' in self.display_info.keys():
                    del self.display_info['build'];
                cmd_version.action(self.display_info);
            else:
                logging_helper.getLogger().error(': Invalid version name!');
        else:
            logging_helper.getLogger().info(': Please select a release type before using the "version" command.');
    
    def complete_version(self, text, line, begidx, endidx):
        completions = [];
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type'];
            release_versions = cmd_version.validValues(release_type);
            if not text:
                completions = release_versions[:];
            else:
                completions = [ item for item in release_versions if item.startswith(text) ];
        else:
            logging_helper.getLogger().info(': Please select a release type before using the "version" command.');
        return completions;
    
    # Cache Control
    def help_cache(self):
        self.DisplayUsage(cmd_cache.usage());
    
    def do_cache(self, line):
        result = cmd_cache.query(self.GetArguments(line));
        if result[0] == True:
            self.display_info['cache'] = result[1];
            cmd_cache.action(self.display_info);
        else:
            logging_helper.getLogger().error(': Invalid cache command!');
    
    def complete_cache(self, text, line, begidx, endidx):
        cache_completions = cmd_cache.validValues();
        if not text:
            completions = cache_completions[:];
        else:
            completions = [ item for item in cache_completions if item.startswith(text) ];
        return completions;
    
    # Update
    def help_update(self):
        self.DisplayUsage(cmd_update.usage());
    
    def do_update(self, line):
        result = cmd_update.query(self.GetArguments(line));
        if result[0] == True:
            cmd_update.action(self.display_info);
        else:
            logging_helper.getLogger().error(': Fatal error, cannot update!');
    
    # Download
    def help_download(self):
        self.DisplayUsage(cmd_download.usage());
    
    def do_download(self, line):
        result = cmd_download.query(self.GetArguments(line));
        if result[0] == True:
            cmd_download.action(self.display_info);
        else:
            logging_helper.getLogger().error(': Fatal error, cannot download!');
    
    # Build
    def help_build(self):
        self.DisplayUsage(cmd_build.usage());
        
    def complete_build(self, text, line, begidx, endidx):
        completions = [];
        if 'type' in self.display_info.keys() and 'package' in self.display_info.keys():
            release_type = self.display_info['type'];
            package_name = self.display_info['package'];
            build_numbers = cmd_build.validValues(release_type, package_name);
            if not text:
                completions = build_numbers[:];
            else:
                completions = [ item for item in build_numbers if item.startswith(text) ];
        else:
            logging_helper.getLogger().info(': Please select a release type and package before using the "build" command.');
        return completions;
    
    def do_build(self, line):
        if 'type' in self.display_info.keys() and 'package' in self.display_info.keys():
            release_type = self.display_info['type'];
            package_name = self.display_info['package'];
            result = cmd_build.query(release_type, package_name, self.GetArguments(line));
            if result[0] == True:
                if 'version' in self.display_info.keys():
                    del self.display_info['version'];
                self.display_info['build'] = result[1];
                cmd_build.action(self.display_info);
            else:
                logging_helper.getLogger().error(': Invalid build number!');
        else:
            logging_helper.getLogger().info(': Please select a release type and package before using the "build" command.');