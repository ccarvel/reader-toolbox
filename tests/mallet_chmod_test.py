# regression test for B1 rank 7 / Plan A A3.2:
# _checkForMallet() called chmod( 0x755 ) -- the hex literal for
# decimal 1877 (octal 3525) -- instead of the octal literal 0o755.

# require
import io
import stat
import zipfile
from pathlib import Path

import requests

import rdr
import rdr.rdr as cli


def _fake_mallet_zip_bytes() :

	buffer = io.BytesIO()
	with zipfile.ZipFile( buffer, 'w' ) as zip : zip.writestr( 'mallet/bin/mallet', '#!/bin/sh\necho mallet\n' )
	return buffer.getvalue()


def test_mallet_binary_gets_mode_0o755_after_download( tmp_path, monkeypatch ) :

	monkeypatch.setattr( Path, 'home', lambda : tmp_path )

	class FakeResponse : content = _fake_mallet_zip_bytes()
	monkeypatch.setattr( requests, 'get', lambda url : FakeResponse() )

	fake_configuration = lambda name : { 'localLibrary' : tmp_path, 'tikaHome' : tmp_path, 'notebooksHome' : tmp_path }[ name ]
	monkeypatch.setattr( rdr, 'configuration', fake_configuration )
	monkeypatch.setattr( cli, 'configuration', fake_configuration )

	cli._checkForMallet( str( tmp_path/'mallet'/'bin'/'mallet' ) )

	binary = tmp_path/'mallet'/'bin'/'mallet'
	mode   = stat.S_IMODE( binary.stat().st_mode )
	assert oct( mode ) == '0o755'
