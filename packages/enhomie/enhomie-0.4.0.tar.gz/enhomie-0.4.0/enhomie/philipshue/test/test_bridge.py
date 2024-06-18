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

from httpx import Response

from respx import MockRouter

from . import SAMPLES
from . import SCENE_PATHS
from . import SCENE_PHIDS
from ...conftest import REPLACES

if TYPE_CHECKING:
    from ...homie import Homie



def test_PhueBridge(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    bridges = homie.phue_bridges
    bridge = bridges['jupiter']


    attrs = list(bridge.__dict__)

    assert attrs == [
        '_PhueBridge__homie',
        '_PhueBridge__params',
        '_PhueBridge__bridge',
        '_PhueBridge__name',
        '_PhueBridge__fetched',
        '_PhueBridge__merged',
        '_PhueBridge__timer']


    assert inrepr(
        'bridge.PhueBridge object',
        bridge)

    assert hash(bridge) > 0

    assert instr(
        'bridge.PhueBridge object',
        bridge)


    assert bridge.homie is homie

    assert bridge.params is not None

    assert bridge.bridge is not None

    assert bridge.name == 'jupiter'

    assert bridge.connect is False


    sample_path = (
        f'{SAMPLES}/bridge/fetched.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=bridge.fetched,
        replace=REPLACES)

    expect = prep_sample(
        content=bridge.fetched,
        replace=REPLACES)

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/bridge/merged.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=bridge.merged,
        replace=REPLACES)

    expect = prep_sample(
        content=bridge.merged,
        replace=REPLACES)

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/bridge/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=bridge.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=bridge.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_PhueBridge_source(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    bridges = homie.phue_bridges
    bridge = bridges['jupiter']


    source = bridge.get_source(
        '8155e7b2-e89b-3b1d'
        '-80af-a937994d9a78')

    assert source is not None
    assert source['id'] == (
        '8155e7b2-e89b-3b1d'
        '-80af-a937994d9a78')



def test_PhueBridge_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    bridges = homie.phue_bridges
    bridge = bridges['jupiter']

    phid = (
        '8155e7b2-e89b-3b1d'
        '-80af-a937994d9a78')


    source = bridge.get_source(
        label='Jupiter Button')

    assert source is not None
    assert source['id'] == phid


    source = bridge.get_source(
        phid, type='device')

    assert source is not None
    assert source['id'] == phid


    group = homie.groups['jupiter_room']
    scene = homie.scenes['awake']


    source = bridge.get_source(
        label=scene.params.phue_label,
        type='scene',
        grid=group.phue_unique)

    assert source is not None
    assert source['id'] == (
        scene.phue_unique(group))


    source = bridge.get_source(
        phid=scene.phue_unique(group),
        type='scene',
        grid=group.phue_unique)

    assert source is not None
    assert source['id'] == (
        scene.phue_unique(group))



def test_PhueBridge_scene(
    homie: 'Homie',
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param respx_mock: Object for mocking request operation.
    """

    groups = homie.groups
    bridges = homie.phue_bridges


    for path in SCENE_PATHS:

        (respx_mock
         .put(path)
         .mock(Response(200)))


    bridge = bridges['jupiter']
    group = groups['jupiter_zone']

    assert group.phue_unique

    scene = bridge.scene_get(
        group.phue_unique)

    assert scene is not None
    assert scene[:8] == '35ac3411'

    bridge.scene_set(SCENE_PHIDS[0])


    bridge = bridges['neptune']
    group = groups['neptune_zone']

    assert group.phue_unique

    scene = bridge.scene_get(
        group.phue_unique)

    assert scene is not None
    assert scene[:8] == 'd8bc6c89'

    bridge.scene_set(SCENE_PHIDS[1])


    scene = bridge.scene_get('dne')

    assert scene is None
