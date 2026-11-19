"""Check that agent skill packages have valid, discoverable entrypoints.

No third-party code or software is executed by this test.
"""
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILLS=ROOT/'.agents'/'skills'
EXPECTED={
    'parametric-part-cad','agentscad-fdm-dfam','tolerance-stackup',
    'machine-element-sizing','linkage-synthesis','dfm-review',
    'design-review-package','parametric-3d-printing','skill-creator',
    'orcaslicer-mcp-skills','opengrid-interface-engineering','fusion-mcp',
    'bambu-studio-slicing','freecad-openscad','mesh-validation'
}

def test_expected_skills_present():
    names={p.name for p in SKILLS.iterdir() if p.is_dir() and (p/'SKILL.md').is_file()}
    assert names==EXPECTED

def test_valid_frontmatter_and_name_matches_folder():
    for name in sorted(EXPECTED):
        data=(SKILLS/name/'SKILL.md').read_text(encoding='utf-8')
        assert data.startswith('---\n'), name
        header=data.split('\n---\n',1)[0]
        match=re.search(r'^name:\s*(\S+)\s*$',header,re.M)
        assert match and match.group(1)==name, (name,match.group(1) if match else None)
        assert re.search(r'^description:\s*\S+',header,re.M),name

def test_native_interface_guard_and_docs():
    rules=(SKILLS/'opengrid-interface-engineering'/'SKILL.md').read_text(encoding='utf-8').lower()
    assert 'upstream' in rules and 'physical' in rules and 'snap' in rules
    assert (ROOT/'docs'/'MCP_INTEGRATIONS.md').exists()
    assert (ROOT/'docs'/'THIRD_PARTY_SKILLS.md').exists()
