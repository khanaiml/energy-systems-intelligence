import argparse,json,sys
from pathlib import Path
import pandas as pd,yaml
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"backend")); from app.dispatch import compare
p=argparse.ArgumentParser(); p.add_argument("scenario",nargs="?",default="cloudy-day"); a=p.parse_args(); s=yaml.safe_load((ROOT/"scenarios"/f"{a.scenario}.yaml").read_text()); c=s["changes"]; d=pd.read_csv(ROOT/"data"/"demo"/"demo_day.csv"); results=compare(d.load_kw*c.get("load_multiplier",1),d.pv_kw*c.get("pv_multiplier",1),d.import_price*c.get("price_multiplier",1),c.get("config",{}),c.get("outage_hours",[])); print(json.dumps({"scenario":s,"results":results},indent=2,default=float))
