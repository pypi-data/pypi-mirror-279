"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr

from ..params import HomieWhenParams
from ..when import HomieWhen
from ...builtins import WhenTimePeriodParams

if TYPE_CHECKING:
    from ..homie import Homie



def test_HomieWhen(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    time_period = (
        WhenTimePeriodParams(
            start='-2d'))

    params = HomieWhenParams(
        time_period=time_period)

    when = HomieWhen(homie, params)


    attrs = list(when.__dict__)

    assert attrs == [
        '_HomieWhen__homie',
        '_HomieWhen__params']


    assert inrepr(
        'when.HomieWhen object',
        when)

    assert hash(when) > 0

    assert instr(
        'when.HomieWhen object',
        when)


    assert when.homie is homie

    assert when.params is not None

    assert when.negate is False

    assert when.family == 'default'

    assert when.outcome is True
