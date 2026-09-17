# replaces the stale constants_test.py, extents_test.py, ngrams_test.py,
# and provenance_test.py (B3): those files depended on a 'test-carrel'
# fixture that was never shipped with the package, hard-coded values from
# the original maintainer's machine (creator=='eric', a 2022 date, a
# /Users/eric/... path), and stale renamed constants
# (DATABASE=='reader.db', CORPUS=='reader.txt', renamed to carrel.db/
# carrel.txt in 8c4c8bf). These build the real, committed
# tests/fixtures/mini/ corpus (see conftest.py's mini_carrel fixture,
# session-scoped so it only builds once) and check real, current behavior
# instead of frozen assumptions.

# require
import getpass

import rdr


def test_build_produces_the_expected_directory_structure( mini_carrel ) :

	for name in ( 'adr', 'bib', 'cache', 'ent', 'etc', 'figures', 'pos', 'txt', 'urls', 'wrd' ) :
		assert ( mini_carrel/name ).is_dir(), name

	assert ( mini_carrel/'etc'/rdr.DATABASE ).exists()
	assert ( mini_carrel/'etc'/rdr.CORPUS ).exists()
	assert ( mini_carrel/'index.tsv' ).exists()
	assert ( mini_carrel/'readme.txt' ).exists()


def test_provenance_reflects_the_current_run( mini_carrel ) :

	fields = ( mini_carrel/'index.tsv' ).read_text( encoding='utf-8' ).strip().split( '\t' )

	# 8 fields as of B2.2 (process, originalID, date, time, creator, input,
	# profile, stopwordSHA256) -- not the 5-6 the stale test assumed
	assert len( fields ) == 8
	process, originalID, date, time, creator, input, profile, sha256 = fields

	assert process    == 'toolbox'
	assert originalID == 'mini'
	assert profile    == 'neutral'
	assert len( sha256 ) == 64             # a real sha256 hex digest, not a placeholder
	assert creator    == getpass.getuser() # whoever actually ran this build


def test_extents_reports_real_counts_for_three_documents( mini_carrel ) :

	items  = rdr.extents( 'mini', 'items',  localLibrary=mini_carrel.parent )
	words  = rdr.extents( 'mini', 'words',  localLibrary=mini_carrel.parent )
	flesch = rdr.extents( 'mini', 'flesch', localLibrary=mini_carrel.parent )

	assert items == 3                # sleepy-hollow, iliad, pride-and-prejudice excerpts
	assert 500 < words < 2000        # sane range for ~900 words of raw excerpt text
	assert 0 <= flesch <= 100         # a valid Flesch reading-ease score


def test_ngrams_produces_nonempty_output( mini_carrel ) :

	result = rdr.ngrams( 'mini', localLibrary=mini_carrel.parent )
	lines  = result.strip().split( '\n' )

	assert len( lines ) > 50          # real unigrams from ~900 words, stopwords removed
