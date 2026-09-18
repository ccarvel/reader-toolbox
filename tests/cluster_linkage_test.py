# regression test for B2.5 / analysis.md §4/§5 (SciPy ward() misuse):
# cluster() called scipy.cluster.hierarchy.ward() directly on a SQUARE,
# precomputed distance matrix (1 - cosine_similarity), which SciPy treats
# as raw observations rather than a distance matrix and warns about ("looks
# suspiciously like an uncondensed distance matrix"); the code suppressed
# that exact warning with a blanket warnings.filterwarnings("ignore"). It
# also used sklearn MDS's dissimilarity= parameter, deprecated in sklearn
# 1.8 and removed in 1.10.

# require
import matplotlib.pyplot as plt
import numpy as np
import pytest
from scipy.cluster.hierarchy import ClusterWarning, ward

import rdr


def _make_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'txt' ).mkdir( parents=True )
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'etc'/rdr.STOPWORDS ).write_text( '', encoding='utf-8' )

	# four tiny, overlapping-vocabulary documents so TfidfVectorizer's
	# min_df=2 default keeps a non-empty vocabulary
	docs = {
		'a.txt' : 'hector fought achilles near troy',
		'b.txt' : 'achilles fought hector near troy',
		'c.txt' : 'penelope waited for ulysses at home',
		'd.txt' : 'ulysses sailed home to penelope',
	}
	for name, text in docs.items() : ( carrel/'txt'/name ).write_text( text, encoding='utf-8' )

	return carrel


def test_ward_on_the_square_distance_matrix_really_does_warn() :

	# establishes the defect is real on this scipy version, not assumed
	distance = np.array( [ [ 0, 0.3, 0.9, 0.9 ], [ 0.3, 0, 0.9, 0.9 ], [ 0.9, 0.9, 0, 0.2 ], [ 0.9, 0.9, 0.2, 0 ] ] )
	with pytest.warns( ClusterWarning ) :
		ward( distance )


def test_cluster_dendrogram_does_not_call_ward_on_the_square_matrix( tmp_path, monkeypatch ) :

	# cluster() calls warnings.filterwarnings("ignore") internally on
	# baseline, which defeats an *external* pytest.warns/simplefilter check
	# by design (that's the exact defect: it globally swallows the warning
	# it itself provokes). Assert on the actual call instead: ward() must
	# never be invoked on the square distance matrix at all.
	fixed_similarity = 1 - np.array( [
		[ 0,   0.3, 0.9, 0.9 ],
		[ 0.3, 0,   0.9, 0.9 ],
		[ 0.9, 0.9, 0,   0.2 ],
		[ 0.9, 0.9, 0.2, 0   ],
	] )
	monkeypatch.setattr( 'sklearn.metrics.pairwise.cosine_similarity', lambda matrix : fixed_similarity )
	monkeypatch.setattr( 'matplotlib.pyplot.show', lambda : None )

	def _boom( *args, **kwargs ) :
		raise AssertionError( 'cluster() must not call ward() directly on a square distance matrix' )
	monkeypatch.setattr( 'scipy.cluster.hierarchy.ward', _boom )

	_make_carrel( tmp_path )
	try    : rdr.cluster( 'carrel', localLibrary=tmp_path, type='dendrogram' )   # must not raise (i.e. must not call ward())
	finally : plt.close( 'all' )   # don't leak this figure's axes into later tests


def test_cluster_cube_uses_the_non_deprecated_mds_parameter( tmp_path, monkeypatch ) :

	captured = {}

	class _FakeMDS :

		def __init__( self, **kwargs ) :
			captured.update( kwargs )

		def fit_transform( self, matrix ) :
			return np.zeros( ( len( matrix ), 3 ) )

	monkeypatch.setattr( 'sklearn.manifold.MDS', _FakeMDS )
	monkeypatch.setattr( 'matplotlib.pyplot.show', lambda : None )

	_make_carrel( tmp_path )
	try    : rdr.cluster( 'carrel', localLibrary=tmp_path, type='cube' )
	finally : plt.close( 'all' )   # don't leak this 3D figure's axes into later tests

	assert captured.get( 'metric' ) == 'precomputed'
	assert 'dissimilarity' not in captured
