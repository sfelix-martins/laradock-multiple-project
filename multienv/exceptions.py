class HintMessageException(Exception):
    error = None
    hint = None

    def __init__(self, error, hint=None):
        self.error = error
        self.hint = hint


class InvalidArgumentException(HintMessageException):
    pass


class ProjectNotDefinedException(HintMessageException):
    pass


class ServicesNotDefinedException(HintMessageException):
    pass


class InvalidYamlFileException(HintMessageException):
    pass


class InvalidProjectDefinitions(HintMessageException):
    pass


class ConfigFileNotFoundException(HintMessageException):
    pass


class EnvVarContainerBuildNotFoundException(HintMessageException):
    pass
