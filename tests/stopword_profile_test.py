# regression test for B2.2 / Plan A A4.3:
# the shipped stoplist asymmetrically dropped gendered pronouns (she, her,
# his, him, they, it -- but not he or i) and ethnonym/color terms (black,
# white, african, american, chinese, ...), silently biasing frequency,
# topic, and embedding results for literary text. _initialize() now
# defaults to a neutral profile (no personal pronouns filtered at all,
# no domain jargon) and keeps the original list as an opt-in 'academic'
# profile; the chosen profile's SHA-256 is written into provenance.

# require
import hashlib

import rdr


def test_default_profile_is_neutral_and_omits_pronouns_and_ethnonyms( tmp_path ) :

	source = tmp_path/'source'
	source.mkdir()
	( source/'a.txt' ).write_text( 'hi', encoding='utf-8' )

	rdr._initialize( 'carrel', str( source ), localLibrary=tmp_path )

	words = ( tmp_path/'carrel'/'etc'/'stopwords.txt' ).read_text( encoding='utf-8' ).split()

	for pronoun in ( 'he', 'she', 'him', 'her', 'his', 'they', 'it', 'i', 'we', 'you' ) :
		assert pronoun not in words, pronoun

	for ethnonym in ( 'black', 'white', 'african', 'american', 'chinese' ) :
		assert ethnonym not in words, ethnonym


def test_academic_profile_is_opt_in_and_matches_the_original_list( tmp_path ) :

	source = tmp_path/'source'
	source.mkdir()
	( source/'a.txt' ).write_text( 'hi', encoding='utf-8' )

	rdr._initialize( 'carrel', str( source ), localLibrary=tmp_path, profile='academic' )

	words = ( tmp_path/'carrel'/'etc'/'stopwords.txt' ).read_text( encoding='utf-8' ).split()

	# the original bias, preserved as an explicit opt-in choice
	assert 'she' in words
	assert 'black' in words
	assert 'he' not in words
	assert 'i' not in words


def test_provenance_records_the_profile_and_its_sha256( tmp_path ) :

	source = tmp_path/'source'
	source.mkdir()
	( source/'a.txt' ).write_text( 'hi', encoding='utf-8' )

	rdr._initialize( 'carrel', str( source ), localLibrary=tmp_path, profile='academic' )

	fields = ( tmp_path/'carrel'/'index.tsv' ).read_text( encoding='utf-8' ).strip().split( '\t' )
	profile, digest = fields[ -2 ], fields[ -1 ]

	assert profile == 'academic'

	words    = ( tmp_path/'carrel'/'etc'/'stopwords.txt' ).read_text( encoding='utf-8' )
	expected = hashlib.sha256( words.encode( 'utf-8' ) ).hexdigest()
	assert digest == expected
