# regression test for B1 rank 4 / Plan A A3.13:
# checkForSemanticIndex(), _carrel2doc(), sentences(), and
# _checkForIndex() only checked whether their cached artifact
# existed, never whether stopwords.txt or txt/ had changed since, so
# an edited stopword list never changed semantics()/grammars()/
# sentences()/search() output.

# require
import time

import rdr


CORPUS = 'Hector fought bravely against the Greeks. Hector was brave and strong. ' * 20


def _make_carrel( tmp_path, stopwords='the\na\n' ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'txt' ).mkdir( parents=True )
	( carrel/'etc'/rdr.STOPWORDS ).write_text( stopwords, encoding='utf-8' )
	( carrel/'txt'/'a.txt' ).write_text( CORPUS, encoding='utf-8' )

	return carrel


def test_semantic_index_rebuilds_when_stopwords_change( tmp_path ) :

	carrel  = _make_carrel( tmp_path )
	vectors = carrel/'etc'/'carrel.vec'

	rdr.checkForSemanticIndex( 'carrel', tmp_path )
	assert vectors.exists()
	first = vectors.stat().st_mtime_ns

	time.sleep( 0.01 )
	with open( carrel/'etc'/rdr.STOPWORDS, 'a', encoding='utf-8' ) as handle : handle.write( 'hector\n' )

	rdr.checkForSemanticIndex( 'carrel', tmp_path )
	assert vectors.stat().st_mtime_ns != first


def test_semantic_index_does_not_rebuild_when_nothing_changed( tmp_path ) :

	carrel  = _make_carrel( tmp_path )
	vectors = carrel/'etc'/'carrel.vec'

	rdr.checkForSemanticIndex( 'carrel', tmp_path )
	first = vectors.stat().st_mtime_ns

	rdr.checkForSemanticIndex( 'carrel', tmp_path )
	assert vectors.stat().st_mtime_ns == first
