/* Web version of the Streamlit app (dutch_vocab_app.py): same filters and cards.
 * The data (data/words.json) is generated from the Excel file by scripts/export_web.py. */
"use strict";
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const shuffle = (a) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

/** Search phrase for YouGlish (same as youglish_query() in dutch_vocab_app.py): the first
 * alternative, without notes in brackets. "onder druk staan/zetten" -> "onder druk staan". */
function youglishQuery(text) {
  let t = String(text).replace(/^\s*ook:\s*/, "");
  t = t.replace(/(\S )\(([\p{L}\p{N}_]+)\)(?= \S)/gu, "$1$2");      // "op (zichzelf) aangewezen": keep the word
  t = t.replace(/\([^)]*\)|\[[^\]]*\]/g, "");                        // other notes in brackets
  t = t.split(/\s+\/\s*|\s*\/\s+|\n|,|;/)[0];                       // first of several alternatives
  let prev = null;
  while (prev !== t) { prev = t; t = t.replace(/([\p{L}\p{N}_'-]+)\/\s*[\p{L}\p{N}_'.…-]+/u, "$1"); }   // staan/zetten -> staan
  t = t.replace(/\.\.\.|…/g, " ").replace(/\s+/g, " ").replace(/^[ .]+|[ .]+$/g, "");
  return t.replace(/^(de|het) (?=\S+$)/, "");                           // "de nuance" -> "nuance"
}
/** YouGlish with Dutch as spoken in the Netherlands (NL, not BE). */
function youglishLink(text) {
  const q = youglishQuery(text);
  return `<p><a href="https://youglish.com/pronounce/${encodeURIComponent(q)}/dutch/nl" target="_blank" rel="noopener">🎧 Hear it in real conversations (YouGlish, NL)</a>${q.includes(" ") ? ` <span class="caption">· results for phrases may be inaccurate</span>` : ""}</p>`;
}

const GOOGLE_TOPICS = "translation, break down word/phrase logic, etymology, synonyms, examples";
/** Google search for the word or phrase as written in the list, plus GOOGLE_TOPICS. */
function googleLink(text) {
  const q = `${String(text).split(/\s+/).filter(Boolean).join(" ")} ${GOOGLE_TOPICS}`;
  return `<p><a href="https://www.google.com/search?q=${encodeURIComponent(q)}" target="_blank" rel="noopener">🔎 Search on Google (translation, word logic, etymology, synonyms, examples)</a></p>`;
}

let ROWS = [];
const N_OPTIONS = ["5", "10", "20", "All"];
let S = { h: [], t: [], n: "5" };
try { Object.assign(S, JSON.parse(localStorage.getItem("nnp-settings") || "{}")); } catch (e) { /* ignore */ }
const save = () => { try { localStorage.setItem("nnp-settings", JSON.stringify(S)); } catch (e) { /* ignore */ } };
let deckNl = [], deckEn = [];
let dir = location.hash === "#en" ? "en" : "nl";   // which tab: Dutch -> English or English -> Dutch

function matching() {
  return ROWS.filter((r) => (!S.h.length || S.h.includes(r.h)) && (!S.t.length || S.t.includes(r.t)));
}
function newSet() {
  const m = matching();
  const n = S.n === "All" ? m.length : Math.min(+S.n, m.length);
  deckNl = shuffle(m.slice()).slice(0, n);
  deckEn = shuffle(m.slice()).slice(0, n);   // the English -> Dutch tab gets its own selection
  render();
}

function card(r) {
  const el = document.createElement("article");
  el.className = "card";
  const en = dir === "en";
  // English -> Dutch: the English example sentence goes on the front as context
  // (only once: it is not repeated in the answer).
  el.innerHTML = `<div class="card-head"><h3>${esc(en ? r.en : r.nl)}</h3><span class="meta">H${r.h} · T${r.t}</span></div>
    ${en ? `<p class="caption"><em>e.g. ${esc(r.ex_en)}</em></p>` : ""}
    <button class="btn toggle primary">Show answer</button>
    <div class="answer" hidden>
      <p><strong>${en ? "Dutch" : "English"}:</strong> ${esc(en ? r.nl : r.en)}</p>
      <p><strong>Voorbeeldzin:</strong> ${esc(r.ex)}</p>
      ${en ? "" : `<p class="ex-en"><em>${esc(r.ex_en)}</em></p>`}
      ${youglishLink(r.nl)}
      ${googleLink(r.nl)}
    </div>`;
  const btn = el.querySelector(".toggle"), ans = el.querySelector(".answer");
  el._set = (v) => { ans.hidden = !v; btn.textContent = v ? "Hide answer" : "Show answer"; btn.classList.toggle("primary", !v); };
  btn.onclick = () => el._set(ans.hidden);
  return el;
}

function render() {
  const out = $("#out");
  const total = matching().length;
  const deck = dir === "en" ? deckEn : deckNl;
  out.innerHTML = `<p class="caption">Showing ${deck.length} of ${total} matching entries${dir === "en" ? " · read the English meaning and think of the Dutch word or phrase" : ""}.</p>`;
  if (!deck.length) { out.insertAdjacentHTML("beforeend", `<div class="notice warn-box">No words match these filters.</div>`); return; }
  const bar = document.createElement("div"); bar.className = "toolbar";
  bar.innerHTML = `<button class="btn">🔀 New set</button><button class="btn">Show all</button><button class="btn">Hide all</button>`;
  out.appendChild(bar);
  const grid = document.createElement("div"); grid.className = "cards";
  const cards = deck.map(card); cards.forEach((c) => grid.appendChild(c));
  out.appendChild(grid);
  const [a, b, c] = bar.querySelectorAll("button");
  a.onclick = newSet; b.onclick = () => cards.forEach((x) => x._set(true)); c.onclick = () => cards.forEach((x) => x._set(false));
  const n = (S.h.length ? 1 : 0) + (S.t.length ? 1 : 0);
  $("#filterCount").hidden = !n; $("#filterCount").textContent = `${n} filter${n > 1 ? "s" : ""}`;
}

function chips(id, key, values, single = false, label = (v) => v) {
  const box = $(id); box.innerHTML = "";
  for (const v of values) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "chip"; b.textContent = label(v);
    const on = () => single ? S[key] === v : S[key].includes(v);
    b.setAttribute("aria-pressed", on());
    b.onclick = () => {
      if (single) S[key] = v;
      else S[key] = S[key].includes(v) ? S[key].filter((x) => x !== v) : [...S[key], v];
      box.querySelectorAll(".chip").forEach((c, i) => c.setAttribute("aria-pressed", single ? S[key] === values[i] : S[key].includes(values[i])));
      save(); newSet();
    };
    box.appendChild(b);
  }
}
const uniq = (k) => [...new Set(ROWS.map((r) => r[k]))].sort((a, b) => a - b);
function buildFilters() {
  chips("#f-h", "h", uniq("h"), false, (v) => `Hoofdstuk ${v}`);
  chips("#f-t", "t", uniq("t"), false, (v) => `Tekst ${v}`);
  chips("#f-n", "n", N_OPTIONS, true);
}
function showTab(d, draw = true) {
  dir = d;
  document.querySelectorAll(".tabs button").forEach((b) => b.setAttribute("aria-selected", b.dataset.dir === d));
  try { history.replaceState(null, "", d === "en" ? "#en" : "#nl"); } catch (e) { /* ignore */ }
  if (draw) { render(); window.scrollTo({ top: 0 }); }
}
function openSettings(open) {
  $("#settings").classList.toggle("open", open);
  $("#backdrop").hidden = !open;
  $("#menuBtn").setAttribute("aria-expanded", open);
}

fetch("data/words.json").then((r) => r.json()).then((rows) => {
  ROWS = rows;
  S.h = S.h.filter((v) => rows.some((r) => r.h === v)); S.t = S.t.filter((v) => rows.some((r) => r.t === v));
  if (!N_OPTIONS.includes(S.n)) S.n = "5";
  $("#loading").hidden = true;
  buildFilters();
  $("#menuBtn").onclick = () => openSettings(true);
  $("#closeSettings").onclick = $("#backdrop").onclick = $("#applySettings").onclick = () => openSettings(false);
  $("#resetFilters").onclick = () => { S = { h: [], t: [], n: "5" }; save(); buildFilters(); newSet(); };
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") openSettings(false); });
  document.querySelectorAll(".tabs button").forEach((b) => { b.onclick = () => showTab(b.dataset.dir); });
  showTab(dir, false);
  newSet();
}).catch(() => { $("#loading").textContent = "Could not load the word list. Check your connection and reload."; });

if ("serviceWorker" in navigator) window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
