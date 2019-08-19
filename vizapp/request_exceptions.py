class InvalidRequestException(Exception):
    pass


class MissingRequestJsonData(InvalidRequestException):
    def __str__(self):
        return "Missing json data in request"


class MissingRequestDataKey(InvalidRequestException):
    def __init__(self, key):
        self.__key = key

    def __str__(self):
        return "Missing key '{}' in request json data".format(self.__key)


class InvalidRequestDataFormat(InvalidRequestException):
    def __init__(self, key, expected_type):
        self.__key = key
        self.__expected_type = expected_type

    def __str__(self):
        return "Request data format for key '{}' should be of type {}".format(self.__key, self.__expected_type)


class EmptyRequestData(InvalidRequestException):
    def __init__(self, key):
        self.__key = key

    def __str__(self):
        return "Empty request data key '{}'".format(self.__key)

