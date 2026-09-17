Supporting software
===================

This Toolbox is really an amalgamation of other tools used to exploit Distant Reader study carrels. They are listed below:

   * `Click <https://palletsprojects.com/p/click/>`_ - implements the command-line interface to the Toolbox, and wonderful because its framework makes the interface consistent

   * `Apache Tika <https://tika.apache.org/>`_ - run as a local server during ``build`` to convert PDF, Word, HTML, and other formats to plain text and extract author/title/date metadata

   * `gensim <https://radimrehurek.com/gensim/>`_ - implements the ``Word2Vec`` model backing the ``semantics`` subcommand's similarity, distance, and analogy queries

   * `MALLET <https://mimno.github.io/Mallet/>`_ - used by the ``tm`` subcommand to extract latent themes

   * `Matplotlib <https://matplotlib.org>`_ - used in the ``cluster`` subcommand to visualize the results, and elsewhere to render boxplots and histograms

   * `Natural Language Toolkit (NLTK) <http://www.nltk.org>`_ - used in a number of places throughout the Toolbox, and makes it easy to tokenize a text into words, ngrams, and sentences, and to implement the concordance and word-sense disambiguation (Lesk) subcommands

   * `networkx <https://networkx.org/>`_ - builds the item-author-keyword graph exported by ``rdfgraph`` as GML

   * `pytextrank <https://github.com/DerwenAI/pytextrank>`_ - a spaCy pipe used to rank phrases for the extractive summaries stored in the ``bib`` table

   * `rdflib <https://rdflib.readthedocs.io/>`_ - builds and serializes the Linked Data (RDF) graph exported by ``rdfgraph``

   * `scikit-learn <https://scikit-learn.org/>`_ - used in the ``cluster`` subcommand for TF-IDF feature extraction, cosine distance, and multidimensional scaling

   * `SciPy <https://www.scipy.org>`_ - used in the ``cluster`` subcommand to compute hierarchical clustering (average-linkage)

   * `textacy <https://github.com/chartbeat-labs/textacy>`_ - builds on the functionality of `spaCy <https://spacy.io>`_ and provides support for outputting sentence fragments matching particular grammars, readability statistics, and YAKE keyword extraction

   * `wordcloud <https://github.com/amueller/word_cloud>`_ - renders the word-cloud images used by ``ngrams -w``, ``ent -w``, ``pos -w``, and ``wrd -w``
