from datetime import date

from lpa.config import load_election_status
from lpa.politikku_shell import NAV_LINKS
from lpa.politikku_vote_path_prototype import (
    CLAIM_IDS,
    build_chooser_page,
    build_prose_page,
    build_scroll_page,
    write_prototype_pages,
)


def _pages() -> tuple[str, str, str]:
    status = load_election_status()
    day = date(2026, 1, 1)
    return (
        build_chooser_page(day, status),
        build_prose_page(day, status),
        build_scroll_page(day, status),
    )


def test_samples_are_noindex_and_not_in_nav() -> None:
    chooser, prose, scroll = _pages()
    for page in (chooser, prose, scroll):
        assert "noindex" in page
        assert "<!doctype html>" in page
    assert not any("prototypes" in link.href for link in NAV_LINKS)


def test_prose_and_scroll_share_the_same_claims() -> None:
    _, prose, scroll = _pages()
    for claim_id in CLAIM_IDS:
        marker = f'id="{claim_id}"'
        assert marker in prose
        assert marker in scroll
        prose_cite = prose.split(marker, 1)[1].split("data-cite=", 1)[1].split('"', 2)[1]
        scroll_cite = scroll.split(marker, 1)[1].split("data-cite=", 1)[1].split('"', 2)[1]
        assert prose_cite == scroll_cite
        prose_text = prose.split(marker, 1)[1].split(">", 1)[1].split("</span>", 1)[0]
        scroll_text = scroll.split(marker, 1)[1].split(">", 1)[1].split("</span>", 1)[0]
        assert prose_text == scroll_text


def test_registers_differ_in_layout_not_facts() -> None:
    _, prose, scroll = _pages()
    assert "term-entry" in prose
    assert 'class="toc"' in prose
    assert 'class="pk-header"' in prose
    assert 'class="scene"' in scroll
    assert 'class="split-card"' in scroll
    assert 'class="pk-bare"' in scroll
    assert "pk-learn-container" not in scroll


def test_write_prototype_pages(tmp_path) -> None:
    written = write_prototype_pages(output_dir=str(tmp_path))
    names = sorted(path.name for path in written)
    assert names == ["act1-prose.html", "act1-scroll.html", "index.html"]
    for path in written:
        assert "noindex" in path.read_text(encoding="utf-8")
