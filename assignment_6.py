import cdsapi
import xarray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tools

# I will use the data provided by the professor because the download page is down. 

#Part 2: Data Pre-Processing 

dset = xarray.open_dataset(r"C:\Users\mayra\geo_env\assignment 6\download.nc")
t2m = np.array(dset.variables['t2m'])
tp = np.array(dset.variables['tp'])
latitude = np.array(dset.variables['latitude'])
longitude = np.array(dset.variables['longitude'])
time_dt = np.array(dset.variables['valid_time'])

t2m = t2m- 273.15
tp = tp * 1000

if t2m.ndim == 4:
 t2m = np.nanmean(t2m, axis=1)
 tp = np.nanmean(tp, axis=1)

# Create a Pandas dataframe containing time series data for both air temperature and precipitation

df_era5 = pd.DataFrame(index=time_dt)
df_era5['t2m'] = t2m[:,3,2]
df_era5['tp'] = tp[:,3,2]
ylabel = 'Temperature (°C) / Precipitation (mm)'
legend = ['Temperature (°C)', 'Precipitation (mm)'] 
df_era5.plot(legend=legend, ylabel=ylabel) 
#plt.legend(legend)
#plt.show()

#What is the average annual precipitation in mm y−1?
annual_precip = df_era5['tp'].resample('YE').mean()*24*365.25
mean_anual_precip = np.nanmean(annual_precip)
#print(f"Mean annual precipitation: {mean_anual_precip} mm")


#Part 3: Calculation of Potential Evaporation (PE)
tmin = df_era5['t2m'].resample('D').min().values
tmax = df_era5['t2m'].resample('D').max().values
tmean = df_era5['t2m'].resample('D').mean().values
lat = 21.25
doy = df_era5['t2m'].resample('D').mean().index.dayofyear

#Compute the PE using
pe = tools.hargreaves_samani_1982(tmin, tmax, tmean, lat, doy)

# Mean PE
mean_pe = np.nanmean(pe)
print(f"Mean potential evaporation: {mean_pe} mm/day")

#Plot the PE time series
ts_index = df_era5['t2m'].resample('D').mean().index
plt.figure()
plt.plot(ts_index, pe, label='Potential Evaporation')
plt.xlabel('Time')
plt.ylabel('Potential evaporation (mm/day)')
plt.show()