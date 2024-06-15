import numpy as np


def convert_units(
    x,
    y,
    x_energy_in_eV,
    y_inverse_energy_in_eV,
    y_inverse_area_in_m2,
    y_inverse_time_in_s,
    y_scale_energy_in_eV,
    y_scale_energy_power,
    target_x_energy_in_eV,
    target_y_inverse_energy_in_eV,
    target_y_inverse_area_in_m2,
    target_y_inverse_time_in_s,
    target_y_scale_energy_in_eV,
    target_y_scale_energy_power,
):
    """
    Convert the units, and the power-law-scale of your input-SED to the units
    and power-law-scale of your target-SED.
    You have to express the units of both input-SED, and target-SED in
    SI-units (energy/eV, area/m^2, time/s).

    Parameters
    ----------
    x                   The support-positions on the x-axis, i.e. energy-axis.
                        Energy in units of your input-SED.

    y                   The values on the y-axis, i.e. differential-flux times
                        some power-law-scaling of the energy-axis.
                        Energy in units of your input-SED.
    """
    assert len(x) == len(y)
    x = np.array(x)
    y = np.array(y)

    # unscale power law from input y
    _x_in_units_of_y_scale_energy = x * (x_energy_in_eV / y_scale_energy_in_eV)
    _y = y / (_x_in_units_of_y_scale_energy**y_scale_energy_power)

    # convert energy axis to SI base units
    x_eV = x * x_energy_in_eV

    # convert differential flux axis to SI base units
    y_per_m2_per_s_per_eV = _y / (
        y_inverse_energy_in_eV * y_inverse_area_in_m2 * y_inverse_time_in_s
    )

    # convert energy axis to target units
    x_target = x_eV / target_x_energy_in_eV

    # convert diff. flux axis to target units
    _y_target = y_per_m2_per_s_per_eV * (
        target_y_inverse_energy_in_eV
        * target_y_inverse_area_in_m2
        * target_y_inverse_time_in_s
    )

    _x_in_units_of_target_y_scale_energy = x_eV / target_y_scale_energy_in_eV

    y_target = _y_target * (
        _x_in_units_of_target_y_scale_energy**target_y_scale_energy_power
    )

    return x_target, y_target


def convert_units_with_style(
    x,
    y,
    input_style,
    target_style,
):
    inp = input_style
    tgt = target_style
    return convert_units(
        x=x,
        y=y,
        x_energy_in_eV=inp["x_energy_in_eV"],
        y_inverse_energy_in_eV=inp["y_inverse_energy_in_eV"],
        y_inverse_area_in_m2=inp["y_inverse_area_in_m2"],
        y_inverse_time_in_s=inp["y_inverse_time_in_s"],
        y_scale_energy_in_eV=inp["y_scale_energy_in_eV"],
        y_scale_energy_power=inp["y_scale_energy_power"],
        target_x_energy_in_eV=tgt["x_energy_in_eV"],
        target_y_inverse_energy_in_eV=tgt["y_inverse_energy_in_eV"],
        target_y_inverse_area_in_m2=tgt["y_inverse_area_in_m2"],
        target_y_inverse_time_in_s=tgt["y_inverse_time_in_s"],
        target_y_scale_energy_in_eV=tgt["y_scale_energy_in_eV"],
        target_y_scale_energy_power=tgt["y_scale_energy_power"],
    )


convert_units_with_style.__doc__ = convert_units.__doc__
convert_units_with_style.__doc__ += (
    "\n"
    "    input_style         Dictionary\n"
    "\n"
    "    target_style        Dictionary\n"
    "\n"
    "    Example style\n"
    "    -------------\n"
    "    science_magazine_sed_style = {\n"
    "        'x_energy_in_eV': 1e6,\n"
    "        'y_inverse_energy_in_eV': 1e6,\n"
    "        'y_inverse_area_in_m2': 1e-4,\n"
    "        'y_inverse_time_in_s': 1.0,\n"
    "        'y_scale_energy_in_eV': 1e6,\n"
    "        'y_scale_energy_power': 2.0,\n"
    "    }\n"
    "\n"
)
