# Battery benchmark

The copied executed notebook evaluates NASA Ames batteries B0005, B0006, B0007, and B0018 with leave-one-battery-out splits at 100%, 50%, 25%, and 10% development life. Each neural configuration uses seeds 13, 42, and 77. Inputs are 24 features from the first 600 seconds of discharge. Full metrics, predictions, controlled contrasts, histories, and figures are under `benchmark-evidence/`.

The Physics-regularized MLP leads full-data mean RMSE (0.027193), while empirical degradation leads the 10% regime (approximately 0.10993 RMSE). Ensemble dispersion is a seed diagnostic, not a calibrated interval.
