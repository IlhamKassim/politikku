"""Civic vote-path walkthrough in the scrollcraft register.

Decisions recorded from Ilham on 2026-09-13, after the Act 1 HITL samples:

- Register: scrollcraft (Sample B), not learn-prose.
- Route: ``/learn/how-a-vote-works/`` and ``/ms/learn/how-a-vote-works/``.
- Six acts. Act 6 is the long closer — YDPA and Dewan Negara get real space.
- "Why they did it" is allowed when a source says why. We attribute. We do
  not invent a motive in this site's own voice.
- On this page, after Act 4: year-by-year Seat charts (GE13–GE15, named
  as the blocs that contested that year), a sourced political compass
  (Wikipedia positions, not invented x/y scores), and a client-side
  Dewan Rakyat simulator (222 Seats, Majority at 112). The simulator is
  a teaching tool, not a live feed of today's house.
- Always teach the exclusion: Kuala Lumpur, Labuan, and Putrajaya have no DUN.

Parent map: #192. Copy ticket: #195.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from lpa.config import load_election_status
from lpa.domain import ElectionStatus
from lpa.politikku_shell import Language, landing_url, render_shell, route, t

PAGE_PATH = "learn/how-a-vote-works/"

CONTEXT_MD = "https://raw.githubusercontent.com/IlhamKassim/live-political-analysis/main/CONTEXT.md"
PARLIAMENT_WIKI = "https://en.wikipedia.org/wiki/Parliament_of_Malaysia?action=raw"
POLITICS_WIKI = "https://en.wikipedia.org/wiki/Politics_of_Malaysia?action=raw"
DUN_WIKI = "https://en.wikipedia.org/wiki/Dewan_Undangan_Negeri?action=raw"
STATES_WIKI = "https://en.wikipedia.org/wiki/States_and_federal_territories_of_Malaysia?action=raw"
ELECTIONS_WIKI = "https://en.wikipedia.org/wiki/Elections_in_Malaysia?action=raw"
GE13_WIKI = "https://en.wikipedia.org/wiki/2013_Malaysian_general_election?action=raw"
GE14_WIKI = "https://en.wikipedia.org/wiki/2018_Malaysian_general_election?action=raw"
GE15_WIKI = "https://en.wikipedia.org/wiki/2022_Malaysian_general_election?action=raw"
PH_WIKI = "https://en.wikipedia.org/wiki/Pakatan_Harapan?action=raw"
PN_WIKI = "https://en.wikipedia.org/wiki/Perikatan_Nasional?action=raw"
BN_WIKI = "https://en.wikipedia.org/wiki/Barisan_Nasional?action=raw"
GPS_WIKI = "https://en.wikipedia.org/wiki/Gabungan_Parti_Sarawak?action=raw"
GRS_WIKI = "https://en.wikipedia.org/wiki/Gabungan_Rakyat_Sabah?action=raw"

_CHART_COLORS = {
    "PH": "#d7263d",
    "PN": "#15387c",
    "BN": "#1f9bd6",
    "GPS": "#b8332e",
    "GRS": "#e8772e",
    "WARISAN": "#16a085",
    "PR": "#6b3fa0",
    "GS": "#008900",
    "OTHER": "#5d6b7d",
}
MAJORITY_SEATS = 112
DEWAN_SEATS = 222


def _claim(claim_id: str, cite: str, text: str) -> str:
    return f'<span data-claim id="{claim_id}" data-cite="{cite}">{text}</span>'


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


def _legend_row(label: str, seats: int, color: str) -> str:
    return (
        f'<li><i class="swatch" style="background:{color}"></i>'
        f"<b>{label}</b> <span>{seats}</span></li>"
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
    min-height: 72vh;
    display: grid;
    align-content: center;
    padding: 48px 0;
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
  .majority-tick {
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
  .compass-dot[data-c="PH"] { left: 30%; top: 34%; background: #d7263d; }
  .compass-dot[data-c="BN"] { left: 58%; top: 36%; background: #1f9bd6; }
  .compass-dot[data-c="PN"] { left: 82%; top: 30%; background: #15387c; }
  .compass-dot[data-c="GPS"] { left: 62%; top: 78%; background: #b8332e; }
  .compass-dot[data-c="GRS"] { left: 48%; top: 84%; background: #e8772e; }
  .compass-you {
    background: var(--accent);
    color: #102018;
    border-color: var(--ink);
    z-index: 2;
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
""".strip()


def _header(language: Language) -> str:
    home = landing_url(language)
    en_href = route(Language.EN, PAGE_PATH)
    ms_href = route(Language.MS, PAGE_PATH)
    en_on = ' class="on"' if language is Language.EN else ""
    ms_on = ' class="on"' if language is Language.MS else ""
    en_cur = ' aria-current="page"' if language is Language.EN else ""
    ms_cur = ' aria-current="page"' if language is Language.MS else ""
    title = t(language, "How a vote works", "Ke mana undi pergi")
    find = t(language, "Find your Seat", "Cari kerusi anda")
    return f"""<header class="pk-scroll-head">
  <a class="pk-scroll-brand" href="{home}">PolitikKu<small>{title}</small></a>
  <div class="pk-scroll-tools">
    <div class="seg lang-seg sb-lang" role="group" aria-label="{t(language, "Language", "Bahasa")}">
      <a{en_on} href="{en_href}"{en_cur} data-pk-set-lang="en">EN</a>
      <a{ms_on} href="{ms_href}"{ms_cur} data-pk-set-lang="ms">BM</a>
    </div>
    <a class="pk-scroll-home" href="{home}">{find}</a>
  </div>
</header>"""


def _body_en() -> str:
    c = {
        "seat-unit": _claim(
            "claim-seat-unit",
            CONTEXT_MD,
            "A Seat is one of the 222 parliamentary constituencies in the "
            "Dewan Rakyat — the unit an election is actually won or lost in.",
        ),
        "seat-222": _claim(
            "claim-222",
            CONTEXT_MD,
            "The Dewan Rakyat has 222 Seats.",
        ),
        "street": _claim(
            "claim-street-in-seat",
            CONTEXT_MD,
            "A Malaysian postcode maps to every Seat it could fall in, and a "
            "postcode can straddle two Seats.",
        ),
        "thirteen": _claim(
            "claim-thirteen-states",
            STATES_WIKI,
            "Malaysia is a federation of thirteen states and three federal territories.",
        ),
        "each-state-dun": _claim(
            "claim-each-state-dun",
            STATES_WIKI,
            "Each state also has a Westminster-style unicameral legislature "
            "called the Dewan Undangan Negeri (DUN).",
        ),
        "dun": _claim(
            "claim-dun-is-state-assembly",
            DUN_WIKI,
            "A Dewan Undangan Negeri is a state legislative assembly.",
        ),
        "two-rolls": _claim(
            "claim-two-rolls",
            ELECTIONS_WIKI,
            "Federal elections elect members of the Dewan Rakyat, while state "
            "elections in each of the 13 states elect members of their "
            "respective state legislative assembly.",
        ),
        "ft-names": _claim(
            "claim-ft-names",
            STATES_WIKI,
            "The three federal territories—Kuala Lumpur, Labuan and "
            "Putrajaya—were created later from land separated from existing "
            "states.",
        ),
        "ft-direct": _claim(
            "claim-ft-direct",
            STATES_WIKI,
            "The federal territories are directly governed by the federal government.",
        ),
        "ft-no-subnational": _claim(
            "claim-ft-no-subnational",
            STATES_WIKI,
            "There are no subnational elections in the federal territories.",
        ),
        "state-power": _claim(
            "claim-state-legislature",
            POLITICS_WIKI,
            "Legislative power is vested in the federal parliament and the 13 state assemblies.",
        ),
        "fptp": _claim(
            "claim-fptp",
            PARLIAMENT_WIKI,
            "The Dewan Rakyat consists of 222 members of Parliament (MPs) "
            "elected from single-member constituencies drawn based on "
            "population in a general election using the first-past-the-post "
            "system.",
        ),
        "westminster": _claim(
            "claim-westminster",
            POLITICS_WIKI,
            "The system of government in Malaysia is closely modelled on that "
            "of the Westminster parliamentary system, a legacy of British "
            "colonial rule.",
        ),
        "majority": _claim(
            "claim-majority",
            CONTEXT_MD,
            "A Majority means holding more than half of the 222 seats (112+).",
        ),
        "coalitions": _claim(
            "claim-coalitions",
            CONTEXT_MD,
            "The five Coalitions this site tracks are PH, BN, PN, GPS and GRS.",
        ),
        "gov-coalition": _claim(
            "claim-gov-coalition",
            CONTEXT_MD,
            "The Government Coalition, the current governing bloc, is PH + BN "
            "+ GPS + GRS plus minor parties.",
        ),
        "non-gov": _claim(
            "claim-non-government",
            CONTEXT_MD,
            "Non-government means every Seat or Coalition outside the Government Coalition.",
        ),
        "hung": _claim(
            "claim-hung-ge15",
            GE15_WIKI,
            "The 2022 general election resulted in a hung parliament, the "
            "first federal election to have had such a result in the nation's "
            "history.",
        ),
        "hung-why": _claim(
            "claim-hung-form",
            GE15_WIKI,
            "In the event of a hung parliament, where no single party obtains "
            "the majority of seats, the government may still form through a "
            "coalition.",
        ),
        "anwar-sworn": _claim(
            "claim-anwar-sworn",
            GE15_WIKI,
            "Anwar Ibrahim was appointed and sworn in as prime minister on 24 "
            "November 2022 by the Yang di-Pertuan Agong.",
        ),
        "confidence": _claim(
            "claim-confidence",
            GE15_WIKI,
            "The head of government is the person who commands the confidence "
            "of the majority of members in the respective legislature.",
        ),
        "bill": _claim(
            "claim-bill",
            CONTEXT_MD,
            "A Bill is a piece of legislation before the Dewan Rakyat.",
        ),
        "division": _claim(
            "claim-division",
            CONTEXT_MD,
            "A Division is a counted vote in the Dewan Rakyat, in which "
            "Hansard names every Member as agreeing, disagreeing, abstaining "
            "or absent.",
        ),
        "parliament-houses": _claim(
            "claim-parliament-houses",
            PARLIAMENT_WIKI,
            "The bicameral parliament consists of the Dewan Rakyat and the Dewan Negara.",
        ),
        "parliament-ydpa": _claim(
            "claim-parliament-ydpa",
            PARLIAMENT_WIKI,
            "The Yang di-Pertuan Agong, as the head of state, is the third "
            "component of Parliament.",
        ),
        "reid": _claim(
            "claim-reid",
            PARLIAMENT_WIKI,
            "The Reid Commission, which drafted the Constitution of Malaya, "
            "modelled the Malayan system of government after the British "
            "system: a bicameral parliament, with one house being directly "
            "elected, and the other having limited powers with some members "
            "being appointed by the King.",
        ),
        "reid-federal": _claim(
            "claim-reid-federal",
            PARLIAMENT_WIKI,
            "In line with the federal nature of the new country, the upper "
            "house would also have members elected by state legislative "
            "assemblies in addition to members appointed by the King.",
        ),
        "senate-70": _claim(
            "claim-senate-70",
            PARLIAMENT_WIKI,
            "The Dewan Negara consists of 70 members (Senators); 26 are "
            "elected by the 13 state assemblies (2 senators per state), 4 are "
            "appointed by the Yang di-Pertuan Agong to represent the 3 "
            "federal territories, and the remaining 40 members are appointed "
            "by the Yang di-Pertuan Agong on the advice of the Prime Minister.",
        ),
        "senate-term": _claim(
            "claim-senate-undissolved",
            PARLIAMENT_WIKI,
            "The dissolution of the Parliament does not affect the Dewan Negara.",
        ),
        "pm-appoint": _claim(
            "claim-pm-appoint",
            PARLIAMENT_WIKI,
            "The Yang di-Pertuan Agong appoints the Prime Minister, who is "
            "the Head of Government, from the Dewan Rakyat.",
        ),
        "pm-practice": _claim(
            "claim-pm-practice",
            PARLIAMENT_WIKI,
            "In practice, the Prime Minister shall be the one who commands "
            "the confidence of the majority of the Dewan Rakyat.",
        ),
        "executive": _claim(
            "claim-executive",
            PARLIAMENT_WIKI,
            "The executive government, comprising the Prime Minister and his "
            "Cabinet, is drawn from the members of Parliament and is "
            "responsible to the Parliament.",
        ),
        "assent": _claim(
            "claim-royal-assent",
            PARLIAMENT_WIKI,
            "If the bill passes, it is presented to the Yang di-Pertuan "
            "Agong, who has 30 days to consider the bill.",
        ),
        "branches": _claim(
            "claim-three-branches",
            POLITICS_WIKI,
            "The hierarchy of authority in Malaysia, in accordance to the "
            "Federal Constitution, stipulates the three branches of the "
            "Malaysian government as consisting of the Executive, Judiciary "
            "and Legislative branch.",
        ),
        "judiciary": _claim(
            "claim-judiciary",
            POLITICS_WIKI,
            "The judiciary is independent of the executive and the legislature.",
        ),
        "ydpa-head": _claim(
            "claim-ydpa-head",
            POLITICS_WIKI,
            "The Yang di-Pertuan Agong is head of state and the Prime "
            "Minister of Malaysia is the head of government.",
        ),
        "ge13-bn-133": _claim(
            "claim-ge13-bn-133",
            GE13_WIKI,
            "Barisan Nasional won 133 seats in the 2013 general election.",
        ),
        "ge13-pr-89": _claim(
            "claim-ge13-pr-89",
            GE13_WIKI,
            "Pakatan Rakyat won 89 of the 222 seats.",
        ),
        "ge13-pr-vote": _claim(
            "claim-ge13-pr-vote",
            GE13_WIKI,
            "The unofficial opposition Pakatan Rakyat coalition led by "
            "Anwar Ibrahim received a majority of the vote, with its three "
            "member parties collectively receiving 50.9% of the vote.",
        ),
        "ge13-bn-vote": _claim(
            "claim-ge13-bn-vote",
            GE13_WIKI,
            "The incumbent governing alliance, Barisan Nasional, received "
            "47.4% of the vote and won 133 seats.",
        ),
        "ge14-ph-113": _claim(
            "claim-ge14-ph-113",
            GE14_WIKI,
            "Pakatan Harapan won 113 seats in the 2018 general election.",
        ),
        "ge14-bn-79": _claim(
            "claim-ge14-bn-79",
            GE14_WIKI,
            "Barisan Nasional won 79 seats in the 2018 general election.",
        ),
        "ge14-gs-18": _claim(
            "claim-ge14-gs-18",
            GE14_WIKI,
            "Gagasan Sejahtera won 18 seats in the 2018 general election.",
        ),
        "ge14-warisan-8": _claim(
            "claim-ge14-warisan-8",
            GE14_WIKI,
            "Warisan won 8 seats in the 2018 general election.",
        ),
        "ge14-majority-112": _claim(
            "claim-ge14-majority-112",
            GE14_WIKI,
            "The 2018 general election required 112 seats for a majority.",
        ),
        "gps-founded": _claim(
            "claim-gps-founded",
            GPS_WIKI,
            "Gabungan Parti Sarawak was founded on 12 June 2018.",
        ),
        "gps-from-bn": _claim(
            "claim-gps-from-bn",
            GPS_WIKI,
            "Gabungan Parti Sarawak was established in 2018 by four former "
            "Barisan Nasional component parties operating solely in Sarawak "
            "following the federal coalition's defeat in the 2018 Malaysian "
            "general election.",
        ),
        "ge15-ph-82": _claim(
            "claim-ge15-ph-82",
            GE15_WIKI,
            "Pakatan Harapan won 82 seats in the 2022 general election, a "
            "figure that includes MUDA.",
        ),
        "ge15-pn-74": _claim(
            "claim-ge15-pn-74",
            GE15_WIKI,
            "Perikatan Nasional won 74 seats in the 2022 general election.",
        ),
        "ge15-bn-30": _claim(
            "claim-ge15-bn-30",
            GE15_WIKI,
            "Barisan Nasional won 30 seats in the 2022 general election.",
        ),
        "ge15-gps-23": _claim(
            "claim-ge15-gps-23",
            GE15_WIKI,
            "Gabungan Parti Sarawak won 23 seats in the 2022 general election.",
        ),
        "ge15-grs-6": _claim(
            "claim-ge15-grs-6",
            GE15_WIKI,
            "Gabungan Rakyat Sabah won 6 seats in the 2022 general election.",
        ),
        "ge15-warisan-3": _claim(
            "claim-ge15-warisan-3",
            GE15_WIKI,
            "Warisan won 3 seats in the 2022 general election.",
        ),
        "ph-founded": _claim(
            "claim-ph-founded",
            PH_WIKI,
            "Pakatan Harapan was founded on 22 September 2015.",
        ),
        "pn-founded": _claim(
            "claim-pn-founded",
            PN_WIKI,
            "Perikatan Nasional was founded on 29 February 2020.",
        ),
        "grs-founded": _claim(
            "claim-grs-founded",
            GRS_WIKI,
            "Gabungan Rakyat Sabah was established in September 2020, when "
            "Hajiji Noor set up an informal alliance of that name.",
        ),
        "ph-position": _claim(
            "claim-ph-position",
            PH_WIKI,
            "Pakatan Harapan's political position is centre to centre-left.",
        ),
        "pn-position": _claim(
            "claim-pn-position",
            PN_WIKI,
            "Perikatan Nasional's political position is right-wing to far-right.",
        ),
        "bn-position": _claim(
            "claim-bn-position",
            BN_WIKI,
            "Barisan Nasional's political position is centre-right to right-wing.",
        ),
        "gps-position": _claim(
            "claim-gps-position",
            GPS_WIKI,
            "Gabungan Parti Sarawak's political position is centre-right to "
            "right-wing.",
        ),
        "gps-sarawak": _claim(
            "claim-gps-sarawak",
            GPS_WIKI,
            "Gabungan Parti Sarawak is a Sarawak-based political alliance in "
            "Malaysia.",
        ),
        "grs-position": _claim(
            "claim-grs-position",
            GRS_WIKI,
            "Gabungan Rakyat Sabah's political position is centre to "
            "centre-right.",
        ),
        "grs-sabah": _claim(
            "claim-grs-sabah",
            GRS_WIKI,
            "Gabungan Rakyat Sabah is a Malaysian coalition of Sabah-based "
            "parties.",
        ),
    }
    ge13_bar = _stack_bar(
        (
            ("BN", 133, _CHART_COLORS["BN"]),
            ("Pakatan Rakyat", 89, _CHART_COLORS["PR"]),
        )
    )
    ge14_bar = _stack_bar(
        (
            ("PH", 113, _CHART_COLORS["PH"]),
            ("BN", 79, _CHART_COLORS["BN"]),
            ("Gagasan Sejahtera", 18, _CHART_COLORS["GS"]),
            ("WARISAN", 8, _CHART_COLORS["WARISAN"]),
            ("Others", 4, _CHART_COLORS["OTHER"]),
        )
    )
    ge15_bar = _stack_bar(
        (
            ("PH", 82, _CHART_COLORS["PH"]),
            ("PN", 74, _CHART_COLORS["PN"]),
            ("BN", 30, _CHART_COLORS["BN"]),
            ("GPS", 23, _CHART_COLORS["GPS"]),
            ("GRS", 6, _CHART_COLORS["GRS"]),
            ("WARISAN", 3, _CHART_COLORS["WARISAN"]),
            ("Others", 4, _CHART_COLORS["OTHER"]),
        )
    )
    return f"""
<div class="pk-scroll">
  <nav class="act-nav" aria-label="Acts">
    <a href="#act-1">1 · Place</a>
    <a href="#act-2">2 · Person</a>
    <a href="#act-3">3 · Seat</a>
    <a href="#act-4">4 · Government</a>
    <a href="#act-4-years">Seats by year</a>
    <a href="#act-4-compass">Compass</a>
    <a href="#act-5">5 · Work</a>
    <a href="#vote-sim">House</a>
    <a href="#act-6">6 · Above this</a>
  </nav>

  <section class="scene" id="open">
    <div class="pk-eyebrow">A walkthrough for a first-time voter</div>
    <h1>Where does a vote go?</h1>
    <p class="line">Not into the whole country at once. Into a place, then a chamber, then a government.</p>
  </section>

  <section class="scene" id="act-1">
    <div class="pk-eyebrow">01 · You vote in a place</div>
    <h2>One street. One federal Seat.</h2>
    <p class="prose-claim">
      {c["seat-unit"]}
      {c["seat-222"]}
      {c["street"]}
      The home-page lookup uses that index. It may show more than one Seat for one postcode. That is a fact about postcodes, not a guess.
    </p>
    <div class="place-track" aria-hidden="true">
      <div class="place-step"><b>Street</b> A place you already know</div>
      <div class="place-step"><b>Roll</b> The list of voters for that place</div>
      <div class="place-step"><b>Seat</b> The Dewan Rakyat constituency</div>
    </div>
    <div class="split">
      <article class="split-card">
        <div class="tag">Federal</div>
        <h3>Seat</h3>
        <p>Chooses an MP for the Dewan Rakyat.</p>
      </article>
      <article class="split-card">
        <div class="tag">State</div>
        <h3>DUN</h3>
        <p>Chooses an ADUN for the state assembly — if you live in a state.</p>
      </article>
    </div>
    <p class="prose-claim">
      {c["thirteen"]}
      {c["each-state-dun"]}
      {c["dun"]}
      {c["two-rolls"]}
      {c["state-power"]}
      So in a state, the same voter is on the roll for one federal Seat and one DUN. Those votes can fall on different days.
    </p>
    <p class="caveat">
      <strong>The exclusion.</strong>
      {c["ft-names"]}
      {c["ft-direct"]}
      {c["ft-no-subnational"]}
      If you live in Kuala Lumpur, Labuan, or Putrajaya, this walkthrough
      stops at the federal Seat. Do not read “often a DUN too” as a rule
      that covers every Malaysian voter.
    </p>
  </section>

  <section class="scene" id="act-2">
    <div class="pk-eyebrow">02 · You choose a person for a chamber</div>
    <h2>An MP is not an ADUN.</h2>
    <div class="chamber-grid">
      <article class="split-card">
        <div class="tag">Dewan Rakyat</div>
        <h3>MP</h3>
        <p>One person for one federal Seat. They sit in the house this site projects.</p>
      </article>
      <article class="split-card">
        <div class="tag">Dewan Undangan Negeri</div>
        <h3>ADUN</h3>
        <p>One person for one state constituency. They sit in a DUN, not in the Dewan Rakyat.</p>
      </article>
    </div>
    <p class="more">Federal and state elections can fall on different days. The person and the chamber are a pair. A vote does not elect a Coalition by itself. It elects a person who may sit with a Coalition.</p>
  </section>

  <section class="scene" id="act-3">
    <div class="pk-eyebrow">03 · Votes become one Seat</div>
    <h2>Most votes in that Seat win it.</h2>
    <p class="prose-claim">{c["fptp"]}</p>
    <aside class="why">
      <div class="tag">Why this count</div>
      <h3>First past the post, on purpose</h3>
      <p>
        {c["westminster"]}
        The country does not add up every vote nationwide and hand government to the popular-vote winner. Government is built from Seats.
      </p>
    </aside>
  </section>

  <section class="scene" id="act-4">
    <div class="pk-eyebrow">04 · Seats become a government</div>
    <h2>112 of 222 is a Majority.</h2>
    <p class="prose-claim">
      {c["majority"]}
      {c["coalitions"]}
      {c["gov-coalition"]}
      {c["non-gov"]}
    </p>
    <p class="more">
      For who sits inside each Coalition, see
      <a href="/learn/coalitions.html">The five Coalitions</a>.
      The next scene draws Seat totals for three general elections.
    </p>
    <aside class="why">
      <div class="tag">Why a Government Coalition</div>
      <h3>GE15 produced a hung parliament</h3>
      <p>
        {c["hung"]}
        {c["hung-why"]}
        {c["confidence"]}
        {c["anwar-sworn"]}
      </p>
    </aside>
  </section>

  <section class="scene long-scene" id="act-4-years">
    <div class="pk-eyebrow">04b · Seats by year</div>
    <h2>The same house. Different Coalitions.</h2>
    <p class="prose-claim">
      {c["ph-founded"]}
      {c["gps-founded"]}
      {c["gps-from-bn"]}
      {c["pn-founded"]}
      {c["grs-founded"]}
    </p>
    <p class="caveat">
      The five Coalitions this site tracks did not all exist in 2013. PH
      was founded in 2015. GPS was formed after GE14, when Sarawak BN
      parties left. PN and GRS came later. Each chart names the blocs that
      contested that year. The yellow mark is 112 Seats — a Majority.
    </p>
    <div class="year-charts">
      <article class="year-card">
        <div class="tag">GE13 · 2013</div>
        <h3>BN held a Majority</h3>
        {ge13_bar}
        <p class="majority-note">Majority line · 112 of 222</p>
        <ul class="bar-legend">
          {_legend_row("BN", 133, _CHART_COLORS["BN"])}
          {_legend_row("Pakatan Rakyat", 89, _CHART_COLORS["PR"])}
        </ul>
        <p class="prose-claim">
          {c["ge13-bn-133"]}
          {c["ge13-pr-89"]}
          {c["ge13-pr-vote"]}
          {c["ge13-bn-vote"]}
        </p>
      </article>
      <article class="year-card">
        <div class="tag">GE14 · 2018</div>
        <h3>PH crossed 112</h3>
        {ge14_bar}
        <p class="majority-note">Majority line · 112 of 222</p>
        <ul class="bar-legend">
          {_legend_row("PH", 113, _CHART_COLORS["PH"])}
          {_legend_row("BN", 79, _CHART_COLORS["BN"])}
          {_legend_row("Gagasan Sejahtera", 18, _CHART_COLORS["GS"])}
          {_legend_row("WARISAN", 8, _CHART_COLORS["WARISAN"])}
        </ul>
        <p class="prose-claim">
          {c["ge14-majority-112"]}
          {c["ge14-ph-113"]}
          {c["ge14-bn-79"]}
          {c["ge14-gs-18"]}
          {c["ge14-warisan-8"]}
        </p>
      </article>
      <article class="year-card">
        <div class="tag">GE15 · 2022</div>
        <h3>No Coalition held a Majority</h3>
        {ge15_bar}
        <p class="majority-note">Majority line · 112 of 222</p>
        <ul class="bar-legend">
          {_legend_row("PH", 82, _CHART_COLORS["PH"])}
          {_legend_row("PN", 74, _CHART_COLORS["PN"])}
          {_legend_row("BN", 30, _CHART_COLORS["BN"])}
          {_legend_row("GPS", 23, _CHART_COLORS["GPS"])}
          {_legend_row("GRS", 6, _CHART_COLORS["GRS"])}
          {_legend_row("WARISAN", 3, _CHART_COLORS["WARISAN"])}
        </ul>
        <p class="prose-claim">
          {c["ge15-ph-82"]}
          {c["ge15-pn-74"]}
          {c["ge15-bn-30"]}
          {c["ge15-gps-23"]}
          {c["ge15-grs-6"]}
          {c["ge15-warisan-3"]}
        </p>
      </article>
    </div>
  </section>

  <section class="scene long-scene" id="act-4-compass">
    <div class="pk-eyebrow">04c · A political compass</div>
    <h2>Where Wikipedia places each Coalition</h2>
    <p class="caveat">
      This is a teaching sketch, not a scientific score. Wikipedia does
      not publish x and y numbers. The dots follow the left–right labels
      on each Coalition’s page, and they drop GPS and GRS toward East
      Malaysia because those Coalitions are state-based. The exact pixel
      is ours. A click is your mark only. This page will not name a
      Coalition for you.
    </p>
    <div class="compass-panel">
      <div class="compass-board" id="vote-compass" role="img" aria-label="Political compass teaching sketch">
        <span class="compass-label top">Peninsula</span>
        <span class="compass-label bottom">East Malaysia</span>
        <span class="compass-label left">Left</span>
        <span class="compass-label right">Right</span>
        <span class="compass-dot" data-c="PH" title="PH">PH</span>
        <span class="compass-dot" data-c="BN" title="BN">BN</span>
        <span class="compass-dot" data-c="PN" title="PN">PN</span>
        <span class="compass-dot" data-c="GPS" title="GPS">GPS</span>
        <span class="compass-dot" data-c="GRS" title="GRS">GRS</span>
        <span class="compass-you" id="vote-compass-you" hidden>You</span>
      </div>
      <div class="compass-tools">
        <label>Left to right
          <input id="vote-compass-x" type="range" min="2" max="98" value="50">
        </label>
        <label>Peninsula to East Malaysia
          <input id="vote-compass-y" type="range" min="2" max="98" value="50">
        </label>
        <p class="more" id="vote-compass-note">Place a mark if you want one. The page does not score you.</p>
      </div>
      <div class="compass-legend prose-claim">
        {c["ph-position"]}
        {c["bn-position"]}
        {c["pn-position"]}
        {c["gps-position"]}
        {c["gps-sarawak"]}
        {c["grs-position"]}
        {c["grs-sabah"]}
      </div>
    </div>
  </section>

  <section class="scene long-scene" id="act-5">
    <div class="pk-eyebrow">05 · What that government does here</div>
    <h2>Bills, then a counted vote.</h2>
    <p class="prose-claim">
      {c["bill"]}
      {c["division"]}
      {c["assent"]}
    </p>
    <p class="more">
      Watch the current Bills on <a href="/bills/">the Bill tracker</a>.
      Watch who speaks on <a href="/dewan/">Dewan</a>.
    </p>
    <div class="vote-sim" id="vote-sim">
      <div class="tag">A legislature simulator</div>
      <h3>Try a house of 222 Seats</h3>
      <p class="more">
        This is not a live feed of today’s Dewan Rakyat. It is a teaching
        tool on this page. Tick which Coalitions sit in the Government
        Coalition. A Majority is 112 Seats. A Bill still needs 112 yes
        votes on a Division.
      </p>
      <div class="sim-presets">
        <button type="button" data-sim-preset="ge15">GE15 night</button>
        <button type="button" data-sim-preset="ge14">GE14 night</button>
        <button type="button" data-sim-preset="majority">Just over Majority</button>
      </div>
      <div class="sim-rows" style="display:grid;gap:10px;margin-top:16px">
        <div class="sim-row">
          <b>PH</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="PH" aria-label="Fewer PH Seats">−</button>
          <input data-sim-seats="PH" type="number" min="0" max="222" value="82">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="PH" aria-label="More PH Seats">+</button>
          <label class="sim-gov"><input data-sim-gov="PH" type="checkbox" checked> Government Coalition</label>
        </div>
        <div class="sim-row">
          <b>PN</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="PN" aria-label="Fewer PN Seats">−</button>
          <input data-sim-seats="PN" type="number" min="0" max="222" value="74">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="PN" aria-label="More PN Seats">+</button>
          <label class="sim-gov"><input data-sim-gov="PN" type="checkbox"> Government Coalition</label>
        </div>
        <div class="sim-row">
          <b>BN</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="BN" aria-label="Fewer BN Seats">−</button>
          <input data-sim-seats="BN" type="number" min="0" max="222" value="30">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="BN" aria-label="More BN Seats">+</button>
          <label class="sim-gov"><input data-sim-gov="BN" type="checkbox" checked> Government Coalition</label>
        </div>
        <div class="sim-row">
          <b>GPS</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="GPS" aria-label="Fewer GPS Seats">−</button>
          <input data-sim-seats="GPS" type="number" min="0" max="222" value="23">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="GPS" aria-label="More GPS Seats">+</button>
          <label class="sim-gov"><input data-sim-gov="GPS" type="checkbox" checked> Government Coalition</label>
        </div>
        <div class="sim-row">
          <b>GRS</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="GRS" aria-label="Fewer GRS Seats">−</button>
          <input data-sim-seats="GRS" type="number" min="0" max="222" value="6">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="GRS" aria-label="More GRS Seats">+</button>
          <label class="sim-gov"><input data-sim-gov="GRS" type="checkbox" checked> Government Coalition</label>
        </div>
        <div class="sim-row">
          <b>Others</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="OTHER" aria-label="Fewer other Seats">−</button>
          <input data-sim-seats="OTHER" type="number" min="0" max="222" value="7">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="OTHER" aria-label="More other Seats">+</button>
          <label class="sim-gov"><input data-sim-gov="OTHER" type="checkbox"> Government Coalition</label>
        </div>
      </div>
      <p class="sim-meta">Seats in this house: <span data-sim-total>222</span> / 222. Majority = 112.</p>
      <p class="sim-status" data-sim-status data-state="pass">This house has a Majority if the ticked Coalitions hold 112 Seats.</p>
      <div data-sim-stack>{ge15_bar}</div>
      <div class="sim-chamber" data-sim-chamber aria-hidden="true"></div>
    </div>
  </section>

  <section class="scene long-scene" id="act-6">
    <div class="pk-eyebrow">06 · Who else sits above this</div>
    <h2>Parliament is three parts. GE16 only projects one of them.</h2>
    <p class="prose-claim">{c["parliament-houses"]} {c["parliament-ydpa"]}</p>
    <div class="stack">
      <article>
        <div class="tag">Why two houses</div>
        <h3>Dewan Negara was built for a federation</h3>
        <p>{c["reid"]}</p>
        <p>{c["reid-federal"]}</p>
        <p>{c["senate-70"]}</p>
        <p>{c["senate-term"]} A general election refreshes the Dewan Rakyat. It does not empty the Senate.</p>
      </article>
      <article>
        <div class="tag">The Yang di-Pertuan Agong</div>
        <h3>Head of state, not a Seat</h3>
        <p>{c["ydpa-head"]}</p>
        <p>{c["pm-appoint"]} {c["pm-practice"]}</p>
        <p>A passed Bill still goes to the Yang di-Pertuan Agong. Royal assent is how it becomes law. That is not a Seat Call.</p>
      </article>
      <article>
        <div class="tag">Executive</div>
        <h3>Government is drawn from Parliament</h3>
        <p>{c["executive"]}</p>
      </article>
      <article>
        <div class="tag">Judiciary</div>
        <h3>A third branch, not this walkthrough</h3>
        <p>{c["branches"]}</p>
        <p>{c["judiciary"]} This page stops there. It does not explain the courts.</p>
      </article>
    </div>
    <p class="more">
      What GE16 projects on this site is the next Dewan Rakyat — 222 Seats,
      and whether a Coalition holds a Majority. It does not project the
      Dewan Negara, the YDPA, or the courts.
      <a href="/learn/ge16-process.html">How GE16 is called</a>
      is a separate page.
    </p>
  </section>
</div>
""".strip()


def _body_ms() -> str:
    c = {
        "seat-unit": _claim(
            "claim-seat-unit",
            CONTEXT_MD,
            "Kerusi ialah unit yang dimenangi atau kalah dalam pilihan raya.",
        ),
        "seat-222": _claim(
            "claim-222",
            CONTEXT_MD,
            "Dewan Rakyat mempunyai 222 Kerusi.",
        ),
        "street": _claim(
            "claim-street-in-seat",
            CONTEXT_MD,
            "Poskod Malaysia dipetakan kepada setiap Kerusi yang mungkin termasukinya, dan satu poskod boleh merentasi dua Kerusi.",
        ),
        "thirteen": _claim(
            "claim-thirteen-states",
            STATES_WIKI,
            "Malaysia ialah sebuah persekutuan tiga belas negeri dan tiga wilayah persekutuan.",
        ),
        "each-state-dun": _claim(
            "claim-each-state-dun",
            STATES_WIKI,
            "Setiap negeri juga mempunyai badan perundangan ekadewan bergaya Westminster yang dipanggil Dewan Undangan Negeri (DUN).",
        ),
        "dun": _claim(
            "claim-dun-is-state-assembly",
            DUN_WIKI,
            "Dewan Undangan Negeri ialah dewan undangan sesebuah negeri.",
        ),
        "two-rolls": _claim(
            "claim-two-rolls",
            ELECTIONS_WIKI,
            "Pilihan raya persekutuan memilih ahli Dewan Rakyat, manakala pilihan raya negeri di setiap 13 negeri memilih ahli dewan undangan negeri masing-masing.",
        ),
        "ft-names": _claim(
            "claim-ft-names",
            STATES_WIKI,
            "Tiga wilayah persekutuan—Kuala Lumpur, Labuan dan Putrajaya—dicipta kemudian daripada tanah yang dipisahkan daripada negeri sedia ada.",
        ),
        "ft-direct": _claim(
            "claim-ft-direct",
            STATES_WIKI,
            "Wilayah persekutuan ditadbir secara langsung oleh kerajaan persekutuan.",
        ),
        "ft-no-subnational": _claim(
            "claim-ft-no-subnational",
            STATES_WIKI,
            "Tiada pilihan raya subnasional di wilayah persekutuan.",
        ),
        "state-power": _claim(
            "claim-state-legislature",
            POLITICS_WIKI,
            "Kuasa perundangan terletak pada parlimen persekutuan dan 13 dewan undangan negeri.",
        ),
        "fptp": _claim(
            "claim-fptp",
            PARLIAMENT_WIKI,
            "Dewan Rakyat terdiri daripada 222 ahli Parlimen yang dipilih daripada kawasan pilihan raya berahli tunggal berdasarkan populasi dalam pilihan raya umum menggunakan sistem first-past-the-post.",
        ),
        "westminster": _claim(
            "claim-westminster",
            POLITICS_WIKI,
            "Sistem kerajaan Malaysia dimodelkan rapat pada sistem parlimen Westminster, suatu warisan pemerintahan kolonial British.",
        ),
        "majority": _claim(
            "claim-majority",
            CONTEXT_MD,
            "Majoriti bermaksud memegang lebih daripada separuh daripada 222 kerusi (112+).",
        ),
        "coalitions": _claim(
            "claim-coalitions",
            CONTEXT_MD,
            "Lima Gabungan yang dijejaki laman ini ialah PH, BN, PN, GPS dan GRS.",
        ),
        "gov-coalition": _claim(
            "claim-gov-coalition",
            CONTEXT_MD,
            "Gabungan Kerajaan, blok pemerintah semasa, ialah PH + BN + GPS + GRS serta parti kecil.",
        ),
        "non-gov": _claim(
            "claim-non-government",
            CONTEXT_MD,
            "Bukan kerajaan bermaksud setiap Kerusi atau Gabungan di luar Gabungan Kerajaan.",
        ),
        "hung": _claim(
            "claim-hung-ge15",
            GE15_WIKI,
            "Pilihan raya umum 2022 menghasilkan parlimen tergantung, pilihan raya persekutuan pertama dengan keputusan begitu dalam sejarah negara.",
        ),
        "hung-why": _claim(
            "claim-hung-form",
            GE15_WIKI,
            "Jika parlimen tergantung, iaitu tiada satu parti memperoleh majoriti kerusi, kerajaan masih boleh dibentuk melalui gabungan.",
        ),
        "anwar-sworn": _claim(
            "claim-anwar-sworn",
            GE15_WIKI,
            "Anwar Ibrahim dilantik dan mengangkat sumpah sebagai perdana menteri pada 24 November 2022 oleh Yang di-Pertuan Agong.",
        ),
        "confidence": _claim(
            "claim-confidence",
            GE15_WIKI,
            "Ketua kerajaan ialah orang yang mendapat kepercayaan majoriti ahli dalam badan perundangan berkenaan.",
        ),
        "bill": _claim(
            "claim-bill",
            CONTEXT_MD,
            "Rang Undang-Undang ialah suatu undang-undang yang dibawa ke Dewan Rakyat.",
        ),
        "division": _claim(
            "claim-division",
            CONTEXT_MD,
            "Bahagian ialah undian yang dikira di Dewan Rakyat, di mana Hansard menamakan setiap Ahli sebagai setuju, tidak setuju, berkecuali atau tidak hadir.",
        ),
        "parliament-houses": _claim(
            "claim-parliament-houses",
            PARLIAMENT_WIKI,
            "Parlimen dwidewan terdiri daripada Dewan Rakyat dan Dewan Negara.",
        ),
        "parliament-ydpa": _claim(
            "claim-parliament-ydpa",
            PARLIAMENT_WIKI,
            "Yang di-Pertuan Agong, sebagai ketua negara, ialah komponen ketiga Parlimen.",
        ),
        "reid": _claim(
            "claim-reid",
            PARLIAMENT_WIKI,
            "Suruhanjaya Reid, yang merangka Perlembagaan Persekutuan Tanah Melayu, memodelkan sistem kerajaan Tanah Melayu mengikut sistem British: parlimen dwidewan, dengan satu dewan dipilih secara langsung, dan dewan satu lagi berkuasa terhad dengan sebahagian ahlinya dilantik oleh Raja.",
        ),
        "reid-federal": _claim(
            "claim-reid-federal",
            PARLIAMENT_WIKI,
            "Selaras dengan sifat persekutuan negara baharu itu, dewan atasan juga akan mempunyai ahli yang dipilih oleh dewan undangan negeri selain ahli yang dilantik oleh Raja.",
        ),
        "senate-70": _claim(
            "claim-senate-70",
            PARLIAMENT_WIKI,
            "Dewan Negara terdiri daripada 70 ahli (Senator); 26 dipilih oleh 13 dewan undangan negeri (2 senator setiap negeri), 4 dilantik oleh Yang di-Pertuan Agong untuk mewakili 3 wilayah persekutuan, dan 40 lagi dilantik oleh Yang di-Pertuan Agong atas nasihat Perdana Menteri.",
        ),
        "senate-term": _claim(
            "claim-senate-undissolved",
            PARLIAMENT_WIKI,
            "Pembubaran Parlimen tidak menjejaskan Dewan Negara.",
        ),
        "pm-appoint": _claim(
            "claim-pm-appoint",
            PARLIAMENT_WIKI,
            "Yang di-Pertuan Agong melantik Perdana Menteri, yang merupakan Ketua Kerajaan, daripada Dewan Rakyat.",
        ),
        "pm-practice": _claim(
            "claim-pm-practice",
            PARLIAMENT_WIKI,
            "Dalam amalan, Perdana Menteri hendaklah orang yang mendapat kepercayaan majoriti Dewan Rakyat.",
        ),
        "executive": _claim(
            "claim-executive",
            PARLIAMENT_WIKI,
            "Kerajaan eksekutif, yang terdiri daripada Perdana Menteri dan Jemaah Menteri, diambil daripada ahli Parlimen dan bertanggungjawab kepada Parlimen.",
        ),
        "assent": _claim(
            "claim-royal-assent",
            PARLIAMENT_WIKI,
            "Jika rang undang-undang diluluskan, ia dibentangkan kepada Yang di-Pertuan Agong, yang mempunyai 30 hari untuk menimbangnya.",
        ),
        "branches": _claim(
            "claim-three-branches",
            POLITICS_WIKI,
            "Hirarki kuasa di Malaysia, menurut Perlembagaan Persekutuan, menetapkan tiga cabang kerajaan Malaysia sebagai Eksekutif, Kehakiman dan Perundangan.",
        ),
        "judiciary": _claim(
            "claim-judiciary",
            POLITICS_WIKI,
            "Badan kehakiman berasingan daripada eksekutif dan badan perundangan.",
        ),
        "ydpa-head": _claim(
            "claim-ydpa-head",
            POLITICS_WIKI,
            "Yang di-Pertuan Agong ialah ketua negara dan Perdana Menteri Malaysia ialah ketua kerajaan.",
        ),
        "ge13-bn-133": _claim(
            "claim-ge13-bn-133",
            GE13_WIKI,
            "Barisan Nasional memenangi 133 kerusi dalam pilihan raya umum 2013.",
        ),
        "ge13-pr-89": _claim(
            "claim-ge13-pr-89",
            GE13_WIKI,
            "Pakatan Rakyat memenangi 89 daripada 222 kerusi.",
        ),
        "ge13-pr-vote": _claim(
            "claim-ge13-pr-vote",
            GE13_WIKI,
            "Gabungan pembangkang tidak rasmi Pakatan Rakyat pimpinan Anwar Ibrahim menerima majoriti undi, dengan tiga parti ahlinya secara kolektif menerima 50.9% undi.",
        ),
        "ge13-bn-vote": _claim(
            "claim-ge13-bn-vote",
            GE13_WIKI,
            "Gabungan pemerintah sedia ada, Barisan Nasional, menerima 47.4% undi dan memenangi 133 kerusi.",
        ),
        "ge14-ph-113": _claim(
            "claim-ge14-ph-113",
            GE14_WIKI,
            "Pakatan Harapan memenangi 113 kerusi dalam pilihan raya umum 2018.",
        ),
        "ge14-bn-79": _claim(
            "claim-ge14-bn-79",
            GE14_WIKI,
            "Barisan Nasional memenangi 79 kerusi dalam pilihan raya umum 2018.",
        ),
        "ge14-gs-18": _claim(
            "claim-ge14-gs-18",
            GE14_WIKI,
            "Gagasan Sejahtera memenangi 18 kerusi dalam pilihan raya umum 2018.",
        ),
        "ge14-warisan-8": _claim(
            "claim-ge14-warisan-8",
            GE14_WIKI,
            "Warisan memenangi 8 kerusi dalam pilihan raya umum 2018.",
        ),
        "ge14-majority-112": _claim(
            "claim-ge14-majority-112",
            GE14_WIKI,
            "Pilihan raya umum 2018 memerlukan 112 kerusi untuk majoriti.",
        ),
        "gps-founded": _claim(
            "claim-gps-founded",
            GPS_WIKI,
            "Gabungan Parti Sarawak ditubuhkan pada 12 Jun 2018.",
        ),
        "gps-from-bn": _claim(
            "claim-gps-from-bn",
            GPS_WIKI,
            "Gabungan Parti Sarawak ditubuhkan pada 2018 oleh empat bekas parti komponen Barisan Nasional yang beroperasi hanya di Sarawak selepas kekalahan gabungan persekutuan dalam pilihan raya umum Malaysia 2018.",
        ),
        "ge15-ph-82": _claim(
            "claim-ge15-ph-82",
            GE15_WIKI,
            "Pakatan Harapan memenangi 82 kerusi dalam pilihan raya umum 2022, angka yang merangkumi MUDA.",
        ),
        "ge15-pn-74": _claim(
            "claim-ge15-pn-74",
            GE15_WIKI,
            "Perikatan Nasional memenangi 74 kerusi dalam pilihan raya umum 2022.",
        ),
        "ge15-bn-30": _claim(
            "claim-ge15-bn-30",
            GE15_WIKI,
            "Barisan Nasional memenangi 30 kerusi dalam pilihan raya umum 2022.",
        ),
        "ge15-gps-23": _claim(
            "claim-ge15-gps-23",
            GE15_WIKI,
            "Gabungan Parti Sarawak memenangi 23 kerusi dalam pilihan raya umum 2022.",
        ),
        "ge15-grs-6": _claim(
            "claim-ge15-grs-6",
            GE15_WIKI,
            "Gabungan Rakyat Sabah memenangi 6 kerusi dalam pilihan raya umum 2022.",
        ),
        "ge15-warisan-3": _claim(
            "claim-ge15-warisan-3",
            GE15_WIKI,
            "Warisan memenangi 3 kerusi dalam pilihan raya umum 2022.",
        ),
        "ph-founded": _claim(
            "claim-ph-founded",
            PH_WIKI,
            "Pakatan Harapan ditubuhkan pada 22 September 2015.",
        ),
        "pn-founded": _claim(
            "claim-pn-founded",
            PN_WIKI,
            "Perikatan Nasional ditubuhkan pada 29 Februari 2020.",
        ),
        "grs-founded": _claim(
            "claim-grs-founded",
            GRS_WIKI,
            "Gabungan Rakyat Sabah ditubuhkan pada September 2020, apabila Hajiji Noor menubuhkan pakatan tidak rasmi dengan nama itu.",
        ),
        "ph-position": _claim(
            "claim-ph-position",
            PH_WIKI,
            "Kedudukan politik Pakatan Harapan ialah tengah hingga tengah kiri.",
        ),
        "pn-position": _claim(
            "claim-pn-position",
            PN_WIKI,
            "Kedudukan politik Perikatan Nasional ialah sayap kanan hingga jauh kanan.",
        ),
        "bn-position": _claim(
            "claim-bn-position",
            BN_WIKI,
            "Kedudukan politik Barisan Nasional ialah tengah kanan hingga sayap kanan.",
        ),
        "gps-position": _claim(
            "claim-gps-position",
            GPS_WIKI,
            "Kedudukan politik Gabungan Parti Sarawak ialah tengah kanan hingga sayap kanan.",
        ),
        "gps-sarawak": _claim(
            "claim-gps-sarawak",
            GPS_WIKI,
            "Gabungan Parti Sarawak ialah pakatan politik berasaskan Sarawak di Malaysia.",
        ),
        "grs-position": _claim(
            "claim-grs-position",
            GRS_WIKI,
            "Kedudukan politik Gabungan Rakyat Sabah ialah tengah hingga tengah kanan.",
        ),
        "grs-sabah": _claim(
            "claim-grs-sabah",
            GRS_WIKI,
            "Gabungan Rakyat Sabah ialah gabungan Malaysia yang terdiri daripada parti berasaskan Sabah.",
        ),
    }
    ge13_bar = _stack_bar(
        (
            ("BN", 133, _CHART_COLORS["BN"]),
            ("Pakatan Rakyat", 89, _CHART_COLORS["PR"]),
        )
    )
    ge14_bar = _stack_bar(
        (
            ("PH", 113, _CHART_COLORS["PH"]),
            ("BN", 79, _CHART_COLORS["BN"]),
            ("Gagasan Sejahtera", 18, _CHART_COLORS["GS"]),
            ("WARISAN", 8, _CHART_COLORS["WARISAN"]),
            ("Lain-lain", 4, _CHART_COLORS["OTHER"]),
        )
    )
    ge15_bar = _stack_bar(
        (
            ("PH", 82, _CHART_COLORS["PH"]),
            ("PN", 74, _CHART_COLORS["PN"]),
            ("BN", 30, _CHART_COLORS["BN"]),
            ("GPS", 23, _CHART_COLORS["GPS"]),
            ("GRS", 6, _CHART_COLORS["GRS"]),
            ("WARISAN", 3, _CHART_COLORS["WARISAN"]),
            ("Lain-lain", 4, _CHART_COLORS["OTHER"]),
        )
    )
    return f"""
<div class="pk-scroll">
  <nav class="act-nav" aria-label="Bab">
    <a href="#act-1">1 · Tempat</a>
    <a href="#act-2">2 · Orang</a>
    <a href="#act-3">3 · Kerusi</a>
    <a href="#act-4">4 · Kerajaan</a>
    <a href="#act-4-years">Kerusi mengikut tahun</a>
    <a href="#act-4-compass">Kompas</a>
    <a href="#act-5">5 · Kerja</a>
    <a href="#vote-sim">Dewan</a>
    <a href="#act-6">6 · Di atas ini</a>
  </nav>

  <section class="scene" id="open">
    <div class="pk-eyebrow">Panduan untuk pengundi kali pertama</div>
    <h1>Ke mana undi pergi?</h1>
    <p class="line">Bukan ke seluruh negara sekaligus. Ke suatu tempat, kemudian suatu dewan, kemudian suatu kerajaan.</p>
  </section>

  <section class="scene" id="act-1">
    <div class="pk-eyebrow">01 · Anda mengundi di suatu tempat</div>
    <h2>Satu jalan. Satu Kerusi persekutuan.</h2>
    <p class="prose-claim">
      {c["seat-unit"]}
      {c["seat-222"]}
      {c["street"]}
      Carian di laman utama menggunakan indeks itu. Ia mungkin menunjukkan lebih daripada satu Kerusi untuk satu poskod. Itu fakta tentang poskod, bukan tekaan.
    </p>
    <div class="place-track" aria-hidden="true">
      <div class="place-step"><b>Jalan</b> Tempat yang anda sudah kenali</div>
      <div class="place-step"><b>Daftar</b> Senarai pengundi untuk tempat itu</div>
      <div class="place-step"><b>Kerusi</b> Kawasan Dewan Rakyat</div>
    </div>
    <div class="split">
      <article class="split-card">
        <div class="tag">Persekutuan</div>
        <h3>Kerusi</h3>
        <p>Memilih Ahli Parlimen untuk Dewan Rakyat.</p>
      </article>
      <article class="split-card">
        <div class="tag">Negeri</div>
        <h3>DUN</h3>
        <p>Memilih ADUN untuk dewan negeri — jika anda tinggal di sebuah negeri.</p>
      </article>
    </div>
    <p class="prose-claim">
      {c["thirteen"]}
      {c["each-state-dun"]}
      {c["dun"]}
      {c["two-rolls"]}
      {c["state-power"]}
      Jadi di sebuah negeri, pengundi yang sama ada dalam daftar satu Kerusi persekutuan dan satu DUN. Undi itu boleh jatuh pada hari yang berbeza.
    </p>
    <p class="caveat">
      <strong>Pengecualian.</strong>
      {c["ft-names"]}
      {c["ft-direct"]}
      {c["ft-no-subnational"]}
      Jika anda tinggal di Kuala Lumpur, Labuan, atau Putrajaya, panduan
      ini berhenti di Kerusi persekutuan. Jangan baca “selalunya ada DUN
      juga” sebagai peraturan untuk setiap pengundi Malaysia.
    </p>
  </section>

  <section class="scene" id="act-2">
    <div class="pk-eyebrow">02 · Anda memilih seorang untuk suatu dewan</div>
    <h2>Ahli Parlimen bukan ADUN.</h2>
    <div class="chamber-grid">
      <article class="split-card">
        <div class="tag">Dewan Rakyat</div>
        <h3>Ahli Parlimen</h3>
        <p>Seorang untuk satu Kerusi persekutuan. Mereka duduk di dewan yang diunjurkan laman ini.</p>
      </article>
      <article class="split-card">
        <div class="tag">Dewan Undangan Negeri</div>
        <h3>ADUN</h3>
        <p>Seorang untuk satu kawasan negeri. Mereka duduk di DUN, bukan di Dewan Rakyat.</p>
      </article>
    </div>
    <p class="more">Pilihan raya persekutuan dan negeri boleh jatuh pada hari yang berbeza. Orang dan dewan ialah satu pasangan. Satu undi tidak memilih Gabungan dengan sendirinya. Ia memilih seorang yang mungkin duduk bersama suatu Gabungan.</p>
  </section>

  <section class="scene" id="act-3">
    <div class="pk-eyebrow">03 · Undi menjadi satu Kerusi</div>
    <h2>Undi terbanyak dalam Kerusi itu memenanginya.</h2>
    <p class="prose-claim">{c["fptp"]}</p>
    <aside class="why">
      <div class="tag">Mengapa kiraan ini</div>
      <h3>First past the post, dengan sengaja</h3>
      <p>
        {c["westminster"]}
        Negara tidak menjumlahkan setiap undi di seluruh negara lalu menyerahkan kerajaan kepada pemenang undi popular. Kerajaan dibina daripada Kerusi.
      </p>
    </aside>
  </section>

  <section class="scene" id="act-4">
    <div class="pk-eyebrow">04 · Kerusi menjadi kerajaan</div>
    <h2>112 daripada 222 ialah Majoriti.</h2>
    <p class="prose-claim">
      {c["majority"]}
      {c["coalitions"]}
      {c["gov-coalition"]}
      {c["non-gov"]}
    </p>
    <p class="more">
      Untuk siapa yang duduk dalam setiap Gabungan, lihat
      <a href="/ms/learn/coalitions.html">Lima Gabungan</a>.
      Bab seterusnya melukis jumlah Kerusi untuk tiga pilihan raya umum.
    </p>
    <aside class="why">
      <div class="tag">Mengapa Gabungan Kerajaan</div>
      <h3>PRU15 menghasilkan parlimen tergantung</h3>
      <p>
        {c["hung"]}
        {c["hung-why"]}
        {c["confidence"]}
        {c["anwar-sworn"]}
      </p>
    </aside>
  </section>

  <section class="scene long-scene" id="act-4-years">
    <div class="pk-eyebrow">04b · Kerusi mengikut tahun</div>
    <h2>Dewan yang sama. Gabungan yang berbeza.</h2>
    <p class="prose-claim">
      {c["ph-founded"]}
      {c["gps-founded"]}
      {c["gps-from-bn"]}
      {c["pn-founded"]}
      {c["grs-founded"]}
    </p>
    <p class="caveat">
      Lima Gabungan yang dijejaki laman ini tidak semuanya wujud pada 2013.
      PH ditubuhkan pada 2015. GPS dibentuk selepas PRU14, apabila parti
      BN Sarawak keluar. PN dan GRS datang kemudian. Setiap carta menamakan
      blok yang bertanding tahun itu. Tanda kuning ialah 112 Kerusi —
      suatu Majoriti.
    </p>
    <div class="year-charts">
      <article class="year-card">
        <div class="tag">PRU13 · 2013</div>
        <h3>BN memegang Majoriti</h3>
        {ge13_bar}
        <p class="majority-note">Garisan Majoriti · 112 daripada 222</p>
        <ul class="bar-legend">
          {_legend_row("BN", 133, _CHART_COLORS["BN"])}
          {_legend_row("Pakatan Rakyat", 89, _CHART_COLORS["PR"])}
        </ul>
        <p class="prose-claim">
          {c["ge13-bn-133"]}
          {c["ge13-pr-89"]}
          {c["ge13-pr-vote"]}
          {c["ge13-bn-vote"]}
        </p>
      </article>
      <article class="year-card">
        <div class="tag">PRU14 · 2018</div>
        <h3>PH melepasi 112</h3>
        {ge14_bar}
        <p class="majority-note">Garisan Majoriti · 112 daripada 222</p>
        <ul class="bar-legend">
          {_legend_row("PH", 113, _CHART_COLORS["PH"])}
          {_legend_row("BN", 79, _CHART_COLORS["BN"])}
          {_legend_row("Gagasan Sejahtera", 18, _CHART_COLORS["GS"])}
          {_legend_row("WARISAN", 8, _CHART_COLORS["WARISAN"])}
        </ul>
        <p class="prose-claim">
          {c["ge14-majority-112"]}
          {c["ge14-ph-113"]}
          {c["ge14-bn-79"]}
          {c["ge14-gs-18"]}
          {c["ge14-warisan-8"]}
        </p>
      </article>
      <article class="year-card">
        <div class="tag">PRU15 · 2022</div>
        <h3>Tiada Gabungan memegang Majoriti</h3>
        {ge15_bar}
        <p class="majority-note">Garisan Majoriti · 112 daripada 222</p>
        <ul class="bar-legend">
          {_legend_row("PH", 82, _CHART_COLORS["PH"])}
          {_legend_row("PN", 74, _CHART_COLORS["PN"])}
          {_legend_row("BN", 30, _CHART_COLORS["BN"])}
          {_legend_row("GPS", 23, _CHART_COLORS["GPS"])}
          {_legend_row("GRS", 6, _CHART_COLORS["GRS"])}
          {_legend_row("WARISAN", 3, _CHART_COLORS["WARISAN"])}
        </ul>
        <p class="prose-claim">
          {c["ge15-ph-82"]}
          {c["ge15-pn-74"]}
          {c["ge15-bn-30"]}
          {c["ge15-gps-23"]}
          {c["ge15-grs-6"]}
          {c["ge15-warisan-3"]}
        </p>
      </article>
    </div>
  </section>

  <section class="scene long-scene" id="act-4-compass">
    <div class="pk-eyebrow">04c · Kompas politik</div>
    <h2>Di mana Wikipedia meletakkan setiap Gabungan</h2>
    <p class="caveat">
      Ini lakaran pengajaran, bukan skor saintifik. Wikipedia tidak
      menerbitkan nombor x dan y. Titik mengikut label kiri–kanan pada
      laman setiap Gabungan, dan GPS serta GRS diturunkan ke Malaysia
      Timur kerana Gabungan itu berasaskan negeri. Piksel tepat ialah
      milik kami. Klik ialah tanda anda sahaja. Laman ini tidak akan
      menamakan Gabungan untuk anda.
    </p>
    <div class="compass-panel">
      <div class="compass-board" id="vote-compass" role="img" aria-label="Lakaran pengajaran kompas politik">
        <span class="compass-label top">Semenanjung</span>
        <span class="compass-label bottom">Malaysia Timur</span>
        <span class="compass-label left">Kiri</span>
        <span class="compass-label right">Kanan</span>
        <span class="compass-dot" data-c="PH" title="PH">PH</span>
        <span class="compass-dot" data-c="BN" title="BN">BN</span>
        <span class="compass-dot" data-c="PN" title="PN">PN</span>
        <span class="compass-dot" data-c="GPS" title="GPS">GPS</span>
        <span class="compass-dot" data-c="GRS" title="GRS">GRS</span>
        <span class="compass-you" id="vote-compass-you" hidden>Anda</span>
      </div>
      <div class="compass-tools">
        <label>Kiri ke kanan
          <input id="vote-compass-x" type="range" min="2" max="98" value="50">
        </label>
        <label>Semenanjung ke Malaysia Timur
          <input id="vote-compass-y" type="range" min="2" max="98" value="50">
        </label>
        <p class="more" id="vote-compass-note">Letakkan tanda jika anda mahu. Laman ini tidak menskor anda.</p>
      </div>
      <div class="compass-legend prose-claim">
        {c["ph-position"]}
        {c["bn-position"]}
        {c["pn-position"]}
        {c["gps-position"]}
        {c["gps-sarawak"]}
        {c["grs-position"]}
        {c["grs-sabah"]}
      </div>
    </div>
  </section>

  <section class="scene long-scene" id="act-5">
    <div class="pk-eyebrow">05 · Apa yang kerajaan itu buat di sini</div>
    <h2>Rang undang-undang, kemudian undian yang dikira.</h2>
    <p class="prose-claim">
      {c["bill"]}
      {c["division"]}
      {c["assent"]}
    </p>
    <p class="more">
      Lihat Rang Undang-Undang semasa di <a href="/bills/">penjejak RUU</a>.
      Lihat siapa bersuara di <a href="/dewan/">Dewan</a>.
    </p>
    <div class="vote-sim" id="vote-sim">
      <div class="tag">Simulator badan perundangan</div>
      <h3>Cuba sebuah dewan 222 Kerusi</h3>
      <p class="more">
        Ini bukan suapan langsung Dewan Rakyat hari ini. Ia ialah alat
        pengajaran di laman ini. Tanda Gabungan mana yang duduk dalam
        Gabungan Kerajaan. Majoriti ialah 112 Kerusi. Rang Undang-Undang
        masih memerlukan 112 undi ya dalam suatu Bahagian.
      </p>
      <div class="sim-presets">
        <button type="button" data-sim-preset="ge15">Malam PRU15</button>
        <button type="button" data-sim-preset="ge14">Malam PRU14</button>
        <button type="button" data-sim-preset="majority">Sedikit di atas Majoriti</button>
      </div>
      <div class="sim-rows" style="display:grid;gap:10px;margin-top:16px">
        <div class="sim-row">
          <b>PH</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="PH" aria-label="Kurang Kerusi PH">−</button>
          <input data-sim-seats="PH" type="number" min="0" max="222" value="82">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="PH" aria-label="Lebih Kerusi PH">+</button>
          <label class="sim-gov"><input data-sim-gov="PH" type="checkbox" checked> Gabungan Kerajaan</label>
        </div>
        <div class="sim-row">
          <b>PN</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="PN" aria-label="Kurang Kerusi PN">−</button>
          <input data-sim-seats="PN" type="number" min="0" max="222" value="74">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="PN" aria-label="Lebih Kerusi PN">+</button>
          <label class="sim-gov"><input data-sim-gov="PN" type="checkbox"> Gabungan Kerajaan</label>
        </div>
        <div class="sim-row">
          <b>BN</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="BN" aria-label="Kurang Kerusi BN">−</button>
          <input data-sim-seats="BN" type="number" min="0" max="222" value="30">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="BN" aria-label="Lebih Kerusi BN">+</button>
          <label class="sim-gov"><input data-sim-gov="BN" type="checkbox" checked> Gabungan Kerajaan</label>
        </div>
        <div class="sim-row">
          <b>GPS</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="GPS" aria-label="Kurang Kerusi GPS">−</button>
          <input data-sim-seats="GPS" type="number" min="0" max="222" value="23">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="GPS" aria-label="Lebih Kerusi GPS">+</button>
          <label class="sim-gov"><input data-sim-gov="GPS" type="checkbox" checked> Gabungan Kerajaan</label>
        </div>
        <div class="sim-row">
          <b>GRS</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="GRS" aria-label="Kurang Kerusi GRS">−</button>
          <input data-sim-seats="GRS" type="number" min="0" max="222" value="6">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="GRS" aria-label="Lebih Kerusi GRS">+</button>
          <label class="sim-gov"><input data-sim-gov="GRS" type="checkbox" checked> Gabungan Kerajaan</label>
        </div>
        <div class="sim-row">
          <b>Lain-lain</b>
          <button type="button" class="sim-step" data-sim-step="-1" data-sim-step-code="OTHER" aria-label="Kurang Kerusi lain">−</button>
          <input data-sim-seats="OTHER" type="number" min="0" max="222" value="7">
          <button type="button" class="sim-step" data-sim-step="1" data-sim-step-code="OTHER" aria-label="Lebih Kerusi lain">+</button>
          <label class="sim-gov"><input data-sim-gov="OTHER" type="checkbox"> Gabungan Kerajaan</label>
        </div>
      </div>
      <p class="sim-meta">Kerusi dalam dewan ini: <span data-sim-total>222</span> / 222. Majoriti = 112.</p>
      <p class="sim-status" data-sim-status data-state="pass">Dewan ini mempunyai Majoriti jika Gabungan yang ditanda memegang 112 Kerusi.</p>
      <div data-sim-stack>{ge15_bar}</div>
      <div class="sim-chamber" data-sim-chamber aria-hidden="true"></div>
    </div>
  </section>

  <section class="scene long-scene" id="act-6">
    <div class="pk-eyebrow">06 · Siapa lagi yang duduk di atas ini</div>
    <h2>Parlimen ada tiga bahagian. PRU16 hanya mengunjurkan satu.</h2>
    <p class="prose-claim">{c["parliament-houses"]} {c["parliament-ydpa"]}</p>
    <div class="stack">
      <article>
        <div class="tag">Mengapa dua dewan</div>
        <h3>Dewan Negara dibina untuk sebuah persekutuan</h3>
        <p>{c["reid"]}</p>
        <p>{c["reid-federal"]}</p>
        <p>{c["senate-70"]}</p>
        <p>{c["senate-term"]} Pilihan raya umum menyegarkan Dewan Rakyat. Ia tidak mengosongkan Dewan Negara.</p>
      </article>
      <article>
        <div class="tag">Yang di-Pertuan Agong</div>
        <h3>Ketua negara, bukan sebuah Kerusi</h3>
        <p>{c["ydpa-head"]}</p>
        <p>{c["pm-appoint"]} {c["pm-practice"]}</p>
        <p>Rang Undang-Undang yang diluluskan masih pergi kepada Yang di-Pertuan Agong. Perkenan diraja ialah cara ia menjadi undang-undang. Itu bukan Seat Call.</p>
      </article>
      <article>
        <div class="tag">Eksekutif</div>
        <h3>Kerajaan diambil daripada Parlimen</h3>
        <p>{c["executive"]}</p>
      </article>
      <article>
        <div class="tag">Kehakiman</div>
        <h3>Cabang ketiga, bukan panduan ini</h3>
        <p>{c["branches"]}</p>
        <p>{c["judiciary"]} Laman ini berhenti di situ. Ia tidak menjelaskan mahkamah.</p>
      </article>
    </div>
    <p class="more">
      Apa yang PRU16 unjurkan di laman ini ialah Dewan Rakyat yang seterusnya
      — 222 Kerusi, dan sama ada suatu Gabungan memegang Majoriti. Ia tidak
      mengunjurkan Dewan Negara, YDPA, atau mahkamah.
      <a href="/ms/learn/ge16-process.html">Bagaimana PRU16 diisytiharkan</a>
      ialah laman berasingan.
    </p>
  </section>
</div>
""".strip()


def build_vote_path_page(language: Language, updated_at: date, status: ElectionStatus) -> str:
    return render_shell(
        title=t(
            language,
            "How a vote works | PolitikKu",
            "Ke mana undi pergi | PolitikKu",
        ),
        description=t(
            language,
            "A first-time-voter walkthrough: street to Seat to DUN, first-past-the-post, Majority, Seat charts, a sourced compass, and a legislature simulator.",
            "Panduan pengundi kali pertama: jalan ke Kerusi ke DUN, first-past-the-post, Majoriti, carta Kerusi, kompas bersumber, dan simulator badan perundangan.",
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
        chrome=False,
        header_html=_header(language),
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
