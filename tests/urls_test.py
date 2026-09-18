# regression test for B1 rank 8 / Plan A A3.4:
# urls( select='domain' ) referenced an undefined `item`, raising
# NameError, and -c counts were always 1 because COUNT(DISTINCT(x))
# inside a GROUP BY x group is always 1. The domain SELECT also used
# LOWER(DISTINCT(domain)), which SQLite accepts but silently ignores
# the DISTINCT on a scalar function, so it returned every row instead
# of the distinct domain list.

# require
import sqlite3

import rdr


def _make_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE url ( id TEXT, url TEXT, domain TEXT )' )
	rows = [
		( 'a', 'http://x.com/1', 'x.com' ),
		( 'b', 'http://x.com/1', 'x.com' ),  # same url, seen twice (e.g. cited in two documents)
		( 'c', 'http://y.com/1', 'y.com' ),
	]
	connection.executemany( 'INSERT INTO url VALUES ( ?, ?, ? )', rows )
	connection.commit()
	connection.close()


def _use_carrel_as_local_library( monkeypatch, localLibrary ) :

	monkeypatch.setattr( rdr, 'configuration', lambda name : localLibrary if name == 'localLibrary' else None )


def test_urls_domain_select_does_not_raise( tmp_path, monkeypatch ) :

	_make_carrel( tmp_path )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	result = rdr.urls( 'carrel', select='domain' )

	assert sorted( result.split( '\n' ) ) == [ 'x.com', 'y.com' ]


def test_urls_domain_count_is_the_real_row_count( tmp_path, monkeypatch ) :

	_make_carrel( tmp_path )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	result = rdr.urls( 'carrel', select='domain', count=True )
	counts = dict( line.split( '\t' ) for line in result.split( '\n' ) )

	assert counts == { 'x.com' : '2', 'y.com' : '1' }


def test_urls_url_count_is_the_real_row_count( tmp_path, monkeypatch ) :

	_make_carrel( tmp_path )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	result = rdr.urls( 'carrel', select='url', count=True )
	counts = dict( line.split( '\t' ) for line in result.split( '\n' ) )

	assert counts == { 'http://x.com/1' : '2', 'http://y.com/1' : '1' }
