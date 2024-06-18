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
    from ...homie import Homie



def test_UbiqClient(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    clients = homie.ubiq_clients
    client = clients['jupiter_desktop']


    attrs = list(client.__dict__)

    assert attrs == [
        '_UbiqClient__homie',
        '_UbiqClient__params',
        '_UbiqClient__name',
        '_UbiqClient__sources',
        '_UbiqClient__routers']


    assert inrepr(
        'client.UbiqClient object',
        client)

    assert hash(client) > 0

    assert instr(
        'client.UbiqClient object',
        client)


    assert client.homie is homie

    assert client.params is not None

    assert client.name == 'jupiter_desktop'

    assert client.routers is None

    assert client.sources is None

    assert client.uniques is None

    assert client.present is False

    assert client.connect is False

    assert client.lastseen is None


    client.refresh_source()


    sample_path = (
        f'{SAMPLES}/client/sources.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=client.sources,
        replace=REPLACES)

    expect = prep_sample(
        content=client.sources,
        replace=REPLACES)

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/client/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=client.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=client.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_UbiqClient_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    clients = homie.ubiq_clients
    client = clients['jupiter_desktop']


    client.params.ubid = (
        '65d963e0e9285243cbbe6116')

    client.params.mac = None
    client.params.ip = None
    client.params.label = None

    client.refresh_source()

    assert client.routers is not None
    assert client.sources is not None
    assert client.present is not False
    assert len(client.present) == 1
    assert client.connect is not False
    assert len(client.connect) == 1


    client.params.ip = '192.168.1.100'

    client.params.ubid = None
    client.params.mac = None
    client.params.label = None

    client.refresh_source()

    assert client.routers is not None
    assert client.sources is not None
    # assert removed for mypy warning
    assert len(client.present) == 1
    # assert removed for mypy warning
    assert len(client.connect) == 1


    client.params.label = 'jupiter_desktop'

    client.params.ubid = None
    client.params.mac = None
    client.params.ip = None

    client.refresh_source()

    assert client.routers is not None
    assert client.sources is not None
    # assert removed for mypy warning
    assert len(client.present) == 1
    # assert removed for mypy warning
    assert len(client.connect) == 1


    client.params.label = 'noexst'

    client.params.ubid = None
    client.params.mac = None
    client.params.ip = None

    client.refresh_source()

    assert client.routers is None
    assert client.sources is None
    assert client.present is False
    assert client.connect is False


    client.params.router = 'noexst'

    client.refresh_source()

    assert client.routers is None
    assert client.sources is None
    assert client.present is False
    assert client.connect is False
