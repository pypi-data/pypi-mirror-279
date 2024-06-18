"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..homie import HomieWhen



def when_ubiq_client(
    when: 'HomieWhen',
) -> bool:
    """
    Return the boolean indicating whether condition matched.

    :param when: Primary class instance for the conditonal.
    :returns: Boolean indicating whether condition matched.
    """

    params = (
        when.params.ubiq_client)

    assert params is not None

    _routers = params.routers
    _clients = params.clients
    since = params.since

    routers = when.homie.ubiq_routers
    clients = when.homie.ubiq_clients


    def _append_outcome() -> None:

        _router_names = (
            _routers or routers)

        assert connect is not False
        assert lseen is not None

        for name in _router_names:

            _lseen = lseen.get(name)

            if (_lseen is not None
                    and _lseen.since < since):
                outcomes.append(True)

            elif name in connect:
                outcomes.append(True)


    outcomes: list[bool] = []

    for name in _clients:

        client = clients[name]
        client.refresh_source()

        present = client.present
        connect = client.connect
        lseen = client.lastseen

        if present is False:
            outcomes.append(False)
            continue

        if connect is False:
            outcomes.append(False)
            continue

        _append_outcome()


    return any(outcomes)



def chck_ubiq_client(
    when: 'HomieWhen',
) -> None:
    """
    Return the boolean indicating whether conditional valid.

    :param when: Primary class instance for the conditonal.
    """

    params = (
        when.params.ubiq_client)

    assert params is not None

    routers = (
        when.homie.ubiq_routers)


    _routers = (
        params.routers or [])

    for name in _routers:
        assert name in routers
