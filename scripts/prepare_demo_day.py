from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
load=pd.read_csv(ROOT/"data"/"demo"/"hourly_load.csv"); weather=pd.read_csv(ROOT/"data"/"demo"/"hourly_weather.csv")
load["timestamp"]=pd.to_datetime(load.timestamp); weather["timestamp"]=pd.to_datetime(weather.timestamp)
day=load.merge(weather,on="timestamp"); day=day[day.timestamp.dt.date==day.timestamp.dt.date.max()].copy()
day["load_kw"]*=10.0
# Irradiance-to-nameplate reference availability; runtime PV service uses pvlib transposition.
day["pv_kw"]=(12*day.shortwave_radiation/1000*0.96*(1-0.14)).clip(0,12)
day["import_price"]=[.14 if h<7 or h>=22 else .36 if 17<=h<21 else .22 for h in day.timestamp.dt.hour]
day[["timestamp","load_kw","pv_kw","import_price"]].to_csv(ROOT/"data"/"demo"/"demo_day.csv",index=False)
day[["timestamp","import_price"]].assign(export_price=.04).to_csv(ROOT/"data"/"demo"/"tariff.csv",index=False)
print(day[["timestamp","load_kw","pv_kw"]].to_string(index=False))
