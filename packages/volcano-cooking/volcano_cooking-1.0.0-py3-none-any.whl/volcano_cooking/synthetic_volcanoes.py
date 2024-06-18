"""Create synthetic volcanic eruptions.

This script creates a .nc file consisting of volcanic eruptions and the
corresponding time of arrival down to the nearest day and the magnitude of the
eruption.

The lat/lon location is also included, but considered unimportant and thus the
same location is used for all volcanoes.
"""

from typing import Optional

from volcano_cooking.modules import create

# ====================================================================================== #
# Need:
#
# Dimension(s):
## Eruption number (do not contain variable attributes)
#
# Variable(s):
## Eruption (dim: Eruption_Number)
## -  Volcano number (not important, used to classify real volcanoes)
## -  Volcano name (not important)
## -  Notes and references (not important)
## VEI (dim: Eruption_Number)
## Year_of_Emission (dim: Eruption_Number)
## Month_of_Emission (dim: Eruption_Number)
## Day_of_Emission (dim: Eruption_Number)
## Latitude (dim: Eruption_Number)
## Longitude (dim: Eruption_Number)
## Total_Emission (dim: Eruption_Number)
## Maximum_Injection_Height (dim: Eruption_Number)
## Minimum_Injection_Height (dim: Eruption_Number)
# ====================================================================================== #


__GENERATORS__: dict[int, type[create.Generate]] = {
    0: create.GenerateRandomNormal,
    1: create.GenerateFPP,
    2: create.GenerateSingleVolcano,
    3: create.GenerateRegularIntervals,
    4: create.GenerateFromFile,
}


def create_volcanoes(
    size: int = 251,
    init_year: int = 1850,
    version: int = 0,
    option: int = 0,
    file: Optional[str] = None,
) -> None:
    """Create volcanoes starting at the year 1850.

    This will re-create the same data as can be found in forcing files used within the
    CESM2 general circulation model.

    Parameters
    ----------
    size : int
        The total number of eruptions
    init_year : int
        First year in the climate model
    version : int
        Choose one of the versions from the '__GENERATORS__' dictionary
    option : int
        Choose which option to use when generating forcing
    file : Optional[str]
        Read eruption dates and emissions from file.

    Raises
    ------
    IndexError
        If `version` is not a valid index of the generator dictionary.
    """
    # CREATE DATA -------------------------------------------------------------------- #

    if version not in __GENERATORS__ or version < 0:
        raise IndexError(
            f"No version exists for index {version}. "
            + "It must be one of {__GENERATORS__.keys()}."
        )
    if file is not None:
        print(f"Generating with '{__GENERATORS__[4].__name__}'...")
        print(
            "WARNING: When generating with this option, eruptions are not shifted to "
            "have one eruption prior to the first simulation year. Add an extra "
            "eruption at an early (and late) time that you know will cover the whole "
            "simulation you are planning."
        )
        g = __GENERATORS__[4](size, init_year, file)
    else:
        print(f"Generating with '{__GENERATORS__[version].__name__}'...")
        g = __GENERATORS__[version](size, init_year)
    g.generate()
    all_arrs = g.get_arrays()

    # CREATE NETCDF FILE AND SAVE ---------------------------------------------------- #

    frc_cls = create.ReWrite(*all_arrs) if option == 1 else create.Data(*all_arrs)
    frc_cls.make_dataset()
    frc_cls.save_to_file()


def main():
    """Run the main function."""
    create_volcanoes(size=300, init_year=1)


if __name__ == "__main__":
    main()
