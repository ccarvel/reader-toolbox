Limitations
===========

English-only models
--------------------

Every language model the Toolbox loads is hard-coded to English: ``en_core_web_sm`` and ``en_core_web_md`` for NER, POS tagging, keyword extraction, and summarization, and the English Flesch reading-ease formula for readability. There is no language detection step. Feeding the Toolbox a French, German, or other non-English document does not fail outright, but its output is close to meaningless: entities and parts-of-speech are guessed by a model trained on the wrong language, and non-English function words routinely surface as whole "topics" in ``tm`` output (see :doc:`usecases`, the DHQ use case, for a concrete example -- two of its seven topics are French and Spanish function words).

If your carrel is multilingual, treat any ``ent``, ``pos``, ``grammars``, ``readability``, or ``tm`` output for non-English documents as unreliable, and consider running those documents through a matching spaCy model (for example ``fr_core_news_md`` or ``de_core_news_md``) outside the Toolbox instead.

Stopword profile
------------------

``rdr build`` defaults to the ``neutral`` stopword profile: the standard NLTK English stopword list with every personal pronoun, possessive, and reflexive form removed, so no pronoun of any gender is ever silently dropped from ``ngrams``, ``tm``, ``cluster``, or ``semantics`` output. An older ``academic`` profile is available with ``-p academic``; it additionally drops journal/publishing jargon (``doi``, ``vol``, ``journal``, ...), but it also asymmetrically drops some gendered pronouns (``she``/``her``/``his``/``him``/``they``/``it``, but not ``he`` or ``i``) and drops ethnonym/color terms (``black``, ``white``, ``african``, ``american``, ``chinese``, ...). Choosing ``academic`` for literary or social analysis will silently bias frequency, topic, and embedding results toward that asymmetry. Both profiles are recorded in every carrel's provenance (see :doc:`structure`, ``index.tsv``) by name and by the SHA-256 of the exact word list used, so which profile built a given carrel is always recoverable.

Readability (Flesch) validity
-------------------------------

The ``readability``, ``sizes``, and ``info`` commands report the Flesch reading-ease score, computed with English syllabification and sentence-splitting rules applied uniformly to every document regardless of its actual language, genre, or condition. Three cases where the score is not meaningful:

* **Non-English text** -- see above; the syllable-counting heuristic is English-specific.
* **Verse and drama** -- the formula assumes prose sentence structure; line and speaker breaks are not accounted for.
* **OCR output** -- garbled or noisy OCR text produces an artificially low score because of spurious "words" and broken sentence boundaries, which can be a useful OCR-quality signal but should not be read as a genuine readability measurement.

The carrel-level score reported by ``info`` is an unweighted mean of each document's own integer score, not a word-weighted average.

Word embeddings and corpus size
----------------------------------

``semantics`` trains a fresh, from-scratch gensim ``Word2Vec`` model on your carrel's own text every time its cache is invalidated -- it does not draw on any pretrained embedding. Word2Vec needs a large amount of running text to place words reliably in a low-dimensional vector space; the docstring for ``rdr semantics`` puts the credible floor at about 1.5 million words. Below that, and especially for the single-book- or single-article-sized carrels the ``build`` documentation encourages, similarity, distance, and analogy results should be treated as unreliable regardless of how plausible any individual answer looks.

Memory guidance
------------------

Two commands can use substantially more memory than the size of their input text would suggest:

* **build** -- as of B2.4, each worker process loads its spaCy model once and parses each document once via ``nlp.pipe()``, with documents over 1,000,000 characters chunked at word boundaries before parsing. This measurably reduced peak memory (roughly 24% lower on a 175-document corpus in internal testing) and wall time, but it does not eliminate spaCy's own per-parse memory cost -- budget accordingly for large batches of long documents in parallel.
* **grammars** -- parses the *entire* concatenated carrel as a single spaCy ``Doc`` (via ``_carrel2doc()``), not per-document. This is a fundamentally different, much larger memory profile than ``build``'s per-document chunking and is not addressed by B2.4's fix: a single multi-million-word carrel can push peak RSS into multiple gigabytes. If ``rdr grammars`` is killed or hangs on a large carrel, this whole-corpus parse is the likely cause; there is currently no workaround short of running it on a machine with more RAM or against a smaller sub-carrel.
