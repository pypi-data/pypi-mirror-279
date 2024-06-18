"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import TYPE_CHECKING

from encommon.types import getate

if TYPE_CHECKING:
    from ..homie import HomieWhat



def what_phue_motion(
    what: 'HomieWhat',
    event: dict[str, Any],
) -> bool:
    """
    Return the boolean indicating whether condition matched.

    :param what: Primary class instance for the conditonal.
    :param event: Event which was yielded from the stream.
    :returns: Boolean indicating whether condition matched.
    """

    params = (
        what.params.phue_motion)

    assert params is not None

    _device = params.device
    _sensor = params.sensor


    devices = (
        what.homie.phue_devices)

    device = devices[_device]

    if not device.unique:
        device.refresh_source()

    unique = device.unique

    if unique is None:
        return False


    sensors = device.sensors

    assert sensors is not None

    sensor = sensors[_sensor]


    matched: list[bool] = []


    if 'data' not in event:
        return False

    for item in event['data']:

        if 'motion' not in item:
            continue

        _sensor = item['id']
        _unique = item['owner']['rid']

        if unique != _unique:
            continue

        if sensor != _sensor:
            continue  # NOCVR

        matched.append(True)


    return any(matched)



def chck_phue_motion(
    what: 'HomieWhat',
) -> None:
    """
    Return the boolean indicating whether conditional valid.

    :param what: Primary class instance for the conditonal.
    """

    params = (
        what.params.phue_motion)

    assert params is not None

    devices = (
        what.homie.phue_devices)


    _device = params.device

    assert _device in devices



def what_phue_button(
    what: 'HomieWhat',
    event: dict[str, Any],
) -> bool:
    """
    Return the boolean indicating whether condition matched.

    :param what: Primary class instance for the conditonal.
    :param event: Event which was yielded from the stream.
    :returns: Boolean indicating whether condition matched.
    """

    params = (
        what.params.phue_button)

    assert params is not None

    _device = params.device
    _sensor = params.sensor
    _events = params.events


    devices = (
        what.homie.phue_devices)

    device = devices[_device]

    if not device.unique:
        device.refresh_source()

    unique = device.unique

    if unique is None:
        return False


    sensors = device.sensors

    assert sensors is not None

    sensor = sensors[_sensor]


    matched: list[bool] = []


    if 'data' not in event:
        return False

    for item in event['data']:

        if 'button' not in item:
            continue

        _sensor = item['id']
        _unique = item['owner']['rid']
        _event = getate(
            item, 'button/last_event')

        if unique != _unique:
            continue

        if sensor != _sensor:
            continue

        if _event not in _events:
            continue

        matched.append(True)


    return any(matched)



def chck_phue_button(
    what: 'HomieWhat',
) -> None:
    """
    Return the boolean indicating whether conditional valid.

    :param what: Primary class instance for the conditonal.
    """

    params = (
        what.params.phue_button)

    assert params is not None

    devices = (
        what.homie.phue_devices)


    _device = params.device

    assert _device in devices
