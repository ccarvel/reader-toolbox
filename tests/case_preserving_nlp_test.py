# regression test for B2.1 / Plan A A4.1, A4.2, A4.9:
# _txt2ent(), _txt2pos(), _txt2wrd(), and _txt2url() all fed spaCy/regex
# lower-cased text via `_normalize(handle.read())`, which measurably
# degraded NER recall (A4.1: 544->404 entities on a LitBank sample) and
# POS/PROPN fidelity (A4.2: 39.5% of PROPN tags lost), and corrupted
# case-sensitive URL paths (A4.9: 2/2 sample URLs altered). The fix reads
# raw (whitespace-collapsed only) text for these four functions, while
# _txt2bow()'s lower-cased carrel.txt (used by ngrams) is unchanged.

# require
import spacy
import textacy.extract.keyterms as keyterms

import rdr


class _FakeToken :

	def __init__( self, text ) :
		self.text   = text
		self.lemma_ = text.lower()
		self.pos_   = 'PROPN' if text[ :1 ].isupper() else 'NOUN'
		self.tag_   = 'NNP' if text[ :1 ].isupper() else 'NN'


class _FakeEntity :

	def __init__( self, text, label='MISC' ) :
		self.text   = text
		self.label_ = label


class _FakeSentence :

	def __init__( self, text ) :
		self._tokens = [ _FakeToken( word ) for word in text.split() ]
		self.ents    = [ _FakeEntity( text ) ]

	def __iter__( self ) :
		return iter( self._tokens )


class _FakeDoc :

	def __init__( self, text ) :
		self.text  = text
		self.sents = [ _FakeSentence( text ) ]


class _FakeNLP :

	def __init__( self ) :
		self.max_length   = None
		self.captured_text = None

	def __call__( self, text ) :
		self.captured_text = text
		return _FakeDoc( text )


def _patch_spacy( monkeypatch ) :

	fake_nlp = _FakeNLP()
	monkeypatch.setattr( spacy, 'load', lambda name : fake_nlp )
	return fake_nlp


def test_txt2ent_does_not_lowercase_input_text( tmp_path, monkeypatch ) :

	fake_nlp = _patch_spacy( monkeypatch )

	carrel = tmp_path/'carrel'
	( carrel/'ent' ).mkdir( parents=True )
	source = tmp_path/'a.txt'
	source.write_text( 'Hector fought near Troy.', encoding='utf-8' )

	rdr._txt2ent( 'carrel', source, localLibrary=tmp_path )

	assert 'Hector' in fake_nlp.captured_text
	assert 'hector' not in fake_nlp.captured_text

	output = ( carrel/'ent'/'a.ent' ).read_text( encoding='utf-8' )
	assert 'Hector' in output


def test_txt2pos_does_not_lowercase_input_text( tmp_path, monkeypatch ) :

	fake_nlp = _patch_spacy( monkeypatch )

	carrel = tmp_path/'carrel'
	( carrel/'pos' ).mkdir( parents=True )
	source = tmp_path/'a.txt'
	source.write_text( 'Hector fought near Troy.', encoding='utf-8' )

	rdr._txt2pos( 'carrel', source, localLibrary=tmp_path )

	assert 'Hector' in fake_nlp.captured_text

	output = ( carrel/'pos'/'a.pos' ).read_text( encoding='utf-8' )
	rows   = [ line.split( '\t' ) for line in output.strip().split( '\n' )[ 1: ] ]
	tokens = { row[ 3 ] for row in rows }
	assert 'Hector' in tokens
	assert 'hector' not in tokens


def test_txt2wrd_does_not_lowercase_input_text( tmp_path, monkeypatch ) :

	fake_nlp = _patch_spacy( monkeypatch )
	monkeypatch.setattr( keyterms, 'yake', lambda doc, **kwargs : [ ( doc.text, 1.0 ) ] )

	carrel = tmp_path/'carrel'
	( carrel/rdr.WRD ).mkdir( parents=True )
	source = tmp_path/'a.txt'
	source.write_text( 'Hector fought near Troy.', encoding='utf-8' )

	rdr._txt2wrd( 'carrel', source, localLibrary=tmp_path )

	assert 'Hector' in fake_nlp.captured_text

	output = ( carrel/rdr.WRD/'a.wrd' ).read_text( encoding='utf-8' )
	assert 'Hector' in output


def test_txt2url_preserves_url_case( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'urls' ).mkdir( parents=True )
	source = tmp_path/'a.txt'
	source.write_text( 'See HTTPS://Example.COM/MixedCase for details.', encoding='utf-8' )

	rdr._txt2url( 'carrel', source, localLibrary=tmp_path )

	output = ( carrel/'urls'/'a.url' ).read_text( encoding='utf-8' )
	assert 'HTTPS://Example.COM/MixedCase' in output
	assert 'https://example.com/mixedcase' not in output
