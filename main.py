from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import json

app = FastAPI()

with open("compatibility.json", "r") as file:
    db = json.load(file)

@app.get("/compatibility-check")
def check_compatibility(cpu: str, motherboard: str, ram: str = "", gpu: str = ""):
    issues = []

    if cpu not in db["cpus"]:
        issues.append(f"CPU '{cpu}' non reconnu.")
    elif motherboard not in db["cpus"][cpu]["motherboards"]:
        issues.append(f"Incompatibilité entre CPU '{cpu}' et carte mère '{motherboard}'.")

    if ram and ram not in db["motherboards"].get(motherboard, {}).get("ram", []):
        issues.append(f"RAM '{ram}' non compatible avec la carte mère '{motherboard}'.")

    if gpu and db["gpus"].get(gpu, {}).get("recommended_psu", 0) > db["motherboards"].get(motherboard, {}).get("psu_limit", 1000):
        issues.append(f"GPU '{gpu}' demande une alimentation plus puissante que celle supportée par la carte mère.")

    return JSONResponse(content={
        "compatible": len(issues) == 0,
        "issues": issues
    })
