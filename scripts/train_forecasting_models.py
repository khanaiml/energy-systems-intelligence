from __future__ import annotations
import json
from pathlib import Path
import joblib,numpy as np,pandas as pd
from sklearn.ensemble import GradientBoostingRegressor,HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error
ROOT=Path(__file__).resolve().parents[1]
import sys; sys.path.insert(0,str(ROOT/"backend")); from app.forecasting import FEATURES,make_features
load=pd.read_csv(ROOT/"data"/"demo"/"hourly_load.csv"); weather=pd.read_csv(ROOT/"data"/"demo"/"hourly_weather.csv")
load["timestamp"]=pd.to_datetime(load.timestamp); weather["timestamp"]=pd.to_datetime(weather.timestamp)
df=load.merge(weather[["timestamp","temperature","humidity"]],on="timestamp"); df.to_csv(ROOT/"data"/"demo"/"forecast_history.csv",index=False); frame=make_features(df).dropna().reset_index(drop=True)
n=len(frame); train=frame.iloc[:int(.7*n)]; val=frame.iloc[int(.7*n):int(.85*n)]; test=frame.iloc[int(.85*n):]
point=HistGradientBoostingRegressor(max_iter=180,l2_regularization=.2,random_state=42).fit(train[FEATURES],train.load_kw)
models={"p10":GradientBoostingRegressor(loss="quantile",alpha=.1,n_estimators=180,random_state=42),"p50":GradientBoostingRegressor(loss="quantile",alpha=.5,n_estimators=180,random_state=42),"p90":GradientBoostingRegressor(loss="quantile",alpha=.9,n_estimators=180,random_state=42)}
for m in models.values(): m.fit(train[FEATURES],train.load_kw)
pred=point.predict(test[FEATURES]); qs={k:m.predict(test[FEATURES]) for k,m in models.items()}; p10=np.minimum(qs["p10"],qs["p50"]); p90=np.maximum(qs["p90"],qs["p50"]); y=test.load_kw.to_numpy()
def metrics(p): return {"mae":float(mean_absolute_error(y,p)),"rmse":float(mean_squared_error(y,p)**.5),"smape_percent":float(np.mean(2*np.abs(y-p)/(np.abs(y)+np.abs(p)+1e-9))*100)}
evaluation={"dataset_period":[str(frame.timestamp.iloc[0]),str(frame.timestamp.iloc[-1])],"split_rows":{"train":len(train),"validation":len(val),"test":len(test)},"split":"chronological 70/15/15","features":FEATURES,"point_model":"HistGradientBoostingRegressor","point":metrics(pred),"baselines":{"last_hour":metrics(test.lag_1),"previous_day":metrics(test.lag_24),"previous_week":metrics(test.lag_168)},"quantiles":{"coverage_p10_p90":float(np.mean((y>=p10)&(y<=p90))),"mean_interval_width_kw":float(np.mean(p90-p10)),"label":"forecast bands"},"source":"UCI ID 235 compact processed window; household reference profile"}
base=ROOT/"backend"/"artifacts"/"forecasting"; base.mkdir(parents=True,exist_ok=True); joblib.dump(point,base/"point_model.joblib")
for k,m in models.items(): joblib.dump(m,base/f"quantile_{k}.joblib")
(base/"feature_schema.json").write_text(json.dumps({"features":FEATURES},indent=2)); (base/"forecast_metadata.json").write_text(json.dumps({"trained_utc":"2026-08-15","random_seed":42,"normal_startup_retrains":False},indent=2)); (base/"evaluation.json").write_text(json.dumps(evaluation,indent=2)); print(json.dumps(evaluation,indent=2))
