# regression test for B1 rank 14 / Plan A A3.10:
# _pivot() and the scatter branch did `labels = LABELS` (an alias to
# the shared module-level list) and then appended to it, so repeated
# in-process calls kept growing the same list and produced
# misaligned columns on the second and later calls.

# require
import sqlite3

import rdr
import rdr.rdr as cli


def _make_pivot_carrel( tmp_path, n_topics=2 ) :

	carrel   = tmp_path/'carrel'
	modeldir = carrel/'etc'/'topic-model'
	modeldir.mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( "CREATE TABLE bib ( id TEXT, title TEXT )" )
	connection.execute( "INSERT INTO bib VALUES ( '1', 'A Title' )" )
	connection.commit()
	connection.close()

	# exactly the file value the SQL template in _pivot() produces
	file_value = f"file:{ tmp_path }/carrel/txt/1.txt"

	header = [ 'docId', 'file' ] + [ str( t ) for t in range( n_topics ) ]
	row    = [ '1', file_value ] + [ '0.5' ] * n_topics
	( modeldir/'topics.tsv' ).write_text( '\t'.join( header ) + '\n' + '\t'.join( row ) + '\n', encoding='utf-8' )

	keys_lines = [ f'{ t }\t0.{ t + 1 }\ttopic{ t }word' for t in range( n_topics ) ]
	( modeldir/'keys.tsv' ).write_text( '\n'.join( keys_lines ) + '\n', encoding='utf-8' )

	return carrel


def test_pivot_twice_in_one_process_stays_aligned( tmp_path, monkeypatch ) :

	_make_pivot_carrel( tmp_path, n_topics=2 )
	monkeypatch.setattr( cli, 'LABELS', list( cli.LABELS ) )  # isolate from other tests

	keys_path = str( tmp_path/'carrel'/'etc'/'topic-model'/'keys.tsv' )

	first  = cli._pivot( tmp_path, 'carrel', 'title', keys_path )
	second = cli._pivot( tmp_path, 'carrel', 'title', keys_path )

	assert list( first.columns ) == list( second.columns )
	assert cli.LABELS == [ 'docId', 'file' ]  # the module constant itself is untouched
