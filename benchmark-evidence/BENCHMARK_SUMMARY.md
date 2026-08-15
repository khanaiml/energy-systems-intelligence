# Physics-Aware Battery SOH Benchmark — Result Summary

## Study

- Dataset: NASA Ames PCoE Li-ion Battery Aging Dataset
- Batteries: B0005, B0006, B0007, B0018
- Early-discharge feature window: 600 seconds
- Features: 24
- Cross-battery protocol: leave one battery out
- Data regimes: 100%, 50%, 25%, 10%
- Neural ensemble seeds: [13, 42, 77]

## Best average model

### Full development data

- Model: **Physics-regularized MLP**
- Mean RMSE: **0.02719**
- Mean MAE: **0.02347**
- Mean late-life RMSE: **0.02698**
- Mean total regeneration: **0.19964**

### 10% observed development life

- Model: **Empirical degradation**
- Mean RMSE: **0.10993**
- Mean MAE: **0.09704**
- Mean late-life RMSE: **0.16614**

## Controlled ablations

### Physics penalty on direct MLP

- Mean RMSE benefit: **+0.01420**
- Median RMSE benefit: **+0.01583**
- Median relative benefit: **+19.6%**
- Fraction of paired settings improved: **62.5%**
- Worst-case RMSE benefit: **-0.05502**
- Batteries with positive mean benefit: **4/4**

### Empirical prior/residual architecture

- Mean RMSE benefit: **+0.00694**
- Median RMSE benefit: **-0.00343**
- Median relative benefit: **-11.6%**
- Fraction of paired settings improved: **43.8%**
- Worst-case RMSE benefit: **-0.03479**
- Batteries with positive mean benefit: **2/4**

### Physics penalty within hybrid

- Mean RMSE benefit: **-0.00723**
- Median RMSE benefit: **-0.00502**
- Median relative benefit: **-13.7%**
- Fraction of paired settings improved: **31.2%**
- Worst-case RMSE benefit: **-0.02967**
- Batteries with positive mean benefit: **1/4**

### Hybrid physics residual vs empirical baseline

- Mean RMSE benefit: **+0.01932**
- Median RMSE benefit: **+0.01342**
- Median relative benefit: **+13.9%**
- Fraction of paired settings improved: **68.8%**
- Worst-case RMSE benefit: **-0.03888**
- Batteries with positive mean benefit: **4/4**

A positive RMSE benefit means the candidate reduced RMSE relative to its matched reference.

## Interpretation policy

The final conclusion must distinguish the empirical-prior architectural effect from the additional effect of sequence-physics penalties.

The benchmark does not assume that physics-aware learning must outperform a matched baseline.

## Research scope

These are research benchmark results and are not certified battery-management or safety claims.