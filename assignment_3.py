#Part 1: Downloading and Importing Jeddah Weather Data

import tools
import pandas as pd
import matplotlib.pyplot as plt

csv_path = (r'C:\Users\mayra\geo_env\Course_Data\ISD_Data\41024099999.csv')
df_isd = tools.read_isd_csv(csv_path)
plot = df_isd.plot(title="ISD data for Jeddah")
plt.show() 

# Part 2: Heat Index (HI) Calculation


df_isd['RH'] = tools.dewpoint_to_rh(df_isd['DEW'].values, df_isd['TMP'].values)
df_isd['HI'] = tools.gen_heat_index(df_isd['TMP'].values, df_isd['RH'].values)

#Calculate highest HI observed in the year
max_hi = df_isd['HI'].max()
print("Highest HI observed:", max_hi)

#Calculate day and time when the highest HI was observed
max_hi_time = df_isd['HI'].idxmax()
print("Day and time HI:", max_hi_time)

#Calculate air temperature and relative humidity
max_hi_conditions = df_isd.loc[max_hi_time, ['TMP', 'RH']]
print("Air temperature and humidity HI max:", max_hi_conditions)

df_daily = df_isd.resample('D').mean()
df_daily['HI'] = tools.gen_heat_index(df_daily['TMP'].values, df_daily['RH'].values)

df_isd['HI'].plot(title="Heat index in Jeddah (2024)")
plt.xlabel("Date")
plt.ylabel("HI (°C)")
plt.savefig("HI_timeseries.png")
plt.show()

# Part 3: Potential Impact of Climate Change
# What is the projected increase in air temperature for Jeddah

warming_offset = 2.7
df_isd['TMP_future'] = df_isd['TMP'] + warming_offset
df_isd['HI_future'] = tools.gen_heat_index(df_isd['TMP_future'].values, df_isd['RH'].values)
print("Highest HI observed:", df_isd['HI'].max())
print("Highest projected HI:", df_isd['HI_future'].max())
print("Increase in HI due to climate change:", df_isd['HI_future'].max() - df_isd['HI'].max())
