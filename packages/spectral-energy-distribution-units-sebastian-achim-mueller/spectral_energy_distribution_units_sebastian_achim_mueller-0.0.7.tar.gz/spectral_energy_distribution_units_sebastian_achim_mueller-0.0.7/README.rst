###############################################
Converting Spectral-Energy-Distributions (SEDs)
###############################################
|TestStatus| |PyPiStatus| |BlackStyle| |BlackPackStyle| |MITLicenseBadge|


In Astronomy, SEDs can have different styles.
The style effects the units and sometimes multiplies the ``y`` -axis with a power-law depending on the ``x`` -axis.
But to compare findings we have to transform to a single style. This function helps you to transform between sed-styles.
Here are example sed-styles ``A`` , ``B`` , ``C`` , and ``D`` showing the differential flux of Crab, and the integral sensitivity of Fermi-LAT.


+----------------+--------------+
| A              | B            |
+================+==============+
| |ImgSedFermi|  |  |ImgSedMy|  |
+----------------+--------------+


.. code-block:: python

    A = {
        "x_energy_in_eV": 1e6,
        "y_inverse_energy_in_eV": 624150907446.0763,  # one erg
        "y_inverse_area_in_m2": 1e-4,
        "y_inverse_time_in_s": 1.0,
        "y_scale_energy_in_eV": 624150907446.0763,  # one erg
        "y_scale_energy_power": 2.0,
    }

    B = {
        "x_energy_in_eV": 1e9,
        "y_inverse_energy_in_eV": 1e9,
        "y_inverse_area_in_m2": 1.0,
        "y_inverse_time_in_s": 1.0,
        "y_scale_energy_in_eV": 1e9,
        "y_scale_energy_power": 0.0,
    }


+----------------+--------------+
| C              | D            |
+================+==============+
| |ImgSedCosmic| | |ImgSedCrab| |
+----------------+--------------+

.. code-block:: python

    C = {
        "x_energy_in_eV": 1,
        "y_inverse_energy_in_eV": 1,
        "y_inverse_area_in_m2": 1,
        "y_inverse_time_in_s": 1.0,
        "y_scale_energy_in_eV": 1,
        "y_scale_energy_power": 2.7,
    }

    D = {
        "x_energy_in_eV": 1e9,
        "y_inverse_energy_in_eV": 1e12,
        "y_inverse_area_in_m2": 1e-4,
        "y_inverse_time_in_s": 1.0,
        "y_scale_energy_in_eV": 1e12,
        "y_scale_energy_power": 2.0,
    }


********
Function
********
Transform the numeric values in the arrays ``x`` -axis, and ``y`` -axis from style ``A`` to ``B``.

.. code-block:: python

    import spectral_energy_distribution_units as sed
    x_B, y_B = sed.convert_units_with_style(x=x_A, y=y_A, input_style=A, target_style=B)


Find also a function for the style-dictionaries ``A`` and ``B`` being unpacked:

.. code-block:: python

    x_B, y_B = sed.convert_units(x=x_A, y=y_A, x_energy_in_eV=... )


*******
Install
*******

.. code-block::

    pip install spectral-energy-distribution-units-sebastian-achim-mueller


*******
Example
*******

See unit-tests
``./spectral_energy_distribution_units/tests/test_convert.py``
to reproduce the upper figures ``A`` , ``B`` , ``C`` , and ``D``.


.. |TestStatus| image:: https://github.com/cherenkov-plenoscope/spectral_energy_distribution_units/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/cherenkov-plenoscope/spectral_energy_distribution_units/actions/workflows/test.yml

.. |PyPiStatus| image:: https://img.shields.io/pypi/v/spectral_energy_distribution_units_sebastian-achim-mueller
    :target: https://pypi.org/project/spectral_energy_distribution_units_sebastian-achim-mueller

.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |BlackPackStyle| image:: https://img.shields.io/badge/pack%20style-black-000000.svg
    :target: https://github.com/cherenkov-plenoscope/black_pack

.. |ImgSedFermi| image:: https://github.com/cherenkov-plenoscope/spectral_energy_distribution_units/blob/main/readme/sed_fermi_style.jpg?raw=True

.. |ImgSedMy| image:: https://github.com/cherenkov-plenoscope/spectral_energy_distribution_units/blob/main/readme/sed_my_style.jpg?raw=True

.. |ImgSedCosmic| image:: https://github.com/cherenkov-plenoscope/spectral_energy_distribution_units/blob/main/readme/sed_cosmic_ray_style.jpg?raw=True

.. |ImgSedCrab| image:: https://github.com/cherenkov-plenoscope/spectral_energy_distribution_units/blob/main/readme/sed_crab_style.jpg?raw=True

.. |MITLicenseBadge| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
