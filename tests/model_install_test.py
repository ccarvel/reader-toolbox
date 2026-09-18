# regression test for B1 rank 17 / Plan A A3.16:
# modelNotFound() shelled out to bare "python -m spacy download",
# which can target a different interpreter than the one rdr is
# running under (e.g. under uv), and had no fallback when pip isn't
# installed in that interpreter.

# require
import importlib.util
import shutil
import subprocess
import sys

import pytest

import rdr


def test_spacyModelWheelURL_builds_a_real_release_url() :

	url = rdr._spacyModelWheelURL( rdr.MODELSMALL )

	assert url.startswith( 'https://github.com/explosion/spacy-models/releases/download/' )
	assert rdr.MODELSMALL in url
	assert url.endswith( '-py3-none-any.whl' )


def test_modelNotFound_uses_sys_executable_when_pip_present( monkeypatch ) :

	calls = []
	monkeypatch.setattr( rdr.click, 'getchar', lambda : 'y' )
	monkeypatch.setattr( subprocess, 'run', lambda args, **kwargs : calls.append( args ) )

	with pytest.raises( SystemExit ) :
		rdr.modelNotFound()

	assert len( calls ) == 2
	for args in calls :
		assert args[ 0 ] == sys.executable  # not the bare string "python"
		assert args[ 1: ] == [ '-m', 'spacy', 'download', rdr.MODELSMALL ] or args[ 1: ] == [ '-m', 'spacy', 'download', rdr.MODELMEDIUM ]


def test_modelNotFound_prints_uv_command_when_pip_absent( monkeypatch, capsys ) :

	monkeypatch.setattr( rdr.click, 'getchar', lambda : 'y' )
	monkeypatch.setattr( importlib.util, 'find_spec', lambda name : None if name == 'pip' else object() )
	monkeypatch.setattr( shutil, 'which', lambda name : '/usr/bin/uv' if name == 'uv' else None )
	monkeypatch.setattr( rdr, '_spacyModelWheelURL', lambda model : f'https://example.com/{ model }.whl' )

	with pytest.raises( SystemExit ) :
		rdr.modelNotFound()

	err = capsys.readouterr().err
	assert f'uv pip install https://example.com/{ rdr.MODELSMALL }.whl' in err
	assert f'uv pip install https://example.com/{ rdr.MODELMEDIUM }.whl' in err
