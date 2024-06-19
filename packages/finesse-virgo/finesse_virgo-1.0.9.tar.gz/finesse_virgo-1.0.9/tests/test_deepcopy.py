import finesse.virgo as virgo


def test_deepcopy():
    # create an instance with a test variable
    ifo = virgo.Virgo()
    ifo.model.parse("var deepcopy_test 0")

    # do a deepcopy
    ifo2 = ifo.deepcopy()

    # change the model in the new copy
    ifo2.model.deepcopy_test.value = 1

    # assert the values are different
    assert ifo2.model.deepcopy_test.value != ifo.model.deepcopy_test.value
