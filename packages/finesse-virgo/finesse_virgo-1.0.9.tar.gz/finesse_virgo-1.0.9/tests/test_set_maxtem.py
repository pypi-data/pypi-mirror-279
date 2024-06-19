import finesse.virgo

def test_set_maxtem():
    virgo = finesse.virgo.Virgo(maxtem="off")
    assert virgo.model.modes_setting["modes"] == "off"
    
    virgo = finesse.virgo.Virgo(maxtem=2)
    assert virgo.model.modes_setting["modes"] == None
    assert virgo.model.modes_setting["maxtem"] == 2

    virgo = finesse.virgo.Virgo(maxtem=("even", 2))
    assert virgo.model.modes_setting["modes"] == "even"
    assert virgo.model.modes_setting["maxtem"] == 2