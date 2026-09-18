Structure of a carrel
=====================

It can not be stated strongly enough, *the Distant Reader Toolbox takes a set of unstructured data (files of narrative text) as input, and it outputs a set of structured data -- a "study carrel" -- intended to be computed against.*

Each study carrel is a data set, and like all other data sets, they are purposely designed to address research questions. Once you understand the structure and content of study carrels, you will be able to address research questions not explicitly addressed by the various Toolbox commands and functions.

First and foremost, the vast majority of the files in a study carrel are plain text files. The only files you can not open and make sense of in your text editor are the various image files found in the ``figures`` directory and the SQLite relational database file (``carrel.db``) found in the ``etc`` directory. Consequently, given any study carrel, the student, researcher, or scholar can compute against it (ask it questions) using a myriad of applications or programming languages: any spreadsheet or database application, OpenRefine for tabular data analysis, Wordle for word clouds, AntConc for concordancing, Gephi for network analysis and visualization, or Topic Modeling Tool for topic modeling.

Second, each study carrel is contained in a single directory with the following consistently named subdirectories and files:

  * adr
  * bib
  * cache
  * ent
  * etc
  * figures
  * index.csv
  * index.htm
  * index.tsv
  * pos
  * readme.txt
  * txt
  * urls
  * wrd

The following sections describe the type of content found in each directory and file.

adr
---

Email addresses

This subdirectory contains a set of tab-delimited files, one per document. Each file's name ends in ``.adr``, and the files have two columns:

   1. **id** - the unique identifier of a document in the carrel

   2. **address** - an email address


bib
---

Bibliographics

This subdirectory contains a set of tab-delimited files, one per document, named with a ``.bib`` extension. The files have thirteen columns:

   1. **id** - the unique identifier of the document; rooted in the name of the original file sans its extension

   2. **author** - the name(s) of the creator(s) of the document; from an optional ``metadata.csv`` file supplied at build time, or extracted from the original document by the Tika server, or empty

   3. **title** - the title of the document; from ``metadata.csv``, extracted by Tika, or the original filename sans extension

   4. **date** - the date of the document; from ``metadata.csv``, extracted by Tika, or empty

   5. **pages** - the number of pages Tika reports for the original document, when the format has a notion of pages

   6. **extension** - the original file's extension (``.pdf``, ``.docx``, etc.)

   7. **mime** - the MIME type Tika detected for the original file

   8. **words** - the number of words in the document

   9. **sentence** - the number of sentences in the document

   10. **flesch** - the document's Flesch reading-ease score, an integer where values closer to 100 are easier to read

   11. **summary** - a computed extractive summary of the document

   12. **cache** - the path, relative to the carrel, of the original file in ``cache/``

   13. **txt** - the path, relative to the carrel, of the plain-text version of the file in ``txt/``

The underlying ``bib`` table also has a fourteenth column, **genre**, declared in the schema but populated only when a ``metadata.csv`` file supplies a ``genre`` value at build time; otherwise it is empty.


cache
-----

Original input files

This subdirectory contains original copies of the files given for analysis, named with a unique and somewhat meaningful name and extension. These files are intended for reading on your computer, or printed and read in the traditional manner.


ent
---

Named entities

This subdirectory contains a set of tab-delimited files, one per document, named with a ``.ent`` extension. The files have five columns:

   1. **id** - the unique identifier of the document

   2. **sid** - the sentence number (0-indexed) the entity occurs in, per spaCy's sentence segmentation of that document

   3. **eid** - the entity's position (0-indexed) among the entities extracted from that document

   4. **entity** - the entity text, in its original case (see :doc:`limitations`)

   5. **type** - the entity's spaCy label (``PERSON``, ``GPE``, ``ORG``, etc.)


etc
---

Miscellaneous and derived files

This directory holds the carrel's database, corpus file, stopword list, and every lazily-computed cache. None of these files exist until the command that produces them is first run, except ``carrel.db``, ``carrel.txt``, and ``stopwords.txt``, which ``build`` always creates.

   1. **carrel.db** - the SQLite database distilling ``adr``, ``bib``, ``ent``, ``pos``, ``urls``, and ``wrd`` into relational tables of the same names, plus an empty ``questions`` table and, after the first ``search``, ``fulltext`` and the FTS5 virtual table ``indx``

   2. **carrel.txt** - every document's plain text concatenated together, whitespace-collapsed, with documents separated by a form-feed (``\n\f\n``) so ``ngrams`` and ``concordance`` do not span document boundaries

   3. **stopwords.txt** - the carrel's stopword list; ``neutral`` by default or ``academic`` if ``-p academic`` was given to ``build`` (see :doc:`limitations`); editable with ``rdr edit``

   4. **cache.json** - records a SHA-256 of ``stopwords.txt`` plus the newest ``txt/`` file's mtime for each lazily-cached feature (semantic index, ``grammars`` pickle, sentences, search index); a mismatch on the next run invalidates and rebuilds that cache automatically, or force it early with ``-r``/``--refresh`` where the command supports it

   5. **carrel.vec** - the word2vec (gensim) embedding model, built on first use of ``semantics``

   6. **carrel.sents** - extracted sentences, one per line, built on first use of ``sentences``

   7. **carrel.tok** - tokenized sentences used to train ``carrel.vec``

   8. **reader.spacy** - the whole corpus parsed as one spaCy ``Doc`` and pickled via textacy, built on first use of ``grammars``

   9. **topic-model/** - MALLET's output directory, built on first use of ``rdr tm``; includes ``keys.tsv`` (topics, each with a Dirichlet ``alpha`` and its top words), ``topics.tsv`` (per-document topic proportions, no header row), ``documents.txt``, ``diagnostics.xml``, and ``model-state.gz``

   10. **carrel.authors**, **carrel.wrds** - Wikidata Q-ID lookup tables consulted by ``rdfgraph``; empty until hand-populated (see the ``rdfgraph`` entry in :doc:`commands`)


figures
-------

Graphics and visualizations

PNG word clouds, boxplots, histograms, and dendrogram/cube images generated by ``-w``/``-v``/``-o`` flags on various commands and by ``rdr summarize``.


index.csv
---------

A verbatim copy of the ``metadata.csv`` file supplied at build time, if one was given; absent otherwise.


index.htm
---------

The carrel's summary dashboard, generated by ``rdr summarize``. Absent until that command is first run.


index.tsv
---------

Provenance

A tab-delimited file with eight unlabeled columns, written once at build time and never updated:

   1. the process used to create the carrel (always ``toolbox``)
   2. the name of the carrel when it was created
   3. the date the carrel was created, ``yyyy-mm-dd``
   4. the local time the carrel was created, ``hh:mm``
   5. the username of the person who created the carrel
   6. the path to the directory of original files used to create the carrel
   7. the stopword profile used (``neutral`` or ``academic``)
   8. the SHA-256 of that profile's stopword list


pos
---

Parts-of-speech

This subdirectory contains a set of tab-delimited files, one per document, named with a ``.pos`` extension. The files have seven columns:

   1. **id** - the unique identifier of the document

   2. **sid** - the sentence number (0-indexed) the token occurs in

   3. **tid** - the token's position (0-indexed) within that sentence

   4. **token** - the token text, in its original case (see :doc:`limitations`)

   5. **lemma** - the token's lemma (root form)

   6. **pos** - the token's spaCy Universal part-of-speech tag (``NOUN``, ``VERB``, ``ADJ``, etc.)

   7. **tag** - the token's Penn Treebank fine-grained tag (``NN``, ``VBD``, ``JJ``, etc.); ``rdr pos -l`` matches against ``pos`` OR ``tag``, so ``-l J`` (adjectives) works even though no Universal POS value begins with J. Carrels built before this column existed simply have no ``tag`` values; ``rdr pos`` degrades gracefully and matches on ``pos`` alone for them.


readme.txt
----------

A short, embedded usage guide written into every carrel at build time.


txt
---

Plain text versions of cached items

This subdirectory contains a plain-text version of every file in ``cache``, produced by Tika. This is the text every analysis command actually reads.


urls
----

Universal Resource Locators

This subdirectory contains a set of tab-delimited files, one per document, named with a ``.url`` extension. The files have three columns:

   1. **id** - the unique identifier of the document

   2. **domain** - the URL's domain, in its original case

   3. **url** - the full URL, in its original case (see :doc:`limitations`)


wrd
---

Statistically significant keywords

This subdirectory contains a set of tab-delimited files, one per document, named with a ``.wrd`` extension. The files have two columns:

   1. **id** - the unique identifier of the document

   2. **keyword** - a keyword or phrase computed per-document by YAKE (not a corpus-relative TF-IDF score; see :doc:`limitations`)
