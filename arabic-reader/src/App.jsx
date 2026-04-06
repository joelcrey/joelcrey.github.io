import { useState, useEffect, useRef } from "react";

const API = "https://api.anthropic.com/v1/messages";
const MODEL = "claude-sonnet-4-20250514";

async function callClaude(messages, system, webSearch = false, apiKey) {
  const body = { model: MODEL, max_tokens: webSearch ? 2500 : 800, messages };
  if (system) body.system = system;
  if (webSearch) body.tools = [{ type: "web_search_20250305", name: "web_search" }];
  const r = await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "anthropic-dangerous-direct-browser-access": "true",
    },
    body: JSON.stringify(body),
  });
  const data = await r.json();
  if (data.error) throw new Error(data.error.message || "API error");
  return data;
}

function extractJson(txt) {
  const stripped = txt.replace(/```(?:json)?[\s\S]*?```/g, m => m.replace(/```(?:json)?|```/g, "")).trim();
  const candidates = [...stripped.matchAll(/\{[\s\S]*\}/g)];
  for (const m of candidates.reverse()) {
    try { return JSON.parse(m[0]); } catch {}
  }
  try { return JSON.parse(stripped); } catch {}
  throw new Error("No valid JSON found in response");
}

function Pill({ label }) {
  return <span style={{ fontSize: 12, color: "#7a5520", backgroundColor: "#f5edd8", padding: "3px 10px", borderRadius: 20, display: "inline-block" }}>{label}</span>;
}

function Section({ label, children }) {
  return (
    <div style={{ marginBottom: 18 }}>
      <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.1em", color: "#b0a898", marginBottom: 7 }}>{label}</div>
      {children}
    </div>
  );
}

const INSTANT_SYS = `You are an Arabic linguistics expert. Return ONLY a valid JSON object, no markdown, no extra text. Use this structure:
{"word":"Arabic word","translation":"concise English translation","transliteration":"simple romanized pronunciation","partOfSpeech":"noun / verb / adjective / particle / etc."}`;

const GRAMMAR_SYS = `You are an Arabic linguistics expert. Return ONLY a valid JSON object, no markdown, no extra text. Use this structure:
{"root":"trilateral root in Arabic script","pattern":"morphological pattern if applicable","grammarNotes":"1-2 sentence grammar explanation"}`;

const FULL_SYS = `You are an Arabic linguistics expert. Return ONLY a valid JSON object, no markdown, no extra text. Use this structure:
{"examples":["Arabic example sentence 1","Arabic example sentence 2"],"references":[{"title":"Source name","url":"real direct URL to word entry","note":"brief note"}]}
Search for REAL working URLs. Preferred: almaany.com (https://www.almaany.com/ar/dict/ar-en/WORD/), en.wiktionary.org, arabdict.com, lisaan.net, qutrub.com for verbs. Include 2-4 references.`;

export default function App() {
  const [apiKey, setApiKey] = useState(() => localStorage.getItem("anthropic_key") || "");
  const [keyInput, setKeyInput] = useState("");
  const [screen, setScreen] = useState("input");
  const [input, setInput] = useState("");
  const [arabicText, setArabicText] = useState("");
  const [fetching, setFetching] = useState(false);
  const [selected, setSelected] = useState(null);
  const [instantInfo, setInstantInfo] = useState(null);
  const [grammarInfo, setGrammarInfo] = useState(null);
  const [fullInfo, setFullInfo] = useState(null);
  const [instantLoading, setInstantLoading] = useState(false);
  const [grammarLoading, setGrammarLoading] = useState(false);
  const [fullLoading, setFullLoading] = useState(false);
  const [glossary, setGlossary] = useState([]);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [showGlossary, setShowGlossary] = useState(false);

  useEffect(() => {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://fonts.googleapis.com/css2?family=Amiri:ital@0;1&display=swap";
    document.head.appendChild(link);
  }, []);

  const saveKey = () => {
    const k = keyInput.trim();
    if (!k.startsWith("sk-")) return alert("That doesn't look like a valid API key.");
    localStorage.setItem("anthropic_key", k);
    setApiKey(k);
  };

  const isUrl = s => /^https?:\/\//i.test(s.trim());
  const clean = w => w.replace(/[\u0610-\u061A\u064B-\u065F\u0640.,،؟!؛:«»()\[\]{}"']/g, "").trim();

  const loadText = async () => {
    if (!input.trim()) return;
    setFetching(true);
    try {
      if (isUrl(input.trim())) {
        const d = await callClaude([{ role: "user", content: `Fetch this URL and extract only the main Arabic body text. Return ONLY the Arabic text: ${input.trim()}` }], null, true, apiKey);
        const txt = d.content.filter(b => b.type === "text").map(b => b.text).join("").trim();
        setArabicText(txt);
      } else {
        setArabicText(input.trim());
      }
      setSelected(null); setInstantInfo(null); setGrammarInfo(null); setFullInfo(null); setSheetOpen(false);
      setScreen("reading");
    } catch (e) {
      alert(`Error: ${e.message}`);
    }
    setFetching(false);
  };

  const analyzeWord = async (raw) => {
    const w = clean(raw);
    if (!w || w.length < 2) return;
    setSelected(w); setInstantInfo(null); setGrammarInfo(null); setFullInfo(null);
    setInstantLoading(true); setGrammarLoading(true); setSheetOpen(true); setShowGlossary(false);

    const instantCall = callClaude([{ role: "user", content: `Translate the Arabic word: "${w}"` }], INSTANT_SYS, false, apiKey)
      .then(d => {
        const parsed = extractJson(d.content.filter(b => b.type === "text").map(b => b.text).join(""));
        setInstantInfo(parsed);
        if (parsed.word && parsed.translation)
          setGlossary(prev => prev.some(g => g.word === parsed.word) ? prev : [...prev, { word: parsed.word, translation: parsed.translation, transliteration: parsed.transliteration }]);
      })
      .catch(e => setInstantInfo({ _error: `Error: ${e.message}` }))
      .finally(() => setInstantLoading(false));

    const grammarCall = callClaude([{ role: "user", content: `Root, pattern, grammar notes for Arabic word: "${w}"` }], GRAMMAR_SYS, false, apiKey)
      .then(d => setGrammarInfo(extractJson(d.content.filter(b => b.type === "text").map(b => b.text).join(""))))
      .catch(() => setGrammarInfo(null))
      .finally(() => setGrammarLoading(false));

    await Promise.all([instantCall, grammarCall]);
  };

  const loadFull = async () => {
    if (!selected || fullLoading) return;
    setFullLoading(true);
    try {
      const d = await callClaude([{ role: "user", content: `For Arabic word "${selected}", find real dictionary URLs and 2 example sentences.` }], FULL_SYS, true, apiKey);
      setFullInfo(extractJson(d.content.filter(b => b.type === "text").map(b => b.text).join("")));
    } catch (e) { setFullInfo({ _error: `Error: ${e.message}` }); }
    setFullLoading(false);
  };

  const tokenize = text => text.split(/(\s+)/).map((t, i) => {
    if (/^\s+$/.test(t)) return <span key={i}>{t}</span>;
    const isSel = clean(t) === selected;
    return (
      <span key={i} onClick={() => analyzeWord(t)} style={{ cursor: "pointer", padding: "2px 5px", borderRadius: 4, backgroundColor: isSel ? "#e8d9bc" : "transparent", WebkitTapHighlightColor: "transparent", transition: "background 0.1s", display: "inline" }}>{t}</span>
    );
  });

  // ── API key screen ─────────────────────────────────────────
  if (!apiKey) return (
    <div style={{ minHeight: "100dvh", display: "flex", alignItems: "center", justifyContent: "center", backgroundColor: "#f9f8f5", padding: "24px 20px", fontFamily: "Georgia, serif", boxSizing: "border-box" }}>
      <div style={{ width: "100%", maxWidth: 480 }}>
        <h1 style={{ fontSize: 22, fontWeight: 400, color: "#1a1a1a", marginBottom: 10 }}>Arabic Reading Assistant</h1>
        <p style={{ color: "#888", fontSize: 14, lineHeight: 1.7, marginBottom: 24 }}>
          This app uses the Anthropic API. Paste your API key below to get started — it's saved locally on your device and never sent anywhere else.
          <br /><br />
          Get a key at <a href="https://console.anthropic.com" target="_blank" rel="noreferrer" style={{ color: "#7a5520" }}>console.anthropic.com</a>.
        </p>
        <input value={keyInput} onChange={e => setKeyInput(e.target.value)} placeholder="sk-ant-..." type="password"
          style={{ width: "100%", padding: "13px 14px", fontSize: 15, border: "1px solid #ddd", borderRadius: 8, boxSizing: "border-box", outline: "none", fontFamily: "monospace", marginBottom: 10 }} />
        <button onClick={saveKey} disabled={!keyInput.trim()}
          style={{ width: "100%", padding: 14, backgroundColor: "#2b2b2b", color: "#fff", border: "none", borderRadius: 9, fontSize: 15, cursor: "pointer", fontFamily: "Georgia, serif" }}>
          Save & Continue →
        </button>
      </div>
    </div>
  );

  // ── Input screen ───────────────────────────────────────────
  if (screen === "input") return (
    <div style={{ minHeight: "100dvh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", backgroundColor: "#f9f8f5", padding: "24px 20px", fontFamily: "Georgia, serif", boxSizing: "border-box" }}>
      <div style={{ width: "100%", maxWidth: 560 }}>
        <h1 style={{ fontSize: 24, fontWeight: 400, color: "#1a1a1a", margin: "0 0 8px" }}>Arabic Reading Assistant</h1>
        <p style={{ color: "#888", fontSize: 14, lineHeight: 1.6, margin: "0 0 24px" }}>Paste Arabic text or a news article URL. Tap any word for a quick translation, or go deeper for grammar and references.</p>
        <textarea value={input} onChange={e => setInput(e.target.value)}
          placeholder={"أدخل النص العربي هنا…\n\nOr paste a URL to an Arabic article."}
          style={{ width: "100%", height: 180, padding: 16, fontSize: 17, border: "1px solid #ddd", borderRadius: 10, resize: "vertical", fontFamily: isUrl(input) ? "monospace" : "'Amiri', Georgia, serif", direction: isUrl(input) ? "ltr" : "rtl", backgroundColor: "#fff", boxSizing: "border-box", outline: "none", color: "#1a1a1a", lineHeight: 1.9 }} />
        <button onClick={loadText} disabled={fetching || !input.trim()}
          style={{ width: "100%", padding: 15, marginTop: 12, backgroundColor: fetching ? "#aaa" : "#2b2b2b", color: "#fff", border: "none", borderRadius: 9, fontSize: 16, cursor: fetching ? "wait" : "pointer", fontFamily: "Georgia, serif" }}>
          {fetching ? "Fetching article…" : "Start Reading →"}
        </button>
        <button onClick={() => { localStorage.removeItem("anthropic_key"); setApiKey(""); }}
          style={{ background: "none", border: "none", color: "#ccc", fontSize: 12, cursor: "pointer", marginTop: 16, display: "block", fontFamily: "inherit" }}>
          Change API key
        </button>
      </div>
    </div>
  );

  // ── Reading screen ─────────────────────────────────────────
  return (
    <div style={{ height: "100dvh", display: "flex", flexDirection: "column", fontFamily: "Georgia, serif", backgroundColor: "#f9f8f5", position: "relative" }}>
      <div style={{ padding: "10px 16px", borderBottom: "1px solid #e6e1da", display: "flex", alignItems: "center", backgroundColor: "#fff", flexShrink: 0, gap: 10 }}>
        <button onClick={() => setScreen("input")} style={{ background: "none", border: "none", cursor: "pointer", color: "#888", fontSize: 13, fontFamily: "inherit", padding: "4px 0" }}>← New text</button>
        <span style={{ flex: 1 }} />
        <button onClick={() => { setShowGlossary(true); setSheetOpen(true); }} style={{ background: "none", border: "1px solid #ddd", borderRadius: 20, padding: "5px 13px", fontSize: 12, cursor: "pointer", fontFamily: "inherit", color: "#555" }}>
          Glossary {glossary.length > 0 && `(${glossary.length})`}
        </button>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "32px 20px", paddingBottom: sheetOpen ? "52vh" : "32px", transition: "padding-bottom 0.35s ease" }}>
        <div style={{ direction: "rtl", fontSize: 22, lineHeight: 2.4, color: "#1a1a1a", fontFamily: "'Amiri', 'Traditional Arabic', serif", maxWidth: 680, margin: "0 auto" }}>
          {tokenize(arabicText)}
        </div>
      </div>

      {sheetOpen && <div onClick={() => setSheetOpen(false)} style={{ position: "fixed", inset: 0, backgroundColor: "rgba(0,0,0,0.18)", zIndex: 10 }} />}

      <div style={{ position: "fixed", left: 0, right: 0, bottom: 0, height: sheetOpen ? "52vh" : "0", backgroundColor: "#fff", borderRadius: "18px 18px 0 0", boxShadow: "0 -4px 24px rgba(0,0,0,0.12)", zIndex: 20, display: "flex", flexDirection: "column", transition: "height 0.35s cubic-bezier(0.4,0,0.2,1)", overflow: "hidden" }}>
        <div style={{ flexShrink: 0, padding: "10px 0 0", display: "flex", justifyContent: "center" }}>
          <div style={{ width: 36, height: 4, borderRadius: 2, backgroundColor: "#ddd" }} />
        </div>
        <div style={{ padding: "8px 20px 0", display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
          {!showGlossary && <div style={{ fontFamily: "'Amiri', serif", fontSize: 28, direction: "rtl", color: "#1a1a1a" }}>{selected}</div>}
          {showGlossary && <span style={{ fontSize: 16, fontWeight: 600, color: "#1a1a1a" }}>Glossary</span>}
          {instantLoading && <span style={{ fontSize: 12, color: "#aaa", fontStyle: "italic" }}>looking up…</span>}
          <button onClick={() => setSheetOpen(false)} style={{ marginLeft: "auto", background: "none", border: "none", fontSize: 22, cursor: "pointer", color: "#aaa", lineHeight: 1 }}>×</button>
        </div>

        <div style={{ flex: 1, overflowY: "auto", padding: "10px 20px 28px" }}>
          {showGlossary && (
            glossary.length === 0
              ? <p style={{ color: "#ccc", textAlign: "center", marginTop: 30, fontSize: 14 }}>Tap words while reading to save them here.</p>
              : glossary.map((g, i) => (
                  <div key={i} style={{ padding: "11px 0", borderBottom: "1px solid #f0ebe3", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div>
                      <div style={{ fontFamily: "'Amiri', serif", fontSize: 22, direction: "rtl" }}>{g.word}</div>
                      {g.transliteration && <div style={{ fontSize: 11, color: "#aaa", fontStyle: "italic" }}>{g.transliteration}</div>}
                    </div>
                    <div style={{ fontSize: 13, color: "#555" }}>{g.translation}</div>
                  </div>
                ))
          )}

          {!showGlossary && instantLoading && <p style={{ color: "#bbb", textAlign: "center", marginTop: 20, fontSize: 13 }}>Translating…</p>}

          {!showGlossary && instantInfo && (
            instantInfo._error
              ? <p style={{ color: "#c00", fontSize: 13 }}>{instantInfo._error}</p>
              : <>
                  <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
                    <span style={{ fontSize: 20, fontWeight: 600, color: "#2b2b2b" }}>{instantInfo.translation}</span>
                    {instantInfo.transliteration && <span style={{ fontSize: 13, color: "#999", fontStyle: "italic" }}>{instantInfo.transliteration}</span>}
                    {instantInfo.partOfSpeech && <Pill label={instantInfo.partOfSpeech} />}
                  </div>
                  {grammarLoading && <p style={{ color: "#ddd", fontSize: 12, fontStyle: "italic" }}>Loading grammar…</p>}
                  {grammarInfo && !grammarLoading && <>
                    {(grammarInfo.root || grammarInfo.pattern) && (
                      <Section label="Root & Pattern">
                        <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
                          {grammarInfo.root && <span style={{ direction: "rtl", fontFamily: "'Amiri', serif", fontSize: 22, color: "#3b2a0e", backgroundColor: "#f5edd8", padding: "2px 12px", borderRadius: 6 }}>{grammarInfo.root}</span>}
                          {grammarInfo.pattern && <span style={{ fontSize: 13, color: "#888", fontStyle: "italic" }}>pattern: {grammarInfo.pattern}</span>}
                        </div>
                      </Section>
                    )}
                    {grammarInfo.grammarNotes && (
                      <Section label="Grammar">
                        <p style={{ margin: 0, color: "#444", fontSize: 13.5, lineHeight: 1.7 }}>{grammarInfo.grammarNotes}</p>
                      </Section>
                    )}
                  </>}
                  {!fullInfo && !fullLoading && !grammarLoading && (
                    <button onClick={loadFull} style={{ width: "100%", padding: 11, marginTop: 4, border: "1px solid #e0d5c0", borderRadius: 8, background: "#faf8f4", color: "#7a5520", fontSize: 13, cursor: "pointer", fontFamily: "Georgia, serif" }}>
                      Load examples & references ↓
                    </button>
                  )}
                  {fullLoading && <p style={{ color: "#bbb", fontSize: 13, fontStyle: "italic", textAlign: "center", marginTop: 8 }}>Searching dictionaries…</p>}
                  {fullInfo && !fullLoading && (
                    fullInfo._error ? <p style={{ color: "#c00", fontSize: 13 }}>{fullInfo._error}</p>
                    : <>
                        {fullInfo.examples?.length > 0 && (
                          <Section label="Examples">
                            {fullInfo.examples.map((ex, i) => (
                              <div key={i} style={{ direction: "rtl", fontFamily: "'Amiri', serif", fontSize: 17, color: "#333", marginBottom: 8, lineHeight: 2, borderRight: "3px solid #e0d5c0", paddingRight: 10 }}>{ex}</div>
                            ))}
                          </Section>
                        )}
                        {fullInfo.references?.length > 0 && (
                          <Section label="References">
                            {fullInfo.references.map((ref, i) => (
                              <div key={i} style={{ marginBottom: 10, padding: "11px 12px", backgroundColor: "#faf8f4", borderRadius: 8, borderLeft: "3px solid #c9a96e" }}>
                                <a href={ref.url} target="_blank" rel="noreferrer" style={{ color: "#7a5520", fontWeight: 600, fontSize: 13, textDecoration: "none", display: "block", marginBottom: 3 }}>{ref.title} ↗</a>
                                {ref.url && <div style={{ fontSize: 11, color: "#bbb", marginBottom: 3, wordBreak: "break-all" }}>{ref.url}</div>}
                                {ref.note && <div style={{ color: "#777", fontSize: 12, lineHeight: 1.5 }}>{ref.note}</div>}
                              </div>
                            ))}
                          </Section>
                        )}
                      </>
                  )}
                </>
          )}
        </div>
      </div>
    </div>
  );
}