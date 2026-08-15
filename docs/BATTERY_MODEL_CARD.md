# Battery model card

Input: exact ordered benchmark features and cycle index. Output: three seed predictions, mean estimated SOH, population standard deviation labelled ensemble dispersion, and empirical reference. Median imputation is allowed for at most eight absent inputs and is always disclosed. Unknown fields are rejected.

The model estimates SOH in the benchmark domain. It does not estimate safety, faults, remaining useful life, or replacement decisions, and it is not validated for real packs or a BMS.
