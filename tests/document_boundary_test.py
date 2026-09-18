# regression test for B2.3 / Plan A A4.4:
# _txt2bow() concatenated every document in txt/ with no separator at all
# (bow += handle.read()), so ngrams() and concordance() could produce
# n-grams and KWIC windows that span two unrelated documents. carrel.txt
# now separates documents with '\n\f\n', and ngrams()/concordance() both
# respect that boundary.

# require
import rdr


def _build_bow_carrel( tmp_path, docs ) :

	carrel = tmp_path/'carrel'
	( carrel/'txt' ).mkdir( parents=True )
	( carrel/'etc' ).mkdir( parents=True )
	for name, content in docs.items() :
		( carrel/'txt'/name ).write_text( content, encoding='utf-8' )
	( carrel/'etc'/rdr.STOPWORDS ).write_text( '', encoding='utf-8' )
	rdr._txt2bow( 'carrel', localLibrary=tmp_path )
	return carrel


def test_txt2bow_separates_documents_with_a_form_feed( tmp_path ) :

	carrel = _build_bow_carrel( tmp_path, { 'a.txt' : 'Hello world', 'b.txt' : 'Goodbye moon' } )

	bow = ( carrel/rdr.ETC/rdr.CORPUS ).read_text( encoding='utf-8' )

	assert bow.count( '\f' ) == 1
	assert 'hello world' in bow
	assert 'goodbye moon' in bow


def test_ngrams_does_not_span_a_document_boundary( tmp_path ) :

	# write etc/carrel.txt directly (as _txt2bow() would produce it post-B2.3:
	# already normalized, documents separated by '\f') so this test targets
	# ngrams()'s own per-document splitting, independent of _txt2bow()'s
	# filesystem glob order. Pre-fix, ngrams() never splits on '\f' at all --
	# nltk.word_tokenize treats it as ordinary whitespace and drops it, so the
	# whole string is tokenized as one stream and the spurious cross-document
	# bigram ('sunrise','sunset') appears; post-fix it must not.
	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/rdr.ETC/rdr.STOPWORDS ).write_text( '', encoding='utf-8' )
	( carrel/rdr.ETC/rdr.CORPUS ).write_text( 'the bright sunrise \f sunset falls slowly', encoding='utf-8' )

	result  = rdr.ngrams( 'carrel', localLibrary=tmp_path, size=2 )
	bigrams = { tuple( line.split( '\t' ) ) for line in result.split( '\n' ) if line }

	assert ( 'sunrise', 'sunset' ) not in bigrams
	assert ( 'bright', 'sunrise' ) in bigrams
	assert ( 'sunset', 'falls' ) in bigrams


def test_concordance_window_does_not_cross_a_document_boundary( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	corpus = 'this document ends right after love \f love starts this other document too'
	( carrel/rdr.ETC/rdr.CORPUS ).write_text( corpus, encoding='utf-8' )

	snippets = rdr.concordance( 'carrel', localLibrary=tmp_path, query='love', width=40 )

	assert len( snippets ) == 2
	for snippet in snippets : assert '\f' not in snippet
	assert 'starts' not in snippets[ 0 ]   # first "love"'s window must not see doc 2
	assert 'ends'   not in snippets[ 1 ]   # second "love"'s window must not see doc 1
