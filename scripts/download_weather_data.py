"""Cache matching Open-Meteo archive weather for the UCI demo period."""
from __future__ import annotations
import hashlib,json,urllib.parse,urllib.request
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
params={"latitude":48.78,"longitude":2.29,"start_date":"2009-01-01","end_date":"2009-03-31","hourly":"temperature_2m,relative_humidity_2m,cloud_cover,shortwave_radiation,direct_normal_irradiance,diffuse_radiation,wind_speed_10m","timezone":"Europe/Paris"}
url="https://archive-api.open-meteo.com/v1/archive?"+urllib.parse.urlencode(params)
with urllib.request.urlopen(url,timeout=90) as response: raw=response.read()
payload=json.loads(raw); h=payload["hourly"]
pd.DataFrame({"timestamp":h["time"],"temperature":h["temperature_2m"],"humidity":h["relative_humidity_2m"],"cloud_cover":h["cloud_cover"],"shortwave_radiation":h["shortwave_radiation"],"dni":h["direct_normal_irradiance"],"diffuse_radiation":h["diffuse_radiation"],"wind_speed":h["wind_speed_10m"]}).to_csv(ROOT/"data"/"demo"/"hourly_weather.csv",index=False)
(ROOT/"data"/"provenance"/"open_meteo_weather.json").write_text(json.dumps({"provider":"Open-Meteo Historical Weather API","request_url":url,"request_parameters":params,"response_sha256":hashlib.sha256(raw).hexdigest(),"timezone":payload.get("timezone"),"license":"CC BY 4.0; weather sources attributed by Open-Meteo"},indent=2))
print(url,len(h["time"]))
