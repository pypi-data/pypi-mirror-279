import shutil
import pathlib as pl
import os
import numpy as np
import math

import finesse_virgo.katscript


def copy_input_file(
    filename="virgo_f3.kat",
    overwrite=False,
    dest_dir=None,
    input_file="00_virgo_common_file.kat",
):
    """Utility function to copy the common file to the current working directory.

    Parameters
    ----------
    filename : Str (optional)
        Destination filename. Defaults to 'virgo_f3.kat'.

    overwrite : bool (optional)
        Flag required to be true if the file already exists.

    dest_dir : Str (optional)
        Directory into which to save the file.
        TODO: could be provided with filename by adding additional logic
    """

    src = pl.Path(__file__).parent.resolve() / "katscript" / input_file

    if dest_dir is None:
        dest_dir = pl.Path().resolve()

    dest = dest_dir / filename

    # only copy if the file doesn't exist or with explicit permission
    if not dest.exists() or (dest.exists() and overwrite):
        shutil.copy(src, dest)
        print(f"Input file `{input_file}` saved to `{dest}`.")

        return True
    else:
        print(f"File `{dest}` already exists.")
        print("Overwrite with `copy_virgo_file(overwrite=True)`.")

        return False


def copy_input_files(directory="katscript", overwrite=False):
    """Utility function to export the common file and additional katscript to a
    specified directory. This directory can then be provided to the Virgo class as the
    katscript source.

    Parameters
    ----------
    directory : Str (optional)
        Destination directory.

    overwrite : bool (optional)
        Flag required to be true if the directory and files already exists.
    """

    dest_dir = pl.Path().resolve() / directory

    # check if the directory already exists
    if dest_dir.exists():
        print(f"Destination directory found: {dest_dir}")
    else:
        print(f"Creating destination directory: {dest_dir}")
        os.mkdir(directory)

    # copy the files
    for file in finesse_virgo.katscript.files:
        print(f"Copying input file: {file}")
        copy_input_file(file, dest_dir=dest_dir, input_file=file, overwrite=overwrite)


def RGA(sm):
    # compute relative gain array of a sensing matrix (sm)
    G = np.asmatrix(sm).astype("float")
    G = np.asarray(G)
    Ginv = np.linalg.inv(G)
    rga = np.multiply(G, Ginv.T)

    return rga


def NI(rga):
    # cpmpute the Niederlinski Index of a relative gain array (rga)
    ni = np.linalg.det(rga) / np.prod(np.diag(rga))
    return ni


from finesse.utilities.tables import NumberTable


def print_table(data, cols, rows, numfmt="{:.4G}"):
    from IPython.display import display

    # convenience function to print a table with row and colum names
    display(
        NumberTable(data, colnames=cols, rownames=rows, numfmt=numfmt, colfunc=None)
    )


def round_to_n(x, n):
    if not x:
        return 0
    power = -int(math.floor(math.log10(abs(x)))) + (n - 1)
    factor = 10**power
    return round(x * factor) / factor
