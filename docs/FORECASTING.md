# Forecasting

Features use calendar/weather context and load lags 1/24/48/168 plus rolling statistics shifted by one hour. This prevents target-hour leakage. The split is chronological 70/15/15. HistGradientBoosting is compared with last-hour, previous-day, and previous-week baselines. Quantile gradient boosting produces P10/P50/P90 bands; empirical P10–P90 coverage is 78.26%, so these are called forecast bands, not guaranteed or calibrated intervals. Exact measured metrics are saved in `backend/artifacts/forecasting/evaluation.json`.
