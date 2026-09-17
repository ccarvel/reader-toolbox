# regression test for B2.6 / Plan A A4.7:
# word2vec()'s analogy branch computed positive=[w0,w2], negative=w1 for a
# 3-word query "w0 w1 w2" -- i.e. w0 - w1 + w2. For the documented example
# "king queen prince" this targets king - queen + prince (a masculine
# direction), not the canonical "king is to queen as prince is to ?"
# relationship (queen - king + prince -> princess). It also returned the
# raw gensim list of tuples instead of the tab-delimited output every
# other word2vec() branch produces.

# require
import gensim

import rdr


class _FakeModel :

	def __init__( self ) :
		self.calls = []

	def most_similar( self, positive=None, negative=None, topn=10 ) :
		self.calls.append( { 'positive' : positive, 'negative' : negative, 'topn' : topn } )
		return [ ( 'princess', 0.75 ), ( 'queen', 0.6 ) ]


def test_analogy_targets_the_queen_minus_king_plus_prince_direction( tmp_path, monkeypatch ) :

	carrel = tmp_path/'carrel'
	carrel.mkdir()

	fake_model = _FakeModel()
	monkeypatch.setattr( rdr, 'checkForSemanticIndex', lambda *args, **kwargs : None )
	monkeypatch.setattr( gensim.models.KeyedVectors, 'load', staticmethod( lambda path : fake_model ) )

	result = rdr.word2vec( 'carrel', localLibrary=tmp_path, type='analogy', query='king queen prince' )

	assert len( fake_model.calls ) == 1
	call = fake_model.calls[ 0 ]
	assert call[ 'positive' ] == [ 'queen', 'prince' ]
	assert call[ 'negative' ] == [ 'king' ]


def test_analogy_output_is_tab_delimited_like_the_other_branches( tmp_path, monkeypatch ) :

	carrel = tmp_path/'carrel'
	carrel.mkdir()

	fake_model = _FakeModel()
	monkeypatch.setattr( rdr, 'checkForSemanticIndex', lambda *args, **kwargs : None )
	monkeypatch.setattr( gensim.models.KeyedVectors, 'load', staticmethod( lambda path : fake_model ) )

	result = rdr.word2vec( 'carrel', localLibrary=tmp_path, type='analogy', query='king queen prince' )

	assert result == 'princess\t0.75\nqueen\t0.6'
