# import pytest

# import finesse
# import finesse_virgo


def test_virgo_with_custom_katfile():
    """The Virgo class is designed to use the common file by default, but users may want
    to use their own version of the common file or pick up from an already tuned model.

    Assuming a custom version of the common file (with minor changes), the user can simply pass in the location of their katscript and assuming key components have the same name everything will function as expected.

    Since the class executes additional katscript on instantiation (vars, dofs, controls, etc.), problems can arise when there is overlap between the custom katscript and the additional katscript. To get around this, the Virgo object can be set to initialize using only the custom katscript.
    """

    # # normal instantiation
    # virgo = finesse_virgo.Virgo()

    # # simple custom instantiation
    # virgo = finesse_virgo.Virgo('custom_katscript.kat')

    # # advanced custom instantiation
    # virgo = finesse_virgo.Virgo('custom_katscript.kat', custom_katscript_only=True)

    # # alternative custom instantiation
    # virgo = finesse_virgo.Virgo('custom_katscripts')
    pass
