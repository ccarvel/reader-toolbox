# regression test for B2.7 / Plan A A4.8:
# cmdTm's pie chart pie-charted keys.tsv's per-topic MALLET "weights"
# (actually the Dirichlet alpha, a prior-concentration parameter) as if
# they were each topic's share of the corpus. A topic with a high alpha
# is not necessarily the topic most documents are actually about. The pie
# now comes from the MEAN document-topic proportion per topic (topics.tsv)
# instead, and keys.tsv's column is renamed weights -> alpha throughout.

# require
import click.testing
import matplotlib
matplotlib.use( 'Agg' )  # no display in tests
import pytest

import rdr
import rdr.rdr as cli


def _make_topic_model( tmp_path ) :

	carrel   = tmp_path/'carrel'
	modeldir = carrel/'etc'/'topic-model'
	modeldir.mkdir( parents=True )

	# keys.tsv: real MALLET format, no header (ids, alpha, features).
	# Topic 0 has the LOWER alpha but the HIGHER mean document-topic
	# proportion; topic 1 has the HIGHER alpha but the LOWER mean
	# proportion -- deliberately inverted so a test that (incorrectly)
	# used alpha for the pie can't accidentally agree with one that uses
	# the real per-document proportions.
	( modeldir/'keys.tsv' ).write_text(
		'0\t0.5\tfoo topic-zero\n'
		'1\t1.9\tbar topic-one\n',
		encoding='utf-8',
	)

	# topics.tsv: real MALLET format, no header (docId, docUri, then one
	# proportion column per topic, each document's row summing to 1.0)
	( modeldir/'topics.tsv' ).write_text(
		'0\tfile:doc0.txt\t0.8\t0.2\n'
		'1\tfile:doc1.txt\t0.4\t0.6\n',
		encoding='utf-8',
	)

	return carrel


def _use_carrel_as_local_library( monkeypatch, localLibrary ) :

	fake = lambda name : { 'localLibrary' : localLibrary, 'malletHome' : localLibrary/'mallet' }[ name ]
	monkeypatch.setattr( rdr, 'configuration', fake )
	monkeypatch.setattr( cli, 'configuration', fake )
	monkeypatch.setattr( cli, '_checkForMallet', lambda mallet : None )
	monkeypatch.setattr( cli, 'LABELS', list( cli.LABELS ) )  # isolate the module-level mutable default


def test_pie_slices_are_mean_document_topic_proportions_not_alpha( tmp_path, monkeypatch ) :

	import matplotlib.pyplot as plt
	from pandas.plotting import PlotAccessor

	_make_topic_model( tmp_path )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	captured = {}
	real_call = PlotAccessor.__call__

	def _spy_call( self, *args, **kwargs ) :
		captured[ 'frame' ] = self._parent.copy()
		return real_call( self, *args, **kwargs )

	monkeypatch.setattr( PlotAccessor, '__call__', _spy_call )

	try :
		runner = click.testing.CliRunner()
		result = runner.invoke( cli.cmdTm, [ '-p', 'read', '-o', 'chart', '-y', 'pie', 'carrel' ] )
		assert result.exit_code == 0, result.output + str( result.exception )
	finally :
		plt.close( 'all' )

	summary = captured[ 'frame' ]
	topic0  = summary.loc[ summary[ 'ids' ] == 0, 'topics' ].iloc[ 0 ]
	topic1  = summary.loc[ summary[ 'ids' ] == 1, 'topics' ].iloc[ 0 ]

	assert topic0 == pytest.approx( 60.0 )    # mean( 0.8, 0.4 ) * 100
	assert topic1 == pytest.approx( 40.0 )    # mean( 0.2, 0.6 ) * 100
	assert summary[ 'topics' ].sum() == pytest.approx( 100.0 )
