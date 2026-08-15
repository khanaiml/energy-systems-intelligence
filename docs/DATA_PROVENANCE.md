# Data provenance

- Battery: NASA Ames PCoE Li-ion Battery Aging Dataset; source-file hashes are retained in benchmark evidence. The executed study downloaded a public mirror. Raw MATLAB files are not redistributed.
- Load: UCI Individual Household Electric Power Consumption, ID 235, DOI 10.24432/C58K54, CC BY 4.0. The committed January–March 2009 hourly subset is average kW from minute observations. Default ×10 scaling is an engineering scenario, not measured community load.
- Weather: Open-Meteo Historical Weather API for Sceaux (48.78, 2.29), Europe/Paris, matching the load period. Request and response hash are in `data/provenance/`.
- Tariff: synthetic engineering assumption, explicitly not a current utility tariff.
