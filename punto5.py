import os
import matplotlib.pyplot as plt
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

# 1. Rango amplio de H0: desde 20 hasta 120 km/s/Mpc
valores_constante_hubble = [20.0, 30.0, 40.0, 50.0, 60.0, 71.0, 80.0, 90.0, 100.0, 110.0, 120.0]
densidad_materia = 0.27

nombres_catalogos = ['virgo', 'coma', 'abell85', 'campo']
etiquetas = {
    'virgo': 'Cúmulo de Virgo',
    'coma': 'Cúmulo de Coma',
    'abell85': 'Cúmulo Abell 85',
    'campo': 'Galaxias de Campo'
}

# 2. Cargamos los datos limpios guardados en data/
datos_originales = {}
for nombre in nombres_catalogos:
    ruta_archivo = os.path.join("data", f"{nombre}.csv")
    datos_originales[nombre] = pd.read_csv(ruta_archivo)

# 3. Calculamos la mediana del diámetro para cada H0
tabla_resumen_hubble = []

for constante_hubble in valores_constante_hubble:
    cosmologia_prueba = FlatLambdaCDM(H0=constante_hubble, Om0=densidad_materia)
    fila_resultado = {'H0': constante_hubble}
    
    for nombre in nombres_catalogos:
        dataframe = datos_originales[nombre]
        redshifts = dataframe['z'].values
        
        distancia_comovil = cosmologia_prueba.comoving_distance(redshifts)
        distancia_angular = distancia_comovil / (1.0 + redshifts)
        diametro_angular_radianes = (2.0 * dataframe['deVRad_r'].values * u.arcsec).to(u.rad)
        
        diametros_fisicos_kpc = (distancia_angular * diametro_angular_radianes.value).to(u.kpc).value
        fila_resultado[f"mediana_{nombre}_kpc"] = pd.Series(diametros_fisicos_kpc).median()
        
    tabla_resumen_hubble.append(fila_resultado)

df_hubble = pd.DataFrame(tabla_resumen_hubble)

print("=" * 80)
print("EVOLUCIÓN DE LA MEDIANA DE DIÁMETROS FÍSICOS SEGÚN H0 (20 a 120 km/s/Mpc)")
print("=" * 80)
print(df_hubble.to_string(index=False))

# 4. Gráfica comparativa con las líneas de referencia del Grupo Local
plt.figure(figsize=(10, 6.5))

colores = {'virgo': '#1f77b4', 'coma': '#ff7f0e', 'abell85': '#2ca02c', 'campo': '#d62728'}

for nombre in nombres_catalogos:
    plt.plot(
        df_hubble['H0'], 
        df_hubble[f"mediana_{nombre}_kpc"], 
        marker='o', 
        linewidth=2, 
        color=colores[nombre], 
        label=etiquetas[nombre]
    )

# Líneas horizontales de referencia de galaxias locales (Tabla de la guía)
plt.axhline(40, color='purple', linestyle='--', alpha=0.7, label='M31 Andrómeda (40 kpc)')
plt.axhline(30, color='blue', linestyle='--', alpha=0.7, label='Vía Láctea (30 kpc)')
plt.axhline(15, color='teal', linestyle='--', alpha=0.7, label='M33 (15 kpc)')
plt.axhline(5, color='gray', linestyle=':', alpha=0.7, label='Pequeña Nube Magallanes (5 kpc)')

plt.title("Dependencia del Diámetro Físico con la Constante de Hubble ($H_0$)", fontsize=13, fontweight='bold')
plt.xlabel("Constante de Hubble $H_0$ [km s$^{-1}$ Mpc$^{-1}$]", fontsize=11)
plt.ylabel("Mediana del Diámetro físico [kpc]", fontsize=11)
plt.xlim(18, 122)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=9, loc='upper right', framealpha=0.9)

os.makedirs("figuras", exist_ok=True)
ruta_grafica_hubble = os.path.join("figuras", "dependencia_h0.png")
plt.tight_layout()
plt.savefig(ruta_grafica_hubble, dpi=300)
plt.close()

print(f"\nGráfica guardada exitosamente en: {ruta_grafica_hubble}")