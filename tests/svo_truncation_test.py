# regression test for B1 rank 11 / Plan A A3.8:
# grammars() kept only feature.subject[0], feature.verb[0], and
# feature.object[0] -- the first token of each span -- truncating
# multi-token subjects/objects (compounds, conjuncts) to one word.

# require
import textacy.extract

import rdr


SENTENCE = 'The tired old dog and the small cat chased the red ball across the yard.'


def _make_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'etc'/rdr.CORPUS ).write_text( SENTENCE, encoding='utf-8' )
	return carrel


def test_svo_keeps_every_token_in_each_span( tmp_path, monkeypatch ) :

	_make_carrel( tmp_path )
	monkeypatch.setattr( rdr, 'configuration', lambda name : tmp_path if name == 'localLibrary' else None )

	# ground truth, straight from textacy on the same text
	import spacy
	nlp    = spacy.load( rdr.MODELSMALL )
	doc    = nlp( SENTENCE )
	triple = next( textacy.extract.subject_verb_object_triples( doc ) )
	expected_subject = ' '.join( token.text for token in sorted( triple.subject, key=lambda t : t.i ) )
	expected_verb    = ' '.join( token.text for token in sorted( triple.verb,    key=lambda t : t.i ) )
	expected_object  = ' '.join( token.text for token in sorted( triple.object,  key=lambda t : t.i ) )

	# sanity: this sentence really does exercise a multi-token span
	assert ' ' in expected_subject or ' ' in expected_object

	result = rdr.grammars( 'carrel', grammar='svo' )
	subject, verb, object_ = [ part.strip() for part in result.split( '\t' ) ]

	assert ( subject, verb, object_ ) == ( expected_subject, expected_verb, expected_object )
