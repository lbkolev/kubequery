import functools


def rgetattr(obj, attr, *args):
    """Get a nested attribute from an object."""

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj, *attr.split(".")])
