# Battery artifact audit

Source: `../physics_aware_battery_soh__benchmark_outputs` in the parent research directory. The executed notebook SHA-256 is `087eb78e9f489fa96fd058d1ae8421f54244ad8125b04d465af95dbae180defa`; all 26 code cells have execution counts and 22 contain outputs.

The schema has exactly 24 ordered features and matches the notebook `FEATURE_COLUMNS`. Preprocessing is the fitted `SimpleImputer(strategy="median")` followed by `StandardScaler`. CPU validation loaded all three models and confirmed `forward(..., Tensor features, Tensor cycle) -> Tensor`, one bounded SOH value per row, deterministic repeated inference, finite outputs, non-negative dispersion, and no CUDA requirement. The median-reference validation case returned seed values 0.87168193, 0.87191963, and 0.86479521 (mean 0.86946559; dispersion 0.00330388).

## Production hashes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| model_seed_13_torchscript.pt | 26,082 | `ce5b95c072c0c55d423426bae87be490808647e90ff9ab8f7e0d199ba7f747b0` |
| model_seed_42_torchscript.pt | 26,082 | `a4a3d60b67bce70f0b8b1c9bef00a3391d67d7d11f1205539cc92fa795c773e4` |
| model_seed_77_torchscript.pt | 26,082 | `35c4e418c484e24ad5c259d0ea19a3210d7a69190f6ab39d9b79f17ed7b7878a` |
| feature_imputer.joblib | 1,383 | `5f72cbcf33140ad80f20f981d09ba23423f20665bf2e4d99525f5400359a61cc` |
| feature_scaler.joblib | 1,191 | `be0d3d084bca917dc7aedf064be12d27d4a4135e315755ba5f5adec70e07a85e` |
| feature_schema.json | 1,107 | `aaa0b6072cf75aece54d8be083eb120b0746951d8375d9c49ef3a085257e5d97` |
| empirical_parameters.json | 154 | `9d4d17ef400c9bc805ea0f4e27e92a1bc831a0d34277c29f95923a59ce886da2` |
| deployment_recommendation.json | 503 | `9faae98fdb5f925c940b04c1ccaf29b3c6573194e62761aa3ad4a96f6728294f` |

Empirical parameters are `c=1.0184459953800824`, `a=0.003308146206927845`, `b=0.001987146081083061`. The recommendation selects Physics-regularized MLP and retains empirical degradation as the 10% data winner.

## Evidence verification

The JSON and aggregate CSV evidence agree: 636 parsed cycles, four held-out batteries, 24 inputs, four data fractions, three neural seeds, and 192 neural fits. At full development data the selected model has mean RMSE 0.0271933623, MAE 0.0234722528, R² 0.9171448457, and late-life RMSE 0.0269847910. Direct-MLP physics penalty median benefit is +0.0158344528; 62.5% of paired settings improved; all four batteries have positive mean benefit; worst case is -0.0550235452. Three-seed spread is not a calibrated prediction interval.
