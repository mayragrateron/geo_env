import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr
dset = xr.open_dataset(r'C:/Users/mayra/geo_env/Course_Data/SRTMGL1_NC.003_Data/N21E039.SRTMGL1_NC.nc')
pdb.set_trace()
dset
dset.variables
DEM = np.array(dset.variables['SRTMGL1_DEM'])
dset.close()
print(DEM.shape)
plt.imshow(DEM)
cbar = plt.colorbar()
cbar.set_label('Elevation (m asl)')

plt.savefig('assignment_1.png', dpi=300)

plt.show()