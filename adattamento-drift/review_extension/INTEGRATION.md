# Integration for Emanuele Pio De Bernardis

This change belongs exclusively to **Paper 2: drift/adaptation**. It does not
change Paper 1, MCU firmware, the original replay implementation, or the original
October reports. The base is `81d99d9020d60b39d3b5a65fc6f06296f89537db`.

## Import the complete revision

The online delivery branch is `paper2/review-extension-20261101` in
`KuznetsovKarazin/kan-ids-v2`. It contains the first-extension commits and new second-review code/results
and manuscript commits. The delivery manifest records the exact final heads. The Git bundle also retains the original local development
history as `paper2/local-protocol-history` and the new pre-run history as
`paper2/review2-protocol-history`; this preserves the protocol and
runner commits made before the new outcomes were inspected. From your existing `kan-ids-v2` checkout:

```bash
git bundle verify /path/to/Paper2_review_extension.bundle
git fetch /path/to/Paper2_review_extension.bundle \
  paper2/review-extension-20261101:paper2/review-extension-20261101
git switch paper2/review-extension-20261101
git log --oneline 81d99d9..HEAD
```

Review or open a pull request from this branch. To integrate onto a later main,
create a new branch from main and cherry-pick the series in chronological order:

```bash
git switch -c paper2/integrate-review main
git cherry-pick $(git rev-list --reverse 81d99d9..paper2/review-extension-20261101)
```

The bundle additionally carries the local-history ref. Import it when auditing
protocol timing:

```bash
git fetch /path/to/Paper2_review_extension.bundle \
  paper2/local-protocol-history:paper2/local-protocol-history
```

That history retains the protocol commit `f4ec381`,
created before inspecting the new predictive outcomes. `178e069` contains the
executed runner; `19892b0` corrects the test for River's benign metric-dictionary
cache behavior. The published results commit is `54871f0f36b22a69fe9a114a617d957b896da7b1`,
whose tree exactly matches local evidence commit `33341bc`. The delivery manifest
lists both histories and the final manuscript commit. The reports also carry the exact SHA-256 of the executed runner.
The new diagnostic protocol is `67239e4`; the initial diagnostic runner is
`bcac962`; `d6c82ec` fixes the AP validity guard before the retained diagnostic
results. The corrected runner SHA-256 is
`81537d6add508cf9f852b756d596c0cb85020fa5edf3a5ba9abcb6e768d0bca9`.
The first extension runner remains byte-identical.

The current results archive supplies a Git bundle as its complete transport.
It includes model states and recorded evidence once, avoiding duplicate large
binary patches. The small CSV previews are also directly accessible in the ZIP.

The second-review code/results commit is `dd9e0ea8bb2d8c9d8283e752e8a059b104291390`. Its tree matches
local evidence commit `7538cf0869fb713efc247703a1d5d8b12bef1a4b`.
The subsequent manuscript commit is recorded in the external delivery manifest.

## What plugs into the existing code

`review_extension/experiment.py` imports the unchanged `ton_temporal/replay.py`,
`calibrazione_recente.py` and `soglia_bilanciata.py`. It reuses their transform,
model representation, immutable roles, replay memory, atomic head transaction
and exact threshold tie rule. The extension adds controllers around those
interfaces, preserving the historical campaign behavior.

- Keep `calibrazione_recente.proponi_transazione` and `applica_transazione` as
  the matched FIT192/CAL64 path.
- Keep `all_cal` separate: it receives all acquired labels and independently
  controls Frozen/CAL256. Do not restrict it to the CAL role or head gate.
- Use `query_indices` for new studies; keep the `legacy` switch only to compare
  the archived October query identities. Never relabel the new results as the
  old campaign.
- Preserve the prediction → query → delayed arrival → update order. No new
  state can affect a prediction that has already been emitted.
- Keep ARF's practical baseline contract explicit: all arrived queried labels
  are learned once, CAL labels are reused, and the model has persistent memory.
  Its thresholds 0.5, B, CAL64 and CAL256 are separate reporting traces.
- Keep cost weights fixed before evaluation. The nine second-review operating points are
  selected from past labels; they are not an oracle ROC frontier fitted on D.

## Reproduce and check

Follow `README.md` for the pinned environment and input reconstruction. First
run the 89-test targeted suite (include `review2/test_runner.py`). Rebuild saved-evidence analysis with:

```bash
PY=.venv-review/bin/python
EXT=adattamento-drift/review_extension
$PY $EXT/manuscript/build_assets.py
$PY $EXT/analyze.py --results $EXT/results \
  --original $EXT/original_reports --out $EXT/analysis
$PY $EXT/review2/analyze.py
cd "$EXT/manuscript"
make all
```

This analysis mode uses the retained time-partition manifest. Supply `--data`
to recompute it from reconstructed NPZs. To rerun predictions without refitting
initial models, use `rebuild_cache.py` as documented, then `run_campaign.py`.
The saved model states matter because a fresh numerical environment need not
reproduce the original initial fit bit for bit.

## Scientific changes to retain during integration

The primary question now compares complete operating policies, rather than
using the lambda=1 contrast as a general head advantage. Keep the cost grid,
matched-error descriptions and causal FPR-target results together. Preserve
the poor LR/ARF initial-state audits, shuffled-A and FIT-only forest controls,
CAL-memory/age/minimum and role-salt sensitivity, and all unfavorable outcomes.
The historical 3/5 count and numerical bridge's 2/5 are both required. The
LR 4/5 is exploratory and uses a different comparator. Neither five seeds nor
a second already-known capture creates a pristine prospective validation.

`review2/runner.py` imports the unchanged first-extension runner. Its initial
cache lookup accepts the supplied `arf_shuffled_<seed>` folders. Use the same
`rebuild_cache.py` for these states, pointing `--models` at `review2/models/<ds>`.
The FIT-only forest learns only FIT-role arrivals and calibrates on CAL64;
it retains persistent trees and must not be described as equal-memory.

Before journal submission, both authors must approve interpretation and
authorship, supply funding and competing-interest declarations, select the
journal's required format, and deposit the complete package if a permanent
archival identifier is needed. Those facts cannot be inferred from code.
