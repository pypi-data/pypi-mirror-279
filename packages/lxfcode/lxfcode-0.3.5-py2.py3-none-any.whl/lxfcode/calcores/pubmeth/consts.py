"""
Scientific constants
"""

from numpy import pi

E_CGS = 4.80320427e-10  # statC = 1 erg^1/2 * cm^1/2
ERG2J = 1e-7  # J
ERG2EV = 6.2415e11  # eV


##  length
cm2m = 1e-2
m2cm = 1e2
m2A = 1e10
m2nm = 1e9
cm2A = cm2m * m2A

c_eV = 1.60217662e-19  # unit: C. quantity of elementary charge
J2EV = 1 / c_eV  #   unit: eV.
h_bar_J = 1.0545718e-34  # unit: J*s
h_planck_J = h_bar_J * 2 * pi  # unit: J*s
h_bar_eV = h_bar_J / c_eV

A2m = 1 / m2A
eV2meV = 1e3
c_speed = 3e8  # m/s
epsilon_0_eV = 1.4185972833444868e-30  # C^2/(eV * m)
epsilon_0_J = epsilon_0_eV / c_eV  # C^2/(J * m)
sigma_xx_mono = c_eV**2 / h_bar_eV / 4
dyn = 1  # g*cm/s^2
amu = 1.660539040e-27  # atomic mass unit
alpha_fsc = c_eV**2 / (
    4 * pi * epsilon_0_eV * h_bar_eV * c_speed
)  #   fine structure constant
eps0_x_c = c_eV**2 / (4 * h_bar_J) / (pi * alpha_fsc)  #   unit: C^2 / (J * s)
RYDBERG = 13.605  # eV
BOHR_R = 0.0529  # nm
mass_e_kg = 9.1093837e-31  #   kg
