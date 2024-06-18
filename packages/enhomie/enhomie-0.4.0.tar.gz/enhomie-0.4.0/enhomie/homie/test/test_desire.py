"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.utils import load_sample
from encommon.utils import prep_sample

from . import SAMPLES
from ...conftest import REPLACES

if TYPE_CHECKING:
    from ..homie import Homie



def test_HomieDesire(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    desires = homie.desires
    desire = desires['jupiter']


    attrs = list(desire.__dict__)

    assert attrs == [
        '_HomieDesire__homie',
        '_HomieDesire__params',
        '_HomieDesire__name',
        '_HomieDesire__when']


    assert inrepr(
        'desire.HomieDesire object',
        desire)

    assert hash(desire) > 0

    assert instr(
        'desire.HomieDesire object',
        desire)


    assert desire.homie is homie

    assert desire.params is not None

    assert desire.name == 'jupiter'

    assert len(desire.whens) == 3

    assert len(desire.groups) == 2

    assert desire.scene == 'awaydark'

    assert desire.weight == 0

    assert desire.delay == 0

    assert desire.when is not None

    assert len(desire.when) == 3

    assert desire.delayed is False

    assert desire.outcomes == {
        'default': [False, True, True]}

    assert desire.outcome is False


    sample_path = (
        f'{SAMPLES}/desire'
        '/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=desire.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=desire.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_HomieDesire_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    desires = homie.desires
    delayed = desires['delayed']
    default = desires['default']


    assert homie.desired == {
        'jupiter_room': default,
        'jupiter_zone': default,
        'neptune_room': default,
        'neptune_zone': default}


    delayed.update_timer(
        f'-{delayed.delay}s')

    assert homie.desired == {
        'jupiter_room': delayed,
        'jupiter_zone': delayed,
        'neptune_room': delayed,
        'neptune_zone': delayed}
