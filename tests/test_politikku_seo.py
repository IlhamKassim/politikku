"""Tests for PolitikKu SEO metadata generation."""

from __future__ import annotations

from datetime import date

from lpa.politikku_seo import (
    SITE_URL,
    get_metadata_for_mp,
    get_metadata_for_section,
)
from lpa.politikku_shell import Language


def test_dewan_seo_metadata() -> None:
    en = get_metadata_for_section("dewan", Language.EN)
    assert "Dewan Rakyat" in en.title
    assert en.canonical_url == f"{SITE_URL}dewan/"
    assert en.alternate_ms_url == f"{SITE_URL}ms/dewan/"
    assert 'rel="alternate" hreflang="en"' in en.head_html()

    ms = get_metadata_for_section("dewan", Language.MS)
    assert "Aktiviti Dewan Rakyat" in ms.title
    assert ms.canonical_url == f"{SITE_URL}ms/dewan/"
    assert ms.alternate_en_url == f"{SITE_URL}dewan/"


def test_projection_dataset_json_ld() -> None:
    en = get_metadata_for_section("projection", Language.EN)
    assert en.canonical_url == f"{SITE_URL}projection/"
    types = [ld.get("@type") for ld in en.json_ld]
    assert "Dataset" in types
    assert "WebSite" in types
    html = en.head_html()
    assert "projection.json" in html
    assert "projection.csv" in html


def test_projection_dataset_has_recommended_fields() -> None:
    """Search Console flags a Dataset with no `creator` as a non-critical issue."""
    for language in (Language.EN, Language.MS):
        dataset = next(
            ld
            for ld in get_metadata_for_section("projection", language).json_ld
            if ld.get("@type") == "Dataset"
        )
        assert dataset["creator"] == {
            "@type": "Organization",
            "name": "PolitikKu",
            "url": SITE_URL,
        }
        assert dataset["license"]
        assert dataset["isAccessibleForFree"] is True


def test_projection_dataset_date_modified() -> None:
    en = get_metadata_for_section("projection", Language.EN, date(2026, 9, 15))
    dataset = next(ld for ld in en.json_ld if ld.get("@type") == "Dataset")
    assert dataset["dateModified"] == "2026-09-15"
    assert '"dateModified": "2026-09-15"' in en.head_html()

    # Omitted rather than guessed when no computed date is supplied.
    plain = get_metadata_for_section("projection", Language.EN)
    plain_dataset = next(ld for ld in plain.json_ld if ld.get("@type") == "Dataset")
    assert "dateModified" not in plain_dataset


def test_mp_profile_person_json_ld() -> None:
    en = get_metadata_for_mp("P.102", Language.EN)
    assert en.canonical_url == f"{SITE_URL}mp/P.102/"
    assert en.alternate_ms_url == f"{SITE_URL}ms/mp/P.102/"
    types = [ld.get("@type") for ld in en.json_ld]
    assert "Person" in types
    html = en.head_html()
    assert "Bangi" in html
    assert "Member of Parliament" in html


def test_politicians_seo_metadata_uses_seat() -> None:
    en = get_metadata_for_section("politicians", Language.EN)
    assert "Seat" in en.description
    assert "constituency" not in en.description.lower()
