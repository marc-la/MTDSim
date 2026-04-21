/* GAP Cytoscape viewer.
 *
 * Data pipeline: the HTML embeds two script tags — the full payload and the
 * initial filter state. This module builds the Cytoscape graph once, then
 * applies filter changes reactively by updating node/edge visibility classes.
 * No data is ever re-fetched.
 *
 * Filtering model. Two-pass to make group/campaign filters intuitive:
 *   1. Compute hard node visibility (tactics, subgraph, group, campaign).
 *   2. An edge is visible iff its evidence/conf/backward checks pass AND
 *      both endpoints are hard-visible.
 *   3. A node is finally visible iff hard-visible AND (has visible edge OR
 *      hide-isolated is off).
 * This guarantees that selecting "APT28" shows APT28's techniques + the
 * edges between them, instead of relying on per-edge group attribution
 * (which is sparse for ontology / co-occurrence edges and produced empty
 * graphs in the previous version).
 */
(function () {
  const PAYLOAD = JSON.parse(document.getElementById("gap-payload").textContent);
  const INITIAL = JSON.parse(document.getElementById("gap-initial-filter").textContent);

  // --------------------------------------------------------------
  // Lookup tables

  const tacticColour = {};
  const tacticLabel = {};
  PAYLOAD.tactics.forEach(t => { tacticColour[t.id] = t.color; tacticLabel[t.id] = t.label; });

  const evidenceColour = {};
  const evidenceLabel = {};
  PAYLOAD.evidence_types.forEach(e => { evidenceColour[e.id] = e.color; evidenceLabel[e.id] = e.label; });

  const nodeById = {};
  PAYLOAD.nodes.forEach(n => { nodeById[n.id] = n; });

  // Subgraph membership (Strategy A — terminal-objective tactic;
  // Strategy B — platform profile). Pre-indexed as Sets for O(1) lookup.
  const subgraphTerminal = {};
  Object.entries(PAYLOAD.subgraphs.terminal_objective || {}).forEach(([k, v]) => {
    subgraphTerminal[k] = new Set(v);
  });
  const subgraphTerminalTechnique = {};
  Object.entries(PAYLOAD.subgraphs.terminal_technique || {}).forEach(([k, v]) => {
    subgraphTerminalTechnique[k] = new Set(v);
  });
  const subgraphTerminalGroupWitnessed = {};
  Object.entries(PAYLOAD.subgraphs.terminal_group_witnessed || {}).forEach(([k, v]) => {
    subgraphTerminalGroupWitnessed[k] = new Set(v);
  });
  const subgraphPlatform = {};
  Object.entries(PAYLOAD.subgraphs.platform || {}).forEach(([k, v]) => {
    subgraphPlatform[k] = new Set(v);
  });

  // Mix a hex colour toward a neutral grey (0..1). Used to fade the tactic
  // hue of an unreachable objective: colour stays recognisable, but reads
  // as "inactive". Produces a seamless visual cue instead of a hard disable.
  function mixWithGrey(hex, pct) {
    if (!hex || hex[0] !== "#" || hex.length < 7) return hex;
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    const target = 0x6a;
    const mix = (c) => Math.round(c * (1 - pct) + target * pct);
    const hx = (n) => n.toString(16).padStart(2, "0");
    return `#${hx(mix(r))}${hx(mix(g))}${hx(mix(b))}`;
  }

  // Readable text colour on top of a saturated tactic swatch.
  function textOn(hex) { return "#1a1b26"; }

  // Subgraph provenance (server-side selector applied via SubgraphView).
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
  // External MITRE ATT&CK URLs

  function groupUrl(gid) {
    return /^G\d+$/.test(gid) ? `https://attack.mitre.org/groups/${gid}/` : null;
  }
  function campaignUrl(cid) {
    return /^C\d+$/.test(cid) ? `https://attack.mitre.org/campaigns/${cid}/` : null;
  }
  function techniqueUrl(tid) {
    if (!/^T\d+(\.\d+)?$/.test(tid)) return null;
    if (tid.includes(".")) {
      const [parent, sub] = tid.split(".");
      return `https://attack.mitre.org/techniques/${parent}/${sub}/`;
    }
    return `https://attack.mitre.org/techniques/${tid}/`;
  }
  function extLink(href, text) {
    return href ? `<a class="ext" href="${href}" target="_blank" rel="noopener">${text}</a>` : text;
  }

  // --------------------------------------------------------------
  // State

  const state = {
    visibleEvidence: new Set(),
    hideIsolated: INITIAL.hide_isolated !== false,
    hideBackward: false,
    dimUnreachable: false,
    dimUnreachableUserSet: false,
    selectedGroups: null,   // null = all
    selectedCampaigns: null,
    selectedTactics: new Set(PAYLOAD.tactics.map(t => t.id)),
    csaObjectiveTactic: "",
    csaObjectiveTechnique: "",
    csaGroupWitnessed: "",
    csaPlatform: "",
    pathHighlight: null,    // { nodes: Set, edges: Set }
  };

  // Seed evidence visibility from explicit list, else from per-evidence
  // ``default_visible`` (built in payload.py).
  if (INITIAL.evidence_types && INITIAL.evidence_types.length) {
    state.visibleEvidence = new Set(INITIAL.evidence_types);
  } else {
    state.visibleEvidence = new Set(
      PAYLOAD.evidence_types.filter(e => e.default_visible).map(e => e.id),
    );
    if (state.visibleEvidence.size === 0) state.visibleEvidence.add("attack_flow");
  }

  // --------------------------------------------------------------
  // Cytoscape elements (compound parents per tactic give faint band
  // backgrounds; technique nodes are children of their tactic parent).

  const tacticParentNodes = PAYLOAD.tactics.map(t => ({
    data: {
      id: `__tactic__${t.id}`,
      label: t.label,
      color: t.color,
    },
    classes: "tactic-band",
    selectable: false,
    grabbable: false,
  }));

  const cyNodes = PAYLOAD.nodes.map(n => ({
    data: {
      id: n.id,
      parent: `__tactic__${n.tactic}`,
      label: `${n.id}\n${(n.label || "").slice(0, 28)}`,
      fullLabel: n.label,
      tactic: n.tactic,
      layer: n.layer,
      group_ids: n.group_ids,
      campaign_ids: n.campaign_ids,
      orphan: n.orphan,
      is_entry: n.is_entry,
      is_objective: n.is_objective,
      reachable_from_entry: n.reachable_from_entry,
      payload: n,
    },
    classes: [
      n.orphan ? "orphan" : "",
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
      backward: e.backward,
      source_groups: e.source_groups,
      campaigns: e.campaigns,
      payload: e,
    },
    classes: e.backward ? "backward" : "forward",
  }));

  // --------------------------------------------------------------
  // Cytoscape init

  if (window.cytoscape && window.cytoscapeDagre) {
    window.cytoscape.use(window.cytoscapeDagre);
  }

  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [...tacticParentNodes, ...cyNodes, ...cyEdges],
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
        // Tactic band (compound parent) — faint coloured frame around all
        // techniques in a tactic column. Restored from the legacy viewer
        // as a perceptual cue: tactic identity is reinforced visually
        // even when many edges criss-cross the canvas.
        selector: "node.tactic-band",
        style: {
          "background-color": "data(color)",
          "background-opacity": 0.06,
          "border-width": 1,
          "border-color": "data(color)",
          "border-opacity": 0.25,
          "border-style": "solid",
          "label": "data(label)",
          "text-valign": "top",
          "text-halign": "center",
          "text-margin-y": -4,
          "font-size": 11,
          "font-weight": 600,
          "color": "data(color)",
          "text-opacity": 0.55,
          "shape": "roundrectangle",
          "padding": 18,
          "events": "no",
          "z-compound-depth": "bottom",
        },
      },
      {
        selector: "node.orphan",
        style: { "border-style": "dashed", "border-color": "#7f88b0", "opacity": 0.6 },
      },
      {
        selector: "node.dim",
        style: { "opacity": 0.18, "text-opacity": 0.18 },
      },
      {
        selector: "node.hidden",
        style: { "display": "none" },
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
      { selector: "edge.dim", style: { "opacity": 0.06 } },
      { selector: "edge.hidden", style: { "display": "none" } },
      { selector: ".path-highlight",
        style: { "line-color": "#f7768e", "target-arrow-color": "#f7768e",
                 "border-color": "#f7768e", "border-width": 3, "opacity": 1,
                 "z-index": 999 } },
    ],
    layout: { name: "preset" },
  });

  // Per-tactic columnar layout: nodes stacked by group_count within layer.
  (function positionByLayer() {
    const byLayer = {};
    cy.nodes().not(".tactic-band").forEach(n => {
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
    if (state.csaObjectiveTechnique) {
      const set = subgraphTerminalTechnique[state.csaObjectiveTechnique];
      if (!set || !set.has(id)) return false;
    }
    if (state.csaGroupWitnessed) {
      const set = subgraphTerminalGroupWitnessed[state.csaGroupWitnessed];
      if (!set || !set.has(id)) return false;
    }
    if (state.csaPlatform) {
      const set = subgraphPlatform[state.csaPlatform];
      if (!set || !set.has(id)) return false;
    }
    return true;
  }

  // Hard visibility: per-node filters that don't depend on edge visibility.
  // Stored on node data so the edge filter can check both endpoints in O(1).
  function nodeHardVisible(n) {
    const d = n.data();
    if (n.hasClass("tactic-band")) return true;
    if (!state.selectedTactics.has(d.tactic)) return false;
    if (!nodeInCsa(d.id)) return false;
    if (state.selectedGroups) {
      if (!d.group_ids.some(g => state.selectedGroups.has(g))) return false;
    }
    if (state.selectedCampaigns) {
      if (!d.campaign_ids.some(c => state.selectedCampaigns.has(c))) return false;
    }
    return true;
  }

  function edgeVisible(e) {
    const d = e.data();
    if (!d.evidence_types.some(t => state.visibleEvidence.has(t))) return false;
    if (state.hideBackward && d.backward) return false;
    const s = cy.getElementById(d.source);
    const t = cy.getElementById(d.target);
    if (!s.scratch("_hard") || !t.scratch("_hard")) return false;
    return true;
  }

  function shouldDimNode(d, isVisible, hasVisibleEdge) {
    if (!state.dimUnreachable || !isVisible) return false;
    if (state.pathHighlight) {
      return !state.pathHighlight.nodes.has(d.id);
    }
    // No active path: dim unreachable objectives and orphans.
    return (d.is_objective && !d.reachable_from_entry);
  }

  function shouldDimEdge(d, isVisible) {
    if (!state.dimUnreachable || !isVisible) return false;
    if (!state.pathHighlight) return false;
    return !state.pathHighlight.edges.has(d.id);
  }

  function applyFilters() {
    // Pass 1: compute hard node visibility, store on scratch.
    cy.nodes().forEach(n => n.scratch("_hard", nodeHardVisible(n)));

    // Pass 2: edges that survive evidence/confidence/backward + endpoint
    // hard-visibility.
    const touched = new Set();
    cy.edges().forEach(e => {
      const show = edgeVisible(e);
      e.toggleClass("hidden", !show);
      if (show) {
        touched.add(e.data("source"));
        touched.add(e.data("target"));
      }
    });

    // Pass 3: final node visibility (hide-isolated kicks in).
    cy.nodes().not(".tactic-band").forEach(n => {
      const hard = n.scratch("_hard");
      const d = n.data();
      let show = hard;
      if (show && state.hideIsolated && !touched.has(d.id)) show = false;
      n.toggleClass("hidden", !show);
      n.toggleClass("dim", shouldDimNode(d, show, touched.has(d.id)));
    });

    // Pass 4: edges — apply dim class.
    cy.edges().forEach(e => {
      const visible = !e.hasClass("hidden");
      e.toggleClass("dim", shouldDimEdge(e.data(), visible));
    });

    // Pass 5: hide tactic-band parents whose children are all hidden.
    cy.nodes(".tactic-band").forEach(parent => {
      const anyVisible = parent.children().filter(c => !c.hasClass("hidden")).length > 0;
      parent.toggleClass("hidden", !anyVisible);
    });

    updateLiveCounts();
    refreshPathTargets();
  }

  function updateLiveCounts() {
    const nv = cy.nodes().not(".tactic-band").filter(n => !n.hasClass("hidden")).length;
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
      applyFilters();
    });
    evList.appendChild(lbl);
  });

  // Subgraph dropdowns ----------------------------------------------------
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

  // Strategy 2b — one option per objective technique, grouped by tactic.
  const csaTechSel = $("#csa-objective-technique");
  const techSubgraphByTactic = {};
  Object.keys(subgraphTerminalTechnique).forEach(tid => {
    const node = nodeById[tid];
    if (!node) return;
    (techSubgraphByTactic[node.tactic] = techSubgraphByTactic[node.tactic] || []).push(tid);
  });
  PAYLOAD.tactics.forEach(t => {
    const ids = techSubgraphByTactic[t.id];
    if (!ids || ids.length === 0) return;
    const og = document.createElement("optgroup");
    og.label = t.label;
    ids.sort().forEach(tid => {
      const node = nodeById[tid];
      const size = subgraphTerminalTechnique[tid].size;
      const opt = document.createElement("option");
      opt.value = tid;
      opt.textContent = `${tid} — ${(node.label || "").slice(0, 28)} · ${size}T`;
      opt.style.backgroundColor = t.color;
      opt.style.color = textOn(t.color);
      og.appendChild(opt);
    });
    csaTechSel.appendChild(og);
  });
  csaTechSel.addEventListener("change", e => {
    state.csaObjectiveTechnique = e.target.value;
    applyFilters();
  });

  // Strategy 2c — group-witnessed per-terminal; same shape as 2b but the
  // subgraph is the ancestor cone pruned to techniques that share a MITRE
  // group with the terminal. Promoted from the 2026-04-17 exploration.
  const csaGroupSel = $("#csa-group-witnessed");
  const groupWitByTactic = {};
  Object.keys(subgraphTerminalGroupWitnessed).forEach(tid => {
    const node = nodeById[tid];
    if (!node) return;
    (groupWitByTactic[node.tactic] = groupWitByTactic[node.tactic] || []).push(tid);
  });
  PAYLOAD.tactics.forEach(t => {
    const ids = groupWitByTactic[t.id];
    if (!ids || ids.length === 0) return;
    const og = document.createElement("optgroup");
    og.label = t.label;
    ids.sort().forEach(tid => {
      const node = nodeById[tid];
      const size = subgraphTerminalGroupWitnessed[tid].size;
      const opt = document.createElement("option");
      opt.value = tid;
      opt.textContent = `${tid} — ${(node.label || "").slice(0, 28)} · ${size}T`;
      opt.style.backgroundColor = t.color;
      opt.style.color = textOn(t.color);
      og.appendChild(opt);
    });
    csaGroupSel.appendChild(og);
  });
  csaGroupSel.addEventListener("change", e => {
    state.csaGroupWitnessed = e.target.value;
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
  $("#tactic-all").addEventListener("click", () => {
    state.selectedTactics = new Set(PAYLOAD.tactics.map(t => t.id));
    tacList.querySelectorAll("input").forEach(i => { i.checked = true; i.parentElement.classList.remove("off"); });
    applyFilters();
  });
  $("#tactic-none").addEventListener("click", () => {
    state.selectedTactics = new Set();
    tacList.querySelectorAll("input").forEach(i => { i.checked = false; i.parentElement.classList.add("off"); });
    applyFilters();
  });

  // Group / campaign pick lists -------------------------------------------
  function renderPickList(containerSel, items, formatFn, stateKey) {
    const container = $(containerSel);
    container.innerHTML = "";
    items.forEach(it => {
      const lbl = document.createElement("label");
      lbl.innerHTML = formatFn(it);
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

  function clearPickListChecks(containerSel) {
    $(containerSel).querySelectorAll("input").forEach(i => { i.checked = false; });
  }

  const groupItems = Object.values(PAYLOAD.groups)
    .filter(g => (g.technique_count || 0) > 0)
    .sort((a, b) => (b.technique_count - a.technique_count) || a.name.localeCompare(b.name));
  $("#group-count").textContent = `(${groupItems.length})`;
  renderPickList("#group-list", groupItems, g => {
    const region = g.regions.length ? ` <span class="muted small">[${g.regions.join(",")}]</span>` : "";
    return `<input type="checkbox" value="${g.id}"> <span>${g.id} — ${g.name}${region}</span>` +
      `<span class="item-count">${g.technique_count}T</span>`;
  }, "selectedGroups");

  $("#group-search").addEventListener("input", e => {
    const q = e.target.value.toLowerCase();
    $("#group-list").querySelectorAll("label").forEach(l => {
      l.style.display = l.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });
  $("#group-reset").addEventListener("click", () => {
    state.selectedGroups = null;
    clearPickListChecks("#group-list");
    $("#group-search").value = "";
    $("#group-list").querySelectorAll("label").forEach(l => { l.style.display = ""; });
    applyFilters();
  });

  const campaignItems = Object.values(PAYLOAD.campaigns)
    .filter(c => (c.technique_count || 0) > 0)
    .sort((a, b) => (b.technique_count - a.technique_count) || a.name.localeCompare(b.name));
  $("#campaign-count").textContent = `(${campaignItems.length})`;
  renderPickList("#campaign-list", campaignItems, c => {
    const sigil = c.source === "attack_flow" ? "⌁" : "●";
    return `<input type="checkbox" value="${c.id}"> <span>${sigil} ${c.name}</span>` +
      `<span class="item-count">${c.technique_count}T</span>`;
  }, "selectedCampaigns");

  $("#campaign-search").addEventListener("input", e => {
    const q = e.target.value.toLowerCase();
    $("#campaign-list").querySelectorAll("label").forEach(l => {
      l.style.display = l.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });
  $("#campaign-reset").addEventListener("click", () => {
    state.selectedCampaigns = null;
    clearPickListChecks("#campaign-list");
    $("#campaign-search").value = "";
    $("#campaign-list").querySelectorAll("label").forEach(l => { l.style.display = ""; });
    applyFilters();
  });

  // Advanced controls
  $("#hide-isolated").addEventListener("change", e => { state.hideIsolated = e.target.checked; applyFilters(); });
  $("#hide-backward").addEventListener("change", e => { state.hideBackward = e.target.checked; applyFilters(); });
  $("#dim-unreachable").addEventListener("change", e => {
    state.dimUnreachable = e.target.checked;
    state.dimUnreachableUserSet = true;
    applyFilters();
  });

  // --------------------------------------------------------------
  // Path explorer dropdowns (entry & objective; tactic-grouped)

  function buildOptgroups(items, valueFn, labelFn, extraDataFn) {
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
      const col = tacticColour[tac];
      if (col) {
        opt.dataset.baseColor = col;
        opt.style.backgroundColor = col;
        opt.style.color = textOn(col);
      }
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
    it => `${it.id} · ${(it.label || "").slice(0, 24)}`,
  ));

  pathToSel.appendChild(buildOptgroups(
    PAYLOAD.objective_nodes,
    it => it.id,
    it => `${it.id} · ${(it.label || "").slice(0, 24)}`,
    (opt, it) => {
      opt.dataset.origLabel = opt.textContent;
      opt.dataset.reachable = it.reachable_from_entry ? "1" : "0";
      // Unreachable objectives: fade the tactic hue toward grey so the
      // colour cue is preserved but reads as inactive.
      if (!it.reachable_from_entry && opt.dataset.baseColor) {
        const faded = mixWithGrey(opt.dataset.baseColor, 0.55);
        opt.style.backgroundColor = faded;
        opt.style.color = "#3a3f58";
        opt.style.fontStyle = "italic";
      }
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

  // Apply the reachable / unreachable visual treatment to one objective
  // option: full tactic colour when reachable, tactic colour faded toward
  // grey + italic when not. Keeps the hue (user can still identify the
  // tactic) but reads as inactive.
  function paintObjectiveOption(opt, reachable) {
    const base = opt.dataset.baseColor;
    if (!base) return;
    if (reachable) {
      opt.style.backgroundColor = base;
      opt.style.color = textOn(base);
      opt.style.fontStyle = "normal";
    } else {
      opt.style.backgroundColor = mixWithGrey(base, 0.55);
      opt.style.color = "#3a3f58";
      opt.style.fontStyle = "italic";
    }
  }

  function refreshPathTargets() {
    const src = pathFromSel.value;
    if (!src) {
      Array.from(pathToSel.querySelectorAll("option")).forEach(opt => {
        if (!opt.value) return;
        const reachable = opt.dataset.reachable === "1";
        opt.disabled = !reachable;
        opt.textContent = opt.dataset.origLabel + (reachable ? "" : " — unreachable");
        paintObjectiveOption(opt, reachable);
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
      paintObjectiveOption(opt, ok);
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
  // Panel collapse + resize.
  //
  // The collapse button toggles `.collapsed`; the grid column itself is
  // shrunk by overwriting --left-w / --right-w. Without this, the column
  // would keep its 300/360px width and the collapsed panel would appear
  // as an empty band beside the graph (the previous bug).

  const PANEL_DEFAULT_W = { "left-panel": "300px", "right-panel": "360px" };

  document.querySelectorAll(".collapse").forEach(btn => {
    btn.addEventListener("click", () => {
      const target = document.getElementById(btn.dataset.target);
      const varName = btn.dataset.target === "left-panel" ? "--left-w" : "--right-w";
      const willCollapse = !target.classList.contains("collapsed");
      target.classList.toggle("collapsed", willCollapse);
      if (willCollapse) {
        target.dataset.prevWidth =
          document.documentElement.style.getPropertyValue(varName) ||
          PANEL_DEFAULT_W[btn.dataset.target];
        document.documentElement.style.setProperty(varName, "36px");
        btn.textContent = btn.dataset.target === "left-panel" ? "›" : "‹";
      } else {
        document.documentElement.style.setProperty(
          varName,
          target.dataset.prevWidth || PANEL_DEFAULT_W[btn.dataset.target],
        );
        btn.textContent = btn.dataset.target === "left-panel" ? "‹" : "›";
      }
      setTimeout(() => cy.resize(), 220);
    });
  });

  document.querySelectorAll(".resize-handle").forEach(h => {
    h.addEventListener("mousedown", (e) => {
      e.preventDefault();
      const panel = document.getElementById(h.dataset.target);
      if (panel.classList.contains("collapsed")) return;
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
        <div class="row"><span class="sw" style="background:transparent;border:1px dashed #7f88b0"></span>Orphan technique</div>
        <div class="row"><span class="sw" style="background:#3b4261;opacity:0.5"></span>Dimmed (unreachable / off-path)</div>
        <div class="row"><span class="ln" style="background:#f7768e;height:3px"></span>Highlighted attack path</div>
      `;
    }
  }
  document.querySelectorAll(".legend-tabs .tab").forEach(t => {
    t.addEventListener("click", () => {
      $("#legend").classList.remove("collapsed");
      $("#legend-toggle").textContent = "−";
      document.querySelectorAll(".legend-tabs .tab").forEach(x => x.classList.remove("active"));
      t.classList.add("active");
      renderLegend(t.dataset.tab);
    });
  });
  $("#legend-toggle").addEventListener("click", () => {
    const legend = $("#legend");
    legend.classList.toggle("collapsed");
    $("#legend-toggle").textContent = legend.classList.contains("collapsed") ? "+" : "−";
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
      const url = groupUrl(gid);
      if (!g) return `<li>${extLink(url, gid)}</li>`;
      const region = g.regions.length ? ` <span class="muted small">[${g.regions.join(",")}]</span>` : "";
      return `<li><strong>${extLink(url, g.id)}</strong> ${g.name}${region}</li>`;
    }).join("");
    const campaignRows = d.campaign_ids.map(cid => {
      const c = PAYLOAD.campaigns[cid];
      const url = campaignUrl(cid);
      return c
        ? `<li><strong>${extLink(url, c.id)}</strong> ${c.name}</li>`
        : `<li>${extLink(url, cid)}</li>`;
    }).join("");
    const subRows = (d.sub_technique_ids || []).map(sid =>
      `<li>${extLink(techniqueUrl(sid), sid)}</li>`).join("");
    const flags = [];
    if (d.is_entry) flags.push("entry");
    if (d.is_objective) flags.push("objective");
    if (d.is_objective && !d.reachable_from_entry) flags.push("unreachable");
    if (d.orphan) flags.push("orphan");
    $("#details").innerHTML = `
      <h3><span class="tid">${extLink(techniqueUrl(d.id), d.id)}</span> ${d.label || ""}</h3>
      <div class="muted small">${tacticLabel[d.tactic] || d.tactic || ""}${flags.length ? " · " + flags.join(" · ") : ""}</div>
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
      ${subRows ? `<section>
        <div class="muted small">Sub-techniques (${d.sub_technique_ids.length})</div>
        <ul>${subRows}</ul>
      </section>` : ""}
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
          ? `<div class="muted small"><a class="ext" href="${ev.source_url}" target="_blank" rel="noopener">source</a></div>` : ""}
      </div>`).join("");
    $("#details").innerHTML = `
      <h3>
        <span class="tid">${extLink(techniqueUrl(d.source), d.source)}</span> →
        <span class="tid">${extLink(techniqueUrl(d.target), d.target)}</span>
      </h3>
      <div class="muted small">
        confidence ${Number(d.confidence).toFixed(2)} ·
        ${d.source_count} source${d.source_count === 1 ? "" : "s"}${d.backward ? " · backward" : ""}
      </div>
      <section>
        <div class="muted small">Evidence</div>
        ${evBlocks}
      </section>
      <section>
        <div class="muted small">Implicated APT groups (${d.source_groups.length})</div>
        ${d.source_groups.map(gid => {
          const g = PAYLOAD.groups[gid];
          const url = groupUrl(gid);
          return g
            ? `<div>${extLink(url, g.id)} — ${g.name}</div>`
            : `<div>${extLink(url, gid)}</div>`;
        }).join("") || '<div class="muted">none</div>'}
      </section>
    `;
  }

  cy.on("tap", "node", evt => {
    if (evt.target.hasClass("tactic-band")) return;
    renderNodeDetails(evt.target);
  });
  cy.on("tap", "edge", evt => renderEdgeDetails(evt.target));
  cy.on("tap", evt => {
    if (evt.target === cy) {
      $("#details").innerHTML = '<p class="muted">Select a node or edge to see provenance.</p>';
    }
  });

  // --------------------------------------------------------------
  // Attack path (k shortest simple paths via BFS over visible edges).

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

  // Live k-slider readout.
  const pathKInput = $("#path-k");
  const pathKVal = $("#path-k-val");
  pathKInput.addEventListener("input", e => {
    pathKVal.textContent = e.target.value;
  });

  $("#btn-path").addEventListener("click", () => {
    const from = pathFromSel.value;
    const to = pathToSel.value;
    const k = Math.max(1, Math.min(10, Number(pathKInput.value) || 3));
    if (!from || !to) {
      $("#btn-path").textContent = "Select endpoints…";
      setTimeout(() => { $("#btn-path").textContent = "Show paths"; }, 1500);
      return;
    }
    const paths = kShortestPaths(from, to, k);
    cy.elements().removeClass("path-highlight");
    if (paths.length === 0) {
      state.pathHighlight = null;
      $("#btn-path").textContent = "No path";
      setTimeout(() => { $("#btn-path").textContent = "Show paths"; }, 1500);
      applyFilters();
      return;
    }
    const nodeSet = new Set(), edgeSet = new Set();
    paths.forEach(p => {
      p.nodes.forEach(n => nodeSet.add(n));
      p.edges.forEach(e => edgeSet.add(e));
    });
    nodeSet.forEach(n => cy.getElementById(n).addClass("path-highlight"));
    edgeSet.forEach(e => cy.getElementById(e).addClass("path-highlight"));
    state.pathHighlight = { nodes: nodeSet, edges: edgeSet };
    // If the user hasn't explicitly toggled the "dim unreachable / off-path"
    // advanced option, auto-enable it now so the highlighted path stands
    // out against the rest of the graph — otherwise the ask ("Show paths")
    // produces no visible contrast.
    if (!state.dimUnreachableUserSet && !state.dimUnreachable) {
      state.dimUnreachable = true;
      const cb = $("#dim-unreachable");
      if (cb) cb.checked = true;
    }
    applyFilters();
    $("#btn-path").textContent = `Showing ${paths.length} path${paths.length === 1 ? "" : "s"}`;
    setTimeout(() => { $("#btn-path").textContent = "Show paths"; }, 1800);
  });
  $("#btn-path-clear").addEventListener("click", () => {
    cy.elements().removeClass("path-highlight");
    state.pathHighlight = null;
    applyFilters();
  });

  // --------------------------------------------------------------
  // Header actions

  $("#btn-fit").addEventListener("click", () => cy.fit(null, 30));
  $("#btn-reset").addEventListener("click", () => window.location.reload());

  // --------------------------------------------------------------
  // Initial paint

  applyFilters();
})();
