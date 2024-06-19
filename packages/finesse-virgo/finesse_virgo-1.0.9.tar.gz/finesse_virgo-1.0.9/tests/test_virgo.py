import pytest

import finesse
import finesse.virgo
import finesse_virgo
import finesse_virgo.katscript


def test_common_virgo_file():
    model = finesse.Model()
    model.parse(finesse_virgo.katscript.virgo_common_file)
    model.unparse()


def test_make_virgo():
    model = finesse_virgo.make_virgo()
    model.unparse()


def test_virgo_class():
    # this returns a Virgo object with a configured model
    model = finesse_virgo.make_virgo(
        display_plots=False,
        thermal_state="design-matched",
        use_3f_error_signals=False,
        with_apertures=False,
        verbose=False,
        x_scale=1,
        zero_k00=False,
    )
    model.unparse()


def test_custom_katscript_directory(tmpdir):
    dest_dir = tmpdir / "custom_katscript"
    finesse_virgo.utils.copy_input_files(str(dest_dir))

    assert finesse_virgo.virgo.Virgo(str(dest_dir))

def test_custom_katscript_list(tmpdir):
    dest_dir = tmpdir / "custom_katscript"
    finesse_virgo.utils.copy_input_files(str(dest_dir))

    assert finesse_virgo.virgo.Virgo([
        str(dest_dir / "00_virgo_common_file.kat"),
        str(dest_dir / "01_additional_katscript.kat"),
    ])

def test_parse_additional_katscript(tmpdir):
    
    # copy the common file
    filename = "00_virgo_common_file.kat"
    finesse_virgo.copy_input_file(
        "00_virgo_common_file.kat",
        dest_dir=tmpdir,
        input_file=filename
    )

    # parse common file with additional katscript flag
    virgo = finesse.virgo.Virgo(
        tmpdir / filename,
        parse_additional_katscript=True
    )

    # should only make if the additional katscript exists
    virgo.make()

@pytest.mark.parametrize("thermal_state", ("design-matched", "cold"))
@pytest.mark.parametrize("use_3f_error_signals", (True, False))
@pytest.mark.parametrize("with_apertures", (True, False))
def test_make_virgo_parametrized(thermal_state, use_3f_error_signals, with_apertures):
    model = finesse.virgo.make_virgo(
        thermal_state=thermal_state,
        use_3f_error_signals=use_3f_error_signals,
        with_apertures=with_apertures,
    )
    model.unparse()
