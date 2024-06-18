from pymongo.errors import PyMongoError


class RedBabyError(PyMongoError):
    """
    Generic error.
    """


class DocumentNotFound(RedBabyError):
    """
    Raised when no document is found.
    """
