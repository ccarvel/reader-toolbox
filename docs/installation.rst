Installation
============

The Reader Toolbox is a suite of Python scripts integrated into a single command-line interface, ``rdr``. It targets Python 3.10-3.12.

Two external, non-Python tools are required before you build your first carrel:

  * **Java 17** -- runs the bundled Apache Tika server that ``build`` uses for text extraction. Install it with, for example: ::

      brew install openjdk@17          # macOS
      apt-get install openjdk-17-jre   # Debian/Ubuntu

  * **MALLET** -- only needed for the ``tm`` (topic modeling) command. If it is not already configured, the first ``rdr tm`` run downloads and configures it for you.

This documentation describes `ccarvel/reader-toolbox <https://github.com/ccarvel/reader-toolbox>`_, a fork of
Eric Lease Morgan's original `ericleasemorgan/reader-toolbox <https://github.com/ericleasemorgan/reader-toolbox>`_
carrying correctness and fidelity fixes (see the project's ``CHANGELOG.md`` and the README's Credits section).
Those fixes aren't published to PyPI, so install from this fork to get them: ::

  pip install "reader-toolbox @ git+https://github.com/ccarvel/reader-toolbox.git@v1.2.0"

The original, unfixed upstream release is also on PyPI: ::

  pip install reader-toolbox

Or install a development checkout of this fork: ::

  git clone https://github.com/ccarvel/reader-toolbox.git
  cd reader-toolbox
  pip install -e .

spaCy language models and NLTK data
------------------------------------

The Toolbox depends on two spaCy models (``en_core_web_sm`` and ``en_core_web_md``) and three NLTK data packages (``punkt_tab``, ``averaged_perceptron_tagger_eng``, ``wordnet``).

NLTK data is downloaded automatically, with a notice on stderr, the first time a command that needs it (``ngrams``, ``sentences``, ``semantics``) runs.

spaCy models are **not** bundled with the ``spacy`` package and must be fetched separately. The Toolbox detects a missing model on first use and downloads it for you, using the same Python interpreter that is running ``rdr`` (so this works correctly inside a virtual environment). You can also install them yourself ahead of time: ::

  python -m spacy download en_core_web_sm
  python -m spacy download en_core_web_md

If you are using `uv <https://docs.astral.sh/uv/>`_ and pip is not available inside your environment, install the model wheel directly by URL instead. Running the failing command once will print the exact ``uv pip install <wheel URL>`` line to use for your installed spaCy version.

First run
---------

Once installed, run: ::

  rdr

The result should be a listing of every ``rdr`` subcommand: ::

  Usage: rdr [OPTIONS] COMMAND [ARGS]...

  Options:
    --help  Show this message and exit.

  Commands:
    adr          Filter email addresses from <carrel>
    bib          Output rudimentary bibliographics from <carrel>
    build        Create <carrel> from files in <directory>
    catalog      List study carrels ...
    cluster      Apply dimension reduction to <carrel> and visualize ...
    concordance  A poor man's search engine
    download     Cache <carrel> from the public library of study carrels
    edit         Modify the stop word list of <carrel>
    ent          Filter named entities and types of entities found in <carrel>
    get          Echo the values denoted by the set subcommand ...
    grammars     Extract sentence fragments from <carrel> ...
    info         Output metadata describing <carrel>
    ngrams       Output and list words or phrases found in <carrel>
    pos          Filter parts-of-speech, words, and lemmas found in <carrel>
    rdfgraph     Create RDF (Linked Data) file against <carrel>
    read         Open <carrel> in your Web browser ...
    readability  Report on the readability (Flesch score) of items in ...
    search       Perform a full text query against <carrel> ...
    semantics    Apply semantic indexing against <carrel> ...
    sentences    Given <carrel> save, output, and process sentences
    set          Configure the location of study carrels, the subsystem ...
    sizes        Report on the sizes (in words) of items in <carrel>
    summarize    Summarize <carrel> ...
    tm           Apply topic modeling against <carrel> ...
    url          Filter URLs and domains from <carrel>
    wrd          Filter statistically computed keywords from <carrel>
    zip          Create an archive (index.zip) file of <carrel>

See :doc:`commands` for the full reference, generated from this same ``--help`` output for every subcommand, and :doc:`exercise_01-quick_start` to build your first carrel.

Building your first carrel
---------------------------

Your first ``rdr build`` also needs to start Tika, so pass ``-s``: ::

  rdr build homer path/to/homer-files -s

If Tika has not been downloaded and configured yet, the Toolbox will do so automatically, and configuration is recorded in ``~/.rdrrc``. On success, you can then issue a subcommand like the following to display a human-readable catalog of every publicly available carrel in the Reader's public library: ::

  rdr catalog -h -l remote
