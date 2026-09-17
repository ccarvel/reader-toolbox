Exercise: Network graphs
========================

Network diagrams illustrate relationships, and when it come to the Toolbox, network diagrams illustrate relationships between words. This section outlines some of the ways you can use the Toolbox to visualize these relationships.

At a minium, network diagrams -- "graphs" -- contains two things: 1) nodes, and 2) edges. Nodes are real world things, and one of the most common types of nodes are people. Edges denote relationships, and when it comes to people, some of the more common types of edges are friend, father, mother, sibling, or child. If you were to draw a number of dots on a piece of paper -- each denoting a person, and you were to connect and label the dots with types of relationships, then you could easily see who is related to whom and how far away.

Since word are known by the company they keep, drawing dots on a piece of paper -- each denoting a word, and then connecting the dots denoting proximity, we can beging to answer the question, "When a given word is used, what other words are used in conjuction?" A more complicated question can be, "When these people are mentioned, what verbs (actions) do they share in common?" In this way the student, researcher, or scholar can compare and contrast things (nodes).

.. note::

   The ``collocations`` subcommand shown in earlier revisions of this
   exercise was removed from the CLI in commit ``ec84060`` (2026-05-27)
   and no longer exists. Its network-graph output can be approximated
   with the ``ngrams`` and ``grammars`` techniques below.

Gephi is a cross-platform, open source piece of software excelling at interpreting network graphs as well as visualizing them. Sure, the application requires a lot of practice, but it is full-featured and enables you to tell compelling stories. The Toolbox itself does not export a bigram- or collocation-based graph directly, but its tab-delimited output is already an adjacency list, so it imports into Gephi with no conversion step.

Bigrams
-------

A simplier and more targeted approach to network digramming is rooted in bigrams.

Remember, graphs are denoted by nodes and edges, and the output of the ngrams subcommand is just that, a pair of nodes and a relationship (adjacency). For example, the following command will output a long list of bigrams from homer::

	# output all bigrams
	rdr ngrams homer -s 2
	
	# output all bigrams to a file
	rdr ngrams homer -s 2 > bigrams.tsv
	
The bigrams.tsv file (called an "adjacency file" in Gephi parlance) can then be imported into Gephi and visualized to look something like the following, but still, there is too much information here, and the resulting story is not compelling:

.. image:: ./figures/network-03.png

A much better approach is to apply a query (-q) to the ngrams command to only export bigrams containing specific words or regular expressions addressing your research question(s), such as this::

	# query (filter) the ngrams command
	rdr ngrams homer -s 2 -q 'achilles|hector'
	
	# same as above but save the result to a file
	rdr ngrams homer -s 2 -q 'achilles|hector|ulysses' > ahu.tsv
	
The resulting adjacency file (ahu.tsv) can then be imported into Gephi and visualized in the following manner:
	
.. image:: ./figures/network-04.png

The following outlines how you can create an illustration such as the one above.

1. Launch Gephi and choose *File > Import Spreadsheet*, select ``ahu.tsv``, and set *As table* to **Edges table**.
2. On the next screen, map the bigram's first word to *Source* and its second word to *Target*; leave the separator as tab.
3. Click *Finish*, then in the *Overview* tab run the *ForceAtlas2* layout (Layout panel) until the graph settles.
4. Under *Statistics*, run *Average Degree* and *Modularity*; color nodes by modularity class and size them by degree to surface clusters and hubs.


Documents and grammars
----------------------

A very similar network can be illustrated by exploiting the grammars subcommand::

	# query (filter) the ngrams command
	rdr grammars homer -q 'achilles|hector|ulysses'

	# same as above but save the result to a file
	rdr grammars homer -s 2 -q 'achilles|hector|ulysses' > ahu.tsv

.. image:: ./figures/network-05.png

Import ``ahu.tsv`` into Gephi the same way as the bigrams example above: *File > Import Spreadsheet*, **Edges table**, first column as *Source*, second as *Target*, then run *ForceAtlas2* from the *Overview* tab.


Documents and keywords
----------------------

The ``sql`` subcommand shown in earlier revisions of this exercise was removed from the CLI; query the carrel's database directly with the ``sqlite3`` command-line tool instead::

	# create an edges table of books and keywords
	sqlite3 -header -separator $'\t' etc/carrel.db "SELECT id AS 'source', keyword AS 'target' FROM wrd" > book-keywords.tsv

.. image:: ./figures/network-06.png
.. image:: ./figures/network-07.png
.. image:: ./figures/network-08.png

1. Import ``book-keywords.tsv`` into Gephi via *File > Import Spreadsheet* as an **Edges table**, with *source* mapped to *Source* and *target* to *Target*.
2. In the *Data Laboratory* tab, open the *Nodes* table and add a boolean column (for example ``is_keyword``) so books and keywords can be styled or filtered separately once merged.
3. Back in *Overview*, run *ForceAtlas2*, then color and size nodes by degree to see which keywords bridge the most books.

