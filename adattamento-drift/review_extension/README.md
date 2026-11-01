# Paper 2: second-review article, diagnostics and integration package

This extension answers **what learning changes beyond a recent threshold, and
where the resulting FN/FP trade-off occurs**. Read `PROTOCOL.md` before using
the results. The original October campaign and the November extension are
distinct evidence stages. The extension contains 55 complete runs: 30 main
dataset/model/seed combinations, five legacy-query bridges, fifteen additional
delay runs, and five low-budget runs.

## Second-review extension

The current article evaluates threshold policy, baseline quality and error
compromises in two previously inspected captures. `review2/` adds 120 fixed
cells: 80 spline settings, 10 LR main cells and 30 ARF initialization/label-use
cells. Thirty cells repeat the earlier main trajectories; they are checks, not
independent replication. The original 55 reports are immutable.

- `manuscript/main.tex` / `main.pdf`: compact current article.
- `manuscript/supplement.tex` / `supplement.pdf`: historical development and full
  diagnostic tables, including first-extension results.
- `review2/PROTOCOL.md`, `runner.py`, `campaign.py`, `test_runner.py`: new design,
  causal controllers and regression tests.
- `review2/results/`: all 120 full reports, audits and execution logs.
- `review2/models/`: ten additional fitted shuffled-A forest states.
- `review2/analysis/`: exact repeat checks, AP, dense cost grid, matched-error
  descriptions, calibration transfer, memory/age/minimum/salt sensitivity.
- `REVIEW_RESPONSE.md`: all three current reviews, including qualifications to
  reviewer interpretations; prior response is preserved separately.
- `ARCHIVE_PREPARATION.md`: exact remaining archival status and deposit metadata.

## First-extension contents

- `manuscript/main.tex`, `references.bib`, and `main.pdf`: revised article.
- `PROTOCOL.md`: design committed before new predictive outcomes.
- `experiment.py`: paired causal controllers and standard ARF baseline.
- `prepare_data.py`, `fetch_data.py`: input reconstruction and mirror hashes.
- `run_campaign.py`: all pre-specified cells, with per-job logs.
- `analyze.py`: numerical invariants, paired differences, tables and figures.
- `test_experiment.py`: leakage, query pairing, threshold/intercept invariance,
  prior-centred objective, and exact duplicate reuse tests.
- `results/`: every full compressed extension report.
- `original_reports/`: all five original reports and their summary.
- `models/`: the fitted initial states used by this extension, with metadata.
- `analysis/`: per-seed and aggregate CSVs, interactions, resampling sensitivity,
  time partitions, resource accounting, and verification manifest.
- `provenance/`: source/array digests and recorded reconstruction checks.
- `REVIEW_RESPONSE.md`: point-by-point response and remaining author-only facts.
- `INTEGRATION.md`: concrete commands for Emanuele to import the commit series.

## Build the paper from saved evidence

First verify the shipped files without loading model pickles:

```bash
python adattamento-drift/review_extension/verify_artifacts.py
```

The LaTeX directory is self-contained and can be imported into Overleaf.

```bash
cd adattamento-drift/review_extension/manuscript
make all
```

To rebuild numerical assets from the complete saved reports, from the repository root:

```bash
python -m venv .venv-review
.venv-review/bin/pip install -r adattamento-drift/review_extension/requirements.txt
.venv-review/bin/python adattamento-drift/review_extension/manuscript/build_assets.py
.venv-review/bin/python adattamento-drift/review_extension/analyze.py \
  --results adattamento-drift/review_extension/results \
  --original adattamento-drift/review_extension/original_reports \
  --out adattamento-drift/review_extension/analysis
.venv-review/bin/python adattamento-drift/review_extension/review2/analyze.py
```

`main.tex`, `supplement.tex` and the generated tables/figures do not require raw data to compile.
Add `--data /path/to/reconstructed-data` to recompute the time-partition manifest
from raw reconstruction; otherwise the retained provenance manifest is used.
On Windows use `.venv-review\Scripts\python.exe` and the corresponding `pip.exe`.

## Reconstruct inputs and run all experiments

Allow roughly 5 GB for raw mirrors and additional space for cached arrays.
Use external working directories, so raw traffic is not committed to Git.

```bash
PY=.venv-review/bin/python
EXT=adattamento-drift/review_extension
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
$PY $EXT/fetch_data.py ton --out /path/to/downloads
$PY $EXT/fetch_data.py unsw --out /path/to/downloads
$PY $EXT/prepare_data.py ton --raw /path/to/downloads/ton_raw --out /path/to/data/ton
$PY $EXT/prepare_data.py unsw --raw /path/to/downloads/unsw_raw --out /path/to/data/unsw
$PY $EXT/experiment.py inventory --data /path/to/data/ton
$PY $EXT/experiment.py inventory --data /path/to/data/unsw
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 $PY $EXT/run_campaign.py \
  --data-root /path/to/data --cache-root /path/to/cache \
  --out /path/to/new-results --workers 2
```

The protocol pins seeds, feedback, controls and cost weights. The forest uses
10 trees with River 0.22.0 defaults; it learns all arriving queried labels.
Its persistent model state and training reuse of CAL observations are disclosed
in the paper. Do not describe it as a 256-example total-memory baseline.

The driver resumes completed files. If a process was forcibly interrupted while
writing a report, remove that incomplete report before resuming. Run `analyze.py`
without `--allow-incomplete` to require all 55 reports and verify them. The
preview flag is for development only and must never be used for final claims.

To reuse the supplied fitted initial states, rebuild their immutable inference
caches before calling the campaign driver:

```bash
$PY $EXT/rebuild_cache.py --data /path/to/data/ton --models $EXT/models/ton \
  --cache /path/to/cache/ton --provenance $EXT/provenance/ton
$PY $EXT/rebuild_cache.py --data /path/to/data/unsw --models $EXT/models/unsw \
  --cache /path/to/cache/unsw --provenance $EXT/provenance/unsw
```

This checks all D array digests and avoids refitting the initial models. The
ordinary `prepare` command refits models and may vary across numerical
environments. Pickles are generated by this package and must only be loaded
from a trusted, hash-verified copy.

To reproduce the second-review cells, first restore the original 30 models
using the commands above, then restore the ten new forest states:

```bash
$PY $EXT/rebuild_cache.py --data /path/to/data/ton --models $EXT/review2/models/ton \
  --cache /path/to/cache/ton --provenance $EXT/provenance/ton
$PY $EXT/rebuild_cache.py --data /path/to/data/unsw --models $EXT/review2/models/unsw \
  --cache /path/to/cache/unsw --provenance $EXT/provenance/unsw
$PY $EXT/review2/campaign.py --data-root /path/to/data --cache-root /path/to/cache \
  --out /path/to/review2-rerun --workers 2
$PY $EXT/review2/analyze.py --results /path/to/review2-rerun \
  --out /path/to/review2-analysis
```

`review2/analyze.py` requires all 120 cells unless explicitly given `--partial`.
It checks the executed runner hash, counts, timing, AP validity coverage and
exact old main-trajectory decisions. The retained `analysis/validation.json`
records complete status. AP is collected for main/shuffled/FIT-only cells;
parameter-sensitivity cells retain AUC and confusion counts. Logs and source
hashes of the excluded AP-guard attempt are documented in `review2/provenance`.
Only the corrected results are shipped as final evidence.

## Validation and interpretation

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv-review/bin/python -m pytest -q \
  adattamento-drift/review_extension/test_experiment.py \
  adattamento-drift/review_extension/review2/test_runner.py \
  adattamento-drift/ton_temporal/test_calibrazione_recente.py \
  adattamento-drift/ton_temporal/test_soglia.py \
  adattamento-drift/ton_temporal/test_replay_validazione_finale.py
```

The recorded targeted suite has 89 passing tests (76 earlier tests plus 13 new diagnostics). Analysis verifies every
block/stream count reconciliation, seen+unseen decomposition, common query
sequence, and intercept/threshold invariance. Original source CSV hashes and
all 710 D row/label block digests match. A reconstruction using the unmodified
original A parser matches the extension output byte for byte.

The old Windows NPZ hashes and all old per-seed predictions are **not** reproduced
bitwise in this Linux reconstruction. `analysis/legacy_replication_bridge.csv`
quantifies the discrepancy. Keep the original results unchanged and cite the
extension separately. The new fixed cost grid is a set of causal operating
policies; it is not a threshold selected retrospectively from D labels.

Seed SDs are conditional randomization variability. Moving-block percentiles
summarize recorded errors without refitting the adaptive state; they are not
generalization confidence intervals. Runtime logs include offline caching and
are not embedded-device latency measurements.

The authors still need to supply study-specific funding/competing-interest
declarations and approve authorship before submission. No archival DOI has
been fabricated. The machine-readable evidence and integration commit are
ready for publication in the project repository and a suitable research archive.
