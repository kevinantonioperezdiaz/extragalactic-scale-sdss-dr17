import os
import matplotlib.pyplot as plt
import pandas as pd

# 1. Carpeta para guardar las figuras
os.makedirs("figuras", exist_ok=True)

# 2. Catálogos y configuración visual
catalogos = {
    'virgo':   {'color': '#1f77b4', 'titulo': 'Cúmulo de Virgo', 'limite_x': 25},
    'coma':    {'color': '#ff7f0e', 'titulo': 'Cúmulo de Coma', 'limite_x': 35},
    'abell85': {'color': '#2ca02c', 'titulo': 'Cúmulo Abell 85', 'limite_x': 40},
    'campo':   {'color': '#d62728', 'titulo': 'Galaxias de Campo (z > 0.1)', 'limite_x': 80}
}

# 3. Generación y guardado de cada figura
for nombre, config in catalogos.items():
    ruta_csv = os.path.join("data", f"{nombre}.csv")
    df = pd.read_csv(ruta_csv)
    
    diametros = df['diametro_kpc'].dropna()
    mediana = diametros.median()
    desviacion_estandar = diametros.std()
    total_galaxias = len(diametros)
    
    plt.figure(figsize=(8, 5))
    
    # Histograma base
    plt.hist(
        diametros, 
        bins=25, 
        range=(0, config['limite_x']), 
        color=config['color'], 
        edgecolor='black', 
        alpha=0.75,
        label=f'Galaxias totales = {total_galaxias}'
    )
    
    # Línea vertical para la Mediana
    plt.axvline(
        mediana, 
        color='black', 
        linestyle='--', 
        linewidth=2, 
        label=f'Mediana = {mediana:.2f} kpc'
    )
    
    # Banda sombreada para el rango de 1 Desviación Estándar (Mediana ± Desv. Estándar)
    limite_inferior_sigma = max(0, mediana - desviacion_estandar)
    limite_superior_sigma = mediana + desviacion_estandar
    
    plt.axvspan(
        limite_inferior_sigma, 
        limite_superior_sigma, 
        color='gray', 
        alpha=0.25, 
        label=f'desviacion estandar ±1σ ({desviacion_estandar:.2f} kpc)'
    )
    
    # Títulos y ejes
    plt.title(f"Distribución de Tamaños Físicos - {config['titulo']}", fontsize=13, fontweight='bold')
    plt.xlabel("Diámetro físico [kpc]", fontsize=11)
    plt.ylabel("Número de galaxias", fontsize=11)
    plt.xlim(0, config['limite_x'])
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    
    # Leyenda consolidada
    plt.legend(fontsize=10, loc='upper right', framealpha=0.9)
    
    # Guardado
    ruta_figura = os.path.join("figuras", f"histograma_{nombre}.png")
    plt.tight_layout()
    plt.savefig(ruta_figura, dpi=300)
    plt.close()
    
    print(f"Figura generada con éxito: {ruta_figura}")