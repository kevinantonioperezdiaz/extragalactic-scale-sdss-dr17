import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
#Omega_M = Om0 = materia barionica + materia oscura
#Omega_Lambda = Ol0 = energia oscura se asume en el modelo cosmologico plano que es 1 - Om0
cosmo = FlatLambdaCDM(H0 = 71, Om0 = 0.27)

tamano_fisico = 1.0*u.Mpc #escala fisica de referencia

#redshif_cumulos
z_virgo = 0.0036
z_coma = 0.0231
z_abell85 = 0.05506

#calculos para virgo
d_comovil_virgo = cosmo.comoving_distance(z_virgo)
d_angular_virgo = d_comovil_virgo/(1+z_virgo)
theta_virgo = ((tamano_fisico/d_angular_virgo) * u.rad).to(u.arcmin)

#calculos para coma
d_comovil_coma = cosmo.comoving_distance(z_coma)    
d_angular_coma = d_comovil_coma/(1+z_coma)
theta_coma = ((tamano_fisico/d_angular_coma) * u.rad).to(u.arcmin)

#calculos para abell85
d_comovil_abell85 = cosmo.comoving_distance(z_abell85)
d_angular_abell85 = d_comovil_abell85/(1+z_abell85)
theta_abell85 = ((tamano_fisico/d_angular_abell85) * u.rad).to(u.arcmin)

print(f"virgo -> Da: {d_angular_virgo:.2f}, theta busqueda: {theta_virgo:.2f}")
print(f"coma -> Da: {d_angular_coma:.2f}, theta busqueda: {theta_coma:.2f}")
print(f"abell85 -> Da: {d_angular_abell85:.2f}, theta busqueda: {theta_abell85:.2f}")