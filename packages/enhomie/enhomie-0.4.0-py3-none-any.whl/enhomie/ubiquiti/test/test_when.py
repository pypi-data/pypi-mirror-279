"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon.utils import save_text

from respx import MockRouter

from ..params import WhenUbiqClientParams
from ...conftest import config_factory
from ...conftest import homie_factory
from ...homie import HomieWhen
from ...homie import HomieWhenParams

if TYPE_CHECKING:
    from ...homie import Homie



def test_when_ubiq_client(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """


    ubiq_client = (
        WhenUbiqClientParams(
            routers=['jupiter'],
            clients=['laptop']))

    params = HomieWhenParams(
        ubiq_client=ubiq_client)

    when = HomieWhen(homie, params)

    assert when.outcome is True


    ubiq_client = (
        WhenUbiqClientParams(
            routers=['jupiter'],
            clients=['laptop'],
            since=10))

    params = HomieWhenParams(
        ubiq_client=ubiq_client)

    when = HomieWhen(homie, params)

    assert when.outcome is True



def test_when_ubiq_client_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    """

    config = (
        'ubiq_clients:\n'
        '  noexst:\n'
        '    router: jupiter\n'
        '    ubid: noexst\n'
        '  doexst:\n'
        '    router: neptune\n'
        '    label: My Phone\n')


    Path.mkdir(
        tmp_path.joinpath('config'))

    save_text(
        f'{tmp_path}/config/test.yml',
        content=config)

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock)


    ubiq_client = (
        WhenUbiqClientParams(
            routers=['jupiter'],
            clients=['noexst']))

    params = HomieWhenParams(
        ubiq_client=ubiq_client)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    ubiq_client = (
        WhenUbiqClientParams(
            clients=['doexst']))

    params = HomieWhenParams(
        ubiq_client=ubiq_client)

    when = HomieWhen(homie, params)

    assert when.outcome is False


    ubiq_client = (
        WhenUbiqClientParams(
            routers=['jupiter'],
            clients=['phone'],
            since=90000))

    params = HomieWhenParams(
        ubiq_client=ubiq_client)

    when = HomieWhen(homie, params)

    assert when.outcome is True
