class ParseError(Exception):
    """
    Parser base exception
    """
    pass


class InvalidNodeError(ParseError):
    """
    Node format invalid
    """
    pass


class MissingFieldError(ParseError):
    """
    Required field missing
    """
    pass


class UnsupportedProtocolError(ParseError):
    """
    Unsupported protocol
    """
    pass
