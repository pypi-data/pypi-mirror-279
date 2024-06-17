from enum import Enum


class Status(Enum):
    VALID = 1
    INVALID = 2


def isStatusValid(function):
    
    def wrapper(object, *args, **kwargs):
        if object.status == Status.VALID:
            return function(object, *args, **kwargs)
        
        else:
            pass
        
    return wrapper