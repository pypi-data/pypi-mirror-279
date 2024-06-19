from finesse.analysis.actions import Action, RunLocks


# can NOT be repeated
# asserts that the rf lock is enabled and dc lock is disabled
# this is not true if it has already been run
class DARM_RF_to_DC(Action):
    """Locks a model using DARM RF readout then transitions the model into using a DC
    readout and locks.

    Parameters
    ----------
    dc_kick : float, optional
        Amount to kick lock away from zero tuning
    lock_gain : float, optional
        Gain for the DC lock
    """

    def __init__(self, dc_offset=0.5e-3, lock_gain=-0.01, name="DarmRF2DC"):
        super().__init__(name)
        self.__lock_rf = RunLocks(
            "DARM_rf_lock", method="newton", display_progress=False
        )
        self.__lock_dc = RunLocks(
            "DARM_dc_lock", method="newton", display_progress=False
        )
        self.dc_offset = dc_offset
        self.lock_gain = lock_gain

    def _do(self, state):
        assert state.model.DARM_rf_lock.enabled
        assert not state.model.DARM_dc_lock.enabled

        self.__lock_rf._do(state)
        state.model.DARM_rf_lock.enabled = False

        # kick lock away from zero tuning for DC lock to grab with
        state.model.DARM.DC += self.dc_offset

        # take a guess at the gain
        state.model.DARM_dc_lock.gain = self.lock_gain
        state.model.DARM_dc_lock.enabled = True
        self.__lock_dc._do(state)
        return None

    def _requests(self, model, memo, first=True):
        memo["changing_parameters"].append("DARM_dc_lock.gain")
        memo["changing_parameters"].append("DARM_dc_lock.enabled")
        memo["changing_parameters"].append("DARM_rf_lock.enabled")
        self.__lock_rf._requests(model, memo)
        self.__lock_dc._requests(model, memo)
        return memo
