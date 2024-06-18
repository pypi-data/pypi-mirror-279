"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..homie import HomieWhen



def when_phue_change(
    when: 'HomieWhen',
) -> bool:
    """
    Return the boolean indicating whether condition matched.

    :param when: Primary class instance for the conditonal.
    :returns: Boolean indicating whether condition matched.
    """

    params = (
        when.params.phue_change)

    assert params is not None

    _devices = params.devices
    _sensors = params.sensors
    since = params.since

    devices = (
        when.homie.phue_devices)


    def _append_outcome() -> None:

        assert changed is not False

        items = changed.items()

        for key, value in items:

            if key not in _sensors:
                continue

            if value is None:
                continue

            _since = value.since

            if _since > since:
                continue

            outcomes.append(True)


    outcomes: list[bool] = []

    for name in _devices:

        device = devices[name]
        device.refresh_source()

        present = device.present
        connect = device.connect
        changed = device.changed

        if not present:
            outcomes.append(False)
            continue

        if not connect:
            outcomes.append(False)
            continue

        if not changed:
            outcomes.append(False)
            continue

        _append_outcome()


    return any(outcomes)



def chck_phue_change(
    when: 'HomieWhen',
) -> None:
    """
    Return the boolean indicating whether conditional valid.

    :param when: Primary class instance for the conditonal.
    """

    params = (
        when.params.phue_change)

    assert params is not None

    devices = (
        when.homie.phue_devices)


    _devices = params.devices

    for name in _devices:
        assert name in devices



def when_phue_scene(
    when: 'HomieWhen',
) -> bool:
    """
    Return the boolean indicating whether condition matched.

    :param when: Primary class instance for the conditonal.
    :returns: Boolean indicating whether condition matched.
    """

    homie = when.homie

    params = (
        when.params.phue_scene)

    assert params is not None

    _group = params.group
    _scenes = params.scenes


    scene = homie.scene_get(
        homie.groups[_group])


    if scene is None:
        return False

    return scene.name in _scenes



def chck_phue_scene(
    when: 'HomieWhen',
) -> None:
    """
    Return the boolean indicating whether conditional valid.

    :param when: Primary class instance for the conditonal.
    """

    params = (
        when.params.phue_scene)

    assert params is not None

    groups = when.homie.groups
    scenes = when.homie.scenes


    _group = params.group

    assert _group in groups


    _scenes = params.scenes

    for name in _scenes:
        assert name in scenes
