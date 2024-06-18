"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Times

if TYPE_CHECKING:
    from ..homie import HomieWhen



def when_time_period(
    when: 'HomieWhen',
) -> bool:
    """
    Return the boolean indicating whether condition matched.

    :param when: Primary class instance for the conditonal.
    :returns: Boolean indicating whether condition matched.
    """

    params = (
        when.params.time_period)

    assert params is not None

    start = params.start
    stop = params.stop
    tzname = params.tzname

    anchor = Times(tzname=tzname)

    assert (
        start is not None
        or stop is not None)


    _start: Optional[Times] = (
        Times(start)
        if start is not None
        else None)

    _stop: Optional[Times] = (
        Times(stop)
        if stop is not None
        else None)


    matched = True

    if (_start is not None
            and anchor < _start):
        matched = False

    if (_stop is not None
            and anchor > _stop):
        matched = False


    return matched



def chck_time_period(
    when: 'HomieWhen',
) -> None:
    """
    Return the boolean indicating whether conditional valid.

    :param when: Primary class instance for the conditonal.
    """

    params = (
        when.params.time_period)

    assert params is not None

    start = params.start
    stop = params.stop
    tzname = params.tzname


    if start is not None:
        Times(start, tzname=tzname)

    if stop is not None:
        Times(stop, tzname=tzname)
