"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from typing import TYPE_CHECKING

from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text

from . import SAMPLES
from ...conftest import REPLACES
from ...philipshue.test import (
    SAMPLES as PHUE_SAMPLES)

if TYPE_CHECKING:
    from ..homie import Homie



def test_HomieAction(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    actions = homie.actions
    action = actions['jupiter']

    _events = loads(
        read_text(
            f'{PHUE_SAMPLES}/events'
            '/source.json'))


    attrs = list(action.__dict__)

    assert attrs == [
        '_HomieAction__homie',
        '_HomieAction__params',
        '_HomieAction__name',
        '_HomieAction__what',
        '_HomieAction__when']


    assert inrepr(
        'action.HomieAction object',
        action)

    assert hash(action) > 0

    assert instr(
        'action.HomieAction object',
        action)


    assert action.homie is homie

    assert action.params is not None

    assert action.name == 'jupiter'

    assert len(action.whats) == 2

    assert len(action.whens) == 1

    assert len(action.groups) == 2

    assert action.scene == 'awake'

    assert action.weight == 10

    assert action.what is not None

    assert action.when is not None

    assert len(action.when) == 1

    assert action.paused is False

    assert action.outcomes == {
        'default': [True]}

    assert action.outcome is True

    matches = action.matches(_events[0])

    assert matches == [True, False]

    match = action.match(_events[0])

    assert match is True


    sample_path = (
        f'{SAMPLES}/action'
        '/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=action.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=action.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_HomieAction_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    actions = homie.actions
    jupiter = actions['jupiter']
    default = actions['default']

    _events = loads(
        read_text(
            f'{PHUE_SAMPLES}/events'
            '/source.json'))


    aspired = homie.aspired(_events[0])

    assert aspired == {
        'jupiter_room': jupiter,
        'jupiter_zone': jupiter,
        'neptune_room': default,
        'neptune_zone': default}


    jupiter.update_timer()

    aspired = homie.aspired(_events[0])

    assert aspired == {
        'jupiter_room': default,
        'jupiter_zone': default,
        'neptune_room': default,
        'neptune_zone': default}


    jupiter.delete_timer()

    aspired = homie.aspired(_events[0])

    assert aspired == {
        'jupiter_room': jupiter,
        'jupiter_zone': jupiter,
        'neptune_room': default,
        'neptune_zone': default}


    aspired = homie.aspired(_events[1])

    assert aspired == {
        'jupiter_room': jupiter,
        'jupiter_zone': jupiter}
