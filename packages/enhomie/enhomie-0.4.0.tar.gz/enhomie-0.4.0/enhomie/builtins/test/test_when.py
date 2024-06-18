"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ..params import WhenTimePeriodParams
from ...homie import HomieWhen
from ...homie import HomieWhenParams

if TYPE_CHECKING:
    from ...homie import Homie



def test_when_time_period(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """


    time_period = (
        WhenTimePeriodParams(
            start='+2d'))

    params = HomieWhenParams(
        time_period=time_period)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    time_period = (
        WhenTimePeriodParams(
            start='-2d'))

    params = HomieWhenParams(
        time_period=time_period)

    when = HomieWhen(homie, params)

    assert when.outcome is True


    time_period = (
        WhenTimePeriodParams(
            start='-2d',
            stop='-1d'))

    params = HomieWhenParams(
        time_period=time_period)

    when = HomieWhen(homie, params)

    assert when.outcome is False
