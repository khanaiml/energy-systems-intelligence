from pathlib import Path
print((Path(__file__).resolve().parents[1]/"backend"/"artifacts"/"forecasting"/"evaluation.json").read_text())
