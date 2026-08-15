# Optimization

SciPy HiGHS solves a continuous LP over hourly import, export, charge, discharge, curtailment, unserved energy, stored energy, and terminal-deviation auxiliaries. Objective terms cover import cost, export revenue, throughput proxy, unserved penalty, curtailment, and terminal target deviation. Outage hours force import/export to zero. Positive throughput cost and efficiency losses economically dominate simultaneous charge/discharge; results are explicitly checked.

Conservative and uncertainty-aware modes use adverse load/PV representations. The current uncertainty-aware implementation is a transparent conservative proxy, not a full shared-first-stage nine-scenario stochastic LP; this limitation is retained in validation reporting.
