# getNLTKText() was removed from rdr/__init__.py at some point before this
# audit but is still called by notebooks 110/120/170 (rdr.getNLTKText).
# Re-added per B5 / .relay/decisions.md ADR-002 as a real API function
# rather than inlined per notebook.

import nltk

import rdr


def test_returns_an_nltk_text_built_from_the_carrels_corpus( mini_carrel ) :

	model = rdr.getNLTKText( mini_carrel.name, localLibrary=mini_carrel.parent )

	assert isinstance( model, nltk.Text )
	assert len( model.tokens ) > 0
