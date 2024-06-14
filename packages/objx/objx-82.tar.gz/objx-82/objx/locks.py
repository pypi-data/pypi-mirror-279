# This file is placed in the Public Domain.


"locks"


import _thread


lock = _thread.allocate_lock()


"interface"


def __dir__():
    return (
        "lock",
    )
