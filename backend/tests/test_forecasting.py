import pandas as pd
from app.forecasting import make_features
def test_lags_are_past_only():
    f=make_features(pd.DataFrame({"timestamp":pd.date_range("2020-01-01",periods=200,freq="h"),"load_kw":range(200),"temperature":10,"humidity":50}))
    assert f.loc[168,"lag_1"]==167 and f.loc[168,"lag_168"]==0 and f.loc[168,"rolling_mean_24"]==155.5
