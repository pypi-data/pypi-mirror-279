"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon.utils import save_text

from respx import MockRouter

from ..params import WhenPhueChangeParams
from ..params import WhenPhueSceneParams
from ...conftest import config_factory
from ...conftest import homie_factory
from ...homie import HomieWhen
from ...homie import HomieWhenParams

if TYPE_CHECKING:
    from ...homie import Homie



def test_when_phue_change(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """


    phue_change = (
        WhenPhueChangeParams(
            devices=['jupiter_motion'],
            sensors=['motion1']))

    params = HomieWhenParams(
        phue_change=phue_change)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    phue_change = (
        WhenPhueChangeParams(
            devices=['jupiter_motion'],
            sensors=['motion1'],
            since=86400))

    params = HomieWhenParams(
        phue_change=phue_change)

    when = HomieWhen(homie, params)

    assert when.outcome is True



def test_when_phue_change_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    """

    config = (
        'phue_devices:\n'
        '  noexst:\n'
        '    bridge: jupiter\n'
        '    phid: noexst\n')


    Path.mkdir(
        tmp_path.joinpath('config'))

    save_text(
        f'{tmp_path}/config/test.yml',
        content=config)

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock)


    phue_change = (
        WhenPhueChangeParams(
            devices=['noexst'],
            sensors=['button1']))

    params = HomieWhenParams(
        phue_change=phue_change)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    phue_change = (
        WhenPhueChangeParams(
            devices=['jupiter_switch'],
            sensors=['button1']))

    params = HomieWhenParams(
        phue_change=phue_change)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    # Motion does not have buttons
    # this helps with the coverage
    phue_change = (
        WhenPhueChangeParams(
            devices=['jupiter_motion'],
            sensors=['button1']))

    params = HomieWhenParams(
        phue_change=phue_change)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    phue_change = (
        WhenPhueChangeParams(
            devices=['jupiter_button'],
            sensors=['button4']))

    params = HomieWhenParams(
        phue_change=phue_change)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    # Plugs do not have sensor but
    # this helps with the coverage
    phue_change = (
        WhenPhueChangeParams(
            devices=['jupiter_plug'],
            sensors=['motion1']))

    params = HomieWhenParams(
        phue_change=phue_change)

    when = HomieWhen(homie, params)

    assert when.outcome is False



def test_when_phue_scene(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """


    phue_scene = (
        WhenPhueSceneParams(
            group='jupiter_zone',
            scenes=['sleep']))

    params = HomieWhenParams(
        phue_scene=phue_scene)

    when = HomieWhen(homie, params)

    assert when.outcome is True


    phue_scene = (
        WhenPhueSceneParams(
            group='jupiter_room',
            scenes=['sleep']))

    params = HomieWhenParams(
        phue_scene=phue_scene)

    when = HomieWhen(homie, params)

    assert when.outcome is False
