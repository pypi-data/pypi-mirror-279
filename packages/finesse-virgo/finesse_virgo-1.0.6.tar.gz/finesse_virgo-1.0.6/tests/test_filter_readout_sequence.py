import finesse.virgo

def test_filter_readout_sequence():
    virgo = finesse.virgo.Virgo()

    sequence = ['dof1', 'readout_Q', 'dof2', 'readout_I']
    filtered_sequence = virgo.filter_readout_sequence(sequence)

    assert filtered_sequence == ['dof2', 'readout_I']

    sequence = ['PRCL', 'B2_8_I', 'MICH', 'B2_56_Q', 'CARM', 'B2_6_I', 'DARM', 'B1p_56_I', 'SRCL', 'B2_56_I']
    filtered_sequence = virgo.filter_readout_sequence(sequence)

    assert filtered_sequence == ['PRCL', 'B2_8_I', 'CARM', 'B2_6_I', 'DARM', 'B1p_56_I', 'SRCL', 'B2_56_I']