from datetime import date

from lpa.config import load_election_status
from lpa.politikku_shell import NAV_LINKS, Language
from lpa.politikku_vote_path import PAGE_PATH, build_vote_path_page, write_vote_path_pages


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
        assert 'class="pk-bare"' in page
        assert 'class="scene"' in page
        assert 'class="split-card"' in page
        assert 'id="act-6"' in page
        assert "data-claim" in page
        assert "Kuala Lumpur" in page
        assert "Labuan" in page
        assert "Putrajaya" in page
    assert "Where does a vote go?" in en
    assert "Ke mana undi pergi?" in ms
    assert any(link.key == "vote-path" and link.href == PAGE_PATH for link in NAV_LINKS)


def test_vote_path_has_attributed_why_and_long_act_six() -> None:
    en, _ = _pages()
    assert "Why this count" in en
    assert "Why a Government Coalition" in en
    assert "Dewan Negara was built for a federation" in en
    assert "Head of state, not a Seat" in en
    assert "A third branch, not this walkthrough" in en
    assert "political compass" not in en.lower()
    assert "simulator" not in en.lower()


def test_en_and_ms_are_different_copy() -> None:
    en, ms = _pages()
    assert "You vote in a place" in en
    assert "Anda mengundi di suatu tempat" in ms
    assert en.count("data-claim") == ms.count("data-claim")
    assert en.count("data-claim") >= 20


def test_write_vote_path_pages(tmp_path) -> None:
    written = write_vote_path_pages(output_dir=str(tmp_path))
    names = sorted(str(path.relative_to(tmp_path)) for path in written)
    assert names == [
        "learn/how-a-vote-works/index.html",
        "ms/learn/how-a-vote-works/index.html",
    ]
