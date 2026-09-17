# regression test for B2.9 / Plan A A4.5 (the escaping/case half; B2.3
# already covered concordance()'s document-boundary clipping):
# concordance() interpolated the raw query straight into
# re.finditer('\b' + query + '\b', corpus), so a query containing regex
# metacharacters (e.g. '.') matched more than intended, and there was no
# way to search case-insensitively against carrel.txt's always-lower-cased
# text. The query is now escaped by default (opt in to real regex with
# regex=True / -r), and a new caseInsensitive=True / -i flag matches
# regardless of case.

# require
import rdr


def _make_carrel( tmp_path, text ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/rdr.ETC/rdr.CORPUS ).write_text( text, encoding='utf-8' )
	return carrel


def test_query_metacharacters_are_escaped_by_default( tmp_path ) :

	# a literal '.' used to act as a regex wildcard, so "3.14" would also
	# match "3x14"
	_make_carrel( tmp_path, 'the file is 3.14 and also 3x14 somewhere' )

	result = rdr.concordance( 'carrel', localLibrary=tmp_path, query='3.14', width=10 )

	assert len( result ) == 1
	assert '3.14' in result[ 0 ]


def test_regex_flag_enables_real_regular_expressions( tmp_path ) :

	_make_carrel( tmp_path, 'hector fought bravely paris also fought' )

	# without -r, the pipe is literal text and matches nothing
	literal = rdr.concordance( 'carrel', localLibrary=tmp_path, query='hector|paris', width=10 )
	assert literal == []

	# with -r, it is alternation and matches both words
	alternation = rdr.concordance( 'carrel', localLibrary=tmp_path, query='hector|paris', width=10, regex=True )
	assert len( alternation ) == 2


def test_case_insensitive_flag_matches_regardless_of_case( tmp_path ) :

	# carrel.txt is always lower-cased (B2.1 left _txt2bow() as-is), so a
	# capitalized query used to match nothing at all
	_make_carrel( tmp_path, 'hector fought bravely' )

	sensitive = rdr.concordance( 'carrel', localLibrary=tmp_path, query='Hector', width=10 )
	assert sensitive == []

	insensitive = rdr.concordance( 'carrel', localLibrary=tmp_path, query='Hector', width=10, caseInsensitive=True )
	assert len( insensitive ) == 1
