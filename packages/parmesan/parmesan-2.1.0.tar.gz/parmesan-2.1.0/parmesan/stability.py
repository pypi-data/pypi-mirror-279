# system modules

# internal modules
from parmesan import units
from parmesan.utils.function import FunctionCollection
from parmesan.symbols import *

# external modules

brunt_vaisala_frequency = FunctionCollection()
"""
Collection of functions to calculate Brunt–Väisälä frequency at which a
displaced air parcel will oscillate when displaced vertically within a
statically stable environment
"""


@brunt_vaisala_frequency.register
@from_sympy()
def brunt_vaisala_frequency_from_potential_temperature():
    return sympy.sqrt(g / θ * dθdz)


@brunt_vaisala_frequency.register
@from_sympy()
def brunt_vaisala_frequency_from_density():
    return sympy.sqrt(-g / ρ * dρdz)


richardson_number = FunctionCollection()
"""
Collection of functions to calculate Richardson number
"""


@richardson_number.register
@from_sympy()
def richardson_number_canonical():
    return g / ρ * dρdz / (duhdz**2)


@richardson_number.register
@from_sympy()
def bulk_richardson_number():
    r"""
    Bulk Richardson Number (BRN) via vertical differences across a layer

    https://glossary.ametsoc.org/wiki/Bulk_richardson_number
    """
    return g / T_v * Δzθ_v * Δz / Δzu_h**2


@richardson_number.register
@from_sympy()
def gradient_richardson_number_from_vaisala():
    return N_BV**2 / duhdz**2


@richardson_number.register
@from_sympy()
def gradient_richardson_number_via_brunt_vaisala_potential_temperature():
    return (
        brunt_vaisala_frequency_from_potential_temperature.equation.rhs
    ) ** 2 / duhdz**2


@richardson_number.register
@from_sympy()
def gradient_richardson_number_via_brunt_vaisala_density():
    return (
        brunt_vaisala_frequency_from_density.equation.rhs
    ) ** 2 / duhdz**2


@richardson_number.register
@from_sympy()
def gradient_richardson_number():
    """
    https://glossary.ametsoc.org/wiki/Gradient_richardson_number
    """
    return g / T_v * dθvdz / duhdz**2


@richardson_number.register
@from_sympy()
def flux_richardson_number():
    """
    https://glossary.ametsoc.org/wiki/Flux_richardson_number
    """
    return g / T_v * cov_θv_w / (cov_uh_w * duhdz)


monin_obukov_length = FunctionCollection()
"""
Collection of functions to calculate the Monin-Obukov Length
"""


@monin_obukov_length.register
@from_sympy()
def monin_obukov_length_from_temperature_and_heat_flux():
    r"""
    https://www.licor.com/env/support/EddyPro/topics/calculate-flux-level-0.html
    """
    return -(friction_velocity**3) / (
        von_karman_constant
        * earth_acceleration
        / temperature
        * sensible_heat_flux
        / (density * c_p_dryair)
    )


@monin_obukov_length.register
@from_sympy()
def monin_obukov_length_from_virtual_potential_temperature_and_covariance():
    r"""
    Monin-Obukov Length from mean virtual potential temperature and heat flux covariance

    https://www.licor.com/env/support/EddyPro/topics/calculate-flux-level-0.html
    """
    return -(friction_velocity**3) / (
        von_karman_constant
        * earth_acceleration
        / virtual_potential_temperature
        * cov_θv_w
    )


@from_sympy(defaults={z_0: units("0 m")})
def monin_obukov_stability_parameter():
    """
    https://www.licor.com/env/support/EddyPro/topics/calculate-flux-level-0.html
    """
    return (z - z_0) / L_MO


@from_sympy(result=Φ_MO_H)
def monin_obukov_stability_function_heat_dyer_hicks():
    r"""
    Monin-Obukov Stability Function for heat (and water vapour)

    Same as :any:`monin_obukov_stability_function_water_vapour_dyer_hicks`

    From Dyer and Hicks (1970): https://doi.org/10.1002/qj.49709641012
    """
    return ((1 - 16 * ζ_MO) ** -sympy.Rational(-1, 2)).subs(
        ζ_MO, monin_obukov_stability_parameter.equation.rhs
    )


@from_sympy(result=Φ_MO_W)
def monin_obukov_stability_function_water_vapour_dyer_hicks():
    r"""
    Monin-Obukov Stability Function for water vapour (and heat)

    Same as :any:`monin_obukov_stability_function_heat_dyer_hicks`

    From Dyer and Hicks (1970): https://doi.org/10.1002/qj.49709641012
    """
    return monin_obukov_stability_function_heat_dyer_hicks.equation.rhs


@from_sympy(result=Φ_MO_M)
def monin_obukov_stability_function_momentum_dyer_hicks():
    r"""
    Monin-Obukov Stability Function for momentum

    From Dyer and Hicks (1970): https://doi.org/10.1002/qj.49709641012
    """
    return ((1 - 16 * ζ_MO) ** -sympy.Rational(-1, 4)).subs(
        ζ_MO, monin_obukov_stability_parameter.equation.rhs
    )


__doc__ = rf"""
Equations
+++++++++

{formatted_list_of_equation_functions(locals().copy())}

API Documentation
+++++++++++++++++
"""
