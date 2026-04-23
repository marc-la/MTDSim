"""Run-metadata + running-metrics sidebar.

Small, text-heavy panel. Rendered on the right of every tab so the analyst
never loses context on *which run* they're looking at or *what's true right
now* at the cursor.

No Plotly — the panel is just Dash components, keyed off ``store-playback``
so every tick updates the running metrics cheaply.

Checklist mapping: §7.3 (run metadata), §3.5 (cost strip lite), §2.4
(technique-coverage summary), §2.1 (current-phase readout alongside the
dedicated tracker).
"""

from __future__ import annotations

from typing import Any, Optional

from dash import html

from mtdsim.viz.replay.log import EventLog


def run_metadata_rows(log: Optional[EventLog]) -> list[tuple[str, str]]:
    if log is None:
        return [("log", "(none)")]
    meta = log.sim_meta or {}
    rows: list[tuple[str, str]] = [
        ("config", str(meta.get("config", "—"))),
        ("scheme", str(meta.get("scheme", "—"))),
        ("seed", str(meta.get("seed", "—"))),
        ("finish_time", f"{meta.get('finish_time', '—')}s"),
    ]
    np = meta.get("network_params") or {}
    if np:
        rows.append(
            (
                "network",
                f"{np.get('total_nodes', '—')} nodes · "
                f"{np.get('total_subnets', '—')} subnets · "
                f"{np.get('total_layers', '—')} layers",
            )
        )
        rows.append(("endpoints", str(np.get("total_endpoints", "—"))))
        rows.append(("databases", str(np.get("total_database", "—"))))
    rows.append(("t_max", f"{log.t_max:.0f}s"))
    rows.append(("events", str(len(log.events))))
    return rows


def running_metric_rows(
    log: Optional[EventLog], *, sim_t: float, event_index: int
) -> list[tuple[str, str]]:
    if log is None or not log.events:
        return [("sim t", "—")]
    counts = log.counts_at(event_index)
    total_nodes = (
        (log.sim_meta.get("network_params") or {}).get("total_nodes")
        or len(log.topology["nodes"])
        if log.topology
        else 0
    )
    hcr = counts["compromised"] / total_nodes if total_nodes else 0.0
    mtd_rate = counts["mtds_deployed"] / (sim_t / 60.0) if sim_t > 1.0 else 0.0
    cursor = log.attacker_cursor(event_index)
    phase = cursor.get("phase") or "—"
    technique = cursor.get("technique_id") or "—"
    host = cursor.get("host_id")
    host_s = "—" if host is None or host < 0 else str(host)
    rows: list[tuple[str, str]] = [
        ("sim t", f"{sim_t:,.1f}s"),
        ("compromised", f"{counts['compromised']}" + (f"/{total_nodes}" if total_nodes else "")),
        ("HCR", f"{hcr:.1%}"),
        ("current phase", phase),
        ("current host", host_s),
        ("current technique", technique),
        ("phases executed", str(counts["phases"])),
        ("MTDs deployed", str(counts["mtds_deployed"])),
        ("MTDs/min", f"{mtd_rate:.2f}"),
        ("interrupts", str(counts["interrupts"])),
    ]
    return rows


def render_kv(rows: list[tuple[str, str]]) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.Span(k, className="text-muted small me-2"),
                    html.Span(v, className="fw-semibold small"),
                ],
                className="d-flex justify-content-between py-1 border-bottom",
                style={"borderColor": "#f1f3f5"},
            )
            for k, v in rows
        ],
        className="px-2",
    )
