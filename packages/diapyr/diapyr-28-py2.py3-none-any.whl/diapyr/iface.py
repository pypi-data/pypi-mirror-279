class MissingAnnotationException(Exception): pass

class Special(object):

    @classmethod
    def gettypelabel(cls, type):
        # TODO: Dotted name can look misleading for nested classes.
        return type.__name__ if issubclass(type, cls) else "%s.%s" % (type.__module__, type.__name__)

class UnsatisfiableRequestException(Exception): pass

class ImpasseException(Exception): pass

unset = object()
