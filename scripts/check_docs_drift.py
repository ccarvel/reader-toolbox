#!/usr/bin/env python
"""Fail if docs/commands.rst can drift from the live `rdr` CLI.

commands.rst is a sphinx-click directive, not a hand-written list, so it
cannot drift from the live command set as long as the directive itself is
intact. This script guards the two ways that guarantee can quietly break:

1. Someone replaces the ``.. click::`` directive with a hand-written list.
2. A command re-enabled in rdr/rdr.py (add_command) is left listed under
   commands.rst's "Removed commands" note.
"""

import re
import sys
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parent.parent / 'docs'
COMMANDS_RST = DOCS_ROOT / 'commands.rst'


def live_commands() :

	from rdr.rdr import rdr as group
	return set( group.commands.keys() )


def documented_removed( text ) :

	section = text.split( 'Removed commands', 1 )[ -1 ]
	return set( re.findall( r'``([a-z]+)``', section ) )


def main() :

	text = COMMANDS_RST.read_text( encoding='utf-8' )
	errors = []

	if '.. click:: rdr.rdr:rdr' not in text or ':nested: full' not in text :
		errors.append(
			"commands.rst no longer contains the sphinx-click directive "
			"('.. click:: rdr.rdr:rdr' with ':nested: full') -- it can "
			"drift from the live CLI again. See handoff Plan B4."
		)

	live      = live_commands()
	removed   = documented_removed( text )
	reenabled = removed & live
	if reenabled :
		errors.append(
			"commands re-enabled in rdr/rdr.py but still listed as removed "
			"in docs/commands.rst: " + ', '.join( sorted( reenabled ) )
		)

	if errors :
		for error in errors : print( 'DRIFT: ' + error, file=sys.stderr )
		sys.exit( 1 )

	print( f'OK: {len(live)} live commands, {len(removed)} documented as removed, no overlap.' )


if __name__ == '__main__' : main()
