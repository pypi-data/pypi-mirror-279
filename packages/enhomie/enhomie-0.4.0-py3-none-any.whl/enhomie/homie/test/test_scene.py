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



def test_HomieScene(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    scenes = homie.scenes
    groups = homie.groups
    scene = scenes['awake']
    group = groups['jupiter_room']


    attrs = list(scene.__dict__)

    assert attrs == [
        '_HomieScene__homie',
        '_HomieScene__params',
        '_HomieScene__name']


    assert inrepr(
        'scene.HomieScene object',
        scene)

    assert hash(scene) > 0

    assert instr(
        'scene.HomieScene object',
        scene)


    assert scene.homie is homie

    assert scene.params is not None

    assert scene.name == 'awake'

    phue_source = (
        scene.phue_source(group))

    phue_unique = (
        scene.phue_unique(group))

    phue_actual = (
        scene.phue_actual(group))

    assert phue_source is not None

    assert phue_unique == (
        '5808a516-aab3-3ec3'
        '-8eee-4db5152b07b5')

    assert phue_actual == 'Awake'


    sample_path = (
        f'{SAMPLES}/scene/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=scene.homie_dumper(group),
        replace=REPLACES)

    expect = prep_sample(
        content=scene.homie_dumper(group),
        replace=REPLACES)

    assert sample == expect



def test_HomieScene_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    scenes = homie.scenes
    groups = homie.groups
    scene = scenes['awake']
    group = groups['jupiter_room']

    scene.params.phue_label = 'noexst'

    assert not (
        scene.phue_unique(group))

    assert not (
        scene.phue_actual(group))


    assert scene.homie_dumper() == {
        'name': 'awake',
        'present': False,
        'params': {
            'phue_label': 'noexst'},
        'phue_actual': None,
        'phue_unique': None}
