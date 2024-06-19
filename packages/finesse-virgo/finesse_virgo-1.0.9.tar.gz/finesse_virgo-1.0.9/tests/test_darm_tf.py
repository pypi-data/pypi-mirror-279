import finesse.virgo

def test_darm_tf():
    ifo = finesse.virgo.Virgo()
    ifo.make()
    ifo.get_DARM()

def test_plot_darm():
    ifo = finesse.virgo.Virgo()
    ifo.make(dc_lock=False)
    ifo.plot_DARM()