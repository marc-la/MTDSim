"""Layout render smoke test.

Asserts the §1 fix for the network double-render: there is exactly one
``dcc.Graph`` whose id maps to the network surface in the active tab on
initial layout. Walks the layout tree without booting a server.
"""

from __future__ import annotations

from typing import Iterator

import pytest

from dash import dcc

from mtdsim.viz.replay.app import build_app


def _walk(node) -> Iterator:
    yield node
    children = getattr(node, "children", None)
    if children is None:
        return
    if isinstance(children, (list, tuple)):
        for c in children:
            yield from _walk(c)
    else:
        yield from _walk(children)


def _all_graph_ids(layout) -> list[str]:
    ids: list[str] = []
    for n in _walk(layout):
        if isinstance(n, dcc.Graph):
            ids.append(getattr(n, "id", ""))
    return ids


@pytest.fixture(scope="module")
def app_no_log():
    return build_app(log=None)


def test_exactly_one_network_graph_on_initial_layout(app_no_log):
    """Before any sim runs we should see one network surface, not two.

    Pre-fix: ``run-preview`` (form-driven) and ``overview-network``
    (log-driven) both rendered. The fix collapses them to ``run-network``.
    """
    ids = _all_graph_ids(app_no_log.layout)
    network_ids = [i for i in ids if "network" in (i or "")]
    assert network_ids == ["run-network"], (
        f"expected exactly one network graph (run-network); got {network_ids}"
    )


def test_profile_tab_does_not_mount_eagerly(app_no_log):
    """The Profile tab body should be a placeholder until the user clicks it."""
    ids = _all_graph_ids(app_no_log.layout)
    # profile-phase-lanes is the Profile tab's main figure; it should not
    # exist on initial layout (it mounts on first tab activation).
    assert "profile-phase-lanes" not in ids


def test_no_legacy_ids_remain(app_no_log):
    """Sanity: ids removed by the §1 fix should not reappear by accident."""
    ids = _all_graph_ids(app_no_log.layout)
    assert "run-preview" not in ids
    assert "overview-network" not in ids
    assert "overview-timeline" not in ids
