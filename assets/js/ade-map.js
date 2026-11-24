// Adjacency map of simple singularities (_includes/ade-map.html, data in _data/ade.yml).
// Each node is drawn at a place given by its family, index and superscript. Switching the characteristic
// moves the nodes: a class that exists in characteristic 0 keeps its place (its `key`), and the classes
// it splits into come out of it.
(function () {
	var D = window.ADE;
	var STACK = 0.9, DUR = 650;
	var root = document.getElementById("ade"), plane = document.getElementById("ade-plane");
	var svg = document.getElementById("ade-edges"), detail = document.getElementById("ade-detail");
	var noteEl = document.getElementById("ade-note"), emptyEl = document.getElementById("ade-empty");
	var SVGNS = "http://www.w3.org/2000/svg";

	var byId = {};
	D.nodes.forEach(function (nd) {
		nd.chars = [];
		nd.forms.forEach(function (f) { f.chars.forEach(function (c) { nd.chars.push(c); }); });
		byId[nd.id] = nd;
	});
	D.edges.forEach(function (e) { e.unfoldings = e.unfoldings || []; });
	function form(nd, ch) { return nd.forms.filter(function (f) { return f.chars.indexOf(ch) >= 0; })[0]; }
	function nodesIn(ch) { return D.nodes.filter(function (nd) { return nd.chars.indexOf(ch) >= 0; }); }
	// Arrows that are compositions of others (`implied`) are not drawn.
	function edgesIn(c) { return D.edges.filter(function (e) { return e.chars.indexOf(c) >= 0 && (e.implied || []).indexOf(c) < 0; }); }
	// A node is drawn where its characteristic-0 class is (its key, e.g. "E7") when it is the most generic
	// class of that name in the characteristic (largest superscript); otherwise it is a new node of its own.
	var TOP = {};
	D.nodes.forEach(function (nd) {
		nd.chars.forEach(function (c) { var t = TOP[c] = TOP[c] || {}, k = parentKey(nd); t[k] = Math.max(t[k] || 0, nd.r || 0); });
	});
	function keyOf(nd, c) { return nd.r === null || nd.r === TOP[c || ch][parentKey(nd)] ? parentKey(nd) : nd.id; }
	function ekey(e, c) { return keyOf(byId[e.from], c) + ">" + keyOf(byId[e.to], c); }
	function parentKey(nd) { return nd.family + nd.n; }
	function charInfo(c) { return D.chars.filter(function (x) { return x.key === c; })[0]; }
	function charLabel(c) { return charInfo(c).label; }
	function isRight(c) { return charInfo(c || ch).equiv === "right"; }

	var keys0 = {}, ekeys0 = {};
	nodesIn("0").forEach(function (nd) { keys0[keyOf(nd, "0")] = 1; });
	edgesIn("0").forEach(function (e) { ekeys0[ekey(e, "0")] = 1; });

	// ---- text ----
	function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
	function tex(id) {
		var m = /^([ADE])(\d+)(?:\^(\d+))?$/.exec(id);
		return m[1] + "_{" + m[2] + "}" + (m[3] !== undefined ? "^{" + m[3] + "}" : "");
	}
	function math(id) { return "\\(" + tex(id) + "\\)"; }
	function an(id) { return (id[0] === "D" ? "a " : "an ") + math(id); }
	// $...$ and $$...$$ (as in the Markdown of the site) to MathJax delimiters; the rest is escaped.
	function md(s) {
		var parts = [];
		s = s.replace(/\$\$([^$]+)\$\$|\$([^$]+)\$/g, function (_, d, i) {
			parts.push(d !== undefined ? "\\[" + d + "\\]" : "\\(" + i + "\\)");
			return "\u0000" + (parts.length - 1) + "\u0000";
		});
		s = esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>");
		return s.replace(/\u0000(\d+)\u0000/g, function (_, i) { return esc(parts[+i]); });
	}
	// MathJax loads asynchronously: wait for it before typesetting.
	function whenMath(cb) {
		if (window.MathJax && MathJax.typesetPromise && MathJax.startup && MathJax.startup.promise) MathJax.startup.promise.then(cb);
		else setTimeout(function () { whenMath(cb); }, 100);
	}
	function typeset(els) {
		whenMath(function () {
			if (MathJax.typesetClear) MathJax.typesetClear(els);
			MathJax.typesetPromise(els).catch(function () {});
		});
	}

	// ---- layout (in grid units: x = column, y = row; A on top, then D, then E) ----
	function layout(ch) {
		var two = ch === "2", surf = ch === "2e";
		var rowD = two ? 4.2 : surf ? 3.4 : 1.6, rowE = two ? 6.6 : surf ? 5.4 : 3.2;
		var list = nodesIn(ch), top = {}, pos = {};
		list.forEach(function (nd) { var k = parentKey(nd); top[k] = Math.max(top[k] || 0, nd.r || 0); });
		list.forEach(function (nd) {
			var n = nd.n, below = top[parentKey(nd)] - (nd.r || 0), x, y;
			if (nd.family === "A") { x = n; y = -below * STACK; }
			// on surfaces the D and E stacks slant to the right, so that the arrows from E up to the D's
			// with lower superscript do not run through the D above them or along the D stack
			else if (nd.family === "D") { x = surf ? n + 0.5 * below : two ? n : n - 0.5; y = rowD - below * STACK; }
			else if (surf) { x = n - 0.3 + 0.8 * below; y = rowE + below * STACK; }
			else if (two) {
				if (below) { x = 6.45; y = (rowD + rowE) / 2; } else { x = n - 0.5; y = rowE; }
			} else if (below) { x = n - 1 + below - 1; y = rowE + 1.3; }
			else { x = n - 1; y = rowE; }
			pos[keyOf(nd, ch)] = { x: x, y: y };
		});
		return pos;
	}

	// ---- drawing ----
	var ch = "0", sel = null, hover = null;
	var nodes = {};   // key -> { el, nd, x, y, s, o, gone }
	var edges = {};   // ekey -> { g, line, hit, e, o, gone }
	var dotEls = {};   // family -> the "..." of that row: { el, x, y, o }
	var extras = [], dying = [];   // end labels and their arrows; those fading out
	var planeW = 0, anim = null, unitX = 80, unitY = 52, PAD = 34, ymin = 0;

	function px(p) { return { x: PAD + (p.x - 0.6) * unitX, y: PAD + (p.y - ymin) * unitY }; }
	function measure(pos) {
		unitX = Math.max(58, Math.min(100, (plane.parentNode.clientWidth - 2 * PAD) / 9.9));
		var ys = Object.keys(pos).map(function (k) { return pos[k].y; });
		var xs = Object.keys(pos).map(function (k) { return pos[k].x; }), wide = Math.max(9.9, Math.max.apply(null, xs.concat([0])) + 0.3);
		if (!ys.length) ys = [0, 1];   // nothing to draw
		ymin = Math.min.apply(null, ys);
		planeW = 2 * PAD + wide * unitX;   // the width, animated with the nodes (see setChar)
		return 2 * PAD + (Math.max.apply(null, ys) - ymin) * unitY + 8;   // the height, animated with the nodes
	}

	function makeNode(nd) {
		var el = document.createElement("button");
		el.type = "button";
		el.className = "ade-node";
		el.addEventListener("click", function (ev) { ev.stopPropagation(); select({ node: nodes[el.dataset.key].nd.id }); });
		el.addEventListener("mouseenter", function () { hover = { node: nodes[el.dataset.key].nd.id }; focus(); });
		el.addEventListener("mouseleave", function () { hover = null; focus(); });
		plane.appendChild(el);
		return el;
	}
	function makeEdge() {
		var g = document.createElementNS(SVGNS, "g"), line = document.createElementNS(SVGNS, "path"), hit = document.createElementNS(SVGNS, "path");
		line.setAttribute("class", "line"); hit.setAttribute("class", "hit");
		g.appendChild(line); g.appendChild(hit); svg.appendChild(g);
		return { g: g, line: line, hit: hit };
	}

	// Where the segment from a to b leaves the node around a (an ellipse the size of a node).
	function clip(a, b, hw, hh) {
		var dx = b.x - a.x, dy = b.y - a.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
		var t = 1 / Math.sqrt(Math.pow(dx / d / hw, 2) + Math.pow(dy / d / hh, 2));
		return { x: a.x + dx / d * t, y: a.y + dy / d * t };
	}
	function drawEdges() {
		Object.keys(edges).forEach(function (k) {
			var E = edges[k], a = nodes[E.fk], b = nodes[E.tk];
			if (!a || !b) return;
			// a node that has just split off starts on top of its parent: nothing to draw yet
			if (Math.abs(a.x - b.x) + Math.abs(a.y - b.y) < 40) { E.line.removeAttribute("d"); E.hit.removeAttribute("d"); return; }
			var p = clip(a, b, 16, 13), q = clip(b, a, 18, 15);
			var d = "M" + p.x.toFixed(1) + " " + p.y.toFixed(1) + "L" + q.x.toFixed(1) + " " + q.y.toFixed(1);
			E.line.setAttribute("d", d); E.hit.setAttribute("d", d);
			E.g.style.opacity = E.o;
		});
	}
	function drawNodes() {
		Object.keys(nodes).forEach(function (k) {
			var N = nodes[k];
			N.el.style.left = N.x + "px"; N.el.style.top = N.y + "px";
			N.el.style.opacity = N.o;
			N.el.style.transform = "translate(-50%, -50%) scale(" + N.s + ")";
		});
		Object.keys(dotEls).forEach(function (f) { var d = dotEls[f]; d.el.style.left = d.x + "px"; d.el.style.top = d.y + "px"; d.el.style.opacity = d.o; });
	}

	function styleEdge(E) {
		var e = E.e, k = E.k, on = E.on, unexp = !!e.unexpected, isNew = !ekeys0[k];
		var has = e.unfoldings.some(function (u) { return u.chars.indexOf(ch) >= 0; });
		E.g.setAttribute("class", "ade-edge" + (unexp ? " un" : isNew ? " new" : "") + (has ? " has" : "") + (on ? " on" : "") +
			(sel && sel.edge === e ? " sel" : ""));
		E.line.setAttribute("marker-end", "url(#" + (sel && sel.edge === e ? "ade-arr-sel" : unexp ? "ade-arr-un" : isNew ? "ade-arr-new" : (has || on) ? "ade-arr-d" : "ade-arr") + ")");
	}

	// Go to characteristic c, moving what stays, growing new classes out of the class they split from
	// and shrinking the ones that disappear back into it.
	function setChar(c, instant) {
		var changed = ch !== c || !noteEl.innerHTML, prev = ch;
		ch = c;
		root.querySelectorAll("#ade-chars button").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.ch === c); });
		if (changed) {
			noteEl.innerHTML = md(charInfo(c).note || "");
			emptyEl.hidden = nodesIn(c).length > 0;
			root.classList.toggle("right", isRight(c));
			typeset([noteEl]);
		}
		var pos = layout(c);
		var h0 = parseFloat(plane.style.height) || 0, w0 = parseFloat(plane.style.width) || 0, h1 = measure(pos), w1 = planeW;
		// "..." after the last A and D drawn. Where the series is finite (right equivalence, p >= 11), its last
		// members A_{p-2} and D_{p-1} follow, placed like the rest of the map (D half a column right of A).
		// The dots slide to their new place; the end labels (extras) fade in after the nodes have moved.
		var ends = charInfo(c).ends || {}, endEls = [], endPx = {}, newDots = {}, newExtras = [];
		function lastOf(fam) {
			var n = 0;
			Object.keys(pos).forEach(function (k) { var m = /^([AD])(\d+)$/.exec(k); if (m && m[1] === fam) n = Math.max(n, +m[2]); });
			return n ? fam + n : null;
		}
		var lastA = lastOf("A"), xEnd = lastA ? pos[lastA].x + 1.6 : 0;
		[lastA, lastOf("D")].filter(function (k) { return k && (ends[k[0]] || /9$/.test(k)); }).forEach(function (k) {
			var fam = k[0], last = ends[fam] ? { x: xEnd + (fam === "D" ? 0.5 : 0), y: pos[k].y } : null;
			var p = newDots[fam] = px({ x: last ? (pos[k].x + last.x) / 2 : pos[k].x + 0.62, y: pos[k].y });
			if (!last) return;
			var q = px(last), e = document.createElement("span");
			e.className = "ade-end"; e.textContent = "\\(" + ends[fam] + "\\)";
			e.style.left = q.x + "px"; e.style.top = q.y + "px"; e.style.opacity = 0;
			plane.appendChild(e); endEls.push(e); newExtras.push(e);
			endPx[fam] = q;
		});
		if (endEls.length) typeset(endEls);
		var oldDots = {};
		Object.keys(dotEls).forEach(function (f) { oldDots[f] = { x: dotEls[f].x, y: dotEls[f].y }; });

		var start = {}, target = {};
		Object.keys(nodes).forEach(function (k) { start[k] = { x: nodes[k].x, y: nodes[k].y, s: nodes[k].s, o: nodes[k].o }; });

		var relabel = [];
		nodesIn(c).forEach(function (nd) {
			var k = keyOf(nd, c), t = px(pos[k]), N = nodes[k];
			if (!N) {
				var from = nodes[parentKey(nd)] || oldDots[nd.family] || t;
				N = nodes[k] = { el: makeNode(nd), x: from.x, y: from.y, s: 0.3, o: 0 };
				start[k] = { x: from.x, y: from.y, s: 0.3, o: 0 };
			}
			N.nd = nd; N.gone = false;
			N.el.dataset.key = k;
			if (N.id !== nd.id) { N.id = nd.id; N.el.textContent = math(nd.id); relabel.push(N.el); }
			N.el.classList.toggle("new", !keys0[k]);
			N.el.setAttribute("aria-label", nd.id.replace("^", " superscript "));
			target[k] = { x: t.x, y: t.y, s: 1, o: 1 };
		});
		if (relabel.length) typeset(relabel);
		Object.keys(nodes).forEach(function (k) {
			if (target[k]) return;
			var N = nodes[k], p = pos[parentKey(N.nd)], t = p ? px(p) : newDots[N.nd.family] || { x: N.x, y: N.y };
			N.gone = true;
			target[k] = { x: t.x, y: t.y, s: 0.3, o: 0 };
		});

		var estart = {}, etarget = {};
		Object.keys(edges).forEach(function (k) { estart[k] = edges[k].o; etarget[k] = 0; });
		edgesIn(c).forEach(function (e) {
			var k = ekey(e, c), E = edges[k];
			if (!E) { E = edges[k] = makeEdge(); E.o = 0; estart[k] = 0; }
			E.e = e; E.k = k; E.fk = keyOf(byId[e.from], c); E.tk = keyOf(byId[e.to], c); E.gone = false;
			E.hit.onclick = function (ev) { ev.stopPropagation(); select({ edge: E.e }); };
			E.hit.onmouseenter = function () { hover = { edge: E.e }; focus(); };
			E.hit.onmouseleave = function () { hover = null; focus(); };
			etarget[k] = 1;
		});
		Object.keys(edges).forEach(function (k) { if (!etarget[k]) edges[k].gone = true; });

		if (sel && sel.node && byId[sel.node].chars.indexOf(c) < 0) {
			var old = keyOf(byId[sel.node], prev), same = nodesIn(c).filter(function (nd) { return keyOf(nd, c) === old; })[0];
			sel = same ? { node: same.id } : null;
		}
		if (sel && sel.edge && edgesIn(c).indexOf(sel.edge) < 0) {
			var k = ekey(sel.edge, prev), E = edges[k];
			sel = E && !E.gone && edgesIn(c).indexOf(E.e) >= 0 ? { edge: E.e } : null;
		}
		focus();
		showDetail();

		var dstart = {}, dtarget = {};
		["A", "D"].forEach(function (f) {
			var d = dotEls[f], n = newDots[f];
			if (!d && !n) return;
			if (!d) {
				var el = document.createElement("span");
				el.className = "ade-dots"; el.textContent = "\u22ef"; plane.appendChild(el);
				d = dotEls[f] = { el: el, x: n.x, y: n.y, o: 0 };
			}
			d.gone = !n;
			dstart[f] = { x: d.x, y: d.y, o: d.o };
			dtarget[f] = n ? { x: n.x, y: n.y, o: 1 } : { x: d.x, y: d.y, o: 0 };
		});
		dying.forEach(function (x) { x.remove(); });   // left over from an interrupted switch
		extras.forEach(function (x) { x.dataset.o0 = x.style.opacity || 1; });
		var oldExtras = dying = extras; extras = newExtras;

		if (anim) cancelAnimationFrame(anim);
		var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
		var t0 = performance.now(), dur = instant || reduce ? 0 : DUR;
		function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
		function frame(now) {
			var t = dur ? Math.min(1, (now - t0) / dur) : 1, u = ease(t);
			Object.keys(target).forEach(function (k) {
				var a = start[k], b = target[k], N = nodes[k];
				N.x = a.x + (b.x - a.x) * u; N.y = a.y + (b.y - a.y) * u;
				N.s = a.s + (b.s - a.s) * u; N.o = a.o + (b.o - a.o) * u;
			});
			// new arrows fade in after the nodes have moved, old ones fade out at once
			Object.keys(etarget).forEach(function (k) {
				var v = etarget[k] ? Math.max(0, (t - 0.55) / 0.45) : Math.max(0, 1 - t / 0.35);
				edges[k].o = etarget[k] ? Math.max(estart[k], v) : Math.min(estart[k], v);
			});
			Object.keys(dtarget).forEach(function (f) {
				var a = dstart[f], b = dtarget[f], d = dotEls[f];
				d.x = a.x + (b.x - a.x) * u; d.y = a.y + (b.y - a.y) * u; d.o = a.o + (b.o - a.o) * u;
			});
			newExtras.forEach(function (x) { x.style.opacity = Math.max(0, (t - 0.55) / 0.45); });
			oldExtras.forEach(function (x) { x.style.opacity = Math.min(+x.dataset.o0, Math.max(0, 1 - t / 0.35)); });
			plane.style.height = (h0 ? h0 + (h1 - h0) * u : h1) + "px";
			plane.style.width = (w0 ? w0 + (w1 - w0) * u : w1) + "px";
			drawNodes(); drawEdges();
			if (t < 1) { anim = requestAnimationFrame(frame); return; }
			anim = null;
			oldExtras.forEach(function (x) { x.remove(); }); dying = [];
			Object.keys(dotEls).forEach(function (f) { if (dotEls[f].gone) { dotEls[f].el.remove(); delete dotEls[f]; } });
			Object.keys(nodes).forEach(function (k) { if (nodes[k].gone) { nodes[k].el.remove(); delete nodes[k]; } });
			Object.keys(edges).forEach(function (k) { if (edges[k].gone) { edges[k].g.remove(); delete edges[k]; } });
		}
		anim = requestAnimationFrame(frame);
	}

	// ---- highlight and selection ----
	function focus() {
		var f = hover || sel, onN = {}, onE = {};
		if (f && f.node) {
			onN[f.node] = 1;
			edgesIn(ch).forEach(function (e) { if (e.from === f.node || e.to === f.node) { onE[ekey(e)] = 1; onN[e.from] = onN[e.to] = 1; } });
		} else if (f && f.edge) { onE[ekey(f.edge)] = 1; onN[f.edge.from] = onN[f.edge.to] = 1; }
		plane.classList.toggle("focus", !!f);
		Object.keys(nodes).forEach(function (k) {
			var N = nodes[k];
			N.el.classList.toggle("on", !!onN[N.nd.id]);
			N.el.classList.toggle("sel", !!(sel && sel.node === N.nd.id));
		});
		Object.keys(edges).forEach(function (k) { var E = edges[k]; if (E.e) { E.on = !!onE[k]; styleEdge(E); } });
	}
	function select(s) { sel = s; focus(); showDetail(); }
	plane.addEventListener("click", function () { if (sel) select(null); });

	function unfoldingHtml(u, to) {
		var h = '<div class="ade-unf">' + (u.chars.indexOf(ch) < 0 ? '<p class="ade-k">Recorded in characteristic ' + esc(u.chars.map(charLabel).join(", ")) + "</p>" : "") +
			"\\[ F_t = " + u.f + " \\]" + (u.where ? "<p>where \\(" + u.where + "\\).</p>" : "") +
			"<p>" + (u.generic ? "For generic \\(t\\)" : "For \\(t \\neq 0\\)") + ", \\(F_t\\) is contact equivalent to " + math(to) + ".</p>";
		if (u.proof) h += '<p class="ade-k">Why</p><p>' + md(u.proof) + "</p>";
		if (u.note) h += "<p>" + md(u.note) + "</p>";
		if (u.singular && !isRight()) h += '<details class="ade-sing"' + (u.generic ? "" : " open") + '><summary>' + (u.generic ? "Check it in Singular" : "Proof in Singular") + "</summary>" +
			(u.singular_note ? "<p>" + md(u.singular_note) + "</p>" : "") + "<pre><code>" + esc(u.singular.trim()) + "</code></pre></details>";
		if (u.source) h += '<p class="ade-src">Source: ' + md(u.source) + "</p>";
		return h + "</div>";
	}
	function heading(tex, extra) {
		return '<h3>\\(' + tex + '\\) <span class="ade-tag">in characteristic ' + esc(charLabel(ch)) + (isRight() ? ", right equivalence" : ", contact equivalence") + "</span>" + (extra || "") + "</h3>";
	}
	function showDetail() {
		var h;
		if (!sel) {
			h = '<p class="ade-hint">Click a singularity or an arrow.</p>';
		} else if (sel.node) {
			var nd = byId[sel.node], f = form(nd, ch), mu = f.mu[ch];
			h = heading(tex(nd.id)) +
				"\\[ f = " + f.nf + " \\]" +
				(charInfo(ch).nf_ref ? '<p class="ade-src">Normal form: ' + md(charInfo(ch).nf_ref) + "</p>" : "") +
				'<p class="ade-nums"><span>Milnor number \\(\\mu = ' + (mu === null ? "\\infty" : mu) + "\\)</span>" +
				"<span>Tjurina number \\(\\tau = " + f.tau[ch] + "\\)" + (f.tau_ref && f.tau_ref[ch] ? " " + md(f.tau_ref[ch]) : "") + "</span></p>" +
				(ch === "0" || isRight() ? "" : '<p class="ade-src">\\(\\mu\\) of this normal form; for \\(p > 0\\) it is not a contact invariant.</p>');
		} else {
			var e = sel.edge;
			var here = e.unfoldings.filter(function (u) { return u.chars.indexOf(ch) >= 0; });
			var elsewhere = e.unfoldings.filter(function (u) { return u.chars.indexOf(ch) < 0; });
			h = heading(tex(e.from) + " \\to " + tex(e.to), e.unexpected ? ' <span class="ade-tag un">unexpected</span>' : "") +
				(e.refs && e.refs[ch] ? '<p class="ade-src">Adjacency: ' + md(e.refs[ch]) + "</p>" : "") +
				(e.unexpected ? '<p class="ade-note">' + md(e.unexpected) + "</p>" : "");
			if (here.length) h += here.map(function (u) { return unfoldingHtml(u, e.to); }).join("");
			else h += '<p class="ade-todo">No unfolding recorded yet for this characteristic.</p>' + elsewhere.map(function (u) { return unfoldingHtml(u, e.to); }).join("");
		}
		detail.innerHTML = h;
		detail.classList.toggle("empty", !sel);
		typeset([detail]);
	}

	// ---- controls ----
	// The characteristic buttons depend on the equivalence; switching keeps the closest characteristic.
	var seg = document.getElementById("ade-chars"), equivSeg = document.getElementById("ade-equiv"), equiv = "contact";
	function buildChars() {
		seg.innerHTML = "";
		D.chars.filter(function (c) { return c.equiv === equiv; }).forEach(function (c) {
			var b = document.createElement("button");
			b.type = "button"; b.dataset.ch = c.key; b.textContent = c.label;
			b.setAttribute("aria-pressed", c.key === ch);
			b.addEventListener("click", function () { if (c.key !== ch) setChar(c.key); });
			seg.appendChild(b);
		});
	}
	["contact", "right"].forEach(function (q) {
		var b = document.createElement("button");
		b.type = "button"; b.dataset.eq = q; b.textContent = q;
		b.setAttribute("aria-pressed", q === equiv);
		b.addEventListener("click", function () {
			if (q === equiv) return;
			equiv = q;
			equivSeg.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x.dataset.eq === q); });
			var next = q === "right" ? "R" + ch : ch.replace(/^R/, "");
			if (!D.chars.some(function (c) { return c.key === next && c.equiv === q; })) next = q === "right" ? "R0" : "0";
			buildChars();
			setChar(next);
		});
		equivSeg.appendChild(b);
	});
	buildChars();
	var rt;
	window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { setChar(ch, true); }, 150); });
	setChar("0", true);
})();
