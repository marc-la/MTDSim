/* GAP Cytoscape viewer.
 *
 * Data pipeline: the HTML embeds two script tags — the full payload and the
 * initial filter state. This module builds the Cytoscape graph once, then
 * applies filter changes reactively by updating node/edge visibility classes.
 * No data is ever re-fetched.
 */
(function () {
  const PAYLOAD = JSON.parse(document.getElementById("gap-payload").textContent);
  const INITIAL = JSON.parse(document.getElementById("gap-initial-filter").textContent);

  const tacticColour = {};
  PAYLOAD.tactics.forEach(t => { tacticColour[t.id] = t.color; });

  const evidenceColour = {};
  const evidenceLabel = {};
  PAYLOAD.evidence_types.forEach(e => { evidenceColour[e.id] = e.color; evidenceLabel[e.id] = e.label; });

  const motivLabel = {};
  const motivColour = {};
  PAYLOAD.motivations.forEach(m => { motivLabel[m.id] = m.label; motivColour[m.id] = m.color; });

  // --------------------------------------------------------------
  // State

  const state = {
    visibleEvidence: new Set(),
    minConf: INITIAL.min_confidence || 0,
    onlyConsensus: !!INITIAL.only_consensus,
    hideIsolated: INITIAL.hide_isolated !== false,
    hideBackward: false,
    selectedMotivations: new Set(PAYLOAD.motivations.map(m => m.id)),
    includeUnattributed: true,
    selectedGroups: null,   // null = all
    selectedCampaigns: null,
    selectedTactics: new Set(PAYLOAD.tactics.map(t => t.id)),
    nodeSearch: "",
    pathHighlight: null,    // {nodes:Set, edges:Set}
  };

  function applyPreset(name) {
    if (name === "attack_flow") {
      state.visibleEvidence = new Set(["attack_flow"]);
    } else if (name === "curated") {
      state.visibleEvidence = new Set(["attack_flow", "ontology"]);
    } else if (name === "all") {
      state.visibleEvidence = new Set(PAYLOAD.evidence_types.map(e => e.id));
    }
  }

  // Seed initial evidence visibility
  if (INITIAL.evidence_types) {
    state.visibleEvidence = new Set(INITIAL.evidence_types);
  } else {
    applyPreset(INITIAL.preset || "attack_flow");
  }

  // --------------------------------------------------------------
  // Cytoscape elements

  const cyNodes = PAYLOAD.nodes.map(n => ({
    data: {
      id: n.id,
      label: `${n.id}\n${(n.label || "").slice(0, 28)}`,
      fullLabel: n.label,
      tactic: n.tactic,
      layer: n.layer,
      group_ids: n.group_ids,
      campaign_ids: n.campaign_ids,
      motivations: n.motivations,
      orphan: n.orphan,
      payload: n,
    },
    classes: n.orphan ? "orphan" : "",
  }));

  const cyEdges = PAYLOAD.edges.map(e => ({
    data: {
      id: e.id,
      source: e.source,
      target: e.target,
      primary_evidence: e.primary_evidence,
      evidence_types: e.evidence_types,
      confidence: e.confidence,
      source_count: e.source_count,
      consensus: e.consensus,
      backward: e.backward,
      motivations: e.motivations,
      source_groups: e.source_groups,
      campaigns: e.campaigns,
      payload: e,
    },
    classes: [
      e.backward ? "backward" : "forward",
      e.consensus ? "consensus" : "",
    ].filter(Boolean).join(" "),
  }));

  // --------------------------------------------------------------
  // Cytoscape init

  if (window.cytoscape && window.cytoscapeDagre) {
    window.cytoscape.use(window.cytoscapeDagre);
  }

  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [...cyNodes, ...cyEdges],
    wheelSensitivity: 0.2,
    style: [
      {
        selector: "node",
        style: {
          "background-color": ele => tacticColour[ele.data("tactic")] || "#888",
          "label": "data(label)",
          "text-wrap": "wrap",
          "text-max-width": 110,
          "font-size": 9,
          "color": "#ddd",
          "text-valign": "bottom",
          "text-margin-y": 3,
          "width": 22, "height": 22,
          "border-width": 1,
          "border-color": "#3b4261",
        },
      },
      {
        selector: "node.orphan",
        style: { "border-style": "dashed", "border-color": "#7f88b0", "opacity": 0.6 },
      },
      {
        selector: "node.dim",
        style: { "opacity": 0.1, "text-opacity": 0.1 },
      },
      {
        selector: "node.hit",
        style: { "border-color": "#f7768e", "border-width": 3 },
      },
      {
        selector: "edge",
        style: {
          "curve-style": "bezier",
          "width": ele => 1 + 3 * (ele.data("confidence") || 0),
          "line-color": ele => evidenceColour[ele.data("primary_evidence")] || "#888",
          "target-arrow-color": ele => evidenceColour[ele.data("primary_evidence")] || "#888",
          "target-arrow-shape": "triangle",
          "arrow-scale": 0.8,
          "opacity": 0.75,
        },
      },
      { selector: "edge.backward", style: { "line-style": "dashed" } },
      { selector: "edge.consensus", style: { "width": 3.5 } },
      { selector: "edge.dim", style: { "opacity": 0.05 } },
      { selector: "edge.hidden", style: { "display": "none" } },
      { selector: "node.hidden", style: { "display": "none" } },
      { selector: ".path-highlight",
        style: { "line-color": "#f7768e", "target-arrow-color": "#f7768e",
                 "border-color": "#f7768e", "border-width": 3, "opacity": 1 } },
    ],
    layout: {
      name: "preset",
      positions: (ele) => {
        const layer = ele.data("layer");
        return {
          x: (layer >= 0 ? layer : PAYLOAD.tactics.length) * 170,
          y: 0,
        };
      },
    },
  });

  // Per-tactic columnar layout: nodes stacked by name within layer
  (function positionByLayer() {
    const byLayer = {};
    cy.nodes().forEach(n => {
      const l = n.data("layer");
      (byLayer[l] = byLayer[l] || []).push(n);
    });
    Object.keys(byLayer).forEach(l => {
      const arr = byLayer[l];
      arr.sort((a, b) => (b.data("payload").group_count - a.data("payload").group_count)
                     || a.data("id").localeCompare(b.data("id")));
      arr.forEach((n, i) => n.position({ x: Number(l) * 200, y: i * 34 }));
    });
    cy.fit(null, 30);
  })();

  // --------------------------------------------------------------
  // Filter engine

  function edgeVisible(e) {
    const d = e.data();
    if (!d.evidence_types.some(t => state.visibleEvidence.has(t))) return false;
    if (d.confidence < state.minConf) return false;
    if (state.onlyConsensus && !d.consensus) return false;
    if (state.hideBackward && d.backward) return false;

    // Motivation/group/campaign filtering: an edge is shown if at least one
    // of its attributed groups matches the selected motivation AND the group
    // filter, OR it has no attribution (shown when "Include unattributed").
    const hasAttribution = d.source_groups.length > 0;
    if (hasAttribution) {
      const motivOK = d.motivations.length === 0
        ? state.includeUnattributed
        : d.motivations.some(m => state.selectedMotivations.has(m));
      if (!motivOK) return false;
      if (state.selectedGroups && !d.source_groups.some(g => state.selectedGroups.has(g))) return false;
      if (state.selectedCampaigns && !d.campaigns.some(c => {
        const cid = PAYLOAD.campaigns[c] ? c : `AF:${c}`;
        return state.selectedCampaigns.has(cid);
      })) return false;
    } else {
      if (!state.includeUnattributed) return false;
    }
    return true;
  }

  function nodeVisible(n, hasVisibleEdge) {
    const d = n.data();
    if (!state.selectedTactics.has(d.tactic)) return false;
    if (state.hideIsolated && !hasVisibleEdge && d.orphan) return false;
    if (state.hideIsolated && !hasVisibleEdge) return false;
    if (state.nodeSearch) {
      const q = state.nodeSearch.toLowerCase();
      const hay = (d.id + " " + (d.payload.label || "")).toLowerCase();
      if (!hay.includes(q)) return false;
    }
    // Motivation + group filters at node level (so endpoint-free nodes with
    // matching attribution still display in a tactic-only scan).
    if (state.selectedGroups) {
      if (!d.group_ids.some(g => state.selectedGroups.has(g))) return false;
    }
    return true;
  }

  function applyFilters() {
    // Pass 1: edge visibility + touched-node set
    const touched = new Set();
    cy.edges().forEach(e => {
      const show = edgeVisible(e);
      e.toggleClass("hidden", !show);
      if (show) {
        touched.add(e.data("source"));
        touched.add(e.data("target"));
      }
    });
    // Pass 2: node visibility
    cy.nodes().forEach(n => {
      const show = nodeVisible(n, touched.has(n.data("id")));
      n.toggleClass("hidden", !show);
    });
    updateLiveCounts();
  }

  function updateLiveCounts() {
    const nv = cy.nodes().filter(n => !n.hasClass("hidden")).length;
    const ev = cy.edges().filter(e => !e.hasClass("hidden")).length;
    document.getElementById("live-counts").textContent =
      `${nv} techniques · ${ev} edges visible  (of ${PAYLOAD.nodes.length} / ${PAYLOAD.edges.length})`;
  }

  // --------------------------------------------------------------
  // Filter UI wiring

  const $ = sel => document.querySelector(sel);

  // Evidence chips
  const evList = $("#evidence-list");
  PAYLOAD.evidence_types.forEach(ev => {
    const lbl = document.createElement("label");
    lbl.innerHTML = `<span class="chip-swatch" style="background:${ev.color}"></span>
      <input type="checkbox" value="${ev.id}" ${state.visibleEvidence.has(ev.id) ? "checked" : ""}> ${ev.label}`;
    lbl.classList.toggle("off", !state.visibleEvidence.has(ev.id));
    lbl.querySelector("input").addEventListener("change", (e) => {
      if (e.target.checked) state.visibleEvidence.add(ev.id);
      else state.visibleEvidence.delete(ev.id);
      lbl.classList.toggle("off", !e.target.checked);
      // Flip preset to custom when user touches evidence directly
      document.querySelector('input[name="preset"][value="custom"]').checked = true;
      applyFilters();
    });
    evList.appendChild(lbl);
  });

  // Presets
  document.querySelectorAll('input[name="preset"]').forEach(r => {
    r.addEventListener("change", (e) => {
      if (e.target.value === "custom") return;
      applyPreset(e.target.value);
      // Sync evidence checkboxes
      evList.querySelectorAll("input").forEach(inp => {
        inp.checked = state.visibleEvidence.has(inp.value);
        inp.parentElement.classList.toggle("off", !inp.checked);
      });
      applyFilters();
    });
  });

  // Motivation chips
  const motivList = $("#motivation-list");
  const groupCoverage = (() => {
    const groups = Object.values(PAYLOAD.groups);
    const withM = groups.filter(g => g.motivations.length > 0).length;
    return `${withM}/${groups.length} groups attributed`;
  })();
  $("#motiv-coverage").textContent = groupCoverage;
  PAYLOAD.motivations.forEach(m => {
    const lbl = document.createElement("label");
    lbl.innerHTML = `<span class="chip-swatch" style="background:${m.color}"></span>
      <input type="checkbox" value="${m.id}" checked> ${m.label}`;
    lbl.querySelector("input").addEventListener("change", (e) => {
      if (e.target.checked) state.selectedMotivations.add(m.id);
      else state.selectedMotivations.delete(m.id);
      lbl.classList.toggle("off", !e.target.checked);
      applyFilters();
    });
    motivList.appendChild(lbl);
  });
  $("#include-unattributed").addEventListener("change", e => {
    state.includeUnattributed = e.target.checked; applyFilters();
  });

  // Tactic chips
  const tacList = $("#tactic-list");
  PAYLOAD.tactics.forEach(t => {
    const lbl = document.createElement("label");
    lbl.innerHTML = `<span class="chip-swatch" style="background:${t.color}"></span>
      <input type="checkbox" value="${t.id}" checked> ${t.label}`;
    lbl.querySelector("input").addEventListener("change", (e) => {
      if (e.target.checked) state.selectedTactics.add(t.id);
      else state.selectedTactics.delete(t.id);
      lbl.classList.toggle("off", !e.target.checked);
      applyFilters();
    });
    tacList.appendChild(lbl);
  });

  // Group list
  function renderPickList(containerSel, items, labelFn, stateKey) {
    const container = $(containerSel);
    container.innerHTML = "";
    items.forEach(it => {
      const lbl = document.createElement("label");
      lbl.innerHTML = `<input type="checkbox" value="${it.id}"> ${labelFn(it)}`;
      lbl.querySelector("input").addEventListener("change", (e) => {
        if (state[stateKey] === null) state[stateKey] = new Set();
        if (e.target.checked) state[stateKey].add(it.id);
        else state[stateKey].delete(it.id);
        if (state[stateKey].size === 0) state[stateKey] = null;
        applyFilters();
      });
      container.appendChild(lbl);
    });
  }
  const groupItems = Object.values(PAYLOAD.groups)
    .sort((a, b) => a.name.localeCompare(b.name));
  renderPickList("#group-list", groupItems,
    g => `${g.id} — ${g.name}${g.regions.length ? ` <span class="muted small">[${g.regions.join(",")}]</span>` : ""}`,
    "selectedGroups");
  $("#group-search").addEventListener("input", e => {
    const q = e.target.value.toLowerCase();
    $("#group-list").querySelectorAll("label").forEach(l => {
      l.style.display = l.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });

  const campaignItems = Object.values(PAYLOAD.campaigns)
    .sort((a, b) => a.name.localeCompare(b.name));
  renderPickList("#campaign-list", campaignItems,
    c => `${c.source === "attack_flow" ? "⌁" : "●"} ${c.name} <span class="muted small">(${c.technique_ids.length}T)</span>`,
    "selectedCampaigns");
  $("#campaign-search").addEventListener("input", e => {
    const q = e.target.value.toLowerCase();
    $("#campaign-list").querySelectorAll("label").forEach(l => {
      l.style.display = l.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });

  // Advanced controls
  $("#min-conf").addEventListener("input", e => {
    state.minConf = Number(e.target.value);
    $("#min-conf-val").textContent = state.minConf.toFixed(2);
    applyFilters();
  });
  $("#only-consensus").addEventListener("change", e => { state.onlyConsensus = e.target.checked; applyFilters(); });
  $("#hide-isolated").addEventListener("change", e => { state.hideIsolated = e.target.checked; applyFilters(); });
  $("#hide-backward").addEventListener("change", e => { state.hideBackward = e.target.checked; applyFilters(); });
  $("#node-search").addEventListener("input", e => { state.nodeSearch = e.target.value; applyFilters(); });

  // --------------------------------------------------------------
  // Panel collapse + resize

  document.querySelectorAll(".collapse").forEach(btn => {
    btn.addEventListener("click", () => {
      document.getElementById(btn.dataset.target).classList.toggle("collapsed");
      btn.textContent = btn.textContent === "‹" ? "›" : (btn.textContent === "›" ? "‹" : btn.textContent);
      setTimeout(() => cy.resize(), 200);
    });
  });

  document.querySelectorAll(".resize-handle").forEach(h => {
    h.addEventListener("mousedown", (e) => {
      e.preventDefault();
      const panel = document.getElementById(h.dataset.target);
      const isLeft = h.classList.contains("left");
      const startX = e.clientX;
      const startW = panel.getBoundingClientRect().width;
      function onMove(ev) {
        const dx = ev.clientX - startX;
        const w = Math.max(180, Math.min(560, startW + (isLeft ? -dx : dx)));
        document.documentElement.style.setProperty(isLeft ? "--right-w" : "--left-w", w + "px");
        cy.resize();
      }
      function onUp() {
        document.removeEventListener("mousemove", onMove);
        document.removeEventListener("mouseup", onUp);
      }
      document.addEventListener("mousemove", onMove);
      document.addEventListener("mouseup", onUp);
    });
  });

  // --------------------------------------------------------------
  // Legend

  function renderLegend(tab) {
    const body = $("#legend-body");
    body.innerHTML = "";
    if (tab === "tactics") {
      PAYLOAD.tactics.forEach(t => {
        body.innerHTML += `<div class="row"><span class="sw" style="background:${t.color}"></span>${t.label}</div>`;
      });
    } else if (tab === "evidence") {
      body.style.gridTemplateColumns = "auto auto";
      PAYLOAD.evidence_types.forEach(e => {
        body.innerHTML += `<div class="row"><span class="sw" style="background:${e.color}"></span>${e.label}</div>`;
      });
    } else if (tab === "motivation") {
      body.style.gridTemplateColumns = "auto auto";
      PAYLOAD.motivations.forEach(m => {
        body.innerHTML += `<div class="row"><span class="sw" style="background:${m.color}"></span>${m.label}</div>`;
      });
    } else if (tab === "lines") {
      body.style.gridTemplateColumns = "auto auto";
      body.innerHTML = `
        <div class="row"><span class="ln" style="background:#aaa"></span>Forward (tactic-respecting)</div>
        <div class="row"><span class="ln" style="background:#aaa;border-top:1px dashed #aaa"></span>Backward (loop)</div>
        <div class="row"><span class="ln" style="background:#aaa;height:4px"></span>Consensus (≥2 sources)</div>
        <div class="row"><span class="sw" style="background:transparent;border:1px dashed #7f88b0"></span>Orphan technique</div>
      `;
    }
  }
  document.querySelectorAll(".legend-tabs .tab").forEach(t => {
    t.addEventListener("click", () => {
      document.querySelectorAll(".legend-tabs .tab").forEach(x => x.classList.remove("active"));
      t.classList.add("active");
      renderLegend(t.dataset.tab);
    });
  });
  renderLegend("tactics");

  // --------------------------------------------------------------
  // Details panel

  function chip(text, colour) {
    const style = colour ? `background:${colour};` : "";
    return `<span class="chip motiv" style="${style}">${text}</span>`;
  }

  function renderNodeDetails(n) {
    const d = n.data("payload");
    const groupRows = d.group_ids.map(gid => {
      const g = PAYLOAD.groups[gid];
      if (!g) return `<li>${gid}</li>`;
      const motChips = g.motivations.map(m => chip(motivLabel[m] || m, motivColour[m])).join(" ");
      const region = g.regions.length ? ` <span class="muted small">[${g.regions.join(",")}]</span>` : "";
      return `<li><strong>${g.id}</strong> ${g.name}${region} ${motChips}</li>`;
    }).join("");
    const campaignRows = d.campaign_ids.map(cid => {
      const c = PAYLOAD.campaigns[cid];
      return c ? `<li><strong>${c.id}</strong> ${c.name}</li>` : `<li>${cid}</li>`;
    }).join("");
    $("#details").innerHTML = `
      <h3><span class="tid">${d.id}</span> ${d.label || ""}</h3>
      <div class="muted small">${d.tactic || ""}${d.orphan ? " · orphan" : ""}</div>
      <section>
        <div class="muted small">Platforms</div>
        ${(d.platforms || []).map(p => chip(p)).join(" ") || '<span class="muted small">—</span>'}
      </section>
      <section>
        <div class="muted small">Description</div>
        <div>${d.description || '<span class="muted">—</span>'}</div>
      </section>
      <section>
        <div class="muted small">APT groups (${d.group_ids.length})</div>
        <ul>${groupRows || '<li class="muted">none</li>'}</ul>
      </section>
      <section>
        <div class="muted small">Campaigns (${d.campaign_ids.length})</div>
        <ul>${campaignRows || '<li class="muted">none</li>'}</ul>
      </section>
    `;
  }

  function renderEdgeDetails(e) {
    const d = e.data("payload");
    const evBlocks = d.evidence.map(ev => `
      <div class="evidence-item">
        <div class="src">${evidenceLabel[ev.source_type] || ev.source_type}</div>
        <div>${ev.description || ''}</div>
        ${ev.campaigns && ev.campaigns.length
          ? `<div class="muted small">Campaigns: ${ev.campaigns.join(", ")}</div>` : ""}
        ${ev.source_url
          ? `<div class="muted small"><a style="color:#7aa2f7" href="${ev.source_url}" target="_blank">source</a></div>` : ""}
      </div>`).join("");
    const motChips = d.motivations.map(m => chip(motivLabel[m] || m, motivColour[m])).join(" ");
    $("#details").innerHTML = `
      <h3><span class="tid">${d.source}</span> → <span class="tid">${d.target}</span></h3>
      <div class="muted small">
        confidence ${Number(d.confidence).toFixed(2)} ·
        ${d.source_count} source${d.source_count === 1 ? "" : "s"}${d.consensus ? " · consensus" : ""}${d.backward ? " · backward" : ""}
      </div>
      <section>
        <div class="muted small">Evidence</div>
        ${evBlocks}
      </section>
      <section>
        <div class="muted small">Implicated APT groups (${d.source_groups.length})</div>
        ${d.source_groups.map(gid => {
          const g = PAYLOAD.groups[gid];
          return g ? `<div>${g.id} — ${g.name}</div>` : `<div>${gid}</div>`;
        }).join("") || '<div class="muted">none</div>'}
      </section>
      <section>
        <div class="muted small">Motivations represented</div>
        ${motChips || '<span class="muted">—</span>'}
      </section>
    `;
  }

  cy.on("tap", "node", evt => renderNodeDetails(evt.target));
  cy.on("tap", "edge", evt => renderEdgeDetails(evt.target));
  cy.on("tap", evt => {
    if (evt.target === cy) {
      $("#details").innerHTML = '<p class="muted">Select a node or edge to see provenance.</p>';
    }
  });

  // --------------------------------------------------------------
  // Attack path queries (k shortest simple paths, BFS-based)

  function kShortestPaths(src, tgt, k) {
    // Simple BFS enumeration, bounded depth
    const results = [];
    const maxDepth = 8;
    const adj = {};
    cy.edges().forEach(e => {
      if (e.hasClass("hidden")) return;
      const s = e.data("source"), t = e.data("target");
      (adj[s] = adj[s] || []).push({ t, edge: e.id() });
    });
    const q = [[src, [src], []]];
    while (q.length && results.length < k) {
      const [cur, path, edges] = q.shift();
      if (cur === tgt && path.length > 1) { results.push({ nodes: path, edges }); continue; }
      if (path.length > maxDepth) continue;
      for (const nb of (adj[cur] || [])) {
        if (path.includes(nb.t)) continue;
        q.push([nb.t, [...path, nb.t], [...edges, nb.edge]]);
      }
    }
    return results;
  }

  $("#btn-path").addEventListener("click", () => {
    const from = $("#path-from").value.trim().toUpperCase();
    const to = $("#path-to").value.trim().toUpperCase();
    const k = Math.max(1, Math.min(10, Number($("#path-k").value) || 3));
    if (!from || !to) { $("#path-results").textContent = "Need both endpoints"; return; }
    const paths = kShortestPaths(from, to, k);
    cy.elements().removeClass("path-highlight");
    if (paths.length === 0) {
      $("#path-results").textContent = "No path found (check filters/direction)";
      return;
    }
    const nodeSet = new Set(), edgeSet = new Set();
    paths.forEach(p => {
      p.nodes.forEach(n => nodeSet.add(n));
      p.edges.forEach(e => edgeSet.add(e));
    });
    nodeSet.forEach(n => cy.getElementById(n).addClass("path-highlight"));
    edgeSet.forEach(e => cy.getElementById(e).addClass("path-highlight"));
    $("#path-results").innerHTML = paths.map((p, i) =>
      `<div>${i + 1}: ${p.nodes.join(" → ")}</div>`).join("");
  });
  $("#btn-path-clear").addEventListener("click", () => {
    cy.elements().removeClass("path-highlight");
    $("#path-results").textContent = "";
  });

  // --------------------------------------------------------------
  // Header actions

  $("#btn-fit").addEventListener("click", () => cy.fit(null, 30));
  $("#btn-reset").addEventListener("click", () => window.location.reload());

  // --------------------------------------------------------------
  // Initial paint

  applyFilters();
})();
