pipelines = {}


class CommandType:
    RUN = "run"
    BUILD = "build"
    DEPLOY = "deploy"

    @classmethod
    def is_valid(cls, command_type):
        return command_type in {cls.RUN, cls.BUILD, cls.DEPLOY}
