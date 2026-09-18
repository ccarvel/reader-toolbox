Python Notebooks
================

The Toolbox ships 45 Jupyter notebooks under ``notebooks/`` demonstrating its Python API (``from rdr import ...``) directly, without the ``rdr`` command line. Most default their carrel parameter to ``mini``, the small public-domain corpus committed at ``tests/fixtures/mini/`` and built once by CI before the notebooks run (see ``.github/workflows/ci.yml``); you can build it yourself locally with ``rdr build mini tests/fixtures/mini``.

CI runs 35 of the 45 (``pytest --nbmake``, ~105 seconds). The other 10 call ``rdr.download()`` or ``rdr.catalog(location='remote')`` against the real public library at distantreader.org; even on a runner with genuine outbound network, distantreader.org itself proved unreliable enough from a CI IP (``BadZipFile``/``JSONDecodeError`` from truncated or error-page responses, confirmed 2026-09-18) that they're excluded from the CI run (``--ignore`` in ``.github/workflows/ci.yml``) rather than left flaking the job. They are **not known-broken** -- every failure traced to the network layer, not a code bug -- and the notebook files themselves are untouched; they still work for local or manual use against a real network. None of the 45 notebooks are labeled *retire* -- every one that could be run headlessly against ``mini`` has been fixed to do so.

.. list-table::
   :header-rows: 1
   :widths: 22 45 13 20

   * - Notebook
     - Purpose
     - Extras
     - Status
   * - ``000-preface``
     - Preface (prose only, no code)
     - --
     - works
   * - ``001-introduction-part-i``
     - Tour of the ``rdr`` Python API (provenance, extents, bibliography, cluster, ngrams, concordance, word2vec) against a real downloaded carrel
     - --
     - needs network
   * - ``010-catalog-reader-library``
     - Remote catalog browsing (prose + a remote ``rdr.catalog()`` call)
     - --
     - needs network
   * - ``015-ngrams``
     - Remote n-gram frequency and word-cloud queries (``location='remote'``)
     - --
     - needs network
   * - ``020-download``
     - Download a carrel from the public library
     - --
     - needs network
   * - ``021-catalog-your-library``
     - Build a local library by downloading several real carrels
     - --
     - needs network
   * - ``022-sizes``
     - Carrel size (word count) reporting
     - --
     - works
   * - ``023-readability``
     - Flesch readability reporting
     - --
     - works
   * - ``024-bibliographics``
     - Bibliography listing (self-downloads its carrel if absent)
     - --
     - needs network
   * - ``025-urls``
     - URL extraction (self-downloads its carrel if absent)
     - --
     - needs network
   * - ``026-email-addresses``
     - Email-address extraction (self-downloads its carrel if absent)
     - --
     - needs network
   * - ``030-parts-of-speech``
     - Parts-of-speech filtering
     - --
     - works
   * - ``035-named-entities``
     - Named-entity filtering
     - --
     - works
   * - ``036-keywords``
     - Statistically significant keyword listing
     - --
     - works
   * - ``038-concordance``
     - Keyword-in-context search
     - --
     - works
   * - ``039-search``
     - Full-text search API tour
     - --
     - works
   * - ``095-build``
     - Build, cluster, and summarize a carrel from raw files (the author's own sandbox notebook)
     - --
     - works
   * - ``101-introduction-part-ii``
     - Introduction, part II (prose only, no code)
     - --
     - works
   * - ``103-provenance``
     - Read and format a carrel's ``index.tsv`` provenance record
     - --
     - works
   * - ``105-size-matters``
     - Compare word counts across every locally cached carrel
     - --
     - works
   * - ``106-feature-extraction-with-textacy``
     - Direct textacy feature extraction (KWIC, readability, ngrams, YAKE, entities, SVO, noun chunks) on a raw spaCy ``Doc``
     - --
     - works
   * - ``107-sql``
     - Raw SQL against a carrel's SQLite database
     - --
     - works
   * - ``108-catalog``
     - Remote catalog bibliography listing
     - --
     - needs network
   * - ``109-harvest``
     - Download and extract a remote carrel's zip archive directly
     - --
     - needs network
   * - ``110-dispersion-plots-with-nltk``
     - NLTK dispersion plot via ``rdr.getNLTKText()``
     - --
     - works
   * - ``120-collocations-with-nltk``
     - NLTK collocations via ``rdr.getNLTKText()``
     - --
     - works
   * - ``130-sentence-extraction-and-saving``
     - Grammar experiment #1: sentence extraction
     - --
     - works
   * - ``133-listing-subject-verb-object-like-sentences``
     - Grammar experiment #2: SVO-pattern sentence matching
     - --
     - works
   * - ``136-exracting-modal-verb-sentences``
     - Grammar experiment #3: modal-verb sentence matching
     - --
     - works
   * - ``140-named-entites-to-network-graph``
     - Build a person/place co-occurrence edge table from ``ent`` via raw SQL
     - --
     - works
   * - ``142-keywords-to-network-grapgh``
     - Build a document/keyword edge table from ``wrd`` via raw SQL
     - --
     - works
   * - ``150-topic-modeling-with-pyldavis``
     - scikit-learn LDA topic modeling visualized with pyLDAvis
     - notebooks (pyLDAvis)
     - works
   * - ``155-keywords-by-date``
     - Keyword frequency trends by publication year via raw SQL
     - --
     - works
   * - ``160-make-subcarrel``
     - Build a smaller carrel from another carrel's search results
     - --
     - works
   * - ``170-find-all``
     - Regex pattern matching over ``rdr.getNLTKText()``
     - --
     - works
   * - ``201-introduction-part-iii``
     - Introduction, part III (prose only, no code)
     - --
     - works
   * - ``205-gentle-introduction``
     - Tokenization and frequency counting from scratch with plain Python
     - --
     - works
   * - ``210-bibliography``
     - Full bibliography report via raw SQL
     - --
     - works
   * - ``215-frequencies``
     - Token frequency counting and tabulation
     - --
     - works
   * - ``220-wordclouds``
     - Word-cloud rendering from raw token frequencies
     - --
     - works
   * - ``230-parts-of-speech``
     - NLTK POS tagging, chunking, and a frequency-based word cloud
     - --
     - works
   * - ``240-nltk``
     - Introductory NLTK tokenization and frequency analysis
     - --
     - works
   * - ``242-nltk-redux``
     - ``240`` revisited with a second carrel for comparison
     - --
     - works
   * - ``250-urls``
     - URL and domain listing via raw SQL
     - --
     - works
   * - ``260-keywords``
     - Keyword frequency listing and word cloud via raw SQL
     - --
     - works

Fixed this pass (B5): renamed-function API drift (``rdr.clusters``/``ngramss``/``searching``/``concordancing`` -> ``cluster``/``ngrams``/``search``/``concordance``); ``pyLDAvis.sklearn`` -> ``pyLDAvis.lda_model``; ``getNLTKText()`` re-added to the API; stale ``reader.db``/``reader.txt``/``provenance.tsv`` filenames; hardcoded ``/Users/eric/...`` paths; ``multiprocessing.Pool`` inside a Jupyter kernel (fragile, replaced with serial processing); ``textacy.TextStats`` (removed class) -> ``textacy.text_stats``; several notebooks' genuinely undefined names (``160``'s ``if metadata.exists :`` always-true bug, ``230``'s missing ``LIBRARY``/``ETC``/``TEXT``/``WIDTH``/``HEIGHT``/``COLOR``, ``109``'s undefined ``TEMPLATE``/``ZIP``/``CARRELS``, rewritten to call the already-correct ``rdr.download()``); browser-opening ``rdr.read()`` calls commented out for headless/CI safety.
