"""HITL register samples for Act 1 of the civic vote-path walkthrough.

Two pages, same claims, different register — the #25 pattern. This is not
the shipped walkthrough. The user picks a register before full copy is
written. Pages are noindex and are not in NAV_LINKS.

Parent map: #192. This prototype: #194.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from lpa.config import load_election_status
from lpa.domain import ElectionStatus
from lpa.politikku_shell import Language, render_shell

CONTEXT_MD = (
    "https://raw.githubusercontent.com/IlhamKassim/live-political-analysis/main/CONTEXT.md"
)
DUN_WIKI = "https://en.wikipedia.org/wiki/Dewan_Undangan_Negeri?action=raw"
STATES_WIKI = (
    "https://en.wikipedia.org/wiki/States_and_federal_territories_of_Malaysia?action=raw"
)
ELECTIONS_WIKI = "https://en.wikipedia.org/wiki/Elections_in_Malaysia?action=raw"

# Stable ids so the two samples can be compared claim-for-claim.
CLAIM_IDS: tuple[str, ...] = (
    "claim-seat-unit",
    "claim-222",
    "claim-street-in-seat",
    "claim-thirteen-states",
    "claim-dun-is-state-assembly",
    "claim-ft-no-dun",
    "claim-two-rolls",
)

_NOINDEX = '<meta name="robots" content="noindex, nofollow">'


def _claim(claim_id: str, cite: str, text: str) -> str:
    return f'<span data-claim id="{claim_id}" data-cite="{cite}">{text}</span>'


def _shared_claims() -> dict[str, str]:
    return {
        "claim-seat-unit": _claim(
            "claim-seat-unit",
            CONTEXT_MD,
            "On this site, a Seat is a parliamentary constituency — the unit "
            "a general election is actually won or lost in.",
        ),
        "claim-222": _claim(
            "claim-222",
            CONTEXT_MD,
            "The Dewan Rakyat has 222 Seats.",
        ),
        "claim-street-in-seat": _claim(
            "claim-street-in-seat",
            CONTEXT_MD,
            "A Malaysian postcode maps to every Seat it could fall in, and a "
            "postcode can straddle two Seats.",
        ),
        "claim-thirteen-states": _claim(
            "claim-thirteen-states",
            STATES_WIKI,
            "Malaysia has thirteen states and three Federal Territories: "
            "Kuala Lumpur, Labuan, and Putrajaya.",
        ),
        "claim-dun-is-state-assembly": _claim(
            "claim-dun-is-state-assembly",
            DUN_WIKI,
            "Each state has a unicameral legislature called the Dewan "
            "Undangan Negeri, also called a DUN or state assembly.",
        ),
        "claim-ft-no-dun": _claim(
            "claim-ft-no-dun",
            STATES_WIKI,
            "The Federal Territories do not have a Dewan Undangan Negeri. "
            "They elect members to the Dewan Rakyat only.",
        ),
        "claim-two-rolls": _claim(
            "claim-two-rolls",
            ELECTIONS_WIKI,
            "State assembly members are elected in single-member "
            "constituencies, and those state constituencies are divisions "
            "of the parliamentary Seats.",
        ),
    }


_PROSE_CSS = """
  .pk-learn-container { max-width: 720px; margin: 0 auto; padding: 2rem var(--gutter-mobile); }
  @media (min-width: 900px) { .pk-learn-container { padding: 4rem var(--gutter-desktop); } }
  .pk-proto-banner {
    margin: 0 0 1.6rem;
    padding: 0.85rem 1.1rem;
    border: 1px dashed var(--line-strong);
    background: var(--surface-soft);
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .03em;
    color: var(--ink-secondary);
    line-height: 1.55;
  }
  .pk-proto-banner a { color: var(--accent); }
  .pk-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--ink-secondary);
  }
  .opening { margin-bottom: clamp(24px, 4vw, 40px); }
  .opening h1 {
    font-family: var(--serif);
    font-weight: 500;
    font-size: clamp(32px, 4.5vw, 44px);
    letter-spacing: -.02em;
    margin: 8px 0 0;
  }
  .lede {
    font-family: var(--serif);
    font-size: 17px;
    line-height: 1.62;
    color: var(--ink-secondary);
    max-width: 64ch;
    margin: 12px 0 0;
  }
  .toc {
    list-style: none;
    padding: 0;
    margin: 20px 0 0;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  .toc li { margin: 0; }
  .toc a {
    display: inline-flex;
    align-items: center;
    min-height: 44px;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .04em;
    color: var(--ink-secondary);
    text-decoration: none;
    border: 1px solid var(--line);
    border-radius: var(--radius-sm);
    padding: 4px 12px;
  }
  .toc a:hover { color: var(--ink); border-color: var(--ink-secondary); }
  .term-entry { padding: clamp(34px, 5vw, 56px) 0 0; border-top: 1px solid var(--line-soft); }
  .opening + .term-entry { border-top: none; }
  .term-entry h2 {
    font-family: var(--serif);
    font-weight: 500;
    font-size: clamp(26px, 3.4vw, 36px);
    letter-spacing: -.015em;
    margin: 0 0 4px;
  }
  .gloss {
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-secondary);
    font-size: 15px;
    margin: 0 0 14px;
  }
  .prose p {
    font-family: var(--serif);
    font-size: 17px;
    line-height: 1.62;
    color: var(--ink);
    margin: 0 0 1em;
  }
  .prose p:last-child { margin-bottom: 0; }
  .prose p a {
    color: inherit;
    border-bottom: 1px solid var(--line);
    text-decoration: none;
  }
  .prose p a:hover { border-bottom-color: var(--ink-secondary); }
""".strip()


def _prose_body(claims: dict[str, str]) -> str:
    return f"""
<div class="pk-learn-container">
  <p class="pk-proto-banner">
    Register sample A — learn prose. Same facts as the
    <a href="act1-scroll.html">scrollcraft sample</a>.
    Not a live page. Compare from the
    <a href="./">chooser</a>. Issue #194.
  </p>
  <section class="opening">
    <div class="pk-eyebrow">Act 1 of a later walkthrough</div>
    <h1>You vote in a place</h1>
    <p class="lede">
      A vote is not cast into the whole country at once. It is cast in a
      place. That place is a Seat. In most of Malaysia it is also a DUN.
    </p>
    <ul class="toc">
      <li><a href="#a-seat">A Seat</a></li>
      <li><a href="#your-street">Your street</a></li>
      <li><a href="#a-dun">A DUN</a></li>
      <li><a href="#the-exception">The exception</a></li>
    </ul>
  </section>

  <section class="prose term-entry" id="a-seat">
    <h2>A Seat</h2>
    <p class="gloss">the unit a general election is won or lost in</p>
    <p>
      {claims["claim-seat-unit"]}
      {claims["claim-222"]}
      This walkthrough uses those words the same way the rest of the site
      does. For the longer glossary, see
      <a href="/learn/glossary.html#term-seat">Core terms</a>.
    </p>
  </section>

  <section class="prose term-entry" id="your-street">
    <h2>Your street</h2>
    <p class="gloss">the roll starts from an address</p>
    <p>
      You vote where you are registered. The register is tied to a place,
      not to a party or a Coalition.
      {claims["claim-street-in-seat"]}
      The home-page lookup uses that index. It may show more than one Seat
      for one postcode. That is a fact about postcodes, not a guess.
    </p>
  </section>

  <section class="prose term-entry" id="a-dun">
    <h2>A DUN</h2>
    <p class="gloss">the state assembly, next to the federal Seat</p>
    <p>
      {claims["claim-thirteen-states"]}
      {claims["claim-dun-is-state-assembly"]}
      {claims["claim-two-rolls"]}
      So in a state, the same voter is on the roll for one federal Seat
      and one DUN. The first chooses an MP for the Dewan Rakyat. The
      second chooses an ADUN for the state assembly. Those votes can fall
      on different days.
    </p>
  </section>

  <section class="prose term-entry" id="the-exception">
    <h2>The exception</h2>
    <p class="gloss">Federal Territories have no DUN</p>
    <p>
      {claims["claim-ft-no-dun"]}
      If you live in Kuala Lumpur, Labuan, or Putrajaya, this Act stops at
      the federal Seat. Do not read “often a DUN too” as a rule that
      covers every Malaysian voter.
    </p>
  </section>
</div>
""".strip()


_SCROLL_CSS = """
  .pk-scroll {
    max-width: 1080px;
    margin: 0 auto;
    padding: 28px var(--gutter-mobile) 80px;
  }
  @media (min-width: 900px) {
    .pk-scroll { padding: 40px var(--gutter-desktop) 96px; }
  }
  .pk-proto-banner {
    margin: 0 0 28px;
    padding: 0.85rem 1.1rem;
    border: 1px dashed var(--line-strong);
    background: var(--surface-soft);
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .03em;
    color: var(--ink-secondary);
    line-height: 1.55;
  }
  .pk-proto-banner a { color: var(--accent); }
  .scene {
    min-height: 72vh;
    display: grid;
    align-content: center;
    padding: 48px 0;
    border-top: 1px solid var(--line-soft);
  }
  .scene:first-of-type { border-top: 0; min-height: 62vh; }
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
    max-width: 16ch;
  }
  .scene h1 { font-size: clamp(44px, 8vw, 84px); line-height: 1.02; }
  .scene h2 { font-size: clamp(32px, 5vw, 56px); line-height: 1.08; }
  .scene .line {
    font-size: clamp(18px, 2.2vw, 24px);
    line-height: 1.45;
    max-width: 28ch;
    color: var(--ink-secondary);
    margin: 18px 0 0;
  }
  .scene .prose-claim {
    font-size: 16px;
    line-height: 1.55;
    max-width: 62ch;
    color: var(--ink);
    margin: 22px 0 0;
  }
  .place-track {
    margin-top: 36px;
    display: grid;
    gap: 10px;
    max-width: 420px;
  }
  .place-step {
    display: flex;
    align-items: center;
    gap: 14px;
    min-height: 52px;
    padding: 12px 16px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
  }
  .place-step b {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--accent);
    width: 4.5rem;
    flex: 0 0 auto;
  }
  .split {
    margin-top: 36px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }
  .split-card {
    padding: 22px 20px 20px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
    min-height: 180px;
  }
  .split-card .tag {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--accent);
  }
  .split-card h3 {
    font-size: 28px;
    letter-spacing: -.02em;
    margin: 10px 0 8px;
  }
  .split-card p {
    color: var(--ink-secondary);
    font-size: 15px;
    line-height: 1.5;
    margin: 0;
  }
  .caveat {
    margin-top: 14px;
    padding: 16px 18px;
    border-left: 3px solid var(--caution);
    background: var(--caution-bg);
    color: var(--ink);
    font-size: 15px;
    line-height: 1.5;
  }
  @media (max-width: 720px) {
    .split { grid-template-columns: 1fr; }
    .scene { min-height: 0; padding: 36px 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    .scene { min-height: 0; }
  }
""".strip()


def _scroll_body(claims: dict[str, str]) -> str:
    return f"""
<div class="pk-scroll">
  <p class="pk-proto-banner">
    Register sample B — scrollcraft scene. Same facts as the
    <a href="act1-prose.html">learn-prose sample</a>.
    Not a live page. Compare from the
    <a href="./">chooser</a>. Issue #194.
  </p>

  <section class="scene" id="open">
    <div class="pk-eyebrow">Act 1 of a later walkthrough</div>
    <h1>You vote in a place.</h1>
    <p class="line">Not into the whole country at once.</p>
  </section>

  <section class="scene" id="a-seat">
    <div class="pk-eyebrow">01 · A Seat</div>
    <h2>One street. One federal Seat.</h2>
    <p class="prose-claim">
      {claims["claim-seat-unit"]}
      {claims["claim-222"]}
    </p>
  </section>

  <section class="scene" id="your-street">
    <div class="pk-eyebrow">02 · The roll</div>
    <h2>The register starts from an address.</h2>
    <div class="place-track" aria-hidden="true">
      <div class="place-step"><b>Street</b> A place you already know</div>
      <div class="place-step"><b>Roll</b> The list of voters for that place</div>
      <div class="place-step"><b>Seat</b> The Dewan Rakyat constituency</div>
    </div>
    <p class="prose-claim">
      {claims["claim-street-in-seat"]}
    </p>
  </section>

  <section class="scene" id="a-dun">
    <div class="pk-eyebrow">03 · And often a DUN</div>
    <h2>Most voters also sit in a state assembly.</h2>
    <div class="split">
      <article class="split-card">
        <div class="tag">Federal</div>
        <h3>Seat</h3>
        <p>Chooses an MP for the Dewan Rakyat.</p>
      </article>
      <article class="split-card">
        <div class="tag">State</div>
        <h3>DUN</h3>
        <p>Chooses an ADUN for the state assembly.</p>
      </article>
    </div>
    <p class="prose-claim">
      {claims["claim-thirteen-states"]}
      {claims["claim-dun-is-state-assembly"]}
      {claims["claim-two-rolls"]}
    </p>
    <p class="caveat">
      {claims["claim-ft-no-dun"]}
    </p>
  </section>
</div>
""".strip()


_CHOOSER_CSS = """
  .pk-learn-container { max-width: 760px; margin: 0 auto; padding: 2rem var(--gutter-mobile); }
  @media (min-width: 900px) { .pk-learn-container { padding: 4rem var(--gutter-desktop); } }
  .pk-proto-banner {
    margin: 0 0 1.6rem;
    padding: 0.85rem 1.1rem;
    border: 1px dashed var(--line-strong);
    background: var(--surface-soft);
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: .03em;
    color: var(--ink-secondary);
    line-height: 1.55;
  }
  .opening h1 {
    font-family: var(--serif);
    font-weight: 500;
    font-size: clamp(32px, 4.5vw, 44px);
    letter-spacing: -.02em;
    margin: 8px 0 0;
  }
  .pk-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--ink-secondary);
  }
  .lede {
    font-family: var(--serif);
    font-size: 17px;
    line-height: 1.62;
    color: var(--ink-secondary);
    max-width: 64ch;
    margin: 12px 0 0;
  }
  .choice-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 32px;
  }
  .choice {
    display: block;
    padding: 22px 20px;
    border: 1px solid var(--line);
    background: var(--paper-alt);
    color: inherit;
    text-decoration: none;
    min-height: 180px;
  }
  .choice:hover { border-color: var(--ink-secondary); }
  .choice .tag {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--accent);
  }
  .choice h2 {
    font-size: 26px;
    letter-spacing: -.02em;
    margin: 10px 0 8px;
  }
  .choice p { color: var(--ink-secondary); font-size: 15px; line-height: 1.5; margin: 0; }
  @media (max-width: 720px) { .choice-grid { grid-template-columns: 1fr; } }
""".strip()


def _chooser_body() -> str:
    return """
<div class="pk-learn-container">
  <p class="pk-proto-banner">
    HITL register prototype for Act 1 only (issue #194). Same claims in both
    samples. Pick one register (or a mix) before the full walkthrough is written.
  </p>
  <section class="opening">
    <div class="pk-eyebrow">Civic walkthrough · Act 1</div>
    <h1>Which register should this story use?</h1>
    <p class="lede">
      Open both. The facts are the same. The question is how it should
      feel to a first-time voter.
    </p>
  </section>
  <div class="choice-grid">
    <a class="choice" href="act1-prose.html">
      <div class="tag">Sample A</div>
      <h2>Learn prose</h2>
      <p>The current /learn/ register: long paragraphs, a table of contents, section rules.</p>
    </a>
    <a class="choice" href="act1-scroll.html">
      <div class="tag">Sample B</div>
      <h2>Scrollcraft</h2>
      <p>Short lines, scene-by-scene, a visual split between Seat and DUN.</p>
    </a>
  </div>
</div>
""".strip()


def build_prose_page(updated_at: date, status: ElectionStatus) -> str:
    return render_shell(
        title="Act 1 sample A — learn prose | PolitikKu",
        description="Register prototype: Act 1 of the civic vote-path walkthrough, in the current learn-prose register.",
        active_nav="glossary",
        language=Language.EN,
        page_path="learn/prototypes/act1-prose.html",
        updated_at=updated_at,
        sources_count=0,
        status=status,
        body_html=f"<style>{_PROSE_CSS}</style>\n{_prose_body(_shared_claims())}",
        extra_head_script=_NOINDEX,
    )


def build_scroll_page(updated_at: date, status: ElectionStatus) -> str:
    return render_shell(
        title="Act 1 sample B — scrollcraft | PolitikKu",
        description="Register prototype: Act 1 of the civic vote-path walkthrough, as a scrollcraft scene.",
        active_nav="glossary",
        language=Language.EN,
        page_path="learn/prototypes/act1-scroll.html",
        updated_at=updated_at,
        sources_count=0,
        status=status,
        body_html=f"<style>{_SCROLL_CSS}</style>\n{_scroll_body(_shared_claims())}",
        extra_head_script=_NOINDEX,
        chrome=False,
    )


def build_chooser_page(updated_at: date, status: ElectionStatus) -> str:
    return render_shell(
        title="Act 1 register samples | PolitikKu",
        description="Compare two registers for Act 1 of the civic vote-path walkthrough.",
        active_nav="glossary",
        language=Language.EN,
        page_path="learn/prototypes/index.html",
        updated_at=updated_at,
        sources_count=0,
        status=status,
        body_html=f"<style>{_CHOOSER_CSS}</style>\n{_chooser_body()}",
        extra_head_script=_NOINDEX,
    )


def write_prototype_pages(*, output_dir: str = "public") -> list[Path]:
    """Write the three HITL samples under learn/prototypes/."""
    status = load_election_status()
    today = date.today()  # noqa: DTZ011
    dest = Path(output_dir) / "learn" / "prototypes"
    dest.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    pages = (
        ("index.html", build_chooser_page),
        ("act1-prose.html", build_prose_page),
        ("act1-scroll.html", build_scroll_page),
    )
    for name, builder in pages:
        path = dest / name
        path.write_text(builder(today, status), encoding="utf-8")
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Act 1 register prototypes")
    parser.add_argument("--output-dir", default="public")
    args = parser.parse_args()
    for path in write_prototype_pages(output_dir=args.output_dir):
        print(f"Wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
