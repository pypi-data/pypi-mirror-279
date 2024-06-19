from .virgo import make_virgo, Virgo
from .utils import copy_input_file, copy_input_files

__all__ = (
    "Virgo",
    "make_virgo",
    "copy_input_file",
    "copy_input_files",
)

from packaging import version
from finesse import __version__ as finesse_version

if "+" in finesse_version:
    finesse_version = finesse_version.split("+")[0]

min_finesse_version = "3.0a23.dev17"  # update in setup.cfg

if version.parse(finesse_version) < version.parse(min_finesse_version):
    raise Exception(
        f"You need at least Finesse {min_finesse_version} or higher to run this version of finesse-virgo, you have {finesse_version}"
    )
