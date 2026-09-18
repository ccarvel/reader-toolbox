# regression test for B1 rank 13 / Plan A A3.9:
# entities() had `like == like.upper()` (a comparison, discarded)
# instead of `like = like.upper()` (an assignment), so a lower-case
# -l value like "person" never matched the `elif like == 'PERSON'`
# wordcloud-save branch and no file was written.

# require
import sqlite3

import rdr


def _make_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'figures' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( "CREATE TABLE ent ( id TEXT, type TEXT, entity TEXT )" )
	rows = [
		( 'a', 'PERSON', 'Hector' ),
		( 'b', 'PERSON', 'Priam' ),
		( 'c', 'PERSON', 'Hector' ),
	]
	connection.executemany( 'INSERT INTO ent VALUES ( ?, ?, ? )', rows )
	connection.commit()
	connection.close()

	return carrel


def test_ent_lowercase_person_saves_the_wordcloud( tmp_path ) :

	carrel = _make_carrel( tmp_path )

	# 'person' (lower-case), exactly as `rdr ent -l person -w -v` passes it
	rdr.entities( 'carrel', localLibrary=tmp_path, select='entity', like='person', count=True, wordcloud=True, save=True )

	assert ( carrel/'figures'/'entities-person.png' ).exists()
