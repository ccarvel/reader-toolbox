Python Notebooks
================

The Toolbox ships 45 Jupyter notebooks under ``notebooks/`` demonstrating its Python API (``from rdr import ...``) directly, without the ``rdr`` command line.

As of the most recent headless run (``pytest --nbmake``), 12 of the 45 notebooks pass unmodified and 33 fail, mostly from API drift: renamed functions (``rdr.clusters``/``rdr.ngramss``/``rdr.searching``/``rdr.concordancing`` no longer exist; the current names are ``cluster``/``ngrams``/``search``/``concordance``), a removed ``rdr.getNLTKText`` helper, hard-coded paths from the original author's machine, and a few unrelated bugs also found independently during verification (a ``NaN``-author crash in ``search()``, a missing ``pyLDAvis.sklearn`` import path).

A full per-notebook triage -- labeling each as *works*, *fixable*, or *retire*, stripping embedded output, fixing the API drift above, and parameterizing each notebook's carrel name so all of them run headless against a small CI-sized carrel -- is tracked as Plan B5 and has not been done yet. This page will carry the resulting index table (notebook, purpose, required extras, status) once that triage completes.
