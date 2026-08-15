from __future__ import annotations
import yaml
from .core import ROOT
def library():
    return [{"id":p.stem,**yaml.safe_load(p.read_text())} for p in sorted((ROOT/"scenarios").glob("*.yaml"))]
def get(sid): return next((s for s in library() if s["id"]==sid),None)
