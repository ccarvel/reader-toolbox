# regression test for B2.4 / Plan A A2 step 3-4, A4.14:
# build()'s Pool reloaded spacy.load(MODELMEDIUM) and re-parsed the same
# document independently inside each of _txt2ent(), _txt2pos(), and
# _txt2wrd() -- three model loads and three parses per document. A new
# _initFeatureWorker() loads the model once per worker process (via the
# Pool initializer) into a module-level _WORKERNLP; _txt2features() reuses
# it and parses each document once (via nlp.pipe(), chunked over 1,000,000
# characters) to write ent/pos/wrd output from the same parse.

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
		self.ents    = [ _FakeEntity( text ) ] if text.strip() else []

	def __iter__( self ) :
		return iter( self._tokens )


class _FakeDoc :

	def __init__( self, text ) :
		self.text  = text
		self.sents = [ _FakeSentence( text ) ]


class _FakeNLP :

	def __init__( self ) :
		self.max_length = None
		self.pipe_calls  = []

	def pipe( self, texts ) :
		texts = list( texts )
		self.pipe_calls.append( texts )
		return [ _FakeDoc( t ) for t in texts ]


def _make_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	for d in ( 'ent', 'pos', 'wrd' ) : ( carrel/d ).mkdir( parents=True )
	return carrel


def test_txt2features_uses_the_preloaded_worker_model_not_a_fresh_load( tmp_path, monkeypatch ) :

	fake_nlp = _FakeNLP()
	monkeypatch.setattr( rdr, '_WORKERNLP', fake_nlp )

	def _boom( name ) : raise AssertionError( 'spacy.load() must not be called inside _txt2features()' )
	monkeypatch.setattr( spacy, 'load', _boom )
	monkeypatch.setattr( keyterms, 'yake', lambda doc, **kwargs : [ ( doc.text, 1.0 ) ] )

	carrel = _make_carrel( tmp_path )
	source = tmp_path/'a.txt'
	source.write_text( 'Hector fought near Troy.', encoding='utf-8' )

	rdr._txt2features( 'carrel', source, localLibrary=tmp_path )

	assert fake_nlp.pipe_calls, 'expected nlp.pipe() to have been used'
	assert ( carrel/'ent'/'a.ent' ).exists()
	assert ( carrel/'pos'/'a.pos' ).exists()
	assert ( carrel/'wrd'/'a.wrd' ).exists()

	pos = ( carrel/'pos'/'a.pos' ).read_text( encoding='utf-8' )
	assert 'Hector' in pos


def test_chunk_text_is_a_noop_under_the_limit() :

	text = 'a short document'
	assert rdr._chunkText( text, maxChars=1000000 ) == [ text ]


def test_chunk_text_splits_at_word_boundaries_and_loses_no_characters() :

	text   = ( 'word ' * 300 ).strip()
	chunks = rdr._chunkText( text, maxChars=17 )

	assert all( len( chunk ) <= 17 for chunk in chunks )
	assert ''.join( chunks ) == text          # every character preserved, nothing duplicated
	# every token recovered from every chunk is a complete "word", never a fragment
	for chunk in chunks :
		for token in chunk.split() : assert token == 'word'


def test_txt2features_sentence_ids_stay_unique_across_chunks( tmp_path, monkeypatch ) :

	fake_nlp = _FakeNLP()
	monkeypatch.setattr( rdr, '_WORKERNLP', fake_nlp )
	monkeypatch.setattr( keyterms, 'yake', lambda doc, **kwargs : [] )

	carrel = _make_carrel( tmp_path )
	source = tmp_path/'a.txt'

	# long enough that _txt2features's 1,000,000-character MAXCHARS forces
	# more than one chunk (and therefore more than one fake sentence, one
	# per chunk in this fake), exercising the running sid offset
	source.write_text( ( 'word ' * 210001 ), encoding='utf-8' )

	rdr._txt2features( 'carrel', source, localLibrary=tmp_path )

	assert len( fake_nlp.pipe_calls[ 0 ] ) > 1, 'expected the document to be split into more than one chunk'

	pos  = ( carrel/'pos'/'a.pos' ).read_text( encoding='utf-8' )
	sids = { line.split( '\t' )[ 1 ] for line in pos.strip().split( '\n' )[ 1: ] }
	assert sids == { '1', '2' }, sids   # one sid per chunk/fake-sentence, never repeated
