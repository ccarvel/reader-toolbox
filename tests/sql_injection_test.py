# regression test for B1 rank 5 / Plan A A3.14:
# search(), addresses(), urls(), pos(), and entities() interpolated
# the -q/--like value directly into a quoted SQL/FTS literal, so a
# quote character in the query broke the statement (or, for -q,
# could inject SQL). Bound parameters fix both.

# require
import sqlite3

import pytest

import rdr


def _use_carrel_as_local_library( monkeypatch, localLibrary ) :

	'''addresses() and urls() resolve localLibrary via
	configuration(), not a parameter; point that at the test carrel
	instead of touching the real ~/.rdrrc.'''

	monkeypatch.setattr( rdr, 'configuration', lambda name : localLibrary if name == 'localLibrary' else None )


def test_addresses_like_with_a_double_quote( tmp_path, monkeypatch ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE adr ( id TEXT, address TEXT )' )
	connection.execute( '''INSERT INTO adr VALUES ( 'a', 'x"y@example.com' )''' )
	connection.commit()
	connection.close()

	_use_carrel_as_local_library( monkeypatch, tmp_path )
	result = rdr.addresses( 'carrel', like='x"y' )

	assert result == 'x"y@example.com'


def test_urls_count_like_with_a_single_quote( tmp_path, monkeypatch ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE url ( id TEXT, url TEXT, domain TEXT )' )
	connection.execute( '''INSERT INTO url VALUES ( 'a', "http://x'y.com/page", 'x.com' )''' )
	connection.commit()
	connection.close()

	_use_carrel_as_local_library( monkeypatch, tmp_path )
	result = rdr.urls( 'carrel', select='url', count=True, like="x'y" )

	assert result.startswith( "http://x'y.com/page\t1" )


def test_pos_parts_like_with_a_single_quote( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( "CREATE TABLE pos ( id TEXT, pos TEXT, tag TEXT )" )
	connection.execute( "INSERT INTO pos VALUES ( 'a', 'NOUN', 'NN' )" )
	connection.commit()
	connection.close()

	# an apostrophe in the like value used to break the single-quoted
	# SQL literal this function built for the 'parts' branch
	result = rdr.pos( 'carrel', select='parts', like="noun'", localLibrary=tmp_path )

	assert result == ''  # no crash; simply no match for a nonsense tag


def test_entities_like_with_a_double_quote( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( "CREATE TABLE ent ( id TEXT, type TEXT, entity TEXT )" )
	connection.execute( '''INSERT INTO ent VALUES ( 'a', 'x"y', 'Hector' )''' )
	connection.commit()
	connection.close()

	result = rdr.entities( 'carrel', select='entity', like='x"y', localLibrary=tmp_path )

	assert result == 'Hector'


def _make_search_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'txt' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE bib ( id TEXT, author TEXT, title TEXT, date TEXT, summary TEXT, words TEXT, sentence TEXT, flesch TEXT, extension TEXT )' )
	connection.execute( 'CREATE TABLE wrd ( id TEXT, keyword TEXT )' )
	connection.execute( "INSERT INTO bib VALUES ( 'a', 'X', 'Hectors son', '2020', 's', '10', '1', '80', '.txt' )" )
	connection.execute( "INSERT INTO wrd VALUES ( 'a', 'hector' )" )
	connection.commit()
	connection.close()

	( carrel/'txt'/'a.txt' ).write_text( "this is about hector's son", encoding='utf-8' )


def test_search_query_with_an_apostrophe_fails_cleanly( tmp_path, capsys ) :

	_make_search_carrel( tmp_path )

	# a bare apostrophe used to break the single-quoted MATCH
	# '##QUERY##' literal with a raw, unhandled traceback. Bound
	# parameters stop that; FTS5's own grammar still rejects the bare
	# apostrophe, but now as a caught, clean error
	with pytest.raises( SystemExit ) :
		rdr.search( 'carrel', localLibrary=tmp_path, query="hector's", output='count' )

	assert 'invalid full text query' in capsys.readouterr().err


def test_search_still_works_for_an_ordinary_query( tmp_path ) :

	_make_search_carrel( tmp_path )

	result = rdr.search( 'carrel', localLibrary=tmp_path, query='hector', output='count' )

	assert result == 'carrel\thector\t1'
