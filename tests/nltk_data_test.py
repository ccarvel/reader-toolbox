# regression test for B1 rank 16 / Plan A A3.15:
# ngrams(), sentences(), and checkForSemanticIndex() never
# provisioned NLTK data, so a fresh machine's first use raised
# LookupError for punkt_tab (or the tagger, or wordnet).

# require
import nltk

import rdr


def test_ensureNLTKData_downloads_only_missing_packages( monkeypatch ) :

	found  = { 'tokenizers/punkt_tab' : True, 'taggers/averaged_perceptron_tagger_eng' : True, 'corpora/wordnet' : False }
	downloaded = []

	def fake_find( resource ) :
		if not found[ resource ] : raise LookupError( resource )

	monkeypatch.setattr( nltk.data, 'find', fake_find )
	monkeypatch.setattr( nltk, 'download', lambda package, quiet=True : downloaded.append( package ) )

	rdr._ensureNLTKData()

	assert downloaded == [ 'wordnet' ]  # only the missing one


def test_ensureNLTKData_downloads_nothing_when_all_present( monkeypatch ) :

	downloaded = []
	monkeypatch.setattr( nltk.data, 'find', lambda resource : None )  # never raises
	monkeypatch.setattr( nltk, 'download', lambda package, quiet=True : downloaded.append( package ) )

	rdr._ensureNLTKData()

	assert downloaded == []
