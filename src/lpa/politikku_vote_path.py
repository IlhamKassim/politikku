"""Civic vote-path walkthrough in the scrollcraft register.

Decisions recorded from Ilham on 2026-09-13, after the Act 1 HITL samples:

- Register: scrollcraft (Sample B), not learn-prose.
- Route: ``/learn/how-a-vote-works/`` and ``/ms/learn/how-a-vote-works/``.
- Four plays, not six essays: place, win one Seat, build a Majority,
  pass one Bill. Extra “why” sits behind a tap. The compass is optional
  after the finish.
- "Why they did it" is allowed when a source says why. We attribute. We do
  not invent a motive in this site's own voice.
- Year boards (GE13–GE15) sit on the Majority play. The house tool is
  client-side only, not a live feed of today's Dewan Rakyat.
- Always teach the exclusion: Kuala Lumpur, Labuan, and Putrajaya have no DUN.

Parent map: #192. Copy ticket: #195.
"""

from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path

from lpa.coalition_colors import party_color
from lpa.config import load_election_status
from lpa.domain import ElectionStatus
from lpa.politikku_shell import Language, render_shell, t
from lpa.politikku_vote_path_plays import body_en, body_ms

PAGE_PATH = "learn/how-a-vote-works/"

_CHART_COLORS = {code: party_color(code) for code in ("PH", "PN", "BN", "GPS", "GRS", "OTHER")}
MAJORITY_SEATS = 112
DEWAN_SEATS = 222


def _claim(claim_id: str, cite: str, text: str) -> str:
    return (
        f'<span data-claim id="{escape(claim_id, quote=True)}" '
        f'data-cite="{escape(cite, quote=True)}">{escape(text)}</span>'
    )


def _stack_bar(segments: tuple[tuple[str, int, str], ...]) -> str:
    parts: list[str] = []
    for label, seats, color in segments:
        if seats <= 0:
            continue
        width = 100 * seats / DEWAN_SEATS
        parts.append(
            f'<span class="stack-seg" style="width:{width:.2f}%;background:{color}" '
            f'title="{label} {seats}"></span>'
        )
    tick = 100 * MAJORITY_SEATS / DEWAN_SEATS
    return (
        f'<div class="stack-bar" role="img" '
        f'aria-label="Seat bars for {DEWAN_SEATS} Seats, Majority at {MAJORITY_SEATS}">'
        f"{''.join(parts)}"
        f'<i class="majority-tick" style="left:{tick:.2f}%"></i>'
        f"</div>"
    )


_SCROLL_CSS = """
  .pk-scroll-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 14px var(--gutter-mobile);
    border-bottom: 1px solid var(--line-soft);
  }
  @media (min-width: 900px) {
    .pk-scroll-head { padding: 16px var(--gutter-desktop); }
  }
  .pk-scroll-brand {
    font-family: var(--font-display);
    letter-spacing: -.02em;
    color: inherit;
    text-decoration: none;
    font-size: 18px;
  }
  .pk-scroll-brand small {
    display: block;
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--ink-secondary);
    margin-top: 2px;
  }
  .pk-scroll-tools {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: flex-end;
  }
  .pk-scroll-tools a.pk-scroll-home {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--accent);
    text-decoration: none;
  }
  .pk-scroll {
    max-width: 1080px;
    margin: 0 auto;
    padding: 28px var(--gutter-mobile) 96px;
  }
  @media (min-width: 900px) {
    .pk-scroll { padding: 40px var(--gutter-desktop) 120px; }
  }
  .act-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 0 0 8px;
  }
  .act-nav a {
    display: inline-flex;
    align-items: center;
    min-height: 44px;
    padding: 4px 12px;
    border: 1px solid var(--line);
    border-radius: var(--radius-sm);
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .04em;
    color: var(--ink-secondary);
    text-decoration: none;
  }
  .act-nav a:hover { color: var(--ink); border-color: var(--ink-secondary); }
  .scene {
    min-height: 0;
    display: grid;
    align-content: start;
    padding: 36px 0;
    border-top: 1px solid var(--line-soft);
  }
  .scene:first-of-type { border-top: 0; min-height: 58vh; }
  .scene .pk-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--ink-secondary);
  }
  .scene h1, .scene h2 {
    font-family: var(--font-display);
    font-weight: 500;
    letter-spacing: -.03em;
    margin: 12px 0 0;
    max-width: 18ch;
  }
  .scene h1 { font-size: clamp(44px, 8vw, 84px); line-height: 1.02; }
  .scene h2 { font-size: clamp(32px, 5vw, 56px); line-height: 1.08; }
  .scene .line {
    font-size: clamp(18px, 2.2vw, 24px);
    line-height: 1.45;
    max-width: 32ch;
    color: var(--ink-secondary);
    margin: 18px 0 0;
  }
  .scene .prose-claim, .scene .more {
    font-size: 16px;
    line-height: 1.55;
    max-width: 62ch;
    color: var(--ink);
    margin: 22px 0 0;
  }
  .scene .more { color: var(--ink-secondary); }
  .scene .more a {
    color: inherit;
    border-bottom: 1px solid var(--line);
    text-decoration: none;
  }
  .place-track, .chamber-grid, .split {
    margin-top: 36px;
    display: grid;
    gap: 14px;
  }
  .place-track { max-width: 420px; gap: 10px; }
  .place-step, .split-card, .why {
    padding: 18px 20px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
  }
  .place-step {
    display: flex;
    align-items: center;
    gap: 14px;
    min-height: 52px;
    padding: 12px 16px;
  }
  .place-step b, .split-card .tag, .why .tag {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--accent);
  }
  .place-step b { width: 4.5rem; flex: 0 0 auto; }
  .split, .chamber-grid { grid-template-columns: 1fr 1fr; }
  .split-card { min-height: 168px; }
  .split-card h3, .why h3 {
    font-size: 26px;
    letter-spacing: -.02em;
    margin: 10px 0 8px;
  }
  .split-card p, .why p {
    color: var(--ink-secondary);
    font-size: 15px;
    line-height: 1.5;
    margin: 0;
  }
  .why { margin-top: 22px; max-width: 62ch; }
  .caveat {
    margin-top: 16px;
    padding: 16px 18px;
    border-left: 3px solid var(--caution);
    background: var(--caution-bg);
    color: var(--ink);
    font-size: 15px;
    line-height: 1.5;
    max-width: 62ch;
  }
  .long-scene { min-height: 0; align-content: start; }
  .stack { display: grid; gap: 14px; margin-top: 28px; max-width: 68ch; }
  .stack article {
    padding: 20px 22px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
  }
  .stack h3 {
    font-size: 22px;
    letter-spacing: -.02em;
    margin: 6px 0 10px;
  }
  .stack p { margin: 0 0 0.8em; color: var(--ink); line-height: 1.55; font-size: 15.5px; }
  .stack p:last-child { margin-bottom: 0; }
  @media (max-width: 720px) {
    .split, .chamber-grid { grid-template-columns: 1fr; }
    .scene { min-height: 0; padding: 36px 0; }
    .pk-scroll-head { flex-wrap: wrap; }
  }
  @media (prefers-reduced-motion: reduce) {
    .scene { min-height: 0; }
  }
  .year-charts, .compass-panel, .vote-sim {
    margin-top: 28px;
    display: grid;
    gap: 16px;
  }
  .year-card, .compass-panel, .vote-sim {
    padding: 20px 20px 18px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
  }
  .year-card h3, .compass-panel h3, .vote-sim h3 {
    font-size: 22px;
    letter-spacing: -.02em;
    margin: 8px 0 12px;
  }
  .stack-bar {
    position: relative;
    display: flex;
    height: 36px;
    overflow: hidden;
    border: 1px solid var(--line);
    background: var(--paper);
  }
  .stack-seg { display: block; height: 100%; }
  .stack-bar > .majority-tick {
    position: absolute;
    top: -3px;
    bottom: -3px;
    width: 2px;
    background: var(--caution);
    pointer-events: none;
  }
  .bar-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 16px;
    list-style: none;
    padding: 12px 0 0;
    margin: 0;
    font-size: 13px;
    color: var(--ink-secondary);
  }
  .bar-legend li { display: inline-flex; align-items: center; gap: 8px; }
  .bar-legend b { color: var(--ink); font-weight: 500; }
  .swatch {
    width: 10px;
    height: 10px;
    border-radius: 2px;
    display: inline-block;
  }
  .majority-note {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--caution);
    margin: 10px 0 0;
  }
  .compass-board {
    position: relative;
    width: min(100%, 440px);
    aspect-ratio: 1;
    margin: 8px auto 0;
    border: 1px solid var(--line);
    background:
      linear-gradient(to right, transparent 49.6%, var(--line) 49.6%, var(--line) 50.4%, transparent 50.4%),
      linear-gradient(to bottom, transparent 49.6%, var(--line) 49.6%, var(--line) 50.4%, transparent 50.4%),
      var(--paper);
    cursor: crosshair;
  }
  .compass-label {
    position: absolute;
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--ink-secondary);
  }
  .compass-label.left { left: 10px; top: 50%; transform: translateY(-50%); }
  .compass-label.right { right: 10px; top: 50%; transform: translateY(-50%); }
  .compass-label.top { top: 8px; left: 50%; transform: translateX(-50%); }
  .compass-label.bottom { bottom: 8px; left: 50%; transform: translateX(-50%); }
  .compass-dot, .compass-you {
    position: absolute;
    width: 30px;
    height: 30px;
    margin: -15px 0 0 -15px;
    border-radius: 50%;
    border: 2px solid var(--paper);
    font-family: var(--mono);
    font-size: 10px;
    display: grid;
    place-items: center;
    color: #fff;
    font-weight: 600;
  }
  .compass-dot[data-c="PH"] { left: 30%; top: 34%; background: var(--vote-ph); }
  .compass-dot[data-c="BN"] { left: 58%; top: 36%; background: var(--vote-bn); }
  .compass-dot[data-c="PN"] { left: 82%; top: 30%; background: var(--vote-pn); }
  .compass-dot[data-c="GPS"] { left: 62%; top: 70%; background: var(--vote-gps); }
  .compass-dot[data-c="GRS"] { left: 42%; top: 78%; background: var(--vote-grs); }
  .compass-you {
    background: var(--accent);
    color: #102018;
    border-color: var(--ink);
    z-index: 2;
    width: 36px;
    height: 36px;
    margin: -18px 0 0 -18px;
  }
  .compass-tools {
    display: grid;
    gap: 10px;
    margin-top: 16px;
    max-width: 440px;
  }
  .compass-tools label {
    display: grid;
    gap: 4px;
    font-size: 13px;
    color: var(--ink-secondary);
  }
  .compass-legend { margin-top: 8px; }
  .sim-presets, .sim-rows { display: flex; flex-wrap: wrap; gap: 8px; }
  .sim-presets button, .sim-step, .sim-row input[type="number"] {
    min-height: 44px;
    border: 1px solid var(--line);
    background: var(--paper);
    color: var(--ink);
    font: inherit;
  }
  .sim-presets button, .sim-step { padding: 0 12px; cursor: pointer; }
  .sim-row {
    display: grid;
    grid-template-columns: 4.5rem 44px 4.5rem 44px auto;
    align-items: center;
    gap: 8px;
    width: min(100%, 420px);
  }
  .sim-row input[type="number"] { width: 4.5rem; text-align: center; }
  .sim-gov {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--ink-secondary);
  }
  .sim-status {
    margin-top: 14px;
    padding: 14px 16px;
    border-left: 3px solid var(--line);
    background: var(--paper);
    font-size: 15px;
    line-height: 1.5;
  }
  .sim-status[data-state="pass"] { border-left-color: var(--accent); }
  .sim-status[data-state="hung"] { border-left-color: var(--caution); }
  .sim-status[data-state="warn"] { border-left-color: var(--line-strong); }
  .sim-chamber {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
    margin-top: 16px;
    max-width: 520px;
  }
  .sim-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: block;
  }
  .sim-meta {
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .04em;
    color: var(--ink-secondary);
    margin: 10px 0 0;
  }
  .why-tap {
    margin-top: 16px;
    max-width: 62ch;
    border: 1px solid var(--line);
    background: var(--paper-alt);
    padding: 12px 16px;
  }
  .why-tap summary {
    cursor: pointer;
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: var(--accent);
    min-height: 44px;
    display: flex;
    align-items: center;
  }
  .why-tap p { margin: 10px 0 0; color: var(--ink-secondary); font-size: 15px; line-height: 1.5; }
  .race, .bill-play, .vote-sim, .compass-panel {
    margin-top: 22px;
    padding: 20px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
  }
  .race-picks { display: grid; gap: 10px; margin-top: 14px; max-width: 420px; }
  .race-picks button, .sim-presets button {
    min-height: 48px;
    padding: 0 14px;
    border: 1px solid var(--line);
    background: var(--paper);
    color: var(--ink);
    font: inherit;
    text-align: left;
    cursor: pointer;
  }
  .race-picks button[data-on="true"] { border-color: var(--accent); }
  .sim-rows { display: grid; gap: 8px; margin-top: 16px; max-width: 440px; }
  .sim-choice {
    display: grid;
    grid-template-columns: 7rem 3.5rem 1fr;
    align-items: center;
    gap: 10px;
    min-height: 44px;
  }
  .sim-choice[hidden] { display: none; }
  .sim-choice b { font-family: var(--mono); font-size: 13px; }
  .bill-play {
    padding: 0;
    border: 0;
    background: transparent;
    max-width: 66ch;
  }
  .bill-play > .more, .bill-play > .caveat { margin-top: 12px; max-width: 62ch; }
  .bill-path {
    display: flex;
    flex-wrap: wrap;
    gap: 0;
    list-style: none;
    padding: 0;
    margin: 16px 0 0;
  }
  .bill-path li {
    min-height: 36px;
    padding: 8px 10px;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--ink-secondary);
    border-bottom: 2px solid transparent;
  }
  .bill-path li[data-on="true"] {
    color: var(--ink);
    border-bottom-color: var(--accent);
  }
  .bill-window {
    margin-top: 14px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
    color: var(--ink);
    display: flex;
    flex-direction: column;
    min-height: 0;
  }
  .bill-stage {
    padding: 18px 16px 8px;
    max-width: 62ch;
    flex: 1 1 auto;
    scroll-margin-bottom: 140px;
  }
  .bill-stage h3 {
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 14px;
  }
  .bill-stage:focus { outline: none; }
  .bill-stage:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; }
  html.js-ready .bill-stage:not(.is-on) { display: none; }
  .bill-speech {
    margin: 0 0 16px;
    padding: 0;
  }
  .bill-speech figcaption {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 6px;
  }
  .bill-speech blockquote {
    margin: 0;
    padding: 12px 14px;
    border-left: 3px solid var(--accent);
    background: #101e23;
  }
  .bill-speech p { margin: 0; font-size: 16px; line-height: 1.5; }
  .bill-note, .bill-stage .more, .bill-stage .prose-claim {
    margin: 12px 0 0;
    font-size: 15px;
    line-height: 1.5;
    color: var(--ink-secondary);
  }
  .bill-choices { margin: 10px 0 0; padding-left: 1.2em; }
  .div-floor {
    margin-top: 16px;
    padding: 14px;
    background: #101e23;
    border: 1px solid var(--line);
  }
  .div-floor[data-split="false"] .div-yes,
  .div-floor[data-split="false"] .div-no,
  .div-floor[data-split="false"] .div-mark { display: none; }
  .div-floor[data-split="true"] .div-pool { display: none; }
  .div-floor[data-split="true"] {
    display: grid;
    grid-template-columns: 1fr 8px 1fr;
    gap: 12px;
    align-items: start;
  }
  .div-floor p {
    margin: 0 0 8px;
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .08em;
    text-transform: uppercase;
  }
  .div-mark {
    width: 8px;
    min-height: 80px;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .div-mark span {
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .12em;
    color: #101e23;
  }
  .div-floor .sim-chamber { margin-top: 0; max-width: none; }
  .div-live {
    margin: 10px 0 0;
    font-size: 15px;
    line-height: 1.45;
  }
  .bill-dock {
    display: none;
    flex-wrap: wrap;
    gap: 10px;
    padding: 10px 16px 16px;
    background: var(--paper-alt);
    border-top: 1px solid var(--line);
  }
  html.js-ready .bill-dock { display: flex; }
  .bill-continue, .bill-alt {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: min(240px, 92%);
    min-height: 48px;
    padding: 10px 14px;
    border: 0;
    font: inherit;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    text-align: center;
    line-height: 1.25;
    white-space: normal;
    cursor: pointer;
  }
  .bill-continue {
    background: var(--accent);
    color: #101e23;
  }
  .bill-alt {
    background: transparent;
    color: var(--ink);
    border: 1px solid var(--line);
  }
  .bill-continue[hidden], .bill-alt[hidden] { display: none; }
  @media (max-width: 700px) {
    .div-floor[data-split="true"] { grid-template-columns: 1fr; }
    .div-mark { width: 100%; min-height: 0; padding: 6px 0; }
    .div-mark span { writing-mode: horizontal-tb; transform: none; }
  }
  @media (prefers-reduced-motion: reduce) {
    .sim-dot, .div-floor, .bill-stage { transition: none; }
  }
  .finish {
    margin-top: 18px;
    padding: 16px 18px;
    border-left: 3px solid var(--accent);
    background: var(--positive-bg);
    max-width: 62ch;
  }
  .journey-next {
    margin-top: 20px;
    padding: 18px 20px;
    max-width: 62ch;
    border: 1px solid var(--line);
    background: var(--paper-alt);
  }
  .journey-next .pk-eyebrow { color: var(--accent); }
  .journey-next h3 {
    margin: 8px 0 6px;
    font-size: 22px;
    line-height: 1.25;
  }
  .journey-next h3 a { color: var(--ink); text-decoration: none; }
  .journey-next h3 a:hover { color: var(--accent); }
  .journey-next p {
    margin: 0;
    max-width: 58ch;
    color: var(--ink-secondary);
    font-size: 15px;
    line-height: 1.5;
  }
  .journey-links {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 16px;
    margin-top: 14px;
  }
  .journey-links a {
    display: inline-flex;
    align-items: center;
    min-height: 44px;
    color: var(--accent);
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .04em;
    text-decoration: none;
  }
  .journey-links a:hover { text-decoration: underline; text-underline-offset: 4px; }
""".strip()


def _body_en() -> str:
    return body_en(_claim, _stack_bar, _CHART_COLORS)


def _body_ms() -> str:
    return body_ms(_claim, _stack_bar, _CHART_COLORS)


def build_vote_path_page(language: Language, updated_at: date, status: ElectionStatus) -> str:
    return render_shell(
        title=t(
            language,
            "How a vote works | PolitikKu",
            "Ke mana undi pergi | PolitikKu",
        ),
        description=t(
            language,
            "Four short plays for a first-time voter: your place, one Seat, a Majority, then one Bill.",
            "Empat permainan pendek untuk pengundi kali pertama: tempat anda, satu Kerusi, suatu Majoriti, kemudian satu Rang Undang-Undang.",
        ),
        active_nav="vote-path",
        language=language,
        page_path=PAGE_PATH,
        updated_at=updated_at,
        sources_count=0,
        status=status,
        body_html=(
            f"<style>{_SCROLL_CSS}</style>\n"
            f"{t(language, _body_en(), _body_ms())}\n"
            '<script src="/learn/vote-path.js" defer></script>'
        ),
    )


def write_vote_path_pages(*, output_dir: str = "public") -> list[Path]:
    status = load_election_status()
    today = date.today()  # noqa: DTZ011
    written: list[Path] = []
    for language, dest in (
        (Language.EN, Path(output_dir) / "learn" / "how-a-vote-works"),
        (Language.MS, Path(output_dir) / "ms" / "learn" / "how-a-vote-works"),
    ):
        dest.mkdir(parents=True, exist_ok=True)
        path = dest / "index.html"
        path.write_text(build_vote_path_page(language, today, status), encoding="utf-8")
        written.append(path)
    return written
