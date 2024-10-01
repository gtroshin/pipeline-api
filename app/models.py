pipelines = {}


class CommandType:
    RUN = "run"
    BUILD = "build"
    DEPLOY = "deploy"

    @classmethod
    def is_valid(cls, command_type):
        """
        Checks if the provided command type is valid.

        Args:
            command_type (str): The command type to be validated.

        Returns:
            bool: True if the command type is valid, False otherwise.
        """
        return command_type in {cls.RUN, cls.BUILD, cls.DEPLOY}
