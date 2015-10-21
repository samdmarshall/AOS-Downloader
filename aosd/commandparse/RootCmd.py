class RootCmd(object):
    """
    root command object, subclass this
    """
    
    @classmethod
    def DisplayUsage(cls):
        cmd_usage_dict = cls.usage()
        cmd_name = cmd_usage_dict.get('name', None)
        cmd_args = cmd_usage_dict.get('args', None)
        cmd_desc = cmd_usage_dict.get('desc', None)
        if (cmd_name != None) and (cmd_args != None) and (cmd_desc != None):
            print('Command: ')
            print('%10s %s\n%10s %s\n' % (cmd_name, cmd_usage, '-', cmd_desc))
        else:
            print('There was an error parsing the usage information for this command!')

    @classmethod
    def usage(cls):
        """
        command usage information
        """
        return {}

    @classmethod
    def valid_values(cls):
        """
        valid values for the command
        """
        return []

    @classmethod
    def query(cls, args):
        """
        validate the value passed to the command
        """
        return (True, None)

    @classmethod
    def action(cls, args):
        """
        empty
        """
        return

    @classmethod
    def process_do(cls, line_text, context):
        ret_val = None
        return ret_val