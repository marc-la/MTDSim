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
  const tacticLabel = {};
  PAYLOAD.tactics.forEach(t => { tacticColour[t.id] = t.color; tacticLabel[t.id] = t.label; });

  const evidenceColour = {};
  const evidenceLabel = {};
  PAYLOAD.evidence_types.forEach(e => { evidenceColour[e.id] = e.color; evidenceLabel[e.id] = e.label; });

  // --------------------------------------------------------------
  // Pre-index payload helpers

  const nodeById = {};
  PAYLOAD.nodes.forEach(n => { nodeById[n.id] = n; });

  // CSA subgraph membership (server pre-computed against the full graph,
  // so client-side filters compose without extra graph traversal).
  const subgraphTerminal = {};
  Object.entries(PAYLOAD.subgraphs.terminal_objective || {}).forEach(([k, v]) => {
    subgraphTerminal[k] = new Set(v);
  });
  const subgraphPlatform = {};
  Object.entries(PAYLOAD.subgraphs.platform || {}).forEach(([k, v]) => {
    subgraphPlatform[k] = new Set(v);
  });

  // --------------------------------------------------------------
  // Subgraph provenance (if a selector was applied server-side)

  if (PAYLOAD.meta && PAYLOAD.meta.view) {
    const v = PAYLOAD.meta.view;
    const bits = Object.entries(v)
      .filter(([k, val]) => k !== "selector" && val !== null && val !== undefined)
      .map(([k, val]) => `${k}=${val}`);
    const label = document.getElementById("view-label");
    if (label) {
      label.textContent = ` · Subgraph: ${v.selector || "custom"}${bits.length ? " (" + bits.join(", ") + ")" : ""}`;
    }
  }

  // --------------------------------------------------------------
  // State

  const state = {
    visibleEvidence: new Set(),
    minConf: INITIAL.min_confidence || 0,
    onlyConsensus: !!INITIAL.only_consensus,
    hideIsolated: INITIAL.hide_isolated !== false,
    hideBackward: false,
    dimUnreachable: true,
    selectedGroups: null,   // null = all
    selectedCampaigns: null,
    selectedTactics: new Set(PAYLOAD.tactics.map(t => t.id)),
    csaObjectiveTactic: "",  // "" = no Strategy A restriction
    csaPlatform: "",         // "" = no Strategy B restriction
    nodeSearch: "",
    pathHighlight: null,
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
      orphan: n.orphan,
      is_objective: n.is_objective,
      reachable_from_entry: n.reachable_from_entry,
      payload: n,
    },
    classes: [
      n.orphan ? "orphan" : "",
      (n.is_objective && !n.reachable_from_entry) ? "unreachable-objective" : "",
    ].filter(Boolean).join(" "),
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
        selector: "node.unreachable-objective.dim-unreachable",
        style: {
          "background-color": "#3b4261",
          "border-color": "#3b4261",
          "border-style": "dotted",
          "opacity": 0.35,
          "color": "#7f88b0",
        },
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

  function nodeInCsa(id) {
    if (state.csaObjectiveTactic) {
      const set = subgraphTerminal[state.csaObjectiveTactic];
      if (!set || !set.has(id)) return false;
    }
    if (state.csaPlatform) {
      const set = subgraphPlatform[state.csaPlatform];
      if (!set || !set.has(id)) return false;
    }
    return true;
  }

  function edgeVisible(e) {
    const d = e.data();
    if (!d.evidence_types.some(t => state.visibleEvidence.has(t))) return false;
    if (d.confidence < state.minConf) return false;
    if (state.onlyConsensus && !d.consensus) return false;
    if (state.hideBackward && d.backward) return false;

    // CSA subgraph constraints — both endpoints must be in the subgraph.
    if (!nodeInCsa(d.source) || !nodeInCsa(d.target)) return false;

    // Group / campaign filtering (group-level attribution — MITRE-canonical).
    if (state.selectedGroups) {
      if (!d.source_groups.some(g => state.selectedGroups.has(g))) return false;
    }
    if (state.selectedCampaigns) {
      if (!d.campaigns.some(c => {
        const cid = PAYLOAD.campaigns[c] ? c : `AF:${c}`;
        return state.selectedCampaigns.has(cid);
      })) return false;
    }
    return true;
  }

  function nodeVisible(n, hasVisibleEdge) {
    const d = n.data();
    if (!state.selectedTactics.has(d.tactic)) return false;
    if (!nodeInCsa(d.id)) return false;
    if (state.hideIsolated && !hasVisibleEdge && d.orphan) return false;
    if (state.hideIsolated && !hasVisibleEdge) return false;
    if (state.nodeSearch) {
      const q = state.nodeSearch.toLowerCase();
      const hay = (d.id + " " + (d.payload.label || "")).toLowerCase();
      if (!hay.includes(q)) return false;
    }
    if (state.selectedGroups) {
      if (!d.group_ids.some(g => state.selectedGroups.has(g))) return false;
    }
    return true;
  }

  function applyFilters() {
    const touched = new Set();
    cy.edges().forEach(e => {
      const show = edgeVisible(e);
      e.toggleClass("hidden", !show);
      if (show) {
        touched.add(e.data("source"));
        touched.add(e.data("target"));
      }
    });
    cy.nodes().forEach(n => {
      const show = nodeVisible(n, touched.has(n.data("id")));
      n.toggleClass("hidden", !show);
      n.toggleClass("dim-unreachable", state.dimUnreachable);
    });
    updateLiveCounts();
    refreshPathTargets();
  }

  function updateLiveCounts() {
    const nv = cy.nodes().filter(n => !n.hasClass("hidden")).length;
    const ev = cy.edges().filter(e => !e.hasClass("hidden")).length;
    const totals = (PAYLOAD.meta && PAYLOAD.meta.totals) || {
      techniques: PAYLOAD.nodes.length, edges: PAYLOAD.edges.length,
    };
    document.getElementById("live-counts").textContent =
      `${nv} techniques · ${ev} edges visible  (of ${totals.techniques} / ${totals.edges})`;
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
      document.querySelector('input[name="preset"][value="custom"]').checked = true;
      applyFilters();
    });
    evList.appendChild(lbl);
  });

  document.querySelectorAll('input[name="preset"]').forEach(r => {
    r.addEventListener("change", (e) => {
      if (e.target.value === "custom") return;
      applyPreset(e.target.value);
      evList.querySelectorAll("input").forEach(inp => {
        inp.checked = state.visibleEvidence.has(inp.value);
        inp.parentElement.classList.toggle("off", !inp.checked);
      });
      applyFilters();
    });
  });

  // CSA subgraph dropdowns -------------------------------------------------
  const csaTacticSel = $("#csa-objective-tactic");
  Object.keys(subgraphTerminal)
    .sort((a, b) => {
      const ai = PAYLOAD.tactics.findIndex(t => t.id === a);
      const bi = PAYLOAD.tactics.findIndex(t => t.id === b);
      return ai - bi;
    })
    .forEach(tac => {
      const opt = document.createElement("option");
      opt.value = tac;
      opt.textContent = `${tacticLabel[tac] || tac} (${subgraphTerminal[tac].size} techs)`;
      csaTacticSel.appendChild(opt);
    });
  csaTacticSel.addEventListener("change", e => {
    state.csaObjectiveTactic = e.target.value;
    applyFilters();
  });

  const csaPlatSel = $("#csa-platform");
  Object.keys(subgraphPlatform).forEach(p => {
    const opt = document.createElement("option");
    opt.value = p;
    opt.textContent = `${p} (${subgraphPlatform[p].size} techs)`;
    csaPlatSel.appendChild(opt);
  });
  csaPlatSel.addEventListener("change", e => {
    state.csaPlatform = e.target.value;
    applyFilters();
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

  // Group / campaign pick lists
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
  $("#dim-unreachable").addEventListener("change", e => { state.dimUnreachable = e.target.checked; applyFilters(); });
  $("#node-search").addEventListener("input", e => { state.nodeSearch = e.target.value; applyFilters(); });

  // --------------------------------------------------------------
  // Path explorer dropdowns (entry & objective; tactic-grouped)

  function buildOptgroups(items, valueFn, labelFn, extraDataFn) {
    // Items already sorted by tactic-layer; group consecutively.
    const frag = document.createDocumentFragment();
    let curGroup = null;
    let curLabel = null;
    items.forEach(it => {
      const tac = it.tactic;
      if (tac !== curLabel) {
        curLabel = tac;
        curGroup = document.createElement("optgroup");
        curGroup.label = tacticLabel[tac] || tac;
        frag.appendChild(curGroup);
      }
      const opt = document.createElement("option");
      opt.value = valueFn(it);
      opt.textContent = labelFn(it);
      if (extraDataFn) extraDataFn(opt, it);
      curGroup.appendChild(opt);
    });
    return frag;
  }

  const pathFromSel = $("#path-from");
  const pathToSel = $("#path-to");

  pathFromSel.appendChild(buildOptgroups(
    PAYLOAD.entry_nodes,
    it => it.id,
    it => `${it.id} — ${(it.label || "").slice(0, 36)}`,
  ));

  pathToSel.appendChild(buildOptgroups(
    PAYLOAD.objective_nodes,
    it => it.id,
    it => `${it.id} — ${(it.label || "").slice(0, 36)}`,
    (opt, it) => {
      opt.dataset.origLabel = opt.textContent;
      opt.dataset.reachable = it.reachable_from_entry ? "1" : "0";
    },
  ));

  function buildAdjacency() {
    const adj = {};
    cy.edges().forEach(e => {
      if (e.hasClass("hidden")) return;
      const s = e.data("source"), t = e.data("target");
      (adj[s] = adj[s] || []).push(t);
    });
    return adj;
  }

  function reachableFrom(adj, src) {
    const seen = new Set([src]);
    const stack = [src];
    while (stack.length) {
      const cur = stack.pop();
      for (const nb of (adj[cur] || [])) {
        if (!seen.has(nb)) { seen.add(nb); stack.push(nb); }
      }
    }
    return seen;
  }

  function refreshPathTargets() {
    const src = pathFromSel.value;
    if (!src) {
      // No source: only the static "globally unreachable from any entry"
      // markers apply.
      Array.from(pathToSel.querySelectorAll("option")).forEach(opt => {
        if (!opt.value) return;
        const reachable = opt.dataset.reachable === "1";
        opt.disabled = !reachable;
        opt.textContent = opt.dataset.origLabel + (reachable ? "" : " — unreachable");
      });
      return;
    }
    const adj = buildAdjacency();
    const reach = reachableFrom(adj, src);
    Array.from(pathToSel.querySelectorAll("option")).forEach(opt => {
      if (!opt.value) return;
      const ok = (opt.value !== src) && reach.has(opt.value);
      opt.disabled = !ok;
      opt.textContent = opt.dataset.origLabel + (ok ? "" : " — unreachable");
    });
    const cur = pathToSel.options[pathToSel.selectedIndex];
    if (cur && cur.disabled) {
      for (const o of pathToSel.options) {
        if (!o.disabled && o.value) { pathToSel.value = o.value; break; }
      }
    }
  }
  pathFromSel.addEventListener("change", refreshPathTargets);

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
        const w = Math.max(220, Math.min(640, startW + (isLeft ? -dx : dx)));
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
    body.style.gridTemplateColumns = "auto auto auto";
    if (tab === "tactics") {
      PAYLOAD.tactics.forEach(t => {
        body.innerHTML += `<div class="row"><span class="sw" style="background:${t.color}"></span>${t.label}</div>`;
      });
    } else if (tab === "evidence") {
      body.style.gridTemplateColumns = "auto auto";
      PAYLOAD.evidence_types.forEach(e => {
        body.innerHTML += `<div class="row"><span class="sw" style="background:${e.color}"></span>${e.label}</div>`;
      });
    } else if (tab === "lines") {
      body.style.gridTemplateColumns = "auto auto";
      body.innerHTML = `
        <div class="row"><span class="ln" style="background:#aaa"></span>Forward (tactic-respecting)</div>
        <div class="row"><span class="ln" style="background:#aaa;border-top:1px dashed #aaa"></span>Backward (loop)</div>
        <div class="row"><span class="ln" style="background:#aaa;height:4px"></span>Consensus (≥2 sources)</div>
        <div class="row"><span class="sw" style="background:transparent;border:1px dashed #7f88b0"></span>Orphan technique</div>
        <div class="row"><span class="sw" style="background:#3b4261;border:1px dotted #3b4261;opacity:0.5"></span>Unreachable objective</div>
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

  function chip(text) {
    return `<span class="chip">${text}</span>`;
  }

  function renderNodeDetails(n) {
    const d = n.data("payload");
    const groupRows = d.group_ids.map(gid => {
      const g = PAYLOAD.groups[gid];
      if (!g) return `<li>${gid}</li>`;
      const region = g.regions.length ? ` <span class="muted small">[${g.regions.join(",")}]</span>` : "";
      return `<li><strong>${g.id}</strong> ${g.name}${region}</li>`;
    }).join("");
    const campaignRows = d.campaign_ids.map(cid => {
      const c = PAYLOAD.campaigns[cid];
      return c ? `<li><strong>${c.id}</strong> ${c.name}</li>` : `<li>${cid}</li>`;
    }).join("");
    const flags = [];
    if (d.is_entry) flags.push("entry");
    if (d.is_objective) flags.push("objective");
    if (d.is_objective && !d.reachable_from_entry) flags.push("unreachable");
    if (d.orphan) flags.push("orphan");
    $("#details").innerHTML = `
      <h3><span class="tid">${d.id}</span> ${d.label || ""}</h3>
      <div class="muted small">${d.tactic || ""}${flags.length ? " · " + flags.join(" · ") : ""}</div>
      <section>
        <div class="muted small">Platform profile</div>
        <div>${d.platform_profile}</div>
        <div class="muted small" style="margin-top:6px">Platforms</div>
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
    const results = [];
    const maxDepth = 8;
    const adj = buildAdjacency();
    const q = [[src, [src], []]];
    while (q.length && results.length < k) {
      const [cur, path, edges] = q.shift();
      if (cur === tgt && path.length > 1) { results.push({ nodes: path, edges }); continue; }
      if (path.length > maxDepth) continue;
      for (const nb of (adj[cur] || [])) {
        if (path.includes(nb)) continue;
        const eid = `${cur}__${nb}`;
        q.push([nb, [...path, nb], [...edges, eid]]);
      }
    }
    return results;
  }

  $("#btn-path").addEventListener("click", () => {
    const from = pathFromSel.value;
    const to = pathToSel.value;
    const k = Math.max(1, Math.min(10, Number($("#path-k").value) || 3));
    if (!from || !to) { $("#path-results").textContent = "Select both endpoints"; return; }
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
