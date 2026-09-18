# regression test for B1 rank 12 / Plan A A3.7:
# grammars()'s sss branch wrote to sy.stderr (a typo for sys.stderr)
# when -g sss was used without -n, raising NameError instead of the
# intended clean error message.

# require
import rdr


def _make_carrel( tmp_path ) :

	carrel = tmp_path/'carrel'
	( carrel/'etc' ).mkdir( parents=True )
	( carrel/'etc'/rdr.CORPUS ).write_text( 'The dog ran.', encoding='utf-8' )
	return carrel


def test_sss_without_noun_gives_a_clean_error( tmp_path, monkeypatch, capsys ) :

	_make_carrel( tmp_path )
	monkeypatch.setattr( rdr, 'configuration', lambda name : tmp_path if name == 'localLibrary' else None )

	raised = None
	try    : rdr.grammars( 'carrel', grammar='sss' )
	except BaseException as error : raised = error

	assert isinstance( raised, SystemExit )
	assert 'the -n option is required' in capsys.readouterr().err
