from __future__ import annotations
import csv, io, json
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .battery import BatteryEstimateRequest, estimate, BASE
from .core import DATA, ROOT, read_json
from .database import delete_run, get_run, list_runs, save
from .dispatch import DEFAULT, compare, optimize
from .forecasting import day_ahead, metadata
from .scenarios import get as get_scenario, library

app=FastAPI(title="Physics-Aware Energy Intelligence API",version="1.0.0",description="Research and engineering demonstration; not a certified control or safety system.")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3000"],allow_methods=["*"],allow_headers=["*"])

class DispatchRequest(BaseModel):
    load_kw:list[float]|None=None; pv_kw:list[float]|None=None; prices:list[float]|None=None
    strategy:str="deterministic"; config:dict={}; outage_hours:list[int]=Field(default_factory=list)
class SimulationRequest(BaseModel):
    load_kw:list[float]|None=None; pv_kw:list[float]|None=None; config:dict={}

def demo_inputs():
    df=pd.read_csv(DATA/"demo_day.csv"); return df.load_kw.tolist(),df.pv_kw.tolist(),df.import_price.tolist()
def inputs(req):
    dl,dp,dc=demo_inputs(); load=req.load_kw or dl; pv=req.pv_kw or dp; prices=req.prices or dc
    if not (len(load)==len(pv)==len(prices) and 1<=len(load)<=168): raise HTTPException(422,"load, PV, and prices require equal lengths from 1 to 168")
    return load,pv,prices

@app.get("/health")
def health(): return {"status":"ok","offline_demo":True}
@app.get("/api/v1/system/info")
def info(): return {"name":"Physics-Aware Energy Intelligence","version":"1.0.0","site":"Sceaux reference scenario","research_use_only":True,"components":["battery SOH","load forecast","PV estimate","digital twin","dispatch"]}
@app.get("/api/v1/battery/model-info")
def battery_info(): return {"selected_model":read_json(BASE/"deployment_recommendation.json"),"schema":read_json(BASE/"feature_schema.json"),"ensemble_seeds":[13,42,77],"spread_label":"ensemble dispersion"}
@app.post("/api/v1/battery/estimate")
def battery_estimate(req:BatteryEstimateRequest): return estimate(req)
@app.post("/api/v1/battery/estimate/batch")
def battery_batch(reqs:list[BatteryEstimateRequest]):
    if not 1<=len(reqs)<=1000: raise HTTPException(422,"batch size must be 1..1000")
    return [estimate(r) for r in reqs]
@app.get("/api/v1/forecast/model-info")
def forecast_info(): return metadata()
@app.get("/api/v1/forecast/day-ahead")
def forecast_day(): return {"forecast":day_ahead(),"label":"forecast bands","source":"packaged UCI-derived demo window"}
@app.post("/api/v1/forecast/evaluate")
def forecast_evaluate(): return metadata()
@app.post("/api/v1/digital-twin/simulate")
def simulate(req:SimulationRequest):
    dl,dp,prices=demo_inputs(); result=optimize(req.load_kw or dl,req.pv_kw or dp,[0]*len(req.load_kw or dl),req.config,"self-consumption")
    result["economics"]["total_objective"]=0; return result
@app.get("/api/v1/dispatch/config")
def dispatch_config(): return {"defaults":DEFAULT,"solver":"scipy.optimize.linprog(method=highs)","engineering_assumptions":True}
@app.post("/api/v1/dispatch/optimize")
def dispatch_optimize(req:DispatchRequest):
    load,pv,prices=inputs(req); result=optimize(load,pv,prices,req.config,req.strategy,req.outage_hours); save(result); return result
@app.post("/api/v1/dispatch/compare")
def dispatch_compare(req:DispatchRequest):
    load,pv,prices=inputs(req); results=compare(load,pv,prices,req.config,req.outage_hours)
    for result in results: save(result)
    return results
@app.get("/api/v1/scenarios")
def scenarios(): return library()
@app.get("/api/v1/scenarios/{scenario_id}")
def scenario(scenario_id:str):
    found=get_scenario(scenario_id)
    if not found: raise HTTPException(404,"scenario not found")
    return found
@app.post("/api/v1/scenarios/{scenario_id}/run")
def run_scenario(scenario_id:str):
    found=get_scenario(scenario_id)
    if not found: raise HTTPException(404,"scenario not found")
    load,pv,prices=demo_inputs(); changes=found.get("changes",{}); load=np.asarray(load)*changes.get("load_multiplier",1); pv=np.asarray(pv)*changes.get("pv_multiplier",1); prices=np.asarray(prices)*changes.get("price_multiplier",1); cfg=changes.get("config",{}); outage=changes.get("outage_hours",[])
    results=compare(load,pv,prices,cfg,outage)
    for result in results: result["scenario"]=scenario_id; save(result)
    return {"scenario":found,"results":results,"explanation":found["analytical_purpose"]}
@app.get("/api/v1/evidence/battery")
def evidence_battery(): return read_json(ROOT/"benchmark-evidence"/"benchmark_summary.json")
@app.get("/api/v1/evidence/forecasting")
def evidence_forecasting(): return metadata()
@app.get("/api/v1/evidence/optimization")
def evidence_optimization(): return {"solver":"HiGHS continuous LP","balance_tolerance_kwh":1e-6,"strategies":["deterministic","conservative","uncertainty-aware"]}
@app.get("/api/v1/runs")
def runs(): return list_runs()
@app.get("/api/v1/runs/{run_id}")
def run(run_id:str):
    result=get_run(run_id)
    if not result: raise HTTPException(404,"run not found")
    return result
@app.delete("/api/v1/runs/{run_id}")
def remove(run_id:str):
    if not delete_run(run_id): raise HTTPException(404,"run not found")
    return Response(status_code=204)
@app.get("/api/v1/exports/{run_id}.json")
def export_json(run_id:str):
    result=get_run(run_id)
    if not result: raise HTTPException(404,"run not found")
    return Response(json.dumps(result,indent=2),media_type="application/json",headers={"Content-Disposition":f'attachment; filename="{run_id}.json"'})
@app.get("/api/v1/exports/{run_id}.csv")
def export_csv(run_id:str):
    result=get_run(run_id)
    if not result: raise HTTPException(404,"run not found")
    out=io.StringIO(); fields=["hour","grid_import","grid_export","charge","discharge","soc","curtailment","unserved_energy"]; writer=csv.DictWriter(out,fieldnames=fields); writer.writeheader()
    for h in range(result["horizon"]): writer.writerow({"hour":h,**{k:result["dispatch"][k][h] for k in fields[1:]}})
    return Response(out.getvalue(),media_type="text/csv",headers={"Content-Disposition":f'attachment; filename="{run_id}.csv"'})
