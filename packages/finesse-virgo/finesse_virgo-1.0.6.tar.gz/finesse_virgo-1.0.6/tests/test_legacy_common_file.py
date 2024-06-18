import finesse
import finesse_virgo.katscript


def test_legacy_common_file():
    """Test to make sure the legacy Finesse 2 common file will parse."""

    kat = finesse.Model()
    kat.parse_legacy(finesse_virgo.katscript.virgo_common_file_f2)
