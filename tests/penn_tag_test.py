# regression test for B2.8 / Plan A A4.2:
# _txt2pos() and _txt2features() wrote only spaCy's Universal POS
# (token.pos_), discarding the finer-grained Penn Treebank tag
# (token.tag_). Documented usage like "rdr pos -l J" for adjectives only
# makes sense against Penn tags (JJ/JJR/JJS) -- Universal POS has no
# J-prefixed tag at all (the closest is ADJ), so this exact usage was a
# silent no-op. A new additive 'tag' column stores the Penn tag, and
# pos()'s -l filter now matches either pos or tag.

# require
import sqlite3

import spacy

import rdr


class _FakeToken :

	def __init__( self, text, pos, tag ) :
		self.text   = text
		self.lemma_ = text.lower()
		self.pos_   = pos
		self.tag_   = tag


class _FakeSentence :

	def __init__( self, tokens ) :
		self._tokens = tokens
		self.ents    = []

	def __iter__( self ) :
		return iter( self._tokens )


class _FakeDoc :

	def __init__( self, tokens ) :
		self.sents = [ _FakeSentence( tokens ) ]


TOKENS = [ _FakeToken( 'quick', 'ADJ', 'JJ' ), _FakeToken( 'fox', 'NOUN', 'NN' ) ]


def test_txt2pos_writes_the_penn_tag_column( tmp_path, monkeypatch ) :

	class _FakeNLP :
		def __init__( self ) : self.max_length = None
		def __call__( self, text ) : return _FakeDoc( TOKENS )

	monkeypatch.setattr( spacy, 'load', lambda name : _FakeNLP() )

	carrel = tmp_path/'carrel'
	( carrel/'pos' ).mkdir( parents=True )
	source = tmp_path/'a.txt'
	source.write_text( 'quick fox', encoding='utf-8' )

	rdr._txt2pos( 'carrel', source, localLibrary=tmp_path )

	output       = ( carrel/'pos'/'a.pos' ).read_text( encoding='utf-8' )
	header, *rows = output.strip().split( '\n' )
	fields       = { row.split( '\t' )[ 3 ] : row.split( '\t' ) for row in rows }

	assert header.split( '\t' ) == [ 'id', 'sid', 'tid', 'token', 'lemma', 'pos', 'tag' ]
	assert fields[ 'quick' ][ 5 ] == 'ADJ'
	assert fields[ 'quick' ][ 6 ] == 'JJ'
	assert fields[ 'fox' ][ 5 ]   == 'NOUN'
	assert fields[ 'fox' ][ 6 ]   == 'NN'


def test_txt2features_writes_the_penn_tag_column( tmp_path, monkeypatch ) :

	class _FakeNLP :
		def __init__( self ) :
			self.max_length = None
		def pipe( self, texts ) :
			return [ _FakeDoc( TOKENS ) for _ in texts ]

	monkeypatch.setattr( rdr, '_WORKERNLP', _FakeNLP() )

	carrel = tmp_path/'carrel'
	for d in ( 'ent', 'pos', 'wrd' ) : ( carrel/d ).mkdir( parents=True )
	source = tmp_path/'a.txt'
	source.write_text( 'quick fox', encoding='utf-8' )

	rdr._txt2features( 'carrel', source, localLibrary=tmp_path )

	output        = ( carrel/'pos'/'a.pos' ).read_text( encoding='utf-8' )
	header, *rows = output.strip().split( '\n' )
	fields        = { row.split( '\t' )[ 3 ] : row.split( '\t' ) for row in rows }

	assert header.split( '\t' ) == [ 'id', 'sid', 'tid', 'token', 'lemma', 'pos', 'tag' ]
	assert fields[ 'quick' ][ 5 ] == 'ADJ'
	assert fields[ 'quick' ][ 6 ] == 'JJ'


def test_pos_dash_l_matches_the_penn_tag_when_universal_pos_would_not( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE pos ( id TEXT, sid INT, tid INT, token TEXT, lemma TEXT, pos TEXT, tag TEXT )' )
	connection.executemany(
		'INSERT INTO pos VALUES ( ?, ?, ?, ?, ?, ?, ? )',
		[
			( 'a', 1, 1, 'quick', 'quick', 'ADJ', 'JJ' ),
			( 'a', 1, 2, 'fox',   'fox',   'NOUN', 'NN' ),
		],
	)
	connection.commit()
	connection.close()

	# 'j' (Penn adjectives) matches nothing under Universal POS alone --
	# there is no J-prefixed Universal tag -- but must now reach 'JJ' via tag
	result = rdr.pos( 'carrel', localLibrary=tmp_path, select='parts', like='j' )

	assert result == 'ADJ'


def test_pos_degrades_gracefully_on_a_carrel_built_before_the_tag_column( tmp_path ) :

	# a carrel built pre-B2.8 has no 'tag' column at all; querying it must
	# not raise "no such column: tag" -- it should just fall back to
	# matching the Universal pos tag alone, same as before this fix
	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )

	connection = sqlite3.connect( str( carrel/'etc'/rdr.DATABASE ) )
	connection.execute( 'CREATE TABLE pos ( id TEXT, sid INT, tid INT, token TEXT, lemma TEXT, pos TEXT )' )
	connection.execute( "INSERT INTO pos VALUES ( 'a', 1, 1, 'fox', 'fox', 'NOUN' )" )
	connection.commit()
	connection.close()

	result = rdr.pos( 'carrel', localLibrary=tmp_path, select='parts', like='noun' )

	assert result == 'NOUN'
