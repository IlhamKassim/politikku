from datetime import date
from pathlib import Path

from lpa.coalition_colors import party_color
from lpa.config import load_election_status
from lpa.politikku_shell import NAV_LINKS, Language
from lpa.politikku_vote_path import PAGE_PATH, build_vote_path_page, write_vote_path_pages

VOTE_PATH_JS = Path(__file__).resolve().parent.parent / "public" / "learn" / "vote-path.js"


def _pages() -> tuple[str, str]:
    status = load_election_status()
    day = date(2026, 1, 1)
    return (
        build_vote_path_page(Language.EN, day, status),
        build_vote_path_page(Language.MS, day, status),
    )


def test_vote_path_is_scrollcraft_and_in_nav() -> None:
    en, ms = _pages()
    for page in (en, ms):
        assert "<!doctype html>" in page
        assert 'class="pk-bare"' not in page
        assert 'id="sidebar"' in page
        assert 'id="topbar"' in page
        assert 'id="sb-vote-path" class="sb-item on"' in page
        assert 'class="scene"' in page
        assert 'class="split-card"' in page
        assert 'id="play-4"' in page
        assert "data-claim" in page
        assert "Kuala Lumpur" in page
        assert "Labuan" in page
        assert "Putrajaya" in page
    assert "Where does a vote go?" in en
    assert "Ke mana undi pergi?" in ms
    assert en.index("<h1>Where does a vote go?</h1>") < en.index('<nav class="act-nav"')
    assert any(link.key == "vote-path" and link.href == PAGE_PATH for link in NAV_LINKS)


def test_vote_path_is_four_plays() -> None:
    en, _ = _pages()
    assert 'id="play-1"' in en
    assert 'id="play-2"' in en
    assert 'id="play-3"' in en
    assert 'id="play-4"' in en
    assert 'id="vote-race"' in en
    assert 'id="vote-sim"' in en
    assert 'id="vote-bill"' in en
    assert 'id="play-compass"' in en
    assert "Why this count" in en
    assert "why-tap" in en
    assert "teaching Bill" in en
    assert "Campus Vote Bill" in en
    assert "Rang Undang-Undang Undi Kampus" not in en
    assert "bill-stage" in en
    assert "bill-continue" in en
    assert "data-div-floor" in en
    assert "claim-undi18-unanimous" in en
    assert "action=raw&amp;section=" in en
    assert "action=raw&section=" not in en
    assert "Need 112 first" not in en
    assert "Open the failed bill" in en
    assert "text-transform: lowercase" not in en
    assert "More info" in en
    assert "political compass" in en.lower()
    assert 'src="/learn/vote-path.js"' in en
    assert "Pakatan Rakyat" in en
    assert "will not name a Coalition for you" in " ".join(en.split())
    assert 'id="course-board"' not in en
    assert "data-proto-switch" not in en
    assert "You are watching" in en
    assert "This play assumes all 222 MPs vote" in en
    assert "it becomes law as if assent had been given" in en
    assert "sent back to Parliament with a list" not in en
    assert 'aria-current="step"' in en


def test_vote_path_connects_each_play_to_the_rest_of_the_site() -> None:
    en, ms = _pages()
    for href in (
        "/#find",
        "/app/",
        "/learn/coalitions.html",
        "/learn/glossary.html#term-seat",
        "/projection/",
        "/learn/glossary.html#term-majority",
        "/bills/",
        "/dewan/",
        "/learn/ge16-process.html",
    ):
        assert f'href="{href}"' in en
    for href in (
        "/ms/#find",
        "/app/",
        "/ms/learn/coalitions.html",
        "/ms/learn/glossary.html#term-seat",
        "/ms/projection/",
        "/ms/learn/glossary.html#term-majority",
        "/bills/",
        "/dewan/",
        "/ms/learn/ge16-process.html",
    ):
        assert f'href="{href}"' in ms


def test_vote_path_uses_the_shared_coalition_colors() -> None:
    en, _ = _pages()
    for code in ("PH", "PN", "BN", "GPS", "GRS"):
        assert f"--vote-{code.lower()}:{party_color(code)}" in en


def test_en_and_ms_are_different_copy() -> None:
    en, ms = _pages()
    assert "Your place" in en
    assert "Tempat anda" in ms
    assert "Campus Vote Bill" in en
    assert "Rang Undang-Undang Undi Kampus" in ms
    assert "Buka Rang Undang-Undang yang gagal" in ms
    assert "Open the failed bill" not in ms
    assert "belah bahagian" in ms.lower()
    assert "seolah-olah perkenan telah diberikan" in ms
    assert en.count("data-claim") == ms.count("data-claim")
    assert en.count("data-claim") >= 20


def test_vote_path_js_is_tracked() -> None:
    text = VOTE_PATH_JS.read_text(encoding="utf-8")
    assert "MAJORITY" in text
    assert "vote-compass" in text
    assert "data-sim-year" in text
    assert "data-race" in text
    assert "data-bill-next" in text
    assert "data-div-floor" in text
    assert "Need 112 first" not in text
    assert 'stack.innerHTML = \'<div class="stack-bar">\' + html + "</div>"' in text
    assert "dataset.variant" not in text
    assert "course-board" not in text
    assert "initCourseBoard" not in text
    assert "js-ready" in text
    assert "COLORS" not in text
    assert "#d7263d" not in text
    assert 'btn.setAttribute("aria-pressed", "true")' in text
    assert 'el.setAttribute("aria-current", "step")' in text
    assert "show(false)" in text
    assert "if (panel && shouldFocus)" in text


def test_write_vote_path_pages(tmp_path) -> None:
    written = write_vote_path_pages(output_dir=str(tmp_path))
    names = sorted(str(path.relative_to(tmp_path)) for path in written)
    assert names == [
        "learn/how-a-vote-works/index.html",
        "ms/learn/how-a-vote-works/index.html",
    ]
