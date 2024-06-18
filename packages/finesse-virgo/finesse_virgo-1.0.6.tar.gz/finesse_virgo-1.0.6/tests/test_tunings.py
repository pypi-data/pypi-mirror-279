import finesse.virgo

def test_get_tunings():
    # create a default Virgo object
    virgo = finesse.virgo.Virgo()

    # keep the initial tunings
    initial = virgo.get_tunings()

    # push on MICH, PRCL, and SRCL
    virgo.model.MICH.DC += 0.1
    virgo.model.PRCL.DC += 0.2
    virgo.model.SRCL.DC += 0.3

    # compare the new tunings
    after = virgo.get_tunings()
    assert after['NE'] == initial['NE'] - 0.1
    assert after['WE'] == initial['WE'] + 0.1
    assert after['PR'] == initial['PR'] + 0.2
    assert after['SR'] == initial['SR'] - 0.3

def test_set_tunings():
    # create a default Virgo object
    virgo = finesse.virgo.Virgo()

    # set initial tunings
    virgo.model.NE.phi = 1
    virgo.model.WE.phi = 1
    virgo.model.NI.phi = 1
    virgo.model.WI.phi = 1
    virgo.model.PR.phi = 1
    virgo.model.SR.phi = 1

    # set new tunings
    virgo.set_tunings({
        'NE': 2,
        'WE': 2,
        'NI': 2,
        'WI': 2,
        'PR': 2,
        'SR': 2,
    })

    # assert new tunings
    assert virgo.model.NE.phi == 2
    assert virgo.model.WE.phi == 2
    assert virgo.model.NI.phi == 2
    assert virgo.model.WI.phi == 2
    assert virgo.model.PR.phi == 2
    assert virgo.model.SR.phi == 2

    # assert dofs are zero
    assert virgo.model.DARM.DC == 0
    assert virgo.model.CARM.DC == 0
    assert virgo.model.MICH.DC == 0
    assert virgo.model.PRCL.DC == 0
    assert virgo.model.SRCL.DC == 0