import io
import requests
import pandas as pd
import os

# Diccionario con los parámetros de cada cúmulo
cumulos = {
    'virgo':   {'ra': 187.7059, 'dec':  12.3911, 'r_arcmin': 100.0, 'z_cen': 0.00360, 'tipo': 'cumulo'},
    'coma':    {'ra': 194.8988, 'dec':  27.9597, 'r_arcmin':  36.23, 'z_cen': 0.02310, 'tipo': 'cumulo'},
    'abell85': {'ra':  10.4600, 'dec':  -9.3031, 'r_arcmin':  15.78, 'z_cen': 0.05506, 'tipo': 'cumulo'},
    'campo':   {'ra': 194.8988, 'dec':  27.9597, 'r_arcmin':  60.00, 'z_cen': None,    'tipo': 'campo'}
}
def consultar_sdss(sql):
    url = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"
    respuesta = requests.get(url, params={'cmd': sql, 'format': 'csv'})
    respuesta.raise_for_status()
    
    lineas = [l for l in respuesta.text.splitlines() if l.strip() and not l.startswith("#")]
    csv_limpio = "\n".join(lineas)
    return pd.read_csv(io.StringIO(csv_limpio))

# Creamos la carpeta donde se guardarán los archivos
os.makedirs("data", exist_ok=True)

# Recorremos el diccionario para consultar y guardar cada catálogo
for nombre, datos in cumulos.items():
    print(f"Descargando datos para: {nombre}...")

    if datos['tipo'] == 'cumulo':
        filtro_z = f"and abs(300000 * ({datos['z_cen']} - q.z)) < 2000"
        top = ""
    else:
        filtro_z = "and q.z > 0.1"
        top = "top 200"

    sql = f"""
    select {top} p.ra, p.dec, p.deVRad_r, q.z
    from galaxy p, dbo.fgetNearByObjEq({datos['ra']}, {datos['dec']}, {datos['r_arcmin']}) n, galSpecInfo q
    where p.objid = n.objid
      and p.specObjID = q.specObjID
      and p.specObjID <> 0
      and q.z > 0
      {filtro_z}
    """

    # Consultamos SDSS y guardamos en CSV
    df = consultar_sdss(sql)
    ruta_guardado = os.path.join("data", f"{nombre}.csv")
    df.to_csv(ruta_guardado, index=False)
    print(f" -> Guardado exitoso: {ruta_guardado} ({len(df)} galaxias)")