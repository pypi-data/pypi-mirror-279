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



def test_UbiqRouter(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    routers = homie.ubiq_routers
    router = routers['jupiter']


    attrs = list(router.__dict__)

    assert attrs == [
        '_UbiqRouter__homie',
        '_UbiqRouter__params',
        '_UbiqRouter__router',
        '_UbiqRouter__name',
        '_UbiqRouter__fetched',
        '_UbiqRouter__merged',
        '_UbiqRouter__timer']


    assert inrepr(
        'router.UbiqRouter object',
        router)

    assert hash(router) > 0

    assert instr(
        'router.UbiqRouter object',
        router)


    assert router.homie is homie

    assert router.params is not None

    assert router.router is not None

    assert router.name == 'jupiter'

    assert router.connect is False


    sample_path = (
        f'{SAMPLES}/router/fetched.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=router.fetched,
        replace=REPLACES)

    expect = prep_sample(
        content=router.fetched,
        replace=REPLACES)

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/router/merged.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=router.merged,
        replace=REPLACES)

    expect = prep_sample(
        content=router.merged,
        replace=REPLACES)

    assert sample == expect


    sample_path = (
        f'{SAMPLES}/router/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=router.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=router.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_UbiqRouter_source(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    routers = homie.ubiq_routers
    router = routers['jupiter']


    source = router.get_source(
        '65d963e0e9285243cbbe6116')

    assert source is not None
    assert source['_id'] == (
        '65d963e0e9285243cbbe6116')



def test_UbiqRouter_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    routers = homie.ubiq_routers
    router = routers['jupiter']

    ubid = '65d963e0e9285243cbbe6116'


    source = router.get_source(
        '1a:01:68:00:11:00')

    assert source is not None
    assert source['_id'] == ubid


    source = router.get_source(
        '192.168.1.100')

    assert source is not None
    assert source['_id'] == ubid


    source = router.get_source(
        label='Jupiter Desktop')

    assert source is not None
    assert source['_id'] == ubid
