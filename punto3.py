import os
import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

# 1. Definimos la cosmología base de la guía
cosmo = FlatLambdaCDM(H0=71, Om0=0.27)

# 2. Función que toma un DataFrame y le calcula el diámetro físico vectorizado
def calcular_diametro(df):
    z_vals = df['z'].values
    distancia_comovil = cosmo.comoving_distance(z_vals)
    distancia_angular = distancia_comovil / (1.0 + z_vals)
    theta_rad = (2.0 * df['deVRad_r'].values * u.arcsec).to(u.rad)
    df['diametro_kpc'] = (distancia_angular * theta_rad.value).to(u.kpc).value
    return df

# 3. Lista con los nombres de los 4 catálogos guardados en data/
nombres = ['virgo', 'coma', 'abell85', 'campo']
resultados = {}

# 4. Procesamos cada archivo
for nombre in nombres:
    ruta = os.path.join("data", f"{nombre}.csv")
    df = pd.read_csv(ruta)
    
    # Aplicamos el cálculo
    df = calcular_diametro(df)
    
    # Sobreescribimos el CSV para que ya conserve la columna calculada
    df.to_csv(ruta, index=False)
    resultados[nombre] = df
    
    # Estadísticos: Mediana y Desviación Estándar
    mediana = df['diametro_kpc'].median()
    std = df['diametro_kpc'].std()
    print(f"{nombre.upper():<8} -> N: {len(df):<3} | Mediana: {mediana:6.2f} kpc | Std: {std:6.2f} kpc")