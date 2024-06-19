import importlib.resources

virgo_common_file = (
    importlib.resources.files("finesse_virgo.katscript")
    .joinpath("00_virgo_common_file.kat")
    .read_text()
)
additional_katscript = (
    importlib.resources.files("finesse_virgo.katscript")
    .joinpath("01_additional_katscript.kat")
    .read_text()
)

virgo_common_file_f2 = (
    importlib.resources.files("finesse_virgo.katscript.legacy")
    .joinpath("virgo_common_file_f2.kat")
    .read_text()
)

# TODO: this can be done better
files = ["00_virgo_common_file.kat", "01_additional_katscript.kat"]

__all__ = ("virgo_common_file", "additional_katscript", "virgo_common_file_f2")
