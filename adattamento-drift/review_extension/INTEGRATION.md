# Integration for Emanuele Pio De Bernardis

This change belongs exclusively to **Paper 2: drift/adaptation**. It does not
change Paper 1, MCU firmware, the original replay implementation, or the original
October reports. The base is `81d99d9020d60b39d3b5a65fc6f06296f89537db`.

## Import the complete revision

The online delivery branch is `paper2/review-extension-20261101` in
`KuznetsovKarazin/kan-ids-v2`. It contains a results/code commit and the manuscript
delivery commit. The Git bundle also retains the original local development
history as `paper2/local-protocol-history`; this preserves the protocol and
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

If importing an email-format patch series instead, use the supplied numbered
patches with `git am` on a clean branch at the same base. Do not apply both the
bundle history and the patches: they are alternative transports of the same work.

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
- Keep cost weights fixed before evaluation. The five operating points are
  selected from past labels; they are not an oracle ROC frontier fitted on D.

## Reproduce and check

Follow `README.md` for the pinned environment and input reconstruction. First
run the 76-test targeted suite. Rebuild saved-evidence analysis with:

```bash
PY=.venv-review/bin/python
EXT=adattamento-drift/review_extension
$PY $EXT/manuscript/build_assets.py
$PY $EXT/analyze.py --results $EXT/results \
  --original $EXT/original_reports --out $EXT/analysis
cd "$EXT/manuscript"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

This analysis mode uses the retained time-partition manifest. Supply `--data`
to recompute it from reconstructed NPZs. To rerun predictions without refitting
initial models, use `rebuild_cache.py` as documented, then `run_campaign.py`.
The saved model states matter because a fresh numerical environment need not
reproduce the original initial fit bit for bit.

## Scientific changes to retain during integration

The new primary explanatory contrast is FIT192/CAL64 versus Frozen/CAL256.
On TON this trades recall for fewer false alarms; on UNSW it trades additional
false alarms for a small recall gain. Retain the original four-trace results,
failed acceptance criterion, seen/unseen decomposition, ARF and LR rows,
budget/delay sensitivity, provenance bridge and unfavorable outcomes.

Before journal submission, both authors must approve interpretation and
authorship, supply funding and competing-interest declarations, select the
journal's required format, and deposit the complete package if a permanent
archival identifier is needed. Those facts cannot be inferred from code.
