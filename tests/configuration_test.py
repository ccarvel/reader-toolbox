# regression test for B1 rank 1 / Plan A A3.1:
# _checkForTika() used to write .rdrrc with only 3 of 4 keys, so the
# next configuration() call raised KeyError on the missing key.

# require
from configparser import ConfigParser
from pathlib       import Path

import rdr


def _write_rdrrc( home, keys ) :

	configurations = ConfigParser()
	configurations[ 'RDR' ] = keys
	with open( home/'.rdrrc', 'w', encoding='utf-8' ) as handle : configurations.write( handle )


def test_configuration_falls_back_when_key_missing( tmp_path, monkeypatch ) :

	'''A .rdrrc written without notebooksHome (as _checkForTika did
	before the fix) must not raise a KeyError; configuration() falls
	back to the initializeConfigurations() default instead.'''

	monkeypatch.setattr( Path, 'home', lambda : tmp_path )
	_write_rdrrc( tmp_path, { 'localLibrary' : str( tmp_path/'reader-library' ),
							  'malletHome'   : str( tmp_path/'mallet' ),
							  'tikaHome'     : str( tmp_path/'tika' ) } )

	assert rdr.configuration( 'notebooksHome' ) == tmp_path/rdr.NOTEBOOKSHOME


def test_writeConfigurations_writes_all_four_keys( tmp_path, monkeypatch ) :

	'''The shared _writeConfigurations() helper must always write
	localLibrary, malletHome, tikaHome, and notebooksHome together,
	so no caller can silently drop one.'''

	monkeypatch.setattr( Path, 'home', lambda : tmp_path )
	rdr._writeConfigurations( tmp_path/'a', tmp_path/'b', tmp_path/'c', tmp_path/'d' )

	assert rdr.configuration( 'localLibrary' )  == tmp_path/'a'
	assert rdr.configuration( 'malletHome' )    == tmp_path/'b'
	assert rdr.configuration( 'tikaHome' )      == tmp_path/'c'
	assert rdr.configuration( 'notebooksHome' ) == tmp_path/'d'
