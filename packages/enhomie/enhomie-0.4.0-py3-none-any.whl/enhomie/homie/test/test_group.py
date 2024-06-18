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



def test_HomieGroup(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    groups = homie.groups
    group = groups['jupiter_room']


    attrs = list(group.__dict__)

    assert attrs == [
        '_HomieGroup__homie',
        '_HomieGroup__params',
        '_HomieGroup__name']


    assert inrepr(
        'group.HomieGroup object',
        group)

    assert hash(group) > 0

    assert instr(
        'group.HomieGroup object',
        group)


    assert group.homie is homie

    assert group.params is not None

    assert group.name == 'jupiter_room'

    assert group.type == 'room'

    assert group.phue_bridge is not None

    assert group.phue_source is not None

    assert group.phue_unique == (
        'da9031f1-6229-3e2d'
        '-b143-64b2c8223915')

    assert group.phue_actual == 'Jupiter'


    sample_path = (
        f'{SAMPLES}/group/dumper.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=group.homie_dumper(),
        replace=REPLACES)

    expect = prep_sample(
        content=group.homie_dumper(),
        replace=REPLACES)

    assert sample == expect



def test_HomieGroup_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    groups = homie.groups
    group = groups['jupiter_room']
    params = group.params

    params.phue_label = 'noexst'

    assert not group.phue_actual
    assert not group.phue_unique
