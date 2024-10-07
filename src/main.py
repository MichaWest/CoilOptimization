# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 13:56:41 2021

@author: Pavel
"""
from DEAP_Field_refactored import Genetic
import numpy as np
from src import Plot, Resistance
import tomli
from src.turns_splitter import split
import macros

with open('parameters.toml', 'rb') as toml:
    parameters = tomli.load(toml)

GA = Genetic(parameters)
GA.preparation()

flat_radii_array = GA.execution()
radii_array = split(flat_radii_array, GA.freq)
Magnetic_field = GA.determine_Bz(GA.hall_of_fame[0])
final_COV = GA.determine_COV(Magnetic_field)

if GA.figure == 'Circular':
    length = Resistance.length_circular_coils(coils=radii_array)
    coil_pic = Plot.plot_coil(a_max=GA.a_max, spacing=GA.spacing, R=flat_radii_array)
    field_pic_3d = Plot.plot_3d(Bz=Magnetic_field,
                                height=GA.height, a_max=GA.a_max,
                                spacing=GA.spacing, cp=GA.cp)
    macros = macros.create_circular_macros(radii_array)
elif GA.figure == 'Rectangle':
    length = Resistance.length_square_coils(coils=radii_array)
    coil_pic = Plot.plot_square_coil(m_max=GA.X_side, n_max=GA.Y_side, spacing=GA.spacing, R=flat_radii_array)
    field_pic_3d = Plot.plot_3d(Bz=Magnetic_field,
                                height=GA.height, a_max=max(GA.X_side, GA.Y_side),
                                spacing=GA.spacing, cp=GA.cp)
    macros = macros.create_rectangular_macros(radii_array)
elif GA.figure == 'Piecewise':
    l = []
    for i in range(len(GA.coords)):
        l.append(np.sqrt((GA.coords[i][0]) ** 2 + (GA.coords[i][1]) ** 2))
    calc_radius = max(l) * GA.spacing

    length = Resistance.length_piecewise_linear_coils(coils=radii_array)
    coil_pic = Plot.plot_piecewise_linear_coil(coords_max=GA.coords, spacing=GA.spacing, R=flat_radii_array)
    field_pic_3d = Plot.plot_3d(Bz=Magnetic_field,
                                height=GA.height, a_max=calc_radius,
                                spacing=GA.spacing, cp=GA.cp)

resistance = Resistance.resistance_contour(l=length, material=GA.material, d=GA.minimal_gap, nu=GA.freq)

print(radii_array)

