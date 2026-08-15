"""Download the official UCI Household Power Consumption archive into data/raw."""
from __future__ import annotations
import hashlib, json, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data"/"raw"; RAW.mkdir(parents=True,exist_ok=True)
URL="https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"
target=RAW/"uci_household_power.zip"
if not target.exists(): urllib.request.urlretrieve(URL,target)
sha=hashlib.sha256(target.read_bytes()).hexdigest()
(ROOT/"data"/"provenance"/"uci_load.json").write_text(json.dumps({"dataset":"Individual Household Electric Power Consumption","uci_id":235,"doi":"10.24432/C58K54","source_url":URL,"license":"CC BY 4.0","sha256":sha,"timezone_assumption":"Europe/Paris local civil time"},indent=2))
print(target,sha)
