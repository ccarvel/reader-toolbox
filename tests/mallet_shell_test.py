# regression test for B1 rank 6 / Plan A A3.18:
# cmdTm built MALLET commands as %-formatted shell strings and ran
# them with os.system(), so a carrel name (or library path) with a
# space or shell metacharacter broke or could inject into the call.

# require
import subprocess

import click.testing

import rdr
import rdr.rdr as cli


def test_tm_model_invokes_mallet_as_an_argv_list_not_a_shell_string( tmp_path, monkeypatch ) :

	carrel = tmp_path/'my carrel'
	( carrel/'txt' ).mkdir( parents=True )
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'etc'/rdr.STOPWORDS ).write_text( '', encoding='utf-8' )

	calls = []
	def _fake_run( args, check=False ) :
		calls.append( args )
		class Result : returncode = 0
		return Result()

	# checkForCarrel() and other helpers live in rdr/__init__.py and
	# resolve configuration() from their own module's globals, so both
	# that module's name and cmdTm's ('from rdr import *') copy of it
	# have to be patched to keep this test off the real ~/.rdrrc
	fake_configuration = lambda name : { 'localLibrary' : tmp_path, 'malletHome' : tmp_path/'mallet' }[ name ]
	monkeypatch.setattr( rdr, 'configuration', fake_configuration )
	monkeypatch.setattr( cli, 'configuration', fake_configuration )
	monkeypatch.setattr( cli, '_checkForMallet', lambda mallet : None )
	monkeypatch.setattr( cli, '_makeSummary', lambda keys, header : 'ok' )
	monkeypatch.setattr( subprocess, 'run', _fake_run )

	runner = click.testing.CliRunner()
	result = runner.invoke( cli.cmdTm, [ '-p', 'model', 'my carrel' ] )

	assert result.exit_code == 0, result.output + str( result.exception )
	assert len( calls ) == 2

	# every call is a list of separate argv tokens, not one shell string
	for args in calls :
		assert isinstance( args, list )
		assert all( isinstance( token, str ) for token in args )

	# the carrel's space-containing path survives as one argv token,
	# not split by a shell
	assert any( str( carrel/'txt' ) in args for args in calls )

	# the thread count is capped at 48, not a bare hard-coded 48
	train = calls[ 1 ]
	threads = train[ train.index( '--num-threads' ) + 1 ]
	assert threads.isdigit() and int( threads ) <= 48
