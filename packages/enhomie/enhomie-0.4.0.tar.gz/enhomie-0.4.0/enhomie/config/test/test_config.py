"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon import ENPYRWS
from encommon.utils import load_sample
from encommon.utils import prep_sample

from . import SAMPLES
from ... import PROJECT
from ...conftest import REPLACES

if TYPE_CHECKING:
    from ..config import Config



def test_Config(
    tmp_path: Path,
    config: 'Config',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param config: Primary class instance for configuration.
    """

    replaces = REPLACES | {
        'pytemp': tmp_path,
        'PROJECT': PROJECT,
        'SAMPLES': SAMPLES}

    sample_path = (
        f'{SAMPLES}/config.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=config.config,
        replace=replaces)

    expect = prep_sample(
        content=config.config,
        replace=replaces)

    assert sample == expect
