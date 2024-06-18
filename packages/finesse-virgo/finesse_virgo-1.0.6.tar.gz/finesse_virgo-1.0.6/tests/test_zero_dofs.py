import finesse.virgo

def test_zero_dofs():
    # create a Virgo object
    virgo = finesse.virgo.Virgo()

    # set some dof values
    virgo.model.DARM.DC = 0.1
    virgo.model.CARM.DC = 0.2
    virgo.model.MICH.DC = 0.3
    virgo.model.PRCL.DC = 0.4
    virgo.model.SRCL.DC = 0.5

    # set phi values
    virgo.model.NE.phi = 1
    virgo.model.NI.phi = 1
    virgo.model.WE.phi = 1
    virgo.model.WI.phi = 1
    virgo.model.PR.phi = 1
    virgo.model.SR.phi = 1

    # get the tunings
    tunings = virgo.get_tunings()

    # zero dofs
    virgo.zero_dof_tunings()

    # assert dof value is now in phi
    assert virgo.model.NE.phi == 1 -0.1 +0.2 -0.3
    assert virgo.model.NI.phi == 1 -0.3
    assert virgo.model.WE.phi == 1 +0.1 +0.2 +0.3
    assert virgo.model.WI.phi == 1 +0.3

    # assert dofs are zero
    assert virgo.model.DARM.DC == 0
    assert virgo.model.CARM.DC == 0
    assert virgo.model.MICH.DC == 0
    assert virgo.model.PRCL.DC == 0
    assert virgo.model.SRCL.DC == 0

    # assert tunings are the same
    assert tunings == virgo.get_tunings()

def test_zero_dof():
    # create a Virgo object
    virgo = finesse.virgo.Virgo()

    # set DARM
    virgo.model.DARM.DC = 0.1

    # set end mirror tunings
    virgo.model.NE.phi = 1
    virgo.model.WE.phi = 1

    # zero DARM
    virgo.zero_dof_tunings(dofs=['DARM'])

    # assert DARM was moved into phi
    assert virgo.model.NE.phi == 1 -0.1
    assert virgo.model.WE.phi == 1 +0.1

    # assert DARM is now zero
    assert virgo.model.DARM.DC == 0