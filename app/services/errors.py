class CatsAPIBaseException(Exception):
    pass


class BreedAlreadyExists(CatsAPIBaseException):
    pass
