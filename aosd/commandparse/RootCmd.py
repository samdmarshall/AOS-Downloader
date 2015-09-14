class RootCmd(object):
    """
    root command object, subclass this
    """

    @classmethod
    def usage(cls):
        """
        command usage information
        """
        return {}

    @classmethod
    def valid_values(cls, release_type, package_name):
        """
        valid values for the command
        """
        return []

    @classmethod
    def query(cls, release_type, package_name, args):
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
