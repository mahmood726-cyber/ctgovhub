from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_hub_shell_contains_required_controls():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    required = [
        "<title>CT.gov Evidence Intelligence Hub</title>",
        'href="#main-content"',
        'id="tool-count"',
        'id="nct-input"',
        'id="quick-links"',
        "function toggleDark",
        "const TOOLS =",
    ]
    missing = [marker for marker in required if marker not in html]
    assert missing == []


def test_hub_links_expected_tools_and_validates_nct_ids():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    expected_tools = [
        "OutcomeSwitchDetector",
        "ProtocolEvolution",
        "TrialAtlas",
        "EnrollmentOracle",
        "Hiddenness Atlas",
        "TrialRadar",
        "CT.gov Search Strategies",
    ]
    missing = [tool for tool in expected_tools if tool not in html]
    assert missing == []
    assert r"^NCT\d{8}$" in html
    assert "{{" not in html
