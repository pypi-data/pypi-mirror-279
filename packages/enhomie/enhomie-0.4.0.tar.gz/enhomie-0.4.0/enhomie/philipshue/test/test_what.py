"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from pathlib import Path
from typing import TYPE_CHECKING

from encommon.utils import read_text
from encommon.utils import save_text

from respx import MockRouter

from . import SAMPLES
from ..params import WhatPhueButtonParams
from ..params import WhatPhueMotionParams
from ...conftest import config_factory
from ...conftest import homie_factory
from ...homie import HomieWhat
from ...homie import HomieWhatParams

if TYPE_CHECKING:
    from ...homie import Homie



def test_what_phue_motion(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    _events = loads(
        read_text(
            f'{SAMPLES}/events'
            '/source.json'))


    phue_motion = (
        WhatPhueMotionParams(
            device='jupiter_motion',
            sensor='motion1'))

    params = HomieWhatParams(
        phue_motion=phue_motion)

    what = HomieWhat(homie, params)

    assert what.match(_events[0])

    assert not what.match(_events[1])



def test_what_phue_motion_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    """

    _events = loads(
        read_text(
            f'{SAMPLES}/events'
            '/source.json'))

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


    phue_motion = (
        WhatPhueMotionParams(
            device='noexst',
            sensor='motion1'))

    params = HomieWhatParams(
        phue_motion=phue_motion)

    what = HomieWhat(homie, params)

    assert not what.match(_events[0])

    assert not what.match(_events[1])


    phue_motion = (
        WhatPhueMotionParams(
            device='neptune_motion',
            sensor='motion1'))

    params = HomieWhatParams(
        phue_motion=phue_motion)

    what = HomieWhat(homie, params)

    assert not what.match(_events[0])

    assert not what.match(_events[1])


    assert not what.match({})



def test_what_phue_button(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    _events = loads(
        read_text(
            f'{SAMPLES}/events'
            '/source.json'))


    phue_button = (
        WhatPhueButtonParams(
            device='jupiter_button',
            sensor='button1',
            events=['initial_press']))

    params = HomieWhatParams(
        phue_button=phue_button)

    what = HomieWhat(homie, params)

    assert not what.match(_events[0])

    assert what.match(_events[1])



def test_what_phue_button_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    """

    _events = loads(
        read_text(
            f'{SAMPLES}/events'
            '/source.json'))

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


    phue_button = (
        WhatPhueButtonParams(
            device='noexst',
            sensor='button1',
            events=['initial_press']))

    params = HomieWhatParams(
        phue_button=phue_button)

    what = HomieWhat(homie, params)

    assert not what.match(_events[0])

    assert not what.match(_events[1])


    phue_button = (
        WhatPhueButtonParams(
            device='neptune_button',
            sensor='button1',
            events=['initial_press']))

    params = HomieWhatParams(
        phue_button=phue_button)

    what = HomieWhat(homie, params)

    assert not what.match(_events[0])

    assert not what.match(_events[1])


    phue_button = (
        WhatPhueButtonParams(
            device='jupiter_button',
            sensor='button2',
            events=['initial_press']))

    params = HomieWhatParams(
        phue_button=phue_button)

    what = HomieWhat(homie, params)

    assert not what.match(_events[0])

    assert not what.match(_events[1])


    assert not what.match({})
