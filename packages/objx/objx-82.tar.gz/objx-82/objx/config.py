# This file is placed in the Public Domain.
#
# pylint: disable=R0903


"configuration"


from . import Default


class Config(Default):

    "Config"


def __dir__():
    return (
        'Config',
    )
