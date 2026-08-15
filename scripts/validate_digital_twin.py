import sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"backend")); from app.dispatch import optimize
d=pd.read_csv(ROOT/"data"/"demo"/"demo_day.csv"); r=optimize(d.load_kw,d.pv_kw,d.import_price); assert r["reliability"]["energy_balance_residual"]<=1e-6; assert .1-1e-8<=min(r["dispatch"]["soc"])<=max(r["dispatch"]["soc"])<=.95+1e-8; print(r["reliability"])
