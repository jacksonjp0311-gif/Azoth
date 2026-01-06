import numpy as np, json, hashlib
from datetime import datetime, timezone

lam = np.linspace(300, 800, 1200)

def channel(lam, c, w, n):
    F = np.exp(-0.5*((lam-c)/w)**2)
    T = np.exp(-0.001*(lam-c)**2)
    score = (F*T)/(1e-6 + n*(lam-c)**2)
    idx = int(np.argmax(score))
    return float(lam[idx]), float(score[idx])

raw_channels = {
  "photon": channel(lam,550,90,0.0015),
  "vibration": channel(lam,420,70,0.0020),
  "chemical": channel(lam,620,110,0.0010)
}

scores = np.array([v[1] for v in raw_channels.values()])
scores_n = (scores - scores.min()) / (scores.ptp() + 1e-9)

channels = {}
for i,(k,v) in enumerate(raw_channels.items()):
    channels[k] = {
        "lambda_star": v[0],
        "score_raw":   v[1],
        "score_norm":  float(scores_n[i])
    }

C_effective = float(scores_n.mean())

state = {
  "protocol": "AzothUniversalSensoryOptima",
  "version":  "2.2",
  "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
  "H7": 0.70,
  "channels": channels,
  "C_effective": C_effective
}

regime_material = "2.2|" + "|".join(sorted(channels.keys())) + "|USO"
state["regime_hash"] = hashlib.sha256(regime_material.encode()).hexdigest()

raw = json.dumps(state, sort_keys=True).encode()
state["sha256"] = hashlib.sha256(raw).hexdigest()
state["bytes"]  = len(raw)

json.dump(state, open("azoth_state.json","w"), indent=2)
