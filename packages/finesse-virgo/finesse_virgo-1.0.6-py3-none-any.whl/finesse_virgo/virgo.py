import finesse

from finesse.knm import Map
from finesse.utilities.maps import circular_aperture
from finesse.utilities.tables import Table, NumberTable
from finesse.symbols import CONSTANTS

from finesse.analysis.actions import (
    Series,
    RunLocks,
    Change,
    SensingMatrixDC,
    Minimize,
    Maximize,
    TemporaryParameters,
    OptimiseRFReadoutPhaseDC,
    Xaxis,
    Noxaxis,
    Temporary,
    FrequencyResponse,
)


import math
import os
import glob
import importlib.resources
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from itertools import zip_longest

from .utils import round_to_n

from .actions import DARM_RF_to_DC

# from finesse.exceptions import ModelAttributeError
from finesse.components import DegreeOfFreedom

# definition of thermal states
THERMAL_STATES = {
    "design-matched": {
        "PR.Rc": -1430,
        "SR.Rc": 1430,
        "f_CPN_TL.value": -338008.0,
        "f_CPW_TL.value": -353134.0,
    },
    "cold": {
        "PR.Rc": -1477,
        "SR.Rc": 1443,
        "f_CPN_TL.value": float("inf"),
        "f_CPW_TL.value": float("inf"),
    },
    "measured": {
        "PR.Rc": -1469.0,  # measured from June '22 (ref?)
        "SR.Rc": 1443.0,
        "f_CPN_TL.value": 62636.0,  # from optimizer
        "f_CPW_TL.value": 60625.0,
    },
}

# definition of aperture size for each mirror.
#   as (coating diameter, substrate diameter)
APERTURE_SIZES = {
    "NI": (0.340, 0.350),
    "NE": (0.340, 0.350),
    "WI": (0.340, 0.350),
    "WE": (0.340, 0.350),
    "PR": (0.340, 0.350),
    "SR": (0.340, 0.350),
    # "BS": (0.530, 0.550), # not implemented yet in F3
}


def make_virgo(**kwargs):
    """Returns a fully tuned Virgo ifo as a Finesse model.

    Accepts same configurations as the Virgo class.
    """
    virgo = Virgo(**kwargs)
    virgo.make()
    return virgo.model


class Virgo:
    """Container for the Virgo tuning script which houses and configures the model
    through individual steps producing a tuned interferometer.

    Parameters
    ----------
    files_to_parse : str or list of str, optional
        File name(s) or directory name to use when parsing.
            When a directory name is given, all files with ending .kat will be parsed
            in alphabetical order. A file name can be given as a string, several file names
            will be provided as a list of strings.
            If this variable is not empty, common file included in the package will be used.

    display_plots : bool, optional
        Automatically display plots for certain methods.

    thermal_state : str, optional
        Thermal configuration to use when creating the model.

    use_3f_error_signals : bool, optional
        Sets the control scheme to use the 3f error signals.

    verbose : bool, optional
        Class-wide option to set the verbosity.

    add_locks : bool, optional
        If unset, will skip parsing the locks. Use when the locks should not be
            added on initialization.

    parse_additional_katscript : bool, optional
        If set, will parse the accompanying additional katscript file. Use when
            parsing only a modified common file rather than a pretuned file.

    x_scale : float, optional
        * Convenience function to set the x_scale.

    zero_k00 : bool, optional
        * Convenience function to set zero_k00 phase configuration.

    with_apertures : bool, optional
        * Convenience function to automaticaly apply apertures to the mirror.

    maxtem : str|int|tuple, optional
        * Convenience function to set the modes. Valid options: 'off', number
            of maxtem, or tuple with modes and maxtem, e.g., ('even', 4).
    """

    def __init__(
        self,
        files_to_parse=None,
        display_plots=False,
        thermal_state=None,
        use_3f_error_signals=False,
        with_apertures=False,
        maxtem=None,
        verbose=False,
        x_scale=1,
        zero_k00=False,
        add_locks=True,
        parse_additional_katscript=False,
        control_scheme=None,
    ):
        self.__sensing_matrix = None

        self.display_plots = display_plots
        self.thermal_state = thermal_state
        self.use_3f_error_signals = use_3f_error_signals
        self.with_apertures = with_apertures
        self.verbose = verbose
        self.control_scheme = control_scheme

        # create the model
        self.model = finesse.Model()

        # parse the katscript file, if provided
        if files_to_parse:
            # if directory is provided, parse every kat file
            if type(files_to_parse) is str and os.path.isdir(files_to_parse):
                if self.verbose:
                    print(f"Parsing input files in '{files_to_parse}':")

                # TODO: need to fix, will only work with local directory
                for input_file in sorted(glob.glob(f"{files_to_parse}/*.kat")):
                    self.model.parse_file(input_file)

                    if self.verbose:
                        print(f"- {input_file}.")
            elif type(files_to_parse) is list:
                # if a list is provided, parse each as a file
                for file in files_to_parse:
                    self.model.parse_file(file)

                if self.verbose:
                    print("Parsed input files", *files_to_parse, sep=", ")
            else:
                # otherwise, parse the provided file
                # this will typically be one of two situations
                #   1) output from the unparser, in which everything needed is provided
                #   2) a modified common file, in which case additional katscript will need to be parsed
                self.model.parse_file(files_to_parse)
                if self.verbose:
                    print(f"Parsed input file {files_to_parse}.")
        else:
            # if no file provided, use the common file
            if self.verbose:
                print("Parsing common katfile...")

            self.model.parse(
                importlib.resources.files("finesse_virgo.katscript")
                .joinpath("00_virgo_common_file.kat")
                .read_text()
            )

        # parse additional katscript if needed
        # case 1) the flag is set
        # case 2) default (no input file/directory provided)
        if parse_additional_katscript or not files_to_parse:
            if self.verbose:
                print("Parsing additional katscript...")

            self.model.parse(
                importlib.resources.files("finesse_virgo.katscript")
                .joinpath("01_additional_katscript.kat")
                .read_text()
            )

        # setting phase config to not zero K00 phase, see 'phase' command in F2.
        self.model._settings.phase_config.zero_k00 = zero_k00

        # set x_scale to (maybe) reduce numerical noise from radiation pressure.
        self.model._settings.x_scale = x_scale

        # By default, surfaces are infinite. Using apertures limit their size.
        if with_apertures:
            self.use_apertures()

        # Set maxtem if provided
        # ex: 'off', 2, ('even', 10)
        if maxtem == "off":
            self.model.modes("off")
        elif isinstance(maxtem, int):
            self.model.modes(maxtem=maxtem)
        elif isinstance(maxtem, tuple) and len(maxtem) == 2:
            self.model.modes(maxtem[0], maxtem=maxtem[1])

        # Setting to adjust the RoCs and focal points as defined in the thermal state.
        if thermal_state:
            self.set_thermal_state(thermal_state)

        # If using 3f error signals, we need to increase the order of modulation in addition to the control scheme for the central interferometer.
        if use_3f_error_signals:
            self.model.eom6.order = 3
            self.model.eom8.order = 3
            self.model.eom56.order = 3

            if control_scheme is None:
                self.control_scheme = {
                    "PRCL": ("B2_6_3f", "I", None, 1e-12),
                    "MICH": ("B2_56_3f", "Q", None, 1e-11),
                    "CARM": ("B2_6", "I", None, 1e-14),
                    "DARM": ("B1p_56", "I", None, 1e-14),
                    "SRCL": ("B2_56_3f", "I", None, 50e-11),
                }

        # TODO: should create and use ControlScheme and Lock objects instead of a tuple
        # Define a control scheme to link DoFs to readouts
        # Should be a dictionary of tuples as dof: (readout, port, accuracy, rms)
        #   Note: accuracy will be calculated using RMS and optical gain if left as None
        if self.control_scheme is None:
            self.control_scheme = {
                "PRCL": ("B2_8", "I", None, 1e-12),
                "MICH": ("B2_56", "Q", None, 1e-11),
                "CARM": ("B2_6", "I", None, 1e-14),
                "DARM": ("B1p_56", "I", None, 1e-14),
                "SRCL": ("B2_56", "I", None, 50e-11),
            }

        self.init_control_scheme()

        # parse the locks using the control scheme
        #   but provide ability to skip in case they already exist
        if add_locks:
            self.add_locks()

    @property
    def sensing_matrix(self):
        """Return the sensing matrix if it exists, otherwise calculate it.

        Returns
        -------
        SensingMatrixSolution
        """

        if self.__sensing_matrix is None:
            self.__sensing_matrix = self.get_sensing_matrix()

        return self.__sensing_matrix

    def init_control_scheme(self):
        # extract individual dof/readout arrays for later use
        self.dofs = [dof for dof in self.control_scheme.keys()]
        self.readouts = [lock[0] for lock in self.control_scheme.values()]
        self.unique_readouts = list(dict.fromkeys(self.readouts))
        self.dof_readouts = [
            f"{lock[0]}_{lock[1]}" for lock in self.control_scheme.values()
        ]

    def deepcopy(self):
        return deepcopy(self)

    def make(self, verbose=False, dc_lock=True):
        """Performs full make process.

        Parameters
        ----------
        dc_lock : bool, optional
            Set to false to skip the final step switching DARM to the DC lock.

        verbose : bool, optional
            If set, displays additional information.
        """

        # step 1: adjust the cavity lengths
        print("Adjusting recycling cavity lengths...")
        self.adjust_recycling_cavity_length("PRC", "lPRC", "lPOP_BS", verbose=verbose)
        self.adjust_recycling_cavity_length("SRC", "lSRC", "lsr", verbose=verbose)

        # step 2: pretune
        print("Pretuning...")
        self.pretune(verbose=verbose)

        # step 3: optimize demodulation phases
        print("Optimizing demodulation phases...")
        self.optimize_demodulation_phase(verbose=verbose)

        # step 4: optimize lock gains
        print("Optimizing lock gains...")
        self.optimize_lock_gains(verbose=verbose)

        # step 5: run RF locks
        print("Running RF locks...")
        if self.verbose:
            self.print_dofs("before locking")

        self.model.run(RunLocks(method="newton"))

        if self.verbose:
            self.print_dofs("after locking")

        # step 6: optionally switch to DC locks
        if dc_lock:
            print("Switching to DARM DC lock...")
            if self.verbose or verbose:
                self.print_dofs("before locking")

            self.model.run(DARM_RF_to_DC())

            if self.verbose or verbose:
                self.print_dofs("after locking")

        print("Done.")

    def print_info(self):
        self.print_lengths()
        self.print_thermal_values()
        self.print_tunings()
        self.print_powers()

    def get_settings(self):
        """Returns a curated list of important settings from the model."""

        return {
            "modes": self.model.modes_setting["modes"],
            "maxtem": self.model.modes_setting["maxtem"],
            "zero_k00": self.model._settings.phase_config.zero_k00,
            "x_scale": self.model._settings.x_scale,
        }

    def print_settings(self):
        settings = self.get_settings()

        table = Table(
            [["Setting", "Value"], *settings.items()],
            headerrow=True,
            headercolumn=True,
            alignment=["left", "right"],
            compact=True,
        )

        print(table)

    def get_dofs_dc(self):
        return [self.model.get(f"{dof}.DC") for dof in self.dofs]

    # can be repeated
    def set_thermal_state(self, state: str) -> None:
        """Sets thermal parameter values for the provided state.

        Parameters
        ----------
        state : str
            Key for desired thermal state as defined in THERMAL_STATES.

        Raises
        ------
        Exception
            Raised when the key does not exist in THERMAL_STATES.
        """

        # make sure the state exists
        if state not in THERMAL_STATES.keys():
            raise Exception(
                f"Invalid thermal state `{state}`. Accepted thermal states: [{', '.join([f'`{key}`' for key in THERMAL_STATES.keys()])}]"
            )

        # set the state
        for key, value in THERMAL_STATES[state].items():
            self.model.set(key, value)

    def use_apertures(self, use_substrate: bool = True) -> None:
        """Convenience function to use apertures. Creates surface maps for each major
        surface in Virgo. See TDR table 5.2.

        Parameters
        ----------
        model : Model
            Finesse Virgo model containing all surfaces.
        substrate : bool
            Option to use the coating diameter (False) or the substrate diameter (True).
        """

        # apply the appropriate aperture size to each mirror
        for mirror, diameters in APERTURE_SIZES.items():
            self.apply_aperture(mirror, diameters[int(use_substrate)])

    def apply_aperture(self, mirror, diameter=None):
        """Applies a circular aperture surface map to the mirror.

        Parameters
        ----------
        mirror : str
            Name of the mirror to which to apply the aperture.
        diameter : float, optional
            Diameter, in meters, of the circular aperture. Defaults to the substrate diameter in the aperture table.
        """

        # use substrate diameter by default
        if diameter is None:
            diameter = APERTURE_SIZES[mirror][1]

        # create the aperture map
        radius = diameter / 2
        x = y = np.linspace(-radius, radius, 100)
        smap = Map(
            x,
            y,
            amplitude=circular_aperture(x, y, radius, x_offset=0.0, y_offset=0.0),
        )

        # apply to the mirror
        self.model.get(mirror).surface_map = smap

    def adjust_PRC_length(self):
        self.adjust_recycling_cavity_length("PRC", "lPRC", "lPOP_BS")

    def adjust_SRC_length(self):
        self.adjust_recycling_cavity_length("SRC", "lSRC", "lsr")

    # can be repeated
    # TODO: should the length in the common file use the variable?
    #   Could otherwise be done with just the cavity space: self.adjust_cavity_length("lsr")
    def adjust_recycling_cavity_length(
        self, cavity: str, L_in: str, S_out: str, verbose=False
    ):
        """Adjust cavity length so that it fulfils the requirement:

            L = 0.5 * c / (2 * f6), see TDR 2.3 (VIR–0128A–12).

        Parameters
        ----------
        cavity : str
            Name of the cavity being adjusted.
        L_in : str
            Variable used to define the length of the cavity. Needed because the common file does not use a variable.
        S_out : str
            Name of the space component used to adjust the cavity.
        """

        # works also for legacy
        f6 = self.model.get("eom6.f").value

        if self.verbose or verbose:
            print(f"——  adjusting {cavity} length")

        # calculate the required adjustment
        tmp = 0.5 * CONSTANTS["c0"] / (2 * f6)
        delta_l = tmp.eval() - self.model.get(L_in).value.eval()

        if self.verbose or verbose:
            print(f"    adjusting {S_out}.L by {delta_l:.4g} m")

        # apply the adjustment
        self.model.get(S_out).L += delta_l

    # can be repeated
    def pretune(self, verbose=None):
        # store the modulation index for use later
        midx = self.model.eom56.midx.value

        if verbose is None:
            verbose = self.verbose

        # do the pretuning
        self.model.run(
            TemporaryParameters(
                Series(
                    # Switch off the modulators and remove SR and PR by misaligning them. This ensures only the carrier is present and the arms are isolated.
                    Change(
                        {
                            "eom6.midx": 0,
                            "eom8.midx": 0,
                            "eom56.midx": 0,
                            "SR.misaligned": True,
                            "PR.misaligned": True,
                            "SRAR.misaligned": True,
                            "PRAR.misaligned": True,
                        }
                    ),
                    # Maximise arm power
                    Maximize("B7_DC", "NE_z.DC", bounds=[-180, 180], tol=1e-14),
                    Maximize("B8_DC", "WE_z.DC", bounds=[-180, 180], tol=1e-14),
                    # Minimise dark fringe power
                    Minimize("B1_DC", "MICH.DC", bounds=[-180, 180], tol=1e-14),
                    # Bring back PR
                    Change({"PR.misaligned": False}),
                    # Maximise PRC power
                    Maximize("CAR_AMP_BS", "PRCL.DC", bounds=[-180, 180], tol=1e-14),
                    # Bring in SR
                    Change({"SR.misaligned": False}),
                    # Maximise SRC power
                    # B4_112 requires 56MHz
                    Change({"SRCL.DC": 0, "eom56.midx": midx}),
                    Maximize("B4_112_mag", "SRCL.DC", bounds=[-180, 180], tol=1e-14),
                ),
                exclude=(
                    "PR.phi",
                    "NI.phi",
                    "NE.phi",
                    "WI.phi",
                    "WE.phi",
                    "SR.phi",
                    "NE_z.DC",
                    "WE_z.DC",
                    "MICH.DC",
                    "PRCL.DC",
                    "SRCL.DC",
                ),
            )
        )

        # round off dofs to a reasonable level of precision
        self.model.NE_z.DC = round(self.model.NE_z.DC.value, 4)
        self.model.WE_z.DC = round(self.model.WE_z.DC.value, 4)
        self.model.MICH.DC = round(self.model.MICH.DC.value, 4)
        self.model.PRCL.DC = round(self.model.PRCL.DC.value, 4)
        self.model.SRCL.DC = round(self.model.SRCL.DC.value, 3)

        if verbose:
            self.print_tunings()
            self.print_powers()

    def print_dofs(self, msg=None):
        print(f"——  DOFs {msg if msg else ''}:")
        for dof in self.dofs:
            print(f'    {dof}: {self.model.get(dof + ".DC").value}')

    # can be repeated
    def apply_dc_offset(self, verbose=False):
        """_summary_"""
        self.model.run(
            Series(
                # Switch off the modulators for pretuning
                TemporaryParameters(
                    Series(
                        Change({"eom6.midx": 0, "eom8.midx": 0, "eom56.midx": 0}),
                        # Find the exact dark fringe, then search only for the negative solution
                        Minimize("B1_DC", "DARM.DC", tol=1e-10),
                        Minimize(
                            "B1_DC",
                            "DARM.DC",
                            method=None,
                            bounds=[self.model.DARM.DC - 90, self.model.DARM.DC],
                            offset=4e-3,
                            tol=1e-14,
                        ),
                    ),
                    exclude=("NE_z.DC", "WE_z.DC", "DARM.DC"),
                )
            )
        )

        if self.display_plots:
            self.plot_QNLS(axis=[5, 500, 100])

        if self.verbose or verbose:
            self.print_powers()

        if self.display_plots:
            self.plot_powers()

    def plot_powers(self, xscale=None, figsize=(8, 6)):
        """Plot grid of dof plots of interest when pretuning."""

        # prepare some lists
        powers_dofs = [
            ("CAR_AMP_W", "WE_z", 1),
            ("CAR_AMP_N", "NE_z", 1),
            ("CAR_AMP_AS", "MICH", 6),
            ("CAR_AMP_BS", "PRCL", 50),
            ("CAR_AMP_AS", "SRCL", 40),
            ("CAR_AMP_AS", "DARM", 0.001),
        ]

        # create the subplot axies
        fig, axs = plt.subplots(3, 2, figsize=figsize)
        axs = axs.flatten()

        # create one plot per dof
        for i, (detector, dof, _xscale) in enumerate(powers_dofs):
            out = self.dof_plot(
                dof,
                detector,
                xscale=xscale or _xscale,
                show=False,
            )

            # TODO: use detector port rather than name
            axs[i].semilogy(out.x[0], np.abs(out[detector]) ** 2, label=detector)

            axs[i].set(
                xlabel=f"{dof} [deg]",
                ylabel=f"{detector} [W]",
            )

        plt.tight_layout(pad=1.2)

        return fig, axs

    def dof_plot(
        self, dof, detector, axis=[-1, 1, 200], xscale=1, logy=True, show=True
    ):
        """Sweep across a DoF, reading out at the provided detector."""
        axis = np.array(axis, dtype=np.float64)
        axis[:2] *= xscale
        out = self.model.run(
            Xaxis(f"{dof}.DC", "lin", axis[0], axis[1], axis[2], relative=True)
        )

        if show:
            try:
                out.plot([detector], logy=logy, degrees=False)
            except AttributeError:
                # Workaround for `out.plot()` not currently working for readouts
                plt.figure()
                if logy:
                    plt.semilogy(out.x[0], np.abs(out[detector]), label=detector)
                else:
                    plt.plot(out.x[0], np.abs(out[detector]), label=detector)
                plt.xlabel(dof.name + " DC")
                plt.ylabel("A.U.")
                plt.show()

        return out

    # TODO: add ability to provide list of detectors (handle ad or pd)?
    def get_powers(self):
        """Return a dictionary of carrier powers keyed by detector."""

        # run the model without modulation to get the carrier powers
        out = self.model.run(
            Series(
                Temporary(
                    Change(
                        {
                            "eom8.midx": 0,
                            "eom6.midx": 0,
                            "eom56.midx": 0,
                        }
                    ),
                    Noxaxis(),
                )
            )
        )

        powers = {}
        for detector in self.model.detectors:
            # only grab output for carrier detectors
            if "CAR_AMP" in detector.name:
                power = np.abs(out[detector]) ** 2
                ratio = power / self.model.i1.P
                powers[detector.name] = [power, ratio]

        return powers

    # TODO: add ability to provide list of detectors (handle ad or pd)?
    def print_powers(self):
        """Display a table listing the carrier powers and power ratios."""

        powers = self.get_powers()

        table = NumberTable(
            list(powers.values()),
            colnames=["Detector", "Power [W]", "Pow. ratio"],
            rownames=list(powers.keys()),
            numfmt=["{:9.4g}", "{:9.4g}"],
            compact=True,
        )

        print(table)

    def filter_readout_sequence(self, sequence):
        """Filter a given sequence of dof readout pairs.

        Given a sequence of dof readout pairs, prioritize I over Q if
        duplicate readouts are found.

        Parameters
        ==========
        sequence: list
            Sequence of dof, readout_signal pairs. E.g.,
            ['PRCL', 'B2_8_I', 'MICH', 'B2_56_Q', 'SRCL', 'B2_56_I'].
            If duplicate readouts are found (B2_56 in the previous example),
            the Q signal and associated dof will be removed.
        """

        # Extracting control signals without the "_I" or "_Q" suffixes
        signals = [signal.rsplit("_", 1)[0] for signal in sequence[1::2]]

        # Identifying duplicates
        duplicates = set([signal for signal in signals if signals.count(signal) > 1])

        # Filtering out the Q to prioritize I
        filtered_sequence = []
        for i in range(0, len(sequence), 2):
            readout = sequence[i + 1].rsplit("_", 1)[0]

            # If it's a duplicate and ends with "_Q", skip
            if readout in duplicates and sequence[i + 1].endswith("_Q"):
                continue

            # Otherwise, add the pair to the filtered list
            filtered_sequence.extend([sequence[i], sequence[i + 1]])

        return filtered_sequence

    # TODO: can probably do this better
    # TODO: ensuring unique readouts should be handled by OptimizeRFReadoutPhaseDC in Finesse?
    def optimize_demodulation_phase(
        self, dofs=None, readouts=None, d_dof=1e-7, verbose=False
    ):
        """Optimize the demodulation phases.

        If provided both I and Q for the same readout, the I quadrature will be
        optimized and the Q ignored.
        """

        if dofs is None:
            dofs = self.dofs

        if readouts is None:
            readouts = self.dof_readouts

        # Ignore any readouts which can be inferred from the others
        #   e.g., B2_56_I and B2_56_Q are always 90 degrees from each other
        #   so only collect and optimize the B2_56_I.
        sequence = [i for s in zip(dofs, readouts) for i in s]
        filtered_dof_readout_pairs = self.filter_readout_sequence(sequence)

        self.model.run(
            OptimiseRFReadoutPhaseDC(*filtered_dof_readout_pairs, d_dof=d_dof)
        )

        # update the sensing matrix
        self.update_sensing_matrix()

        if self.verbose or verbose:
            print("--  Optimized demodulation phases:")
            for dof, lock in self.control_scheme.items():
                readout, port, _, _ = lock

                # only display for provided dofs/readouts
                if dof in dofs and readout in readouts:
                    phase = self.model.get(f"{readout}.phase").value + (
                        0 if port == "I" else 90
                    )
                    print(
                        f"    {dof:8} {'_'.join([readout, port]):10}: phase={phase:8.4f}"
                    )

            print("--  Suggested lock gains:")
            for dof, lock in self.control_scheme.items():
                readout, port, _, _ = lock

                # only display for provided dofs/readouts
                if dof in dofs and readout in readouts:
                    optical_gain = self.sensing_matrix.out[
                        dofs.index(dof), readouts.index(readout)
                    ]
                    lock_gain = -1 / (
                        optical_gain.real if port == "I" else optical_gain.imag
                    )

                    print(
                        f"    {dof:8s} {'_'.join([readout, port]):10s}: {-1 / lock_gain:10.5g}"
                    )

    def get_sensing_matrix(self, dofs=None, readouts=None, d_dof=1e-6):
        """Calculate and return a new sensing matrix.

        This will not automatically update the state of the local sensing matrix.
        Use `update_sensing_matrix()` to do this.

        Parameters
        ----------
        dofs : list of str, optional
            DOFs to include in the sensing matrix. Default to includes all DOFs from control scheme.

        readouts : list of str, optional
            Readouts to include in the sensing matrix. Default to include unique readouts from the control scheme.

        Returns
        -------
        SensingMatrixSolution
            The sensing matrix.
        """

        if dofs is None:
            dofs = self.dofs

        if readouts is None:
            readouts = self.unique_readouts

        return self.model.run(SensingMatrixDC(dofs, readouts, d_dof=d_dof))

    def update_sensing_matrix(self):
        """Update the local sensing matrix. This is to avoid having to re-create the
        sensing matrix each time it is called and will always run the full sensing
        matrix.

        Returns
        -------
        SensingMatrixSolution
        """

        self.__sensing_matrix = self.get_sensing_matrix()

        return self.sensing_matrix

    # TODO: ensure only one plot is shown when only one readout is selected
    def plot_sensing_matrix(
        self, dofs=None, readouts=None, sensing_matrix=None, figsize=(8, 8)
    ):
        """Plots the sensing matrix as a grid of radar plots.

        Parameters
        ----------
        dofs : list of str, optional
            DOFs to include. Defaults to all.

        readouts : list of str, optional
            Readouts to include. Defaults to all.

        sensing_matrix : SensingMatrixDC, optional
            Sensing matrix to use for plots if provided, otherwise attempts to use
            the existing sensing matrix and calculates a new one if needed.
        """

        # use stored sensing matrix if one is not provided
        if sensing_matrix is None:
            sensing_matrix = self.sensing_matrix

        # prepare some lists
        dofs = np.atleast_1d(dofs or self.dofs)
        readouts = np.atleast_1d(readouts or self.unique_readouts)

        # create the subplot axies
        Nrows = int(np.ceil(len(readouts) / 2))
        Ncols = 2
        fig, axs = plt.subplots(
            Nrows,
            Ncols,
            subplot_kw={"projection": "polar"},
            squeeze=False,
            figsize=figsize,
        )
        axs = axs.flatten()

        # create one plot per readout
        for i in range(len(readouts)):
            self.plot_radar(
                readouts[i], dofs=dofs, sensing_matrix=sensing_matrix, ax=axs[i]
            )

        fig.legend(dofs, loc="center", bbox_to_anchor=(0.5, 1), fontsize=8)
        plt.tight_layout(pad=1.2)

        return fig, axs

    def print_sensing_matrix(self):
        """Convenience function for get/plot/print nomenclature consistency."""

        # print it out
        print(self.sensing_matrix)

    def plot_radar(self, readout, dofs=None, sensing_matrix=None, ax=None):
        """Plots a radar plot for a readout according to the sensing matrix.

        Parameters
        ----------
        readout : str
            Readout to use for sensing dofs.
        dofs : [str], optional
            Degrees of freedom to use when sensing.
        sensing_matrix : SensingMatrixDC, optional
            Sensing matrix to use for the plot, otherwise a new one will be created.
        ax : AxesSubplot
            Subplot axes to use when plotting. This is useful if the plot will be added to a grid of several plots. See `plot_sensing_matrix()`.
        """

        if dofs is None:
            dofs = self.dofs

        if sensing_matrix is None:
            sensing_matrix = self.sensing_matrix

        if ax is None:
            _, axs = plt.subplots(
                1,
                1,
                subplot_kw={"projection": "polar"},
                squeeze=False,
            )
            ax = axs[0][0]

        # get the data from the sensing matrix
        data = sensing_matrix.out[
            tuple(sensing_matrix.dofs.index(dof) for dof in dofs),
            sensing_matrix.readouts.index(readout),
        ]

        # determine the radius length
        r_lim = (np.log10(np.abs(data)).min() - 1, np.log10(np.abs(data)).max())

        theta = np.angle(data)
        r = np.log10(np.abs(data))
        ax.plot(
            (theta, theta),
            (r_lim[0] * np.ones_like(r), r),
            marker="D",
            markersize=4,
        )
        ax.set(
            title=f"{readout}, phase = {float(self.model.get(readout).phase):2.4g}°",
            ylim=[r_lim[0], r_lim[1] + 1],
            theta_zero_location="E",
            yticklabels=[],
        )

        return ax

    def update_locks(self):
        # adf test, does not work, as locks are not updating in the model
        for dof, lock in self.control_scheme.items():
            readout, port, accuracy, _ = lock
            if self.verbose:
                print(f"Updating {dof} lock")
            # Handle DARM separately for now since we'll lock on both RF and DC.
            if dof != "DARM":
                self.model.get(f"{dof}_lock").readout = readout
                self.model.get(f"{dof}_lock").port = port
                self.model.get(f"{dof}_lock").accuracy = accuracy
            else:
                self.model.get(f"{dof}_rf_lock").readout = readout
                self.model.get(f"{dof}_rf_lock").port = port
                self.model.get(f"{dof}_rf_lock").accuracy = accuracy

    def add_locks(self):
        """Adds the locks contained within the control scheme. Assumes the locks have
        not already been parsed. If any lock already exists, then this will do nothing.

        Parameters
        ----------
        rms : dict, optional
            Loop accuracies in meters (manually tuned for the loops to work with the
            default file). To compute accuracies from rms, we convert rms to radians
            as rms_rad = rms * 2 pi/lambda and then multiply by the optical gain.

        Returns True when parsing occurs, False when it is skipped.
        """

        # check if any of the locks already exist
        lock_names = [lock.name for lock in self.model.locks]
        new_lock_names = [lock + "_lock" for lock in self.control_scheme.keys()]
        lock_exists = any(lock in lock_names for lock in new_lock_names)

        # if any of the locks already exist, do nothing
        if lock_exists:
            if self.verbose:
                print("Cannot create new locks, other locks already exist.")

            return False

        # to make sure any changes are used, let's run init on control schemes again
        self.init_control_scheme()

        if self.verbose:
            print(f"Adding locks for {new_lock_names}.")

        # We can generate the locks from the control scheme
        for dof, (readout, port, accuracy, rms) in self.control_scheme.items():
            # compute the lock accuracy using the rms and optical gain
            #   optical gain is W/deg
            if not accuracy:
                factor = 360 / self.model.lambda0
                optical_gain = self.get_optical_gain(dof, dof)

                accuracy = round_to_n(np.abs(factor * rms * optical_gain), 2)

            # Handle DARM separately for now since we'll lock on both RF and DC.
            if dof != "DARM":
                self.model.parse(
                    f"lock {dof}_lock {readout}.outputs.{port} {dof}.DC 1 {accuracy}"
                )
            else:
                self.model.parse(
                    f"lock {dof}_rf_lock {readout}.outputs.{port} {dof}.DC 1 {accuracy}"
                )

                # lock DARM to 4mW
                # TODO: incorporate this into the control scheme somehow
                self.model.parse(
                    f"lock {dof}_dc_lock B1.outputs.DC {dof}.DC 1 {accuracy} offset=4m enabled=false"
                )

    def get_optical_gain(self, dof_in, dof_out, sensing_matrix=None):
        # if no sensing matrix is provided, use the existing one, or get a new one
        if not sensing_matrix:
            sensing_matrix = self.sensing_matrix

        in_idx = self.dofs.index(dof_in)
        out_idx = self.readouts.index(self.control_scheme[dof_out][0])
        value = sensing_matrix.out[in_idx][out_idx]

        return value.real if self.control_scheme[dof_out][1] == "I" else value.imag

    def optimize_lock_gains(self, sensing_matrix=None, verbose=False):
        """"""
        if sensing_matrix is None:
            sensing_matrix = self.sensing_matrix

        # for each dof
        for dof, lock in self.control_scheme.items():
            readout, port, _, _ = lock
            # get the optical gain from the sensing matrix and calculate the lock gain
            optical_gain = sensing_matrix.out[
                self.dofs.index(dof), self.readouts.index(readout)
            ]
            lock_gain = -1 / (optical_gain.real if port == "I" else optical_gain.imag)

            # set the lock gain
            if dof != "DARM":
                self.model.get(f"{dof}_lock").gain = lock_gain
            else:
                self.model.get(f"{dof}_rf_lock").gain = lock_gain
                self.model.get(f"{dof}_dc_lock").gain = lock_gain

        if self.verbose or verbose:
            print("--  Optimized lock gains:")
            for dof, lock in self.control_scheme.items():
                readout, port, _, _ = lock

                if dof != "DARM":
                    print(
                        f"    {dof:8s} {'_'.join([readout, port]):10s}: {self.model.get(f'{dof}_lock').gain:10.5g}"
                    )
                else:
                    # lock gain for DARM RF and DC will be the same
                    print(
                        f"    {dof:8s} {'_'.join([readout, port]):10s}: {self.model.get(f'{dof}_rf_lock').gain:10.5g}"
                    )

    def optimize_TL(self, accuracy=1, verbose=False):
        """Optimizes the focal point of the thermal lenses by minimizing a figure of
        merit as defined by the `opt_tl` detector.

        Parameters
        ----------
        accuracy : float, optional
            Accuracy to which to tune the focal length, in meters.
        """

        cp_old = accuracy + 1
        cp_old_w = accuracy + 1
        cp_new = np.abs(self.model.CPN_TL.f.eval())
        cp_new_w = np.abs(self.model.CPW_TL.f.eval())

        while np.abs(cp_new - cp_old) > accuracy:
            if verbose or self.verbose:
                print("ΔCPN_TL.f = ", np.abs(cp_new - cp_old))
                print("ΔCPW_TL.f = ", np.abs(cp_new_w - cp_old_w))

            # keep the old value
            cp_old = np.abs(self.model.CPN_TL.f.eval())
            cp_old_w = np.abs(self.model.CPW_TL.f.eval())

            # optimize and run the locks
            self.model.run(Minimize("opt_tl", ["f_CPN_TL", "f_CPW_TL"]))
            self.optimize_demodulation_phase()
            self.optimize_lock_gains()
            self.model.run(RunLocks(method="newton"))

            # keep the new value
            cp_new = np.abs(self.model.CPN_TL.f.eval())
            cp_new_w = np.abs(self.model.CPW_TL.f.eval())

    def get_DARM(
        self,
        dof="DARM_Fz",
        readout_port="B1p_56.I",
        rf_sidebands=True,
        axis=[0.5, 1000, 200],
    ):
        """Return the DARM transfer function.

        Parameters
        ----------
        dof : str, optional
            The DOF to inject the signal into. This is typically either DARM or DARM_Fz.
        readout_port : str, optional
            The readout port out of which to read the signal. This is typically 'B1p_56.I'.
        rf_sidebands : boolean, optional
            If false, will turn off the modulators producing the RF sidebands.
        axis : [start, stop, points], optional
            Start, stop, and number of points to use on the xaxis.
        """
        model = self.model.deepcopy()

        # optionally turn off the RF sidebands
        if not rf_sidebands:
            model.eom6.order = 0
            model.eom8.order = 0

        # set to signal simulation
        model.fsig.f = 1

        # do frequency response
        return model.run(FrequencyResponse(np.geomspace(*axis), [dof], [readout_port]))

    def plot_DARM(
        self,
        dof="DARM_Fz",
        readout_port="B1p_56.I",
        axis=[0.5, 1000, 200],
        ax=None,
        **kwargs,
    ):
        """Plots the DARM TF.

        Parameters
        ----------
        dof : str, optional
            Degree of freedom to use for measuring DARM.
        readout_port : str, optional
            Detector port to read the output.
        axis : [start, stop, points], optional
            Start, stop, and number of points to use on the xaxis.
        ax : matplotlib.axes.Axes, optional
            Matplotlib axes to use for the plot.
        label : str, optional
            Label to use for the plot.
        """

        # get points for DARM
        out = self.get_DARM(dof=dof, readout_port=readout_port, axis=axis)

        # create a new axis if none exists
        if ax is None:
            _, ax = plt.subplots(2)
            ax[0].set(
                title="DARM TF",
                ylabel=r"Amplitude [$\sqrt{W}$]",
            )
            ax[1].set(
                xlabel="f [Hz]",
                ylabel="Phase [deg]",
            )

        # prepare the default label
        if "label" not in kwargs:
            kwargs["label"] = f"{dof}->{readout_port}"

        H = out.out[:, 0, 0].squeeze()
        ax[0].loglog(out.f, np.abs(H), **kwargs)
        ax[1].semilogx(out.f, np.angle(H, deg=True), **kwargs)

        ax[0].legend()

        return ax

    # can be repeated
    # TODO: convert to utility?
    def get_QNLS(self, axis=[5, 5000, 100]):
        # allows for repetition
        kat = self.model.deepcopy()

        kat.parse(
            """#kat
            # Differentially modulate the arm lengths
            fsig(1)
            sgen darmx LN.h
            sgen darmy LW.h phase=180

            # Output the full quantum noise limited sensitivity
            qnoised NSR_with_RP B1.p1.i nsr=True

            # Output just the shot noise limited sensitivity
            qshot NSR_without_RP B1.p1.i nsr=True
        """
        )

        return kat.run(f'xaxis(darmx.f, "log", {axis[0]}, {axis[1]}, {axis[2]})')

    def plot_QNLS(
        self,
        axis=[5, 5000, 400],
        ax=None,
        shot_noise_only=False,
        **kwargs,
    ):
        """Plots the quantum noise limited sensitivity.

        Parameters
        ----------
        axis : [start, stop, points], optional
            Start, stop, and number of points to use on the xaxis.
        ax : matplotlib.axes.Axes, optional
            Matplotlib axes to use for the plot.
        shot_noise_only : boolean, optional
            Plot only the shot noise.
        """

        # grab QNLS points
        out = self.get_QNLS(axis)

        # prepare default label
        if "label" not in kwargs:
            kwargs["label"] = "NSR" + (" (shot noise only)" if shot_noise_only else "")

        # prepare the plot if making a new one
        if ax is None:
            _, ax = plt.subplots()
            ax.set(
                title="Quantum Noise Limited Sensitivity",
                xlabel="fsig.f [Hz]",
                ylabel=r"ASD [1/$\sqrt{Hz}$]",
            )

        # plot NSR
        ys = abs(out["NSR_without_RP" if shot_noise_only else "NSR_with_RP"])
        ax.loglog(out.x1, ys, **kwargs)
        ax.legend()

        return ax

    # TODO: generate from THERMAL_STATES
    def print_thermal_values(self):
        table = NumberTable(
            [
                [self.model.PR.Rc[0]],
                [self.model.PR.Rc[1]],
                [self.model.SR.Rc[0]],
                [self.model.SR.Rc[1]],
                [self.model.f_CPN_TL.value.value],
                [self.model.f_CPW_TL.value.value],
            ],
            colnames=["Thermal Parameter", "Value"],
            rownames=["PR.Rcx", "PR.Rcy", "SR.Rcx", "SR.Rcy", "f_CPN_TL", "f_CPW_TL"],
            numfmt="{:11.2f}",
            compact=True,
        )

        print(table)

    def plot_error_signals(self, xscale=None, range=None, figsize=(8, 6)):
        """Plot grid of error signals."""

        # create the subplot axies
        fig, axs = plt.subplots(3, 2, figsize=figsize)
        axs = axs.flatten()

        _range = {
            "CARM": [-0.01, 0.01, 200],
            "DARM": [-0.1, 0.1, 200],
            "MICH": [-1.0, 1.0, 200],
            "PRCL": [-1.0, 1.0, 200],
            "SRCL": [-1.0, 1.0, 200],
        }

        if type(range) is dict:
            for _ in range.keys():
                _range[_] = range[_]
        else:
            if range is not None:
                print("range must be a dictionary")

        # create one plot per dof
        for i, lock in enumerate(self.model.locks):
            dof = lock.feedback.name.split(".")[0]
            detector = lock.error_signal.name

            if dof in _range.keys():
                out = self.dof_plot(dof, detector, axis=_range[dof], show=False)
            else:
                out = self.dof_plot(dof, detector, show=False)

            # TODO: use detector port rather than name
            axs[i].plot(out.x[0], out[detector], label=detector)

            axs[i].set(
                xlabel=f"{dof} [deg]",
                ylabel=f"{detector} [W]",
            )
            # axs[i].legend()

        plt.tight_layout(pad=1.2)

        return fig, axs

    def dof_from_lock(self, lock):
        """Extracts the name of the dof controlled by the lock."""
        dof = lock.split("_lock")[0]

        if dof == "DARM_rf" or dof == "DARM_dc":
            return "DARM"

        return dof

    def get_error_signals(self):
        """Returns a list of error signals, keyed by dof."""

        # run the model to get the output
        out = self.model.run(Noxaxis())

        # build the dictionary from the locks that ran
        error_signals = {}
        for lock in self.model.locks:
            dof = self.dof_from_lock(lock.name)
            error_signals[dof] = out[lock.error_signal.name]

        return error_signals

    def get_dof_lock(self, dof):
        """Returns the lock object currently enabled for the DOF.

        Needed to differentiate between DARM DC and RF lock.
        """

        if dof not in self.control_scheme.keys():
            raise Exception(f"DOF {dof} must be defined in the control scheme.")

        # if DARM, return the enabled lock
        if dof == "DARM":
            dc_lock = self.model.DARM_dc_lock
            rf_lock = self.model.DARM_rf_lock

            lock = dc_lock if dc_lock.enabled else rf_lock
        else:
            lock = self.model.get(f"{dof}_lock")

        return lock

    def print_error_signals(self):
        """Display a table of DOFs, the readout error signals, and their current
        values."""

        data = [["DOF", "signal", "error [W]"]]

        for dof, error_signal in self.get_error_signals().items():
            data.append(
                [
                    f"{dof:6}",
                    f"{self.get_dof_lock(dof).error_signal.name:9}",
                    f"{error_signal:9.4g}",
                ]
            )

        table = Table(data, alignment=["left", "left", "right"], compact=True)
        print(table)

    # TODO: find better name since this is not just "lengths"
    def print_lengths(self):
        f6 = float(self.model.eom6.f.value)
        f8 = float(self.model.eom8.f.value)
        f56 = float(self.model.eom56.f.value)

        # TODO: use table generator
        print(
            f"""┌─────────────────────────────────────────────────┐
│- Arm lengths [m]:                               │
│  LN   = {self.model.elements["LN"].L.value:<11.4f} LW = {self.model.elements["LW"].L.value:<11.4f}            │
├─────────────────────────────────────────────────┤
│- Michelson and recycling lengths [m]:           │
│  ln   = {float(self.model.ln.value):<11.4f} lw       = {float(self.model.lw.value):<11.4f}      │
│  lpr  = {float(self.model.lpr.value):<11.4f} lsr      = {float(self.model.lsrbs.value):<11.4f}      │
│  lMI  = {float(self.model.lMI.value):<11.4f} lSchnupp = {float(self.model.lSchnupp.value):<11.4f}      │
│  lPRC = {float(self.model.lPRC.value):<11.4f} lSRC     = {float(self.model.lSRC.value):<11.4f}      │
├─────────────────────────────────────────────────┤
│- Associated cavity frequencies [Hz]:            │
│  fsrN   = {float(self.model.fsrN.value):<11.2f} fsrW   = {float(self.model.fsrW.value):<11.2f}      │
│  fsrPRC = {float(self.model.fsrPRC.value):<11.2f} fsrSRC = {float(self.model.fsrSRC.value):<11.2f}      │
│                                                 │
│- Modulation sideband frequencies [MHz]:         │
│  f6     = {f6 / 1e6:<12.6f} f8     = {f8 / 1e6:<12.6f}    │
│  f56     = {f56 / 1e6:<12.6f}                         │
├─────────────────────────────────────────────────┤
│- Check frequency match [MHz]:                   │
│  125.5*fsrN-300 = {(125.5 * float(self.model.fsrN.value) - 300) / 1e6:<8.6f}                      │
│  0.5*fsrPRC     = {0.5 * float(self.model.fsrPRC.value) / 1e6:<8.6f}                      │
│  0.5*fsrSRC     = {0.5 * float(self.model.fsrSRC.value) / 1e6:<8.6f}                      │
│  9*f6           = {9 * f6 / 1e6:<8.6f}                     │
└─────────────────────────────────────────────────┘"""
        )

    def zero_dof_tunings(self, dofs=None):
        """This function will move the current DoF DC values into the phi parameter of
        the driven component before resetting the DoF DC value to zero.

        Parameters
        ----------
        dofs : list or str, optional
            List of dofs to zero. By default, will zero all dofs found in the model.
        """

        # allow a list of dofs to be passed
        if dofs is None:
            dofs = self.get_dofs()

        # make sure it is
        if type(dofs) is not list:
            dofs = [dofs]

        for dof in dofs:
            # if it isn't a component, get it from the model
            if type(dof) is str:
                dof = self.model.get(dof)

            # move each dof value into phi with the appropriate sign
            for drive, amp in zip(dof.drives, dof.amplitudes):
                component = drive.name.split(".")[0]
                self.model.get(component).phi += dof.DC * amp

            # zero the dof value
            dof.DC = 0

    # TODO: move to Finesse 3 model?
    def get_dofs(self):
        return list(filter(lambda c: type(c) is DegreeOfFreedom, self.model.components))

    # TODO: could be moved the Finesse 3?
    # TODO: rename to get_dofs_by_optic()?
    def get_dofs_by_component(self):
        """Returns a dictionary, keyed by component name, with a list of dof/amp pairs
        driving each component."""
        dofs_by_component = {}

        dofs = self.get_dofs()
        for dof in dofs:
            for drive, amp in zip(dof.drives, dof.amplitudes):
                component = drive.name.split(".")[0]
                if component not in dofs_by_component.keys():
                    dofs_by_component[component] = []

                dofs_by_component[component].append((dof.name, amp))

        return dofs_by_component

    def deg2m(self, deg, inverse=False):
        conversion = self.model.lambda0 / 360
        return deg * conversion ** (-1 if inverse else 1)

    def get_tuning(self, name):
        """Return the full phi + DC tuning for the optic/dof.

        For optics, it is sum of the phi of the mirror and DC value of each dof contribution
        # For dofs, it is the sum of the DC value and phi contribution of each mirror.

        Parameters
        ----------
        name : str
            Name of the component of which to get the tuning.
        """

        component = self.model.get(name)

        if isinstance(component, DegreeOfFreedom):
            # does not seem to work
            # # dof tuning is DC + all optic
            # tuning = component.DC

            # # sum up the contribution from each relevant optic
            # for drive, amp in zip(component.drives, component.amplitudes):
            #     mir = drive.name.split(".")[0]
            #     tuning += amp * self.model.get(mir).phi

            # return tuning
            pass
        else:
            # handle optic
            pairs = self.get_dofs_by_component()[name]

            tuning = component.phi + sum(
                [self.model.get(dof).DC.value * amp for dof, amp in pairs]
            )

        return tuning

    # TODO: move to Finesse 3?
    def get_tunings(
        self,
        include=[
            "NE",
            "WE",
            "NI",
            "WI",
            "PR",
            "SR",
        ],
        meters=False,
    ):
        """Sums together current phi position and all dof contributions.

        Returns dict with deg and meters, combining both mirrors and dofs.
        """
        tunings = {}
        include_all = include is None

        # mirror tunings
        for component, pairs in self.get_dofs_by_component().items():
            # only include provided tunings
            if not include_all and component not in include:
                continue

            phi = self.model.get(f"{component}.phi")

            tuning = phi + sum(
                [self.model.get(dof).DC.value * amp for dof, amp in pairs]
            )

            tunings[component] = tuning if meters is False else self.deg2m(tuning)

        # dof tunings
        for dof in self.get_dofs():
            # only include provided tunings
            if not include_all and dof.name not in include:
                continue

            # tuning = self.get_tuning(dof.name)
            # tunings[dof.name] = tuning if meters is False else self.deg2m(tuning)
            tunings[dof.name] = None

        return tunings

    def get_phi_tunings(self):
        """Returns a dictionary of phi tunings, keyed by optic."""
        phi_tunings = {}

        for optic in self.get_dofs_by_component().keys():
            phi_tunings[optic] = self.model.get(optic).phi.eval()

        return phi_tunings

    def get_dof_tunings(self):
        """Returns a dictionary of dof tunings, keyed by dof."""
        dof_tunings = {}

        for dof in self.control_scheme.keys():
            dof_tunings[dof] = self.model.get(dof).DC.eval()

        return dof_tunings

    def set_phi_tunings(self, phi_tunings):
        """Sets phi parameter for provided dictionary keyed by mirror."""

        for mirror, phi_tuning in phi_tunings.items():
            self.model.get(mirror).phi.value = phi_tuning

    def set_dof_tunings(self, dof_tunings):
        for dof, dof_tuning in dof_tunings.items():
            self.model.get(dof).DC.value = dof_tuning

    # TODO: get optic tunings by dof
    def print_tunings(self):
        data = [
            ["Optic/DOF", "phi [deg]", "dof.DC [deg]", "Tuning [deg]", "Tuning [pm]"]
        ]

        # build phi and dc columns
        for tuning, degs in self.get_tunings().items():
            if degs is not None:
                pmeters = self.deg2m(degs) / 1e-12
            else:
                pmeters = None

            # handle dof and optic differently
            if tuning in self.control_scheme.keys():
                dc = self.model.get(tuning).DC.eval()
                phi = None
            else:
                dc = None
                phi = self.model.get(tuning).phi.eval()

            data.append(
                [
                    tuning,
                    "" if phi is None else f"{phi:10.4g}",
                    "" if dc is None else f"{dc:10.4g}",
                    "" if degs is None else f"{degs:12.6g}",
                    "" if pmeters is None else f"{pmeters:12.6g}",
                ]
            )

        for tuning, dc in self.get_dof_tunings().items():
            data.append(
                [
                    tuning,
                    "",
                    f"{dc:10.4g}",
                    "",
                    "",
                ]
            )

        table = Table(
            data, alignment=["left", "right", "right", "right", "right"], compact=True
        )

        print(table)

    # TODO: check that all mirrors are present
    def set_tunings(self, tunings):
        """Sets the phi parameters on the mirrors and zeroes all dofs so that all
        tunings are contained within the mirrors (rather than a combination of
        phi+dof.DC).

        Parameters
        ----------
        tunings : {}
            Dictionary of tunings, indexed by mirror name. Must contain all relevant mirrors.
        """

        # set the tunings on the mirrors
        for mirror in self.get_dofs_by_component().keys():
            self.model.get(mirror).phi = tunings[mirror]

        # zero out the dofs
        for dof in self.dofs:
            self.model.get(dof).DC = 0

    # TODO: needs testing
    def sensing_W_to_m(
        self, watts, dof, readout_port=None, sensing_matrix=None, inverse=False
    ):
        """Uses the sensing matrix to convert the dof readout power from Watts to meters
        and vice versa.

        Parameters
        ----------
        value : float
            Value to convert from W to m (or m to W)
        dof : str
            The DOF to use for the conversion.
        readout_port : str, optional
            Name of readout port to use for the conversion. Defaults to the one assigned to the DOF according to the control scheme.
        sensing_matrix : SensingMatrix, optional
            Sensing matrix to use, if provided. If not provided, then a new sensing matrix will be computed.
        """

        # compute the sensing matrix if needed
        if sensing_matrix is None:
            sensing_matrix = self.sensing_matrix

        # lookup the readout from the control scheme
        if readout_port is None:
            readout = self.control_scheme[dof][0]
            port = self.control_scheme[dof][1]
        else:
            readout = "_".join(readout_port.split("_")[0:-1])
            port = readout_port.split("_")[-1]

        # get the dof/readout entry from the sensing matrix
        sm_element = sensing_matrix.out[
            self.dofs.index(dof), self.readouts.index(readout)
        ]

        # determine conversion to meters
        # sensing matrix in Finesse is W/deg, so also convert to W/m
        conversion = (
            (sm_element.real if port == "I" else sm_element.imag)
            * 360
            / self.model.lambda0
        )

        return watts * conversion ** (-1 if not inverse else 1)

    def print_pretune_status(self):
        settings = self.get_settings()
        powers = self.get_powers()
        tunings = self.get_tunings()

        print(
            f"╔══════════════════════════════════════════════════════════════════════════╗"
            f"║ Pretuned for maxtem = {(str(settings['maxtem']) + ', zero_k00 = ' + str(settings['zero_k00'])):<34} {' ' * 15} ║"
            f"║ Detector     | Power [W] : P. ratio  ║       | Tuning [deg] : Tuning [m] ║"
            f"╟──────────────┼───────────────────────╫───────┼───────────────────────────╢"
        )

        for power, tuning in zip_longest(powers.items(), tunings.items()):
            if power:
                detector, (watts, ratio) = power
                col1 = f"{str(detector):12} | {float(watts):9.4g} : {float(ratio):9.4g}"
            else:
                col1 = f"{' ' * 12} | {' ' * 9}   {' ' * 9}"

            if tuning:
                optic, degs = tuning
                meters = self.deg2m(degs)
                col2 = f"{str(optic):5} | {float(degs):12.4f} : {float(meters):10.3g}"
            else:
                col2 = f"{' ' * 5} | {' ' * 12}   {' ' * 10}"

            print(f" ║ {col1} ║ {col2} ║")

        print(
            " ╚══════════════╧═══════════════════════╩═══════╧═══════════════════════════╝"
        )

    # TODO: add a __str__ desc to a lock?
    #   something like `PRCL_lock B2_8_I PRCL.DC gain=1 enabled=true accuracy=5.3e-06`
    def print_locks(
        self,
        gain_adjustments={
            "DARM": 1.0,
            "CARM": 1.0,
            "PRCL": 1.0,
            "MICH": 1.0,
            "SRCL": 1.0,
        },
    ):
        """"""

        has_adjustment = any(adj != 1.0 for adj in gain_adjustments.values())

        factor1 = 180 / math.pi
        factor2 = 360.0 / self.model.lambda0

        print(" ╔═══════════════════════════════════════════════════════╗")
        print(" ║ Parameters for locks:                                 ║")
        print(" ╠═══════════════════════════════════════════════════════╣")
        print(
            f" ║ {'Lock name':<14} {'port':<8} {'DOF':<8} {'lock gain':<9} {'enabled':>10} ║"
        )

        # locks
        for lock in self.model.locks:
            print(
                f" ║ {lock.name:<14} {lock.error_signal.name:<8} {lock.feedback.name:<8} {float(lock.gain):>9.2} {str(lock.enabled):>10} ║"
            )

        print(" ╟───────────────────────────────────────────────────────╢")
        print(f" ║ {'Accuracies':<9} {'[deg]':>12}   {'[m]':>12}   {'[W]':>12} ║")

        # prepare lock accuracies
        lock_accs = {}
        for lock in self.model.locks:
            dof = lock.name.split("_")[0]
            lock_accs[dof] = lock.accuracy

        # loop accuracies
        for dof, (_, _, _, rms) in self.control_scheme.items():
            og_w_deg = self.get_optical_gain(dof, dof)
            acc_deg = factor2 * rms
            acc_m = rms
            acc_w = lock_accs[dof]

            print(f" ║ {dof:<9}: {acc_deg:12.6}   {acc_m:12.6}   {acc_w:12.6} ║")

        print(" ╟───────────────────────────────────────────────────────╢")
        print(f" ║ {'Optical gains   [W/deg]'}   {'[W/rad]':>12}   {'[W/m]':>12} ║")

        # optical gains
        for dof, _ in self.control_scheme.items():
            og_w_deg = self.get_optical_gain(dof, dof)
            og_w_rad = og_w_deg * factor1
            og_w_m = og_w_deg * factor2

            print(f" ║ {dof:<9}: {og_w_deg:12.5}   {og_w_rad:12.5}   {og_w_m:12.5} ║")

        if has_adjustment:
            print(" ╟───────────────────────────────────────────────────────╢")
            print(
                f" ║ {'adjustment':>21}   {'-1/opt_gain':>12}   {'adj. lock gain':>14} ║"
            )

            # gain factors
            for dof, _ in self.control_scheme.items():
                og_w_deg = self.get_optical_gain(dof, dof)

                adjustment = gain_adjustments[dof]
                gain_recip = -1 / og_w_deg
                adj_gain = adjustment * gain_recip

                print(
                    f" ║ {dof:<9}:  {adjustment:>9.4} * {gain_recip:12.6} = {adj_gain:14.6} ║"
                )

        print(" ╚═══════════════════════════════════════════════════════╝")
