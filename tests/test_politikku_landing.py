"""Tests for the Observatory landing page integration."""

import hashlib
import re
from datetime import date

from lpa.bill_tracker import Bill
from lpa.domain import ElectionStatus
from lpa.politikku_landing import (
    APP_URL,
    CoalitionRow,
    LandingModel,
    build_and_write_landing_pages,
    deep_link_script,
    render_landing_body,
    render_landing_page,
)
from lpa.politikku_shell import Language

STATUS = ElectionStatus(constitutional_deadline=date(2028, 2, 17), source="test")
ROWS = (
    CoalitionRow("PH", 75, "#d7263d", True),
    CoalitionRow("BN", 41, "#1f9bd6", True),
    CoalitionRow("GPS", 23, "#b8332e", True),
    CoalitionRow("GRS", 7, "#e8772e", True),
    CoalitionRow("PN", 69, "#15387c", False),
)
BILLS = (
    Bill(
        code="D.R.22/2026",
        title="RUU Kumpulan Wang Amanah Negara 2026",
        year=2026,
        stage="Lulus",
        stage_date=date(2026, 7, 16),
        summary="Summary",
        summary_source_url="https://example.com/bill.pdf",
    ),
)


def model() -> LandingModel:
    return LandingModel(
        government_majority=True,
        coalitions=ROWS,
        bills=BILLS,
        majority_threshold=112,
        total_seats=222,
        updated_at=date(2026, 9, 9),
        sources_count=7,
        status=STATUS,
    )


def test_observatory_body_uses_the_reference_scenes():
    body = render_landing_body(model())
    assert "A nation." in body
    assert "In perspective." in body
    assert "Many places." in body
    assert "One Parliament." in body
    assert "Follow the source." in body
    assert "The bigger picture" in body
    assert body.count('class="seat-dot"') == 222


def test_observatory_body_keeps_the_platform_lookup_contract():
    body = render_landing_body(model())
    for attr in (
        "data-pk-lookup-scope",
        "data-pk-lookup-form",
        "data-pk-lookup-input",
        "data-pk-locate",
        "data-pk-lookup-results",
    ):
        assert attr in body
    assert 'data-pk-lookup-results role="status" aria-live="polite" hidden' in body
    assert 'for="pk-lookup-q"' in body
    assert 'id="pk-lookup-q"' in body


def test_observatory_page_is_a_standalone_landing_document():
    page = render_landing_page(model())
    assert page.count("<main") == 1
    assert page.count("<header") == 1
    assert page.count("<footer") == 1
    assert 'id="sidebar"' not in page
    assert 'id="topbar"' not in page
    assert 'href="/assets/observatory/style.css?v=' in page
    assert 'src="/lookup.js"' in page


def test_observatory_css_and_js_links_carry_their_files_fingerprint(tmp_path):
    """A browser may reuse a cached file for ten minutes after a deploy; each
    link names the published file's content hash, so new HTML can't pick up
    old CSS. Checked against the files the build actually writes."""
    build_and_write_landing_pages(tmp_path)
    for index in (tmp_path / "index.html", tmp_path / "ms" / "index.html"):
        links = re.findall(r'(?:href|src)="(/assets/observatory/[^"]+)"', index.read_text())
        # Fonts and artwork are not fingerprinted: their bytes never change
        # under the same name, so a cached copy is always the right copy.
        tagged = [
            link for link in links if not link.endswith((".woff2", ".png", "krackeddevs.svg"))
        ]
        assert len(tagged) == 5, tagged
        for link in tagged:
            path, _, query = link.partition("?")
            published = tmp_path / path.lstrip("/")
            digest = hashlib.sha256(published.read_bytes()).hexdigest()[:10]
            assert query == f"v={digest}", link


def test_observatory_links_into_the_current_platform():
    page = render_landing_page(model())
    assert f'href="{APP_URL}"' in page
    assert 'href="/bills/"' in page
    assert 'href="/methodology.html"' in page
    assert 'href="/dewan/"' in page
    assert 'href="/politicians/"' in page
    assert 'href="/projection/"' in page
    assert 'href="/learn/glossary.html"' in page
    assert 'href="/learn/how-a-vote-works/"' in page
    assert "Explore Suara" not in page


def test_observatory_landing_page_has_social_and_structured_metadata():
    page = render_landing_page(model())
    assert 'property="og:image" content="https://politikku.my/og-image.png"' in page
    assert 'name="twitter:card" content="summary_large_image"' in page
    assert '"@type": "WebSite"' in page


def test_observatory_has_bilingual_root_documents():
    en = render_landing_page(model(), Language.EN)
    ms = render_landing_page(model(), Language.MS)
    assert '<html lang="en">' in en
    assert '<html lang="ms">' in ms
    assert 'href="/" aria-current="page" data-pk-set-lang="en"' in en
    assert 'href="/ms/" aria-current="page" data-pk-set-lang="ms"' in ms
    assert "Sebuah negara." in ms
    assert "Dalam perspektif." in ms
    assert "Cari kerusi anda" in ms


def test_local_observatory_hashes_are_not_forwarded_to_the_map():
    script = deep_link_script()
    assert "location.hash" in script
    assert "#(?:top|perspective|chamber|evidence|find)" in script
    assert "location.replace('/app/' + location.hash)" in script


def test_build_copies_the_observatory_runtime_and_image(tmp_path):
    build_and_write_landing_pages(tmp_path)
    assert (tmp_path / "index.html").is_file()
    assert (tmp_path / "ms" / "index.html").is_file()
    for name in (
        "base.css",
        "style.css",
        "scrollcraft.css",
        "scrollcraft.js",
        "integrated.js",
        "skyline.png",
        "skyline-768.webp",
        "skyline-1024.webp",
        "skyline-1280.webp",
        "skyline-1536.webp",
        "icon.svg",
    ):
        assert (tmp_path / "assets" / "observatory" / name).is_file(), name


def test_every_hero_image_width_is_served_from_the_site_root(tmp_path):
    """The hero art is the page's heaviest download and its LCP element, so it
    ships as three WebP widths behind a srcset with the PNG as the fallback. A
    rewrite that only caught the first path left the other two pointing at
    `assets/skyline-*.webp`, relative to whatever directory the page sits in —
    404 on /ms/, and the browser silently falling back to the 2.2MB PNG."""
    build_and_write_landing_pages(tmp_path)

    for page in (tmp_path / "index.html", tmp_path / "ms" / "index.html"):
        body = page.read_text()
        picture = re.search(r"<picture>.*?</picture>", body, re.DOTALL)
        assert picture, f"no <picture> in {page}"
        markup = picture.group(0)
        for width in (768, 1024, 1280, 1536):
            assert f"/assets/observatory/skyline-{width}.webp" in markup
        assert 'src="/assets/observatory/skyline.png"' in markup
        assert '"assets/skyline' not in markup


def test_the_footer_credits_krackeddevs_in_both_languages(tmp_path):
    """The wordmark is drawn in bright greens for a dark background, so it sits
    on a dark chip inside the lime footer. Its path is rewritten to the site
    root the same way the hero art is — a relative `assets/` path 404s on /ms/."""
    build_and_write_landing_pages(tmp_path)

    for page, label in (
        (tmp_path / "index.html", "Supported by"),
        (tmp_path / "ms" / "index.html", "Disokong oleh"),
    ):
        markup = page.read_text()
        assert label in markup
        assert 'href="https://krackeddevs.com/" target="_blank" rel="noopener"' in markup
        assert 'src="/assets/observatory/krackeddevs.svg"' in markup
        assert '"assets/krackeddevs.svg"' not in markup

    assert (tmp_path / "assets" / "observatory" / "krackeddevs.svg").is_file()


def test_the_supporter_sheen_is_gated_on_the_sites_motion_switch(tmp_path):
    """`integrated.js` clears `js-motion` from the root both when a reader hits
    "Pause motion" and when they have prefers-reduced-motion set. An animation
    that isn't scoped to that class keeps running through either one."""
    build_and_write_landing_pages(tmp_path)
    css = (tmp_path / "assets" / "observatory" / "style.css").read_text()

    for rule in re.findall(r"[^{}]*supporter-mark[^{}]*\{[^{}]*animation:[^{}]*\}", css):
        assert rule.lstrip().startswith(".js-motion"), rule

    # The reveal rule carries four classes; the hover rule has to match that
    # scope or it silently loses and the sheen never replays on hover.
    assert ".js-motion .supporter.is-in .supporter-mark:hover::after{" in css


def test_the_nav_only_lists_destinations_not_scroll_positions(tmp_path):
    """ "The perspective" and "The 222 Seats" jumped to sections of the page the
    reader was already on, sitting in a row of links that otherwise go
    somewhere. The sections stay: /analyst/ deep-links back to both."""
    build_and_write_landing_pages(tmp_path)

    for page in (tmp_path / "index.html", tmp_path / "ms" / "index.html"):
        body = page.read_text()
        nav = re.search(r'<nav class="nav-links".*?</nav>', body, re.DOTALL)
        assert nav, f"no nav in {page}"
        hrefs = re.findall(r'href="([^"]+)"', nav.group(0))
        # #find is the call to action, the one anchor that earns its place.
        assert [h for h in hrefs if h.startswith("#")] == ["#find"], hrefs
        assert 'id="perspective"' in body
        assert 'id="chamber"' in body
