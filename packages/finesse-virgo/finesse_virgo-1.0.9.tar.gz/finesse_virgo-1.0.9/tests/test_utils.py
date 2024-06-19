import finesse.virgo as virgo
import finesse_virgo.katscript


def test_copy_input_file(tmpdir):
    """Tests the ability to copy an input file to the user's file system."""

    filename = "virgo_f3.kat"
    dest = tmpdir / filename

    # make sure the file doesn't exist
    assert not dest.exists()

    # copy it into the tmp directory
    virgo.copy_input_file(filename, dest_dir=tmpdir)

    # make sure it is there
    assert dest.exists()

    # writing again should fail
    assert not virgo.copy_input_file(filename, dest_dir=tmpdir)

    # overwriting should work
    assert virgo.copy_input_file(filename, dest_dir=tmpdir, overwrite=True)


def test_copy_additional_input_file(tmpdir):
    """Tests the ability to choose which input file to copy."""

    # TODO: remove explicit filenames
    filename = "01_additional_katscript.kat"
    dest = tmpdir / filename

    # copy it into the tmp directory
    virgo.copy_input_file(
        filename, dest_dir=tmpdir, input_file="01_additional_katscript.kat"
    )

    # make sure it is there
    assert dest.exists()


def test_copy_input_files(tmpdir):
    """Tests the ability to copy all input files to the user's file system."""

    directory = "test"
    dest = tmpdir / directory

    # make sure the directory doesn't exist
    assert not dest.exists()

    # attempt to copy files into non-existing directory with path
    virgo.copy_input_files(dest)

    # make sure it is there
    assert dest.exists()

    # make sure the files are there
    for file in finesse_virgo.katscript.files:
        dest_file = dest / file
        assert dest_file.exists()

    # make sure overwrite is working
    # change a file
    with open(dest_file, "w") as file:
        file.write("-- test --")

    # try to copy files without overwrite
    virgo.copy_input_files(dest)

    with open(dest_file, "r") as file:
        assert file.readline() == "-- test --"

    # copy files with overwrite
    with open(dest_file, "w") as file:
        file.write("-- test --")

    # try to copy files without overwrite
    virgo.copy_input_files(dest, overwrite=True)

    with open(dest_file, "r") as file:
        assert not file.readline() == "-- test --"
