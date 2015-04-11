import cmd

from ..logging_helper import *

from .cmd_quit import *
from .cmd_type import *
from .cmd_package import *
from .cmd_version import *

class input(cmd.Cmd):
    prompt = ':> ';
    display_info = {};
    AOSD = None;
    
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
            info.append('Type: %s' % self.AOSD.TypeName()[self.display_info['type']]);
        if 'version' in self.display_info.keys():
            info.append('Version: %s' % self.display_info['version']);
        if 'package' in self.display_info.keys():
            info.append('Package: %s' % self.display_info['package']);
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
        cmd_quit.action(self.GetArguments(line));
    
    # Release type
    def help_type(self):
        self.DisplayUsage(cmd_type.usage());
    
    def do_type(self, line):
        result = cmd_type.action(self.GetArguments(line));
        if result[0] == True:
            self.display_info['type'] = result[1];
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
            result = cmd_package.action(self.GetArguments(line));
            if result[0] == True:
                self.display_info['package'] = result[1];
            else:
                logging_helper.getLogger().error(': Invalid package name!');
        else:
            logging_helper.getLogger().info(': Please select a release type before using the "package" command.');
    
    def complete_package(self, text, line, begidx, endidx):
        completions = [];
        if 'type' in self.display_info.keys() and 'version' in self.display_info.keys():
            release_type = self.display_info['type'];
            release_version = self.display_info['version'];
            package_names = cmd_package.validValues(release_type, release_version);
            if not text:
                completions = release_types[:];
            else:
                completions = [ item for item in release_types if item.startswith(text) ];
        return completions;
        
    # Release Version
    def help_version(self):
        self.DisplayUsage(cmd_version.usage());
    
    def do_version(self, line):
        if 'type' in self.display_info.keys():
            result = cmd_package.action(self.GetArguments(line));
            if result[0] == True:
                self.display_info['version'] = result[1];
            else:
                logging_helper.getLogger().error(': Invalid version name!');
        else:
            logging_helper.getLogger().info(': Please select a release type before using the "version" command.');
    
    def complete_version(self, text, line, begidx, endidx):
        completions = [];
        if 'type' in self.display_info.keys():
            release_type = self.display_info['type'];
            package_names = cmd_version.validValues(release_type, self.AOSD);
            if not text:
                completions = release_types[:];
            else:
                completions = [ item for item in release_types if item.startswith(text) ];
        return completions;