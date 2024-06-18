"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from _pytest.logging import LogCaptureFixture

from encommon import ENPYRWS
from encommon.types import inrepr
from encommon.types import instr
from encommon.utils import load_sample
from encommon.utils import prep_sample

from httpx import Response

from respx import MockRouter

from . import SAMPLES
from ..homie import Homie
from ...config import Config
from ...conftest import REPLACES
from ...philipshue.test import (
    SCENE_PATHS as PHUE_SCENE_PATHS)



def test_Homie(
    homie: Homie,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    desires = homie.desires
    desire = desires['default']


    attrs = list(homie.__dict__)

    assert attrs == [
        '_Homie__config',
        '_Homie__timers',
        '_Homie__phue_bridges',
        '_Homie__phue_devices',
        '_Homie__ubiq_routers',
        '_Homie__ubiq_clients',
        '_Homie__groups',
        '_Homie__scenes',
        '_Homie__desires',
        '_Homie__actions']


    assert inrepr(
        'homie.Homie object',
        homie)

    assert hash(homie) > 0

    assert instr(
        'homie.Homie object',
        homie)


    assert homie.config is not None

    assert homie.params is not None

    assert homie.timers is not None

    assert len(homie.groups) == 4

    assert len(homie.rooms) == 2

    assert len(homie.zones) == 2

    assert len(homie.scenes) == 5

    assert len(homie.desires) == 4

    assert len(homie.phue_bridges) == 2

    assert len(homie.phue_devices) == 10

    assert len(homie.ubiq_routers) == 2

    assert len(homie.ubiq_clients) == 6

    assert homie.desired == {
        'jupiter_room': desire,
        'jupiter_zone': desire,
        'neptune_room': desire,
        'neptune_zone': desire}


    sample_path = (
        f'{SAMPLES}/homie/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=homie.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=homie.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_Homie_logger(
    homie: Homie,
    caplog: LogCaptureFixture,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param caplog: pytest object for capturing log message.
    """

    logger = homie.config.logger


    logger.start()

    homie.log_d(message='pytest')
    homie.log_c(message='pytest')
    homie.log_e(message='pytest')
    homie.log_i(message='pytest')
    homie.log_w(message='pytest')

    homie.log(
        level='debug',
        message='custom')

    logger.stop()

    output = caplog.record_tuples

    assert len(output) == 6


    homie.log_d(message='pytest')
    homie.log_c(message='pytest')
    homie.log_e(message='pytest')
    homie.log_i(message='pytest')
    homie.log_w(message='pytest')

    output = caplog.record_tuples

    assert len(output) == 6



def test_Homie_scene(
    homie: Homie,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param respx_mock: Object for mocking request operation.
    """


    for path in PHUE_SCENE_PATHS:

        (respx_mock
         .put(path)
         .mock(Response(200)))


    scene = homie.scene_get(
        homie.groups['jupiter_zone'])

    assert scene is not None
    assert scene.name == 'sleep'

    homie.scene_set(
        homie.groups['jupiter_room'],
        homie.scenes['awake'])


    scene = homie.scene_get(
        homie.groups['neptune_zone'])

    assert scene is not None
    assert scene.name == 'sleep'

    homie.scene_set(
        homie.groups['neptune_room'],
        homie.scenes['awake'])


    scene = homie.scene_get(
        homie.groups['jupiter_room'])

    assert scene is None



def test_Homie_cover(
    tmp_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    """

    Homie(Config())
