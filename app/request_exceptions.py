class InvalidRequestException(Exception):
    pass


class MissingRequestJsonData(InvalidRequestException):
    pass


class MissingRequestDataKey(InvalidRequestException):
    pass


class InvalidRequestDataFormat(InvalidRequestException):
    pass
