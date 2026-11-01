"""Checks for the first Materials and Methods and Results draft."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "genera_materiali_manoscritto.py"
ARTICLE = ROOT / "articolo_02"
ASSETS = ARTICLE / "manuscript_assets"
MANUSCRIPT = ARTICLE / "manuscript_methods_results.md"

SPEC = importlib.util.spec_from_file_location("genera_materiali_manoscritto", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _prose_words(text: str) -> int:
    lines = []
    for line in text.splitlines():
        if line.startswith(("|", "#", "![", "- ")):
            continue
        lines.append(line)
    return len(re.findall(r"\b[\w+/-]+\b", " ".join(lines)))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rgba_pixels(path: Path) -> tuple[tuple[int, int], bytes]:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        return rgba.size, rgba.tobytes()


def test_generator_reproduces_all_committed_assets(tmp_path):
    out = tmp_path / "assets"
    MODULE.generate(
        ARTICLE / "validazione_finale_D" / "analisi_finale.json",
        ROOT / "split_manifest.json",
        out,
    )
    expected = {
        "figure_1_causal_protocol.svg",
        "figure_2_paired_fp_fn.png",
        "figure_2_paired_fp_fn.svg",
        "manifest.json",
        "table_1_protocol.csv",
        "table_1_protocol.md",
        "table_2_results.csv",
        "table_2_results.md",
    }
    assert {p.name for p in out.iterdir()} == expected
    byte_exact = expected - {"figure_2_paired_fp_fn.png", "manifest.json"}
    for name in byte_exact:
        assert (out / name).read_bytes() == (ASSETS / name).read_bytes(), name
    assert _rgba_pixels(out / "figure_2_paired_fp_fn.png") == _rgba_pixels(
        ASSETS / "figure_2_paired_fp_fn.png"
    )

    generated = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    delivered = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    assert generated["schema"] == delivered["schema"] == 2
    assert generated["base_merge"] == delivered["base_merge"]
    assert generated["sources"] == delivered["sources"]
    assert generated["verification"] == delivered["verification"]
    assert [item["path"] for item in generated["products"]] == [
        item["path"] for item in delivered["products"]
    ]


def test_png_exact_sha_and_regenerated_pixels_are_distinct_checks(tmp_path):
    delivered = ASSETS / "figure_2_paired_fp_fn.png"
    recompressed = tmp_path / "figure_2_recompressed.png"
    with Image.open(delivered) as image:
        image.save(recompressed, format="PNG", compress_level=0)
    assert recompressed.read_bytes() != delivered.read_bytes()
    assert _rgba_pixels(recompressed) == _rgba_pixels(delivered)


def test_tables_in_manuscript_are_generated_verbatim():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    table1 = (ASSETS / "table_1_protocol.md").read_text(encoding="utf-8").strip()
    table2 = (ASSETS / "table_2_results.md").read_text(encoding="utf-8").strip()
    assert table1 in manuscript
    assert table2 in manuscript
    assert "352/355" in manuscript and "350/355" in manuscript
    assert "global BA" in manuscript


def test_paired_values_and_interpretation_are_preserved():
    data = json.loads((ARTICLE / "validazione_finale_D" / "analisi_finale.json").read_text(encoding="utf-8"))
    full = data["confronti"]["D_completo"]["principale_pesi"]
    unseen = data["confronti"]["D_non_visto_ABC"]["principale_pesi"]
    assert full["delta_fp"]["per_seme"] == [-84858.0, -89311.0, -73762.0, -77720.0, -81126.0]
    assert full["delta_fn"]["per_seme"] == [54175.0, -115380.0, 125148.0, -40935.0, -69284.0]
    assert unseen["delta_fp"]["per_seme"][2] == 3547.0
    assert unseen["delta_fn"]["per_seme"][2] == 59443.0
    text = MANUSCRIPT.read_text(encoding="utf-8")
    compact = " ".join(text.split())
    assert "seeds 43, 45, and 46" in compact
    assert "seed 44 worsened both" in compact
    assert "not met" in compact
    assert "This decomposition is post-hoc" in compact
    assert "does not establish that repeated vectors caused the reduction" in compact
    assert "principal `FIT192+CAL64 - frozen+CAL64` comparison" in compact


def test_draft_scope_length_and_causal_limits_are_explicit():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    words = _prose_words(text)
    assert 800 <= words <= 1250, words
    compact = " ".join(text.split())
    required = [
        "same chronological D stream",
        "not independent datasets",
        "not a confidence interval",
        "could affect predictions only from *k+2*",
        "D did not select the design or tune parameters",
        "does not remove repetitions within D",
        "`log1p(max(x,0))`",
        "seeded 400,000-record A subsample",
        "`C=1.0`, `max_iter=1000`",
        "A/B/C-unseen feature-vector subset",
        "complete final-evaluation command",
        "D had already been read for structural validation and direct A/B/C/D overlap checks",
        "predictive evaluation was run only after protocol and code were frozen",
    ]
    for phrase in required:
        assert phrase in compact
    assert "statistically significant" not in text.lower()
    assert "general superiority was demonstrated" not in text.lower()
    assert "recovered attacks" not in text.lower()
    assert "| Policy |" not in text


def test_manifest_and_figures_have_the_expected_provenance():
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == 2
    assert manifest["base_merge"] == "200a7985eb99d09926aa2e0c5b4606d0fa30ff4a"
    assert "no fit, replay, or tuning" in manifest["purpose"]
    assert len(manifest["products"]) == 7
    assert set(manifest["generation_environment"]) == {
        "python", "python_implementation", "platform", "numpy", "matplotlib",
        "matplotlib_backend", "pillow",
    }
    assert "exact delivered bytes" in manifest["verification"]["delivered_files"]
    assert "decoded RGBA pixels" in manifest["verification"]["regenerated_png"]
    for product in manifest["products"]:
        path = ASSETS / product["path"]
        assert path.stat().st_size == product["bytes"]
        assert _sha256(path) == product["sha256"]
    png = (ASSETS / "figure_2_paired_fp_fn.png").read_bytes()
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
    svg1 = (ASSETS / "figure_1_causal_protocol.svg").read_text(encoding="utf-8")
    svg2 = (ASSETS / "figure_2_paired_fp_fn.svg").read_text(encoding="utf-8")
    assert "effective from block k+2 only" in svg1
    assert "Requirements satisfied?" in svg1
    assert "Apply candidate state" in svg1
    assert "Keep previous state" in svg1
    assert "Next D block" in svg1
    assert "If requirements fail" not in svg1
    assert "Paired error differences across seeds" in svg2
