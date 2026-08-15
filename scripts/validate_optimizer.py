import sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"backend")); from app.dispatch import compare
d=pd.read_csv(ROOT/"data"/"demo"/"demo_day.csv"); rows=compare(d.load_kw,d.pv_kw,d.import_price); assert all(r["reliability"]["solver_status"]=="optimal" for r in rows); assert all(max(a*b for a,b in zip(r["dispatch"]["charge"],r["dispatch"]["discharge"]))<1e-6 for r in rows); print([(r["strategy"],r["economics"]["total_objective"]) for r in rows])
