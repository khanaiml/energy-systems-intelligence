"""Create the compact chronological 2009 demo slice from the downloaded UCI archive."""
from __future__ import annotations
import zipfile
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; archive=ROOT/"data"/"raw"/"uci_household_power.zip"
with zipfile.ZipFile(archive) as z, z.open("household_power_consumption.txt") as src:
    df=pd.read_csv(src,sep=";",na_values="?",usecols=["Date","Time","Global_active_power"])
df["timestamp"]=pd.to_datetime(df.Date+" "+df.Time,dayfirst=True)
df=df.set_index("timestamp").loc["2009-01-01":"2009-03-31"]
# Global_active_power is mean kW at minute cadence; hourly mean is hourly average power.
hourly=df.Global_active_power.resample("1h").mean().interpolate(limit=2).rename("load_kw").dropna().reset_index()
hourly.to_csv(ROOT/"data"/"demo"/"hourly_load.csv",index=False)
print(hourly.timestamp.min(),hourly.timestamp.max(),len(hourly))
