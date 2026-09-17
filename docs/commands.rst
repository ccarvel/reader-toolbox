Commands
========

This page is generated directly from each command's own ``--help`` text via `sphinx-click <https://sphinx-click.readthedocs.io/>`_, so it cannot drift from the live CLI. A CI job diffs ``rdr --help``'s command list against this page on every build and fails if they disagree.

.. click:: rdr.rdr:rdr
   :prog: rdr
   :nested: full

Removed commands
-----------------

The following commands existed in earlier releases but were removed from the CLI in commit ``ec84060`` ("Purging many things", 2026-05-27) and no longer exist:

* ``about`` -- echoed a one-line description of the Toolbox
* ``browse`` -- perused a carrel like a file system, via Lynx locally or a manifest listing remotely
* ``collocations`` -- built a bigram co-occurrence network graph (NLTK ``BigramAssocMeasures``)
* ``documentation`` -- opened this documentation site in a Web browser
* ``notebooks`` -- opened the bundled Jupyter notebooks
* ``play`` -- played a game of hangman
* ``sql`` -- opened a Datasette-backed SQL prompt against ``etc/carrel.db``
* ``web`` -- started the Flask-based Web server (``rdr/server.py``, deleted in the same commit)

Any exercise or example referencing these commands elsewhere in this documentation predates their removal.
