# system modules

# internal modules
from parmesan.symbols import *

# external modules


@from_sympy()
def trace_gas_mass_density_from_particle_ratio():
    """
    https://gitlab.com/tue-umphy/co2mofetten/co2mofetten-project/-/wikis/Gas-Calculations
    """
    return X_Tgas * p / (R_s * T)


@from_sympy(
    result=X_Tgas, rearrange_from=trace_gas_mass_density_from_particle_ratio
)
def trace_gas_particle_ratio_from_mass_density():
    """
    https://gitlab.com/tue-umphy/co2mofetten/co2mofetten-project/-/wikis/Gas-Calculations
    """
    pass


__doc__ = rf"""
Equations
+++++++++

{formatted_list_of_equation_functions(locals().copy())}

API Documentation
+++++++++++++++++
"""
