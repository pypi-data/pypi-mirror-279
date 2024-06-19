import finesse.virgo

def test_parse_locks(tmpdir):
    # create Virgo with locks and unparse
    model = finesse.virgo.make_virgo()
    model.unparse_file(tmpdir / 'model_with_locks.kat')

    # try to create Virgo using the file with locks
    virgo = finesse.virgo.Virgo(tmpdir / 'model_with_locks.kat')