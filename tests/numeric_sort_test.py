# regression test for B1 rank 2 / Plan A A3.3:
# _tsv2db() stored words/sentence/flesch/pages as TEXT (pandas
# dtype='string' + to_sql(if_exists='replace')), so sizes() and
# flesch() sorted lexicographically ('9999' before '80') instead of
# numerically (80 before 9999).

# require
import sqlite3

import rdr


def _make_carrel( tmp_path, rows ) :

	'''Build just enough of a carrel (a directory plus a bib table)
	for sizes()/flesch() to run against. words/flesch are stored as
	TEXT, exactly as pre-fix _tsv2db() left already-built carrels, to
	prove the ORDER BY CAST fix works without a migration.'''

	carrel = tmp_path/'carrel'
	etc    = carrel/'etc'
	etc.mkdir( parents=True )

	connection = sqlite3.connect( str( etc/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE bib ( id TEXT, words TEXT, flesch TEXT )' )
	connection.executemany( 'INSERT INTO bib VALUES ( ?, ?, ? )', rows )
	connection.commit()
	connection.close()


def test_sizes_sorts_numerically_on_a_text_typed_carrel( tmp_path ) :

	_make_carrel( tmp_path, [ ( 'a', '9999', '9999' ), ( 'b', '250000', '250000' ), ( 'c', '80', '80' ) ] )

	result = rdr.sizes( 'carrel', localLibrary=tmp_path )
	ids    = [ line.split( '\t' )[ 0 ] for line in result.split( '\n' ) ]

	assert ids == [ 'b', 'a', 'c' ]  # 250000 > 9999 > 80, numerically


def test_flesch_sorts_numerically_on_a_text_typed_carrel( tmp_path ) :

	_make_carrel( tmp_path, [ ( 'a', '9999', '9' ), ( 'b', '250000', '80' ), ( 'c', '80', '76' ) ] )

	result = rdr.flesch( 'carrel', localLibrary=tmp_path )
	ids    = [ line.split( '\t' )[ 0 ] for line in result.split( '\n' ) ]

	assert ids == [ 'b', 'c', 'a' ]  # 80 > 76 > 9, numerically ('9' sorts first lexicographically)


def test_tsv2db_casts_numeric_bib_columns_on_new_builds( tmp_path ) :

	directory = tmp_path/'bib'
	directory.mkdir()
	( directory/'a.bib' ).write_text( 'id\twords\tflesch\tpages\tsentence\na\t9999\t80\t3\t12\n', encoding='utf-8' )

	connection = sqlite3.connect( ':memory:' )
	rdr._tsv2db( directory, '*.bib', 'bib', connection )

	types = connection.execute( 'SELECT typeof( words ), typeof( flesch ), typeof( pages ), typeof( sentence ) FROM bib' ).fetchone()
	assert types == ( 'integer', 'integer', 'integer', 'integer' )
