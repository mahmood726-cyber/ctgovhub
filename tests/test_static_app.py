import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read_html():
    return (ROOT / "index.html").read_text(encoding="utf-8")


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


def test_div_balance_and_script_integrity():
    html = _read_html()
    open_divs = len(re.findall(r"<div[\s>]", html))
    close_divs = len(re.findall(r"</div>", html))
    assert open_divs == close_divs, f"div imbalance: {open_divs} open vs {close_divs} close"
    # No literal closing script tag that would prematurely terminate the inline script.
    body = html.split("<script>", 1)[1]
    assert "</script>" in body  # the legitimate terminator exists
    # Exactly one <script> block and one terminator.
    assert html.count("<script>") == 1
    assert html.count("</script>") == 1


def test_dark_toggle_reflects_state():
    html = _read_html()
    # Button carries an id and initial pressed state for accessibility.
    assert 'id="dark-toggle"' in html
    assert 'aria-pressed="false"' in html
    # Toggle logic keeps the button label/aria in sync with the theme.
    assert "function syncDarkToggle" in html
    assert "'Light Mode'" in html


def test_persistence_key_is_unique():
    html = _read_html()
    assert "ctgov_hub_preferences" in html
