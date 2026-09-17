# regression test for B1 rank 3 / Plan A A3.11:
# _txt2wrd()'s bare `except: records = []` silently drops any
# document whose keyword extraction fails, and bibliography()/the
# search INDEX inner-joined bib to wrd, so a document with no wrd
# row (whether from a failed extraction or genuinely zero keywords)
# disappeared from `rdr bib` and `rdr search` entirely.

# require
import sqlite3

import rdr


def test_bibliography_includes_bib_rows_with_no_wrd_row( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE bib ( id TEXT, words TEXT, extension TEXT, flesch TEXT, author TEXT, title TEXT, date TEXT, summary TEXT, mime TEXT )' )
	connection.execute( 'CREATE TABLE wrd ( id TEXT, keyword TEXT )' )
	# two bib rows, only one has a matching wrd row
	connection.execute( "INSERT INTO bib VALUES ( 'a', '10', '.txt', '80', 'X', 'Has keywords', '2020', 's', 'text/plain' )" )
	connection.execute( "INSERT INTO bib VALUES ( 'b', '10', '.txt', '80', 'X', 'Lost its keywords', '2020', 's', 'text/plain' )" )
	connection.execute( "INSERT INTO wrd VALUES ( 'a', 'trojans' )" )
	connection.commit()
	connection.close()

	result = rdr.bibliography( 'carrel', localLibrary=tmp_path, format='json' )
	ids    = { row[ 'id' ] for row in __import__( 'json' ).loads( result ) }

	assert ids == { 'a', 'b' }


def test_checkForIndex_includes_bib_rows_with_no_wrd_row( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'txt' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE bib ( id TEXT, author TEXT, title TEXT, date TEXT, summary TEXT, words TEXT, sentence TEXT, flesch TEXT, extension TEXT )' )
	connection.execute( 'CREATE TABLE wrd ( id TEXT, keyword TEXT )' )
	connection.execute( "INSERT INTO bib VALUES ( 'a', 'X', 'Has keywords', '2020', 's', '10', '1', '80', '.txt' )" )
	connection.execute( "INSERT INTO bib VALUES ( 'b', 'X', 'Lost its keywords', '2020', 's', '10', '1', '80', '.txt' )" )
	connection.execute( "INSERT INTO wrd VALUES ( 'a', 'trojans' )" )
	connection.commit()
	connection.close()

	( carrel/'txt'/'a.txt' ).write_text( 'some text about trojans', encoding='utf-8' )
	( carrel/'txt'/'b.txt' ).write_text( 'some other text', encoding='utf-8' )

	rdr._checkForIndex( 'carrel', tmp_path )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	ids        = { row[ 0 ] for row in connection.execute( 'SELECT id FROM indx' ) }
	connection.close()

	assert ids == { 'a', 'b' }


def test_txt2wrd_logs_and_continues_on_extraction_failure( tmp_path, monkeypatch, capsys ) :

	import textacy.extract.keyterms as keyterms

	def _boom( *args, **kwargs ) : raise ValueError( 'synthetic YAKE failure' )
	monkeypatch.setattr( keyterms, 'yake', _boom )

	carrel = tmp_path/'carrel'
	( carrel/rdr.WRD ).mkdir( parents=True )
	source = tmp_path/'a.txt'
	source.write_text( 'some text', encoding='utf-8' )

	rdr._txt2wrd( 'carrel', source, localLibrary=tmp_path )

	assert not ( carrel/rdr.WRD/'a.wrd' ).exists()
	stderr = capsys.readouterr().err
	assert 'a' in stderr and 'synthetic YAKE failure' in stderr
