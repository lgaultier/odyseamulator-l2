# odyseamulator-l2


Simulation tools for the ODYSEA winds and currents mission. For more information about ODYSEA, see: https://odysea.ucsd.edu/


This simulator enables statistical simulation of ODYSEA-like L2 observations of the surface currents. Its purpose is to generate efficiently realistic observations for science studies. The statistical noise is generated using look up tables provided by the development team

## ODYSEA
ODYSEA (Ocean DYnamics and Surface Exchange with the Atmosphere):  A revolutionary look at winds and surface currents

The ODYSEA satellite will bring into focus daily global surface currents and their interactions with winds to explore the Earth system and to improve weather and climate predictions.

## Installation

Installation is completed via pip. Clone this repository and navigate to odyseamulator-l2 before issuing:

>pip install .

## Run simulator

>odyseamul [parameter-file] --first\_cycle [integer] --last\_cycle [integer]

The parameter-file contains Information regarding the satellite configuration
(orbits, instrumental noise) and the OGCM model that will be used as an input.




## Dependencies

>xarray,
netCDF4,
scipy,
numpy,
pandas,
pyyaml,
cartopy (for plotting only)
tqdm





