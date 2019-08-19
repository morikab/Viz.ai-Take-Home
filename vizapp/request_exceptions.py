class InvalidRequestException(Exception):
    def __init__(self, message, cause=None):
        super().__init__(message)
        self.__cause = cause

    def cause(self):
        return self.__cause


class MissingRequestJsonData(InvalidRequestException):
    def __init__(self):
        super().__init__("Missing json data in request")


class MissingRequestDataKey(InvalidRequestException):
    def __init__(self, key):
        super().__init__("Missing request data key in json", "missing key: " + key)


class InvalidRequestDataFormat(InvalidRequestException):
    def __init__(self, key, expected_type):
        super().__init__("Invalid request data format", "key '{}' should be of type {}".format(key, expected_type))


class EmptyRequestData(InvalidRequestException):
    def __init__(self, key):
        super().__init__("Empty request data key", "key: " + key)

