import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_all_catalog_entries_are_distinct_anchored_repositories():
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    projects = data["repositories"]
    assert len(projects) == data["total"]
    assert len(projects) >= 82
    assert len(set(entry["name"] for entry in projects)) == len(projects)
    for entry in projects:
        assert entry["url"] == "https://github.com/mahmood726-cyber/" + entry["name"]
        assert entry["group"]


def test_all_featured_paths_match_real_case_sensitive_repo_names():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for name in ("outcomeswitchdetector", "protocolevolution",
                 "trialatlas", "enrollmentoracle", "trialradar"):
        assert "../" + name + "/" in html
    for obsolete in ("../OutcomeSwitchDetector/", "../ProtocolEvolution/",
                     "../TrialAtlas/", "../EnrollmentOracle/", "../TrialRadar/"):
        assert obsolete not in html


def test_no_unimplemented_nct_query_parameters_are_promised():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Official trial record" in html
    assert "manual review" in html
    assert "t.param" not in html
    assert "verified automatic NCT-parameter lookup" in html


def test_catalog_rendering_uses_safe_dom_text_and_empty_state():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for marker in ('id="catalog-search"', 'id="catalog-group"',
                   'id="catalog-list"', 'id="catalog-more"', "fetch('catalog.json')",
                   'link.textContent = project.name', 'catalogList.replaceChildren()'):
        assert marker in html
    assert "Repository catalogue could not load" in html
