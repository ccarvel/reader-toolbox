# Changelog

All notable changes to the Distant Reader Toolbox (`reader-toolbox` / `rdr`)
are documented here. This file was started in Plan B3 (2026-09-17); entries
before that date are backfilled from `git log`, PyPI's release history, and
the audit in `handoff/reader-toolbox-analysis.md`, since none of the earlier
releases had their own changelog.

## [Unreleased]

Two fork branches are complete and pending release as part of this repo's
remediation effort (see `handoff/reader-toolbox-handoff.md`); neither has
been tagged or published yet.

### 1.1.2 (patch, correctness only — `b1-correctness-fixes`, 17 commits)
No analytical output changes except to repair it. Fixes a config `KeyError`
after first-run Tika/MALLET download, lexicographic (non-numeric) sorting
of `words`/`flesch`/`pages`, silent document loss from failed keyword
extraction, stale derived caches, SQL/FTS injection in `search`/`addresses`/
`urls`/`pos`/`entities`, shell-interpolated MALLET invocations (carrel names
with spaces or metacharacters), the MALLET binary's file mode (`0x755` typo
→ `0o755`), `urls()`'s `NameError` and always-1 counts, `bib -v`'s broken
argument wiring, the topic-model scatter chart's fixed perplexity, truncated
SVO grammar output, a `sys`/`sy` typo, `ent -l`'s case-comparison-instead-of-
assignment bug, a mutated module-level `LABELS` constant, invalid `-f` pivot
fields, missing NLTK data provisioning, and spaCy model installation under
`uv`.

### 1.2.0 (minor, fidelity — `b2-fidelity-fixes`, 9 commits)
Changes analytical output; ships with before/after metrics for every item.
Stops lower-casing text before NER/POS/keywords/URL extraction; replaces the
default stopword list with a neutral profile (the original list survives as
an opt-in `academic` profile); separates documents in `carrel.txt` with a
form feed so n-grams and concordance windows can't cross a document
boundary; loads the spaCy model once per worker process instead of three
times per document; fixes SciPy `ward()` misuse in `cluster()`; corrects
`word2vec()`'s analogy direction; renames MALLET's per-topic "weights"
(actually alpha, a Dirichlet prior) to `alpha` and pie-charts real
document-topic proportions instead; adds a Penn-tag column to `pos` so
`rdr pos -l J`-style fine-grained filtering works; and escapes
`concordance()` queries by default with new `-r`/`-i` flags for regex and
case-insensitive search.

## [1.1.1] — commit dated 2026-06-26, published to PyPI 2026-06-26
Version-string bump only (`setup.cfg`); no functional changes noted in the
commit message. Published to PyPI the same day as 1.1.0 (below) and an
apparently accidental `0.0.0` upload — all three releases share a publish
date despite 1.1.0 having been committed to the repo over two years
earlier. Yanking the stray `0.0.0` release is the maintainer's call, not
this fork's.

## [1.1.0] — commit dated 2024-05-12, published to PyPI 2026-06-26
Version-string bump only (`setup.cfg`). Sits after a substantial run of
undocumented (commit messages like "???", "Grrr") changes between the 1.0
line and this one, including the `reader.db`/`reader.txt` → `carrel.db`/
`carrel.txt` rename (`8c4c8bf`, 2024-03-26) and later the removal of the
`about`, `browse`, `collocations`, `documentation`, `notebooks`, `play`,
`sql`, and `web` commands and the Flask web server (`ec84060`, "Purging
many things", 2026-05-27) — none of which is reflected in a version bump
of its own.

## [1.0.0] and earlier
Not backfilled in detail. `setup.cfg`'s version history goes back to
`0.0.2` (2021-08-15); see `git log -p -- setup.cfg` for the full sequence
of version-string commits if a more complete history is ever needed.
