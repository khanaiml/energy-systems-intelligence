# Demo data

`hourly_load.csv` is the compact processed UCI ID 235 household series; `hourly_weather.csv` is matching Open-Meteo history. `forecast_history.csv` joins these for modeling. `demo_day.csv` scales the household load ×10 as an engineering reference microgrid and computes reference PV availability from irradiance/system efficiency; the runtime PV service uses pvlib. Raw archives are intentionally ignored.
