# regression test for B1 rank 9 / Plan A A3.5:
# cmdBib declared -v/--save with is_flag=False (so it required a
# value) and then called bibliography(carrel, format, save)
# positionally, which put `format` into bibliography()'s localLibrary
# parameter and the -v value into its format parameter.

# require
import sqlite3

import click.testing

import rdr
import rdr.rdr as cli


def _make_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE bib ( id TEXT, words TEXT, extension TEXT, flesch TEXT, author TEXT, title TEXT, date TEXT, summary TEXT, mime TEXT )' )
	connection.execute( 'CREATE TABLE wrd ( id TEXT, keyword TEXT )' )
	connection.execute( "INSERT INTO bib VALUES ( 'a', '10', '.txt', '80', 'X', 'A Title', '2020', 's', 'text/plain' )" )
	connection.execute( "INSERT INTO wrd VALUES ( 'a', 'trojans' )" )
	connection.commit()
	connection.close()

	return carrel


def _use_carrel_as_local_library( monkeypatch, localLibrary ) :

	fake = lambda name : localLibrary if name == 'localLibrary' else None
	monkeypatch.setattr( rdr, 'configuration', fake )
	monkeypatch.setattr( cli, 'configuration', fake )


def test_bib_dash_v_is_a_bare_flag_and_writes_index_txt( tmp_path, monkeypatch ) :

	carrel = _make_carrel( tmp_path )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	runner = click.testing.CliRunner()
	result = runner.invoke( cli.cmdBib, [ 'carrel', '-v' ] )

	assert result.exit_code == 0, result.output + str( result.exception )
	assert ( carrel/'index.txt' ).exists()
	assert 'A Title' in ( carrel/'index.txt' ).read_text( encoding='utf-8' )


def test_bib_dash_v_with_json_format_writes_index_json( tmp_path, monkeypatch ) :

	carrel = _make_carrel( tmp_path )
	_use_carrel_as_local_library( monkeypatch, tmp_path )

	runner = click.testing.CliRunner()
	result = runner.invoke( cli.cmdBib, [ 'carrel', '-f', 'json', '-v' ] )

	assert result.exit_code == 0, result.output + str( result.exception )
	assert ( carrel/'index.json' ).exists()
	assert 'A Title' in ( carrel/'index.json' ).read_text( encoding='utf-8' )
