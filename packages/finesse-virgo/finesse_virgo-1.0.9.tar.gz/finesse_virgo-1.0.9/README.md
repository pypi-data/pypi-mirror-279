# `finesse-virgo`

Finesse 3.0 Virgo models, tools, and data. This package is an optional extra to the `finesse` package which must be installed to use this package.

## Quick Plots
These plots have been generated using the current configuration of the model (see `scripts/build_plots.py`).

<img src="files/DARM.png" alt="DARM" width="500">
<img src="files/QNLS.png" alt="QNLS" width="500">

## Installation

### From PyPI
If you just want to use the tools and models provided you can use `pip install finesse-virgo` to install the latest tagged commit.

### From Source
If you want to have the latest changes you can instead install from source:

```
git clone https://gitlab.com/ifosim/finesse/finesse-virgo.git
cd finesse-virgo
pip install -e .
```

Periodically running `git pull` will then retrieve any changes.

## Documentation
Documentation explaining the parameters used in the model can be found at https://finesse.ifosim.org/docs/finesse-virgo/latest/ (HTML) and https://finesse.ifosim.org/docs/finesse-virgo/pdf/latest/ (PDF).

Alternatively, the documentation can be built from the source, found at https://git.ligo.org/finesse/finesse-virgo-docs/ .

## Usage
This package includes top-level tools and models for simulating Virgo in Finesse 3. Individual simulations that you perform should be stored elsewhere, such as the [`finesse_playground`](https://git.ligo.org/IFOsim/Finesse_playground/-/tree/master) repository. Your scripts should just import this package.

The Virgo pre-tuning tool can be used to create an AdV+ model and pre-tune it to an operating point.

Start by creating a Virgo model:

```python
# create a new Virgo model
virgo = finesse.virgo.Virgo()
```

This will create a Virgo model using the *current* state of the common file.

Alternatively, an existing configuration can be provided as a starting point: 

```python
# create a Virgo model using a custom input file
virgo = finesse.virgo.Virgo('custom_file.kat')
```

This will parse the necessary files into a Finesse 3 model and prepare the model for tuning. See `examples/creating_virgo.ipynb` for additional examples.

With the Virgo model created, we can then begin to step through the pre-tuning process:

```python
# step 1: adjust the cavity lengths
virgo.adjust_PRC_length()
virgo.adjust_SRC_length()

# step 2: pretune
virgo.pretune()

# step 3: optimize demodulation phases
virgo.optimize_demodulation_phase()

# step 4: optimize lock gains
virgo.optimize_lock_gains()

# step 5: run RF locks
virgo.model.run(RunLocks(method="newton"))

# step 6: switch DARM to DC lock with an offset
virgo.model.run(DARM_RF_to_DC())
```

Alternatively, the previous steps can be combined by simply using `make()`:

```python
# completes all steps at once
virgo.make()
```

See `examples/general_usage.ipynb` for additional examples.

### Printing

Various printing functions are available to display information about the current state of the model.

For example, it may be useful to display important lengths and frequencies:

```python
# display lengths and
virgo.print_lengths()
```

```
┌─────────────────────────────────────────────────┐
│- Arm lengths [m]:                               │
│  LN   = 2999.8180   LW = 2999.7880              │
├─────────────────────────────────────────────────┤
│- Michelson and recycling lengths [m]:           │
│  ln   = 6.0152      lw       = 5.7851           │
│  lpr  = 6.0513      lsr      = 6.0509           │
│  lMI  = 5.9001      lSchnupp = 0.2301           │
│  lPRC = 11.9515     lSRC     = 11.9511          │
├─────────────────────────────────────────────────┤
│- Associated cavity frequencies [Hz]:            │
│  fsrN   = 49968.44    fsrW   = 49968.94         │
│  fsrPRC = 12542050.98 fsrSRC = 12542480.59      │
│                                                 │
│- Modulation sideband frequencies [MHz]:         │
│  f6     = 6.270777     f8     = 8.361036        │
│  f56     = 56.436993                            │
├─────────────────────────────────────────────────┤
│- Check frequency match [MHz]:                   │
│  125.5*fsrN-300 = 6.270739                      │
│  0.5*fsrPRC     = 6.271025                      │
│  0.5*fsrSRC     = 6.271240                      │
│  9*f6           = 56.436993                     │
└─────────────────────────────────────────────────┘
```

Or display the carrier power at key nodes throughout the interferometer:

```python
# display carrier power at key nodes
virgo.print_powers()
```

```
┌────────────────────────────────────────┐
│ Detector         Power [W]  Pow. ratio │
├────────────────────────────────────────┤
│ CAR_AMP_PRin  :         40          1  │
│ CAR_AMP_N     :  2.482e+05       6205  │
│ CAR_AMP_W     :  2.454e+05       6134  │
│ CAR_AMP_BS    :       1748      43.69  │
│ CAR_AMP_AS    :     0.0182   0.000455  │
└────────────────────────────────────────┘
```

See `examples/printing.ipynb` for more printing examples.

### Plotting

The quantum-noise limited sensitivity curve is a good way to determine if we are at an operating point:

```
virgo.plot_QNLS()
```

Similarly, the DARM transfer function can also be plotted:

```
virgo.plot_DARM()
```

See `examples/plotting.ipynb` for additional plotting examples.

## Contributing
If you want to contribute any changes or code to this project then it must be done via a merge request. Merge requests must pass all tests before being merged.

The pipeline will fail if `pre-commit` has not been run. After cloning the git repository please run `pip install pre-commit; pre-commit install`. This will ensure that formatting and simple code errors are fixed using `black` and `flake8`.

Documentation for functions should be in the numpydoc format: https://numpydoc.readthedocs.io/en/latest/format.html

### Adding new katscript

New KatScript elements and commands must be registered with the `FINESSE` parser. This is done in the top level `__init__.py` which registers each of the objects required.

## Support
Please post an issue if you are experiencing any bugs, problems, or feature requests. `https://chat.ligo.org/ligo/channels/finesse` can also be used for broader discussion on Finesse and modelling Virgo with it.

## License
All code here is distributed under GPL v3.

## Packaging

The `finesse-virgo` is automatically uploaded to pypi when new tags are pushed to `main`. Tags must be annotated and be in the semantic versioning form `MAJOR.MINOR.PATCH`:

- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards compatible manner, and
- PATCH version when you make backwards compatible bug fixes.

Only maintainers can push tags to the main branch.
