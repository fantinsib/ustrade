


class USTradeError(Exception):
    """
    Base error for the library
    """

class APITimeOutError(USTradeError):
    pass


##### Data search error ##################################################

class EmptyResult(USTradeError):
    """
    Could not find any data for the specified query
    """
    pass





####### countries error ##################################################

class InvalidCountryError(USTradeError):
    """
    Country is not referenced
    """
    pass

####### codes error ##################################################

class InvalidCodeError(USTradeError):
    """
    Argument of function is not of a valid type
    """
    pass

class CodeNotFoundError(USTradeError):
    """
    Could not find the reference to this code in the base
    """
    pass


