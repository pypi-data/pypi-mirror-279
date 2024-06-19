import finesse.virgo

def test_plot_qnls():
    ifo = finesse.virgo.Virgo()
    ifo.make(dc_lock=False)
    ifo.plot_QNLS()

def test_plot_qnls_shotnoise_only():
    ifo = finesse.virgo.Virgo()
    ifo.make(dc_lock=False)
    ifo.plot_QNLS(shot_noise_only=True)