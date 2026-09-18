

# Distant Reader Toolbox

A command-line interface for creating and interacting with [Distant Reader](https://distantreader.org) study carrels

> **This is a maintained fork.** [ccarvel/reader-toolbox](https://github.com/ccarvel/reader-toolbox) is
> [Cody Carvel](https://github.com/ccarvel)'s fork of Eric Lease Morgan's original
> [ericleasemorgan/reader-toolbox](https://github.com/ericleasemorgan/reader-toolbox), carrying a set of
> correctness and fidelity fixes found during an independent audit (`v1.1.2`, `v1.2.0`) on top of the
> upstream `1.1.1` release. The design, the pipeline, and the idea are Eric's — this fork only repairs and
> tightens what was already there. See [Changelog](#changelog) below and [Credits](#credits).

## Installation

This fork's fixes aren't on PyPI (only Eric's upstream releases are). To get them, install from this fork:

```
  # latest fixed release (recommended)
  pip install "reader-toolbox @ git+https://github.com/ccarvel/reader-toolbox.git@v1.2.0"

  # or the original, unfixed upstream release
  pip install reader-toolbox
```

## Quick start

```  
  # configure; accept the default
 rdr set -s local

  # add an item to your library
  rdr download homer

  # read homer
  rdr read homer

  # list all words
  rdr ngrams homer

  # list all bigrams
  rdr ngrams homer -s 2

  # list all bigrams and count them
  rdr ngrams homer -s 2 -c

  # search
  rdr concordance homer

  # search again, but specify a query
  rdr concordance homer -q war

  # list subject-verb-object fragments; please be patient
  rdr grammars homer

  # list noun phrases
  rdr grammars homer -g nouns

  # cluster; do the items in the carrel group themselves?
  rdr cluster homer

  # topic model; similar to cluster but with more detail
  rdr tm homer

  # page through additional carrels for downloading
  rdr catalog -l remote -h

  # download another carrel
  rdr download pride

  # download yet another carrel
  rdr download sonnets

  # list your carrels
  rdr catalog
```

## Description and background

The Reader Toolbox -- run from the command-line as ``rdr`` -- is designed to create and interact with Distant Reader study carrels. Using the Toolbox you can do things such as but not limited to:

   * search and browse the collection of more than 3,000 publicly available study carrels
   * download study carrels from the public collection and add them to your own collection
   * count & tabulate the most frequent ngrams (one-word, two-word, etc. phrases) occurring in study carrels
   * apply concordancing (keyword-in-context searching) against study carrels
   * apply topic modeling (extracting latent themes) against study carrels
   * extract information from your study carrels matching specific grammars
   * create your own study carrels
   * and more

In the end, the Toolbox empowers you to read, use, and understand large volumes of text quickly and easily.

## Changelog

Full detail, before/after metrics, and migration notes live in [CHANGELOG.md](CHANGELOG.md). Summary:

### v1.2.0 — fidelity, packaging, docs, notebooks
Changes analytical output for the first time in this fork; every item below is backed by a before/after
measurement, not just a description.

* Stopped lower-casing text before NER/POS/keyword/URL extraction (was silently dropping named entities like
  proper nouns and place names)
* Replaced the default stopword list, which asymmetrically dropped gendered pronouns and race/ethnonym terms,
  with a neutral profile; the original list survives as an opt-in `academic` profile
* Separated documents in `carrel.txt` so n-grams and concordance windows can no longer bleed across document
  boundaries
* One spaCy model load and one parse per document, instead of three
* Fixed `cluster()`'s misuse of SciPy `ward()` on a precomputed distance matrix
* Corrected `word2vec()`'s analogy direction
* Renamed MALLET's per-topic "weights" to `alpha` (a Dirichlet prior, not a share) and pie-charts real
  document-topic proportions instead
* Added a Penn-tag column to `pos` so `rdr pos -l J`-style filtering, already documented, actually works
* `concordance()` escapes queries by default, with new `-r`/`-i` flags for regex and case-insensitive search
* Dependencies declared directly with tested lower bounds; stale test suite replaced with a real mini corpus;
  CI added
* Documentation regenerated from live code (`commands.rst` can no longer drift); new `limitations.rst`
* All 45 notebooks cleaned of embedded output, with API drift and several bugs fixed

### v1.1.2 — correctness fixes
No analytical output changes except to repair broken behavior.

* Fixed a config `KeyError` that broke first-run setup right after the automatic Tika/MALLET download
* Numeric columns (`words`, `flesch`, `pages`) were sorting as text; now sort numerically
* Documents whose keyword extraction failed were silently dropped from `bib` and `search`; now logged, not lost
* Derived caches (`semantics`, `grammars`, `sentences`, search) now invalidate when `stopwords.txt` changes
* Closed SQL/FTS injection in `search`/`addresses`/`urls`/`pos`/`entities`
* MALLET is now invoked safely regardless of spaces or shell metacharacters in a carrel name
* Fixed the MALLET binary's file mode (a hex/octal typo), `urls()`'s crash and always-wrong counts, `bib -v`'s
  broken argument wiring, the topic-model scatter chart's impossible fixed perplexity, truncated SVO output, a
  `sys`/`sy` typo, a case-comparison bug in `entities()`, a mutated shared constant, invalid `-f` pivot fields,
  missing NLTK data provisioning, and spaCy model installs failing under `uv`

## Credits

All design, implementation, and the underlying idea of the study carrel are the work of
**[Eric Lease Morgan](https://github.com/ericleasemorgan)**, librarian at the Navari Family Center for Digital
Scholarship, Hesburgh Libraries, University of Notre Dame, who has built and maintained the Distant Reader
project and this toolbox since 2021. This fork exists only to fix defects found during an independent
verification pass — it doesn't change what the toolbox does or why, only how faithfully it does it. Thank you,
Eric, for building and sharing this. See [About the author](https://reader-toolbox.readthedocs.io/en/latest/author.html)
for more.

## Links

   * this fork: [https://github.com/ccarvel/reader-toolbox](https://github.com/ccarvel/reader-toolbox)
   * original download (PyPI, upstream): [https://pypi.org/project/reader-toolbox](https://pypi.org/project/reader-toolbox)
   * original documentation (upstream): [https://reader-toolbox.readthedocs.io](https://reader-toolbox.readthedocs.io)
   * original source code (upstream): [https://github.com/ericleasemorgan/reader-toolbox](https://github.com/ericleasemorgan/reader-toolbox)
   * original bug tracker (upstream): [https://github.com/ericleasemorgan/reader-toolbox/issues](https://github.com/ericleasemorgan/reader-toolbox/issues)
   * this fork's issues/PRs: [https://github.com/ccarvel/reader-toolbox/issues](https://github.com/ccarvel/reader-toolbox/issues)

---
Original toolbox by Eric Lease Morgan &lt;emorgan@nd.edu&gt;, January 5, 2023.  
This fork maintained by Cody Carvel, correctness/fidelity fixes as of September 2026 (see [CHANGELOG.md](CHANGELOG.md)).
