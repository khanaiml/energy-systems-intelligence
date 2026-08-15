# Digital twin

This is an hourly energy-dispatch model with PV, load, battery, grid import/export, curtailment, and unserved-energy slack. Effective capacity equals nominal capacity × clamp(current SOH, minimum operational SOH, 1). Stored energy updates with charge/discharge efficiencies and remains inside SOC bounds. Every result numerically checks the nodal energy balance to 1e-6 kWh.

It is not power flow, protection, voltage/frequency dynamics, or an electrochemical simulator. Throughput and equivalent full cycles are operational-wear proxies, not true SOH loss.
