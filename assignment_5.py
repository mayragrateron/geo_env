import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os


# Cargar datos y procesar temperatura de brillo
dset = xr.open_dataset(r'C:\Users\mayra\geo_env\assignment_5\GRIDSAT-B1.2009.11.25.06.v02r01.nc')
IR = np.array(dset.variables['irwin_cdr']).squeeze()
IR = np.flipud(IR)  # Corregir orientación
IR = IR * 0.01 + 200  # Convertir a Kelvin
IR = IR - 273.15  # Convertir a Celsius

# Graficar temperatura de brillo
plt.figure(figsize=(8, 6))
plt.imshow(IR, extent=[-180.035, 180.035, -70.035, 70.035], aspect='auto')
cbar = plt.colorbar()
cbar.set_label('Brightness temperature (°C)')
plt.scatter(39.2, 21.5, color='red', marker='o', label='Jeddah')
plt.legend()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()


# Obtener temperatura mínima en Jeddah
def get_min_temp(dset):
    lat_idx = np.abs(dset['lat'] - 21.5).argmin()
    lon_idx = np.abs(dset['lon'] - 39.2).argmin()
    temp = dset['irwin_cdr'][:, lat_idx, lon_idx] * 0.01 + 200 - 273.15
    return temp.min().values

# Calcular precipitación acumulada
folder_path = r'C:\Users\mayra\geo_env\assignment_5'
files = [
    r'C:\Users\mayra\geo_env\assignment_5\GRIDSAT-B1.2009.11.25.00.v02r01.nc',
    r'C:\Users\mayra\geo_env\assignment_5\GRIDSAT-B1.2009.11.25.03.v02r01.nc',
    r'C:\Users\mayra\geo_env\assignment_5\GRIDSAT-B1.2009.11.25.06.v02r01.nc',
    r'C:\Users\mayra\geo_env\assignment_5\GRIDSAT-B1.2009.11.25.09.v02r01.nc',
    r'C:\Users\mayra\geo_env\assignment_5\GRIDSAT-B1.2009.11.25.12.v02r01.nc'
]

cumulate = None
for file in files:
    dset = xr.open_dataset(file)
    jeddah_ir = dset['irwin_cdr'].sel(lat=slice(18, 28), lon=slice(35, 45)).squeeze()
    jeddah_ir = np.flipud(jeddah_ir)
    jeddah_ir = jeddah_ir * 0.01 + 200
    temp = -3.6382 * 0.01 * xr.apply_ufunc(np.power, jeddah_ir, 1.2)
    rainfall = 3 * (1.1183 * 10**11 * xr.apply_ufunc(np.exp, temp))
    print(f'The maximum rainfall in {file} is {rainfall.max()} mm')
    cumulate = rainfall if cumulate is None else cumulate + rainfall

# Graficar precipitación acumulada
plt.figure(figsize=(8, 6))
plt.imshow(cumulate, extent=[35, 45, 18, 28], aspect='equal')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
cbar = plt.colorbar()
cbar.set_label('Cumulative Rainfall (mm)')
plt.scatter(39.2, 21.5, color='red', marker='o', label='Jeddah')
plt.legend()
plt.show()