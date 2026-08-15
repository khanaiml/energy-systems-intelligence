import numpy as np
from app.dispatch import optimize
def test_balance_soc_and_repeatability():
    load=np.array([5.,7.,6.,4.]); pv=np.array([0.,4.,5.,0.]); price=np.array([.1,.2,.3,.1])
    a=optimize(load,pv,price); b=optimize(load,pv,price)
    assert a["reliability"]["energy_balance_residual"]<=1e-6
    assert min(a["dispatch"]["soc"])>=.1-1e-8 and max(a["dispatch"]["soc"])<=.95+1e-8
    assert a["economics"]["total_objective"]==b["economics"]["total_objective"]
    assert max(np.array(a["dispatch"]["charge"])*np.array(a["dispatch"]["discharge"]))<1e-6
def test_outage():
    r=optimize([3]*4,[0]*4,[.2]*4,outage_hours=[1,2]); assert r["dispatch"]["grid_import"][1:3]==[0,0]
