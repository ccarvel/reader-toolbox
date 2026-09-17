# regression test for B1 rank 15 / Plan A A3.12:
# cmdTm's -f choices were a hard-coded list ('use', 'track', 'year',
# 'journal', ...) that mostly named columns _file2bib() never
# populated, so -f with any of those "documented" choices raised a
# SQL "no such column" error. _file2bib() also discarded every
# metadata.csv column except author/title/date.

# require
import sqlite3

import pytest

import rdr
import rdr.rdr as cli


def test_pivot_rejects_a_field_that_is_not_a_real_bib_column( tmp_path, capsys ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE bib ( id TEXT, author TEXT, title TEXT, date TEXT )' )
	connection.commit()
	connection.close()

	with pytest.raises( SystemExit ) :
		cli._pivot( tmp_path, 'carrel', 'year', 'unused' )

	err = capsys.readouterr().err
	assert "'year' is not a field" in err
	assert 'author' in err and 'title' in err and 'date' in err


def test_file2bib_ingests_extra_metadata_columns( tmp_path, monkeypatch ) :

	import tika.parser
	import tika.detector
	monkeypatch.setattr( tika.parser,   'from_file', lambda file : { 'content' : 'A short test document about a topic.', 'metadata' : {} } )
	monkeypatch.setattr( tika.detector, 'from_file', lambda file : 'text/plain' )

	carrel = tmp_path/'carrel'
	( carrel/rdr.BIB ).mkdir( parents=True )
	( carrel/rdr.TXT ).mkdir( parents=True )

	source = tmp_path/'a.txt'
	source.write_text( 'A short test document about a topic.', encoding='utf-8' )

	import pandas as pd
	metadata = pd.DataFrame( { 'author' : [ 'X' ], 'title' : [ 'T' ], 'date' : [ '2020' ], 'year' : [ '2020' ], 'journal' : [ 'A Journal' ] }, index=[ 'a.txt' ] )
	metadata.index.name = 'file'

	rdr._file2bib( 'carrel', source, metadata=metadata, localLibrary=tmp_path )

	lines  = ( carrel/rdr.BIB/'a.bib' ).read_text( encoding='utf-8' ).splitlines()
	header = lines[ 0 ].split( '\t' )
	row    = dict( zip( header, lines[ 1 ].split( '\t' ) ) )

	assert 'year' in header and 'journal' in header
	assert row[ 'year' ] == '2020'
	assert row[ 'journal' ] == 'A Journal'
