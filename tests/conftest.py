# shared pytest fixtures (B3): a session-scoped real carrel built from the
# committed public-domain mini corpus (tests/fixtures/mini/), used by
# integration-level tests that need a real, non-mocked build instead of a
# synthetic fixture. Requires a Tika server already reachable on
# localhost:9998 -- started locally via `rdr build ... -s` once, or by the
# apache/tika service container in CI (see .github/workflows/ci.yml) --
# and skips (rather than fails) if none is running.

# require
import os
import subprocess
import sys
from pathlib import Path

import pytest

MINI_CORPUS = Path( __file__ ).parent/'fixtures'/'mini'


def _tika_is_running() :

	import urllib.request

	try :
		with urllib.request.urlopen( 'http://localhost:9998/', timeout=2 ) as response :
			return response.status == 200
	except Exception :
		return False


@pytest.fixture( scope='session' )
def mini_carrel( tmp_path_factory ) :

	"""Build tests/fixtures/mini/ into a real carrel once per test session,
	inside an isolated scratch HOME (never the real ~/.rdrrc or
	~/reader-library). Returns the built carrel's directory. Skips if Tika
	isn't already running."""

	if not _tika_is_running() :
		pytest.skip( 'Tika is not reachable on http://localhost:9998/ -- start it first (see conftest.py)' )

	home = tmp_path_factory.mktemp( 'mini-carrel-home' )
	env  = dict( os.environ )
	env[ 'HOME' ] = str( home )

	rdr = str( Path( sys.executable ).parent/'rdr' )
	subprocess.run( [ rdr, 'build', 'mini', str( MINI_CORPUS ) ], env=env, check=True, capture_output=True, text=True )

	return home/'reader-library'/'mini'
