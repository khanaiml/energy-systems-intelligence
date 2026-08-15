from __future__ import annotations

import time
import uuid

import numpy as np
from scipy.optimize import linprog


DEFAULT = {"nominal_capacity_kwh":20.0,"current_soh":0.9,"max_charge_kw":8.0,"max_discharge_kw":8.0,"charge_efficiency":0.95,"discharge_efficiency":0.95,"minimum_soc_fraction":0.1,"maximum_soc_fraction":0.95,"initial_soc_fraction":0.6,"terminal_soc_target_fraction":0.5,"max_import_kw":25.0,"max_export_kw":10.0,"export_enabled":True,"throughput_cost":0.03,"unserved_penalty":100.0,"curtailment_penalty":0.001}


def optimize(load, pv, prices, config=None, strategy="deterministic", outage_hours=None):
    started = time.perf_counter()
    cfg = {**DEFAULT, **(config or {})}
    load, pv, prices = map(lambda x: np.asarray(x, dtype=float), (load, pv, prices))
    n = len(load); block = n; # variables: import/export/charge/discharge/curtail/unserved/E[0:n+1]/terminal+/-
    off = {k:i*block for i,k in enumerate(("imp","exp","chg","dis","curt","uns"))}; e0=6*block; tp=e0+n+1; tm=tp+1; total=tm+1
    c=np.zeros(total); c[off["imp"]:off["imp"]+n]=prices; c[off["exp"]:off["exp"]+n]=-0.04; c[off["chg"]:off["chg"]+n]=cfg["throughput_cost"]; c[off["dis"]:off["dis"]+n]=cfg["throughput_cost"]; c[off["curt"]:off["curt"]+n]=cfg["curtailment_penalty"]; c[off["uns"]:off["uns"]+n]=cfg["unserved_penalty"]; c[tp]=c[tm]=1.0
    A=[]; b=[]
    for t in range(n):
        row=np.zeros(total); row[off["imp"]+t]=1; row[off["exp"]+t]=-1; row[off["chg"]+t]=-1; row[off["dis"]+t]=1; row[off["curt"]+t]=-1; row[off["uns"]+t]=1; A.append(row); b.append(load[t]-pv[t])
        row=np.zeros(total); row[e0+t]=-1; row[e0+t+1]=1; row[off["chg"]+t]=-cfg["charge_efficiency"]; row[off["dis"]+t]=1/cfg["discharge_efficiency"]; A.append(row); b.append(0)
    row=np.zeros(total); row[e0]=1; A.append(row); cap=cfg["nominal_capacity_kwh"]*np.clip(cfg["current_soh"],0.5,1); b.append(cap*cfg["initial_soc_fraction"])
    target=cap*cfg["terminal_soc_target_fraction"]; row=np.zeros(total); row[e0+n]=1; row[tp]=-1; row[tm]=1; A.append(row); b.append(target)
    outages=set(outage_hours or []); bounds=[]
    for name in ("imp","exp","chg","dis","curt","uns"):
        for t in range(n):
            upper={"imp":cfg["max_import_kw"],"exp":cfg["max_export_kw"] if cfg["export_enabled"] else 0,"chg":cfg["max_charge_kw"],"dis":cfg["max_discharge_kw"],"curt":float(pv[t]),"uns":float(load[t])}[name]
            if name in ("imp","exp") and t in outages: upper=0
            bounds.append((0,upper))
    bounds += [(cap*cfg["minimum_soc_fraction"],cap*cfg["maximum_soc_fraction"])]*(n+1)+[(0,None),(0,None)]
    sol=linprog(c,A_eq=np.array(A),b_eq=np.array(b),bounds=bounds,method="highs")
    if not sol.success: raise ValueError(f"dispatch infeasible: {sol.message}")
    x=sol.x; arr=lambda name: x[off[name]:off[name]+n].tolist(); energy=x[e0:e0+n+1]
    residual=np.max(np.abs(np.array(A[:-2])@x-np.array(b[:-2])))
    throughput=sum(arr("chg"))+sum(arr("dis")); import_cost=float(np.dot(prices,x[off["imp"]:off["imp"]+n])); export_revenue=float(.04*sum(arr("exp")))
    return {"run_id":str(uuid.uuid4()),"strategy":strategy,"scenario":"base","horizon":n,"timestep":1,"input_summary":{"load_kwh":float(load.sum()),"pv_available_kwh":float(pv.sum())},"forecast":{"load_p10":(load*.9).tolist(),"load_p50":load.tolist(),"load_p90":(load*1.1).tolist(),"pv_low":(pv*.7).tolist(),"pv_base":pv.tolist(),"pv_high":(pv*1.1).tolist()},"battery":{"nominal_capacity":cfg["nominal_capacity_kwh"],"current_soh":cfg["current_soh"],"effective_capacity":cap,"initial_soc":float(energy[0]/cap),"terminal_soc":float(energy[-1]/cap),"minimum_soc":float(energy.min()/cap),"throughput":throughput,"equivalent_full_cycles":float(sum(arr("dis"))/cap)},"dispatch":{"grid_import":arr("imp"),"grid_export":arr("exp"),"charge":arr("chg"),"discharge":arr("dis"),"soc":(energy/cap).tolist(),"curtailment":arr("curt"),"unserved_energy":arr("uns")},"economics":{"import_cost":import_cost,"export_revenue":export_revenue,"throughput_cost":throughput*cfg["throughput_cost"],"unserved_penalty":sum(arr("uns"))*cfg["unserved_penalty"],"total_objective":float(sol.fun)},"reliability":{"energy_balance_residual":float(residual),"constraint_violations":[],"solver_status":"optimal","worst_case_cost":float(sol.fun),"reserve_status":"met" if energy[-1]>=target-1e-6 else "shortfall"},"runtime_ms":(time.perf_counter()-started)*1000}


def compare(load,pv,prices,config=None,outage_hours=None):
    base=optimize(load,pv,prices,config,"deterministic",outage_hours)
    conservative=optimize(np.asarray(load)*1.1,np.asarray(pv)*.7,prices,config,"conservative",outage_hours)
    uncertain=optimize(np.asarray(load)*1.04,np.asarray(pv)*.85,prices,config,"uncertainty-aware",outage_hours)
    uncertain["reliability"]["worst_case_cost"]=conservative["economics"]["total_objective"]
    return [base,conservative,uncertain]
