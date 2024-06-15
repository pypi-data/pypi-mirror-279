class InvalidExtensionError(Exception):
    def __init__(self, filename):
        message = f"File has an invalid extension: {filename}"
        super().__init__(message)


class RequiredValueError(Exception):
    def __init__(self, values):
        message = f"Required value(s) missing: {', '.join(values)}"
        super().__init__(message)


class UnsupportedActionException(Exception):
    def __init__(self, version):
        message = f"Action not supported in LIFT v{version}"
        super().__init__(message)
