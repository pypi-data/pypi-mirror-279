"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional

from pydantic import BaseModel

from ..builtins import WhenTimePeriodParams
from ..philipshue import WhatPhueButtonParams
from ..philipshue import WhatPhueMotionParams
from ..philipshue import WhenPhueChangeParams
from ..philipshue import WhenPhueSceneParams
from ..ubiquiti import WhenUbiqClientParams



GROUP_TYPES = Literal['room', 'zone']



class HomieGroupParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    .. note::
       Value is required for ``phue_label`` but may one day
       become optional, should another product be supported.

    :param type: What type of group does the group represent.
    :param phue_bridge: Which bridge will group be found on.
    :param phue_label: Value for matching the name of group.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    type: GROUP_TYPES

    phue_bridge: str
    phue_label: str



class HomieSceneParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    .. note::
       Value is required for ``phue_label`` but may one day
       become optional, should another product be supported.

    :param phue_label: Value for matching the name of scene.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    phue_label: str



class HomieWhenParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    .. warning::
       See documentation on the ``family`` input parameter.

    :param negate: Whether or not final outcome is inverted.
    :param family: Aggregate the conditionals where `any` in
        the family may be `True`. Note for `default` group,
        `all` of the conditionals within must match `True`.
    :param time_period: Pamaters for the conditional plugin.
    :param phue_change: Pamaters for the conditional plugin.
    :param phue_scene: Pamaters for the conditional plugin.
    :param ubiq_client: Pamaters for the conditional plugin.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    negate: bool = False
    family: str = 'default'

    time_period: Optional[WhenTimePeriodParams] = None
    phue_change: Optional[WhenPhueChangeParams] = None
    phue_scene: Optional[WhenPhueSceneParams] = None
    ubiq_client: Optional[WhenUbiqClientParams] = None



class HomieDesireParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param groups: Names of Homie groups which are in scope.
    :param scene: Name of the Homie scene which is desired.
    :param weight: Useful when other conditionals match one
        of the provided groups, will determine precedence.
    :param delay: Delay before taking action on scene change.
        This depends on the state file being defined to work
        between script executions, otherwise delay breaks.
    :param when: List of conditionals for determining match.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    groups: list[str]
    scene: str

    weight: int = 0
    delay: int = 0

    when: Optional[list[HomieWhenParams]] = None



class HomieWhatParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param phue_button: Parameters for use in action plugin.
    :param phue_motion: Parameters for use in action plugin.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    phue_button: Optional[WhatPhueButtonParams] = None
    phue_motion: Optional[WhatPhueMotionParams] = None



class HomieActionParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param groups: Names of Homie groups which are in scope.
    :param scene: Name of the Homie scene which is desired.
    :param weight: Useful when other conditionals match one
        of the provided groups, will determine precedence.
    :param pause: Delay before performing the same action.
        This depends on the state file being defined to work
        between script executions, otherwise delay breaks.
    :param what: List of events which can trigger operation.
    :param when: List of conditionals for determining match.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    groups: list[str]
    scene: str

    weight: int = 0
    pause: int = 5

    what: Optional[list[HomieWhatParams]] = None
    when: Optional[list[HomieWhenParams]] = None
