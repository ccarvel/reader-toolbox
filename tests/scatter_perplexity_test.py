# regression test for B1 rank 10 / Plan A A3.6:
# cmdTm's scatter branch used TSNE(perplexity=1024) on a topic-by-
# document matrix whose sample count equals the topic count, and
# scikit-learn requires 0 < perplexity < n_samples, so this always
# raised ValueError for any carrel with fewer than 1025 topics.

# require
import click.testing
import matplotlib
matplotlib.use( 'Agg' )  # no display in tests

import rdr
import rdr.rdr as cli


def _make_topic_model( tmp_path, n_topics=8, n_documents=5 ) :

	carrel   = tmp_path/'carrel'
	modeldir = carrel/'etc'/'topic-model'
	modeldir.mkdir( parents=True )

	# topics.tsv: one row per document, one column per topic
	header = [ 'docId', 'file' ] + [ str( t ) for t in range( n_topics ) ]
	lines  = [ '\t'.join( header ) ]
	for d in range( n_documents ) :
		row = [ str( d ), f'doc{ d }.txt' ] + [ str( ( d + t ) % 5 / 10 + 0.01 ) for t in range( n_topics ) ]
		lines.append( '\t'.join( row ) )
	( modeldir/'topics.tsv' ).write_text( '\n'.join( lines ) + '\n', encoding='utf-8' )

	# keys.tsv: one row per topic, no header (ids, weights, features)
	lines = []
	for t in range( n_topics ) : lines.append( f'{ t }\t{ 0.1 + t * 0.01 }\ttopic{ t } feature{ t }' )
	( modeldir/'keys.tsv' ).write_text( '\n'.join( lines ) + '\n', encoding='utf-8' )

	return carrel


def _use_carrel_as_local_library( monkeypatch, localLibrary ) :

	fake = lambda name : { 'localLibrary' : localLibrary, 'malletHome' : localLibrary/'mallet' }[ name ]
	monkeypatch.setattr( rdr, 'configuration', fake )
	monkeypatch.setattr( cli, 'configuration', fake )
	monkeypatch.setattr( cli, '_checkForMallet', lambda mallet : None )
	monkeypatch.setattr( cli, 'LABELS', list( cli.LABELS ) )  # isolate the module-level mutable default


def test_scatter_renders_for_eight_topics( tmp_path, monkeypatch ) :

	_make_topic_model( tmp_path, n_topics=8 )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	runner = click.testing.CliRunner()
	result = runner.invoke( cli.cmdTm, [ '-p', 'read', '-o', 'chart', '-y', 'scatter', 'carrel' ] )

	assert result.exit_code == 0, result.output + str( result.exception )
	assert 'Error' not in result.output


def test_scatter_gives_a_clean_error_for_too_few_topics( tmp_path, monkeypatch ) :

	_make_topic_model( tmp_path, n_topics=2 )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	runner = click.testing.CliRunner()
	result = runner.invoke( cli.cmdTm, [ '-p', 'read', '-o', 'chart', '-y', 'scatter', 'carrel' ] )

	assert result.exit_code == 0, result.output + str( result.exception )
	assert 'at least 3 topics' in result.output
