// Timeline page (timeline.md, _includes/timeline.html). Two views of window.TIMELINE:
// a map, where time runs down and each canvas group is a box, packed into columns; and a list,
// which is the only view on narrow screens.
(function () {
	var D = window.TIMELINE;
	var CARD_W = 200, COL_W = 224, HEADER = 22, PAD = 8, CARD_GAP = 6, BOX_GAP = 14, TOP = 16;
	var NARROW = window.matchMedia("(max-width: 736px)");

	var entries = D.entries, fields = D.fields, byId = {};
	entries.forEach(function (e) { byId[e.id] = e; });
	var edges = [];
	entries.forEach(function (e) { e.leads_to.forEach(function (t) { edges.push([e.id, t]); }); });
	entries.forEach(function (e) {
		e.builds_on = edges.filter(function (ed) { return ed[1] === e.id; }).map(function (ed) { return ed[0]; });
	});

	function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
	// The small part of Markdown the canvas uses: links, bold, italics and $math$.
	function md(s, plain) {
		var math = [];
		s = s.replace(/\$([^$]+)\$/g, function (_, m) { math.push(m); return "\u0000" + (math.length - 1) + "\u0000"; });
		s = esc(s)
			.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, plain ? "$1" : '<a href="$2">$1</a>')
			.replace(/\*\*(.+?)\*\*/g, plain ? "$1" : "<strong>$1</strong>")
			.replace(/(^|[^*])\*([^*]+)\*/g, "$1<em>$2</em>")
			.replace(/(^|\s)_([^_]+)_/g, "$1<em>$2</em>");
		return s.replace(/\u0000(\d+)\u0000/g, function (_, i) { return "\\(" + esc(math[+i]) + "\\)"; });
	}
	function typeset(els) {
		if (window.MathJax && MathJax.typesetPromise) return MathJax.typesetPromise(els);
		return Promise.resolve();
	}
	function color(e) { return fields[e.field].color; }

	var root = document.getElementById("tl");
	var plane = document.getElementById("tl-plane"), axis = document.getElementById("tl-axis");
	var mapEl = document.getElementById("tl-map"), listEl = document.getElementById("tl-list");
	var detail = document.getElementById("tl-detail");
	var view = NARROW.matches ? "list" : "map", activeField = null, selected = null;

	// ---- Map ----

	// Each group is a box spanning its years. Boxes are packed into columns, a box going into a free
	// column (one whose last box ended before it starts), preferably one last used by the same field.
	var groups = {};
	entries.forEach(function (e) {
		var g = groups[e.group] = groups[e.group] || { name: e.group, field: e.field, start: e.year, end: e.year };
		g.end = Math.max(g.end, e.year);
	});
	var colX = {}, cols = [];
	Object.keys(groups).map(function (k) { return groups[k]; })
		.sort(function (a, b) { return a.start - b.start || a.field - b.field; })
		.forEach(function (g) {
			var free = cols.map(function (c, i) { return c.end < g.start ? i : -1; }).filter(function (i) { return i >= 0; });
			var same = free.filter(function (i) { return cols[i].field === g.field; });
			var c = same.length ? same[0] : free.length ? free[0] : cols.length;
			cols[c] = { end: g.end, field: g.field };
			colX[g.name] = c * COL_W;
		});

	var cardEls = {}, boxEls = {}, pathEls = [], pos = {};
	entries.forEach(function (e) {
		var d = document.createElement("button");
		d.type = "button";
		d.className = "tl-card";
		d.style.setProperty("--c", color(e));
		d.innerHTML = '<span class="tl-y">' + e.year + "</span>" + md(e.title, true);
		d.onmouseenter = function () { focus(e); };
		d.onmouseleave = function () { focus(selected); };
		d.onclick = function () { select(selected === e ? null : e); };
		cardEls[e.id] = d;
	});

	// Years go down in order. The gap between years grows slowly with the number of years between them,
	// and a year moves further down when a column is still busy with the cards of earlier years.
	function layout() {
		plane.innerHTML = ""; axis.innerHTML = ""; boxEls = {}; pos = {};
		entries.forEach(function (e) { plane.appendChild(cardEls[e.id]); });
		var h = {};
		entries.forEach(function (e) { h[e.id] = cardEls[e.id].offsetHeight; });

		var byYear = {};
		entries.forEach(function (e) { (byYear[e.year] = byYear[e.year] || []).push(e); });
		var years = Object.keys(byYear).map(Number).sort(function (p, q) { return p - q; });

		var colBottom = {}, box = {}, cursor = TOP, prev = null, ticks = [];
		years.forEach(function (y) {
			var at = prev === null ? TOP + HEADER + PAD : cursor + Math.min(70, 10 + 16 * Math.log2(1 + y - prev));
			var seen = {};
			byYear[y].forEach(function (e) {
				var c = colX[e.group];
				if (seen[c] || colBottom[c] === undefined) { seen[c] = 1; return; }
				seen[c] = 1;
				at = Math.max(at, box[e.group] ? colBottom[c] + CARD_GAP : colBottom[c] + BOX_GAP + HEADER + PAD);
			});
			var top = {};
			byYear[y].forEach(function (e) {
				var c = colX[e.group];
				var t = top[c] === undefined ? at : top[c];
				if (!box[e.group]) {
					if (top[c] !== undefined) t += HEADER + PAD;
					box[e.group] = { top: t - HEADER - PAD, left: c };
				}
				pos[e.id] = { x: c + 12, y: t, h: h[e.id] };
				t += h[e.id];
				box[e.group].bottom = colBottom[c] = t + PAD;
				top[c] = t + CARD_GAP;
			});
			ticks.push({ year: y, at: at });
			cursor = at; prev = y;
		});

		var height = Math.max.apply(null, Object.keys(colBottom).map(function (k) { return colBottom[k]; })) + 40;
		var width = cols.length * COL_W + 8;
		plane.style.width = width + "px"; plane.style.height = height + "px"; axis.style.height = height + "px";

		var last = -99;
		ticks.forEach(function (t, i) {
			if (t.at - last < 18) return;
			last = t.at;
			var g = document.createElement("div");
			g.className = "tl-grid"; g.style.top = (t.at + 9) + "px";
			plane.insertBefore(g, plane.firstChild);
			var k = document.createElement("div");
			k.className = "tl-tick" + (i === 0 || t.year % 50 === 0 ? " major" : "");
			k.style.top = t.at + "px"; k.textContent = t.year;
			axis.appendChild(k);
		});

		var first = cardEls[entries[0].id];
		Object.keys(box).forEach(function (g) {
			var b = box[g], d = document.createElement("div");
			d.className = "tl-box";
			d.style.cssText = "left:" + b.left + "px;top:" + b.top + "px;width:" + (CARD_W + 24) + "px;height:" +
				(b.bottom - b.top) + "px;--c:" + fields[groups[g].field].color;
			d.innerHTML = '<div class="tl-lbl" title="' + esc(g) + '">' + esc(g) + "</div>";
			plane.insertBefore(d, first);
			boxEls[g] = d;
		});
		entries.forEach(function (e) {
			cardEls[e.id].style.left = pos[e.id].x + "px";
			cardEls[e.id].style.top = pos[e.id].y + "px";
		});

		var NS = "http://www.w3.org/2000/svg", svg = document.createElementNS(NS, "svg");
		svg.setAttribute("class", "tl-edges");
		svg.setAttribute("width", width); svg.setAttribute("height", height);
		pathEls = edges.map(function (ed) {
			var p = pos[ed[0]], q = pos[ed[1]];
			var x1 = p.x + CARD_W / 2, y1 = p.y + p.h, x2 = q.x + CARD_W / 2, y2 = q.y;
			if (y2 < y1 + 4) {  // same row: join the sides instead
				var right = q.x > p.x;
				x1 = p.x + (right ? CARD_W : 0); y1 = p.y + p.h / 2;
				x2 = q.x + (right ? 0 : CARD_W); y2 = q.y + q.h / 2;
			}
			var dy = Math.max(30, (y2 - y1) / 2), path = document.createElementNS(NS, "path");
			path.setAttribute("d", "M" + x1 + "," + y1 + " C" + x1 + "," + (y1 + dy) + " " + x2 + "," + (y2 - dy) + " " + x2 + "," + y2);
			if (byId[ed[0]].field !== byId[ed[1]].field) path.setAttribute("class", "cross");
			path.dataset.a = ed[0]; path.dataset.b = ed[1];
			svg.appendChild(path);
			return path;
		});
		plane.insertBefore(svg, first);
		focus(selected);
	}

	function focus(e) {
		var on = {};
		if (e) {
			on[e.id] = 1;
			edges.forEach(function (ed) { if (ed[0] === e.id) on[ed[1]] = 1; if (ed[1] === e.id) on[ed[0]] = 1; });
		} else if (activeField !== null) {
			entries.forEach(function (x) { if (x.field === activeField) on[x.id] = 1; });
		}
		plane.classList.toggle("focus", !!e || activeField !== null);
		entries.forEach(function (x) {
			cardEls[x.id].classList.toggle("on", !!on[x.id]);
			cardEls[x.id].classList.toggle("sel", selected === x);
		});
		Object.keys(boxEls).forEach(function (g) {
			boxEls[g].classList.toggle("on", entries.some(function (x) { return x.group === g && on[x.id]; }));
		});
		pathEls.forEach(function (p) {
			var a = p.dataset.a, b = p.dataset.b;
			p.classList.toggle("on", e ? (a === e.id || b === e.id) : !!(on[a] && on[b]));
		});
	}

	function related(ids, word) {
		if (!ids.length) return "";
		return "<p>" + word + "</p><ul>" + ids.map(function (i) {
			return '<li><a href="#" data-id="' + i + '">' + byId[i].year + " · " + md(byId[i].title, true) + "</a></li>";
		}).join("") + "</ul>";
	}

	function select(e) {
		selected = e;
		focus(e);
		if (!e) { detail.hidden = true; return; }
		detail.style.setProperty("--c", color(e));
		detail.innerHTML = '<button type="button" class="tl-x" aria-label="Close">×</button>' +
			'<div class="tl-field">' + esc(fields[e.field].name) + " · " + esc(e.group) + "</div>" +
			"<h3>" + e.year + " · " + md(e.title) + "</h3>" + (e.note ? "<div>" + md(e.note) + "</div>" : "") +
			related(e.builds_on, "Builds on") + related(e.leads_to, "Leads to");
		detail.hidden = false;
		detail.querySelector(".tl-x").onclick = function () { select(null); };
		detail.querySelectorAll("a[data-id]").forEach(function (a) {
			a.onclick = function (ev) {
				ev.preventDefault();
				var t = byId[a.dataset.id];
				select(t);
				mapEl.scrollTo({ left: Math.max(0, pos[t.id].x - 120), top: Math.max(0, pos[t.id].y - 120), behavior: "smooth" });
			};
		});
		typeset([detail]);
	}

	// ---- List ----

	function eraOf(y) { return y < 1900 ? "19th century" : y < 1950 ? "1900–1949" : y < 2000 ? "1950–1999" : "2000–today"; }

	function renderList() {
		var html = "", era = null;
		entries.forEach(function (e) {
			if (activeField !== null && e.field !== activeField) return;
			if (eraOf(e.year) !== era) {
				era = eraOf(e.year);
				html += "<h3>" + era + "</h3>";
			}
			var links = function (ids, word) {
				return ids.length ? '<span class="tl-rel">' + word + " " + ids.map(function (i) {
					return '<a href="#tl-e-' + i + '">' + md(byId[i].title, true) + " (" + byId[i].year + ")</a>";
				}).join(", ") + "</span>" : "";
			};
			html += '<article class="tl-entry" id="tl-e-' + e.id + '" style="--c:' + color(e) + '">' +
				'<div class="tl-year">' + e.year + '</div><div class="tl-body"><div>' + md(e.title) + "</div>" +
				(e.note ? '<div class="tl-note">' + md(e.note) + "</div>" : "") +
				'<div class="tl-meta"><span class="tl-field">' + esc(e.group) + "</span>" +
				links(e.builds_on, "Builds on") + links(e.leads_to, "Leads to") + "</div></div></article>";
		});
		listEl.innerHTML = html;
		listEl.querySelectorAll(".tl-rel a").forEach(function (a) {
			a.onclick = function (ev) {
				var target = document.querySelector(a.getAttribute("href"));
				if (!target) { setField(null); target = document.querySelector(a.getAttribute("href")); }
				if (!target) return;
				ev.preventDefault();
				target.scrollIntoView({ behavior: "smooth", block: "center" });
				target.classList.add("flash");
				setTimeout(function () { target.classList.remove("flash"); }, 1400);
			};
		});
		typeset([listEl]);
	}

	// ---- Controls ----

	// The field chips highlight a field on the map and filter the list.
	var chips = document.getElementById("tl-chips");
	chips.innerHTML = fields.map(function (f, i) {
		return '<button type="button" class="tl-chip" data-i="' + i + '" aria-pressed="false" style="--c:' + f.color +
			'"><span class="dot"></span>' + esc(f.name) + "</button>";
	}).join("");
	function setField(i) {
		activeField = i;
		chips.querySelectorAll(".tl-chip").forEach(function (b) { b.setAttribute("aria-pressed", +b.dataset.i === activeField); });
		if (view === "list") renderList(); else focus(selected);
	}
	chips.querySelectorAll(".tl-chip").forEach(function (b) {
		b.onclick = function () { setField(activeField === +b.dataset.i ? null : +b.dataset.i); };
	});

	var drawn = false;
	function show(v) {
		view = v;
		root.querySelectorAll("[data-view]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.view === v); });
		mapEl.hidden = v !== "map";
		listEl.hidden = v !== "list";
		if (v === "list") { select(null); renderList(); }
		else if (!drawn) {
			drawn = true;
			layout();
			// Card heights change once the fonts and the math are in, so lay out again then.
			var waited = 0, timer = setInterval(function () {
				if (window.MathJax && MathJax.typesetPromise) {
					clearInterval(timer);
					(document.fonts ? document.fonts.ready : Promise.resolve()).then(function () {
						return typeset(entries.map(function (e) { return cardEls[e.id]; }));
					}).then(layout);
				} else if (++waited > 100) clearInterval(timer);
			}, 100);
		}
	}
	root.querySelectorAll("[data-view]").forEach(function (b) { b.onclick = function () { show(b.dataset.view); }; });
	NARROW.addEventListener("change", function () { if (NARROW.matches) show("list"); });
	show(view);
})();
