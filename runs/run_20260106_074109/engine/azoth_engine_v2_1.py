import numpy as np, json, hashlib
from datetime import datetime, timezone

lam = np.linspace(300, 800, 1200)

def channel(lam, c, w, n):
    F = np.exp(-0.5*((lam-c)/w)**2)
    T = np.exp(-0.001*(lam-c)**2)
    score = (F*T)/(0.1+n*(lam-c)**2)
    i = int(np.argmax(score))
    return float(lam[i]), float(score[i])

channels = {
  "photon":    channel(lam,550,90,0.0015),
  "vibration": channel(lam,420,70,0.0020),
  "chemical":  channel(lam,620,110,0.0010)
}

ts = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

state = {
  "protocol": "AzothUniversalSensoryOptima",
  "version":  "2.1",
  "timestamp": ts,
  "H7": 0.70,
  "channels": {}
}

scores = []
for k,(lam_star,score) in channels.items():
    state["channels"][k] = {
        "lambda_star": lam_star,
        "score": score
    }
    scores.append(score)

state["C_effective"] = float(sum(scores)/len(scores))

# Regime identity = structural, not numeric
regime_material = "2.1|" + "|".join(sorted(state["channels"].keys())) + "|USO"
state["regime_hash"] = hashlib.sha256(regime_material.encode("utf-8")).hexdigest()

raw = json.dumps(state, sort_keys=True).encode("utf-8")
state["sha256"] = hashlib.sha256(raw).hexdigest()
state["bytes"]  = len(raw)

with open("azoth_state.json","w",encoding="utf-8") as f:
    json.dump(state,f,indent=2)
