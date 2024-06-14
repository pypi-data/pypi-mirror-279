# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"objects"


from .object  import *
from .decoder import read
from .default import Default
from .encoder import write
from .config  import Config


def __dir__():
    return (
        'Config',
        'Default',
        'Object',
        'construct',
        'edit',
        'fmt',
        'fqn',
        'ident',
        'items',
        'keys',
        'match',
        'read',
        'search',
        'update',
        'values',
        'write'
    )


__all__ = __dir__()
