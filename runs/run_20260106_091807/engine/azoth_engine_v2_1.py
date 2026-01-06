import numpy as np, json, hashlib
from datetime import datetime, timezone

lam = np.linspace(300, 800, 1200)

def channel(lam, c, w, n):
    F = np.exp(-0.5*((lam-c)/w)**2)
    T = np.exp(-0.001*(lam-c)**2)
    score = (F*T)/(0.1+n*(lam-c)**2)
    idx = int(np.argmax(score))
    return float(lam[idx]), float(score[idx])

channels_raw = {
  "photon": channel(lam,550,90,0.0015),
  "vibration": channel(lam,420,70,0.002),
  "chemical": channel(lam,620,110,0.001)
}

# Normalize scores to [0,1]
scores = np.array([v[1] for v in channels_raw.values()])
scores_n = (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)

channels = {}
for i,(k,v) in enumerate(channels_raw.items()):
    channels[k] = {
        "lambda_star": v[0],
        "score_raw": v[1],
        "score_norm": float(scores_n[i])
    }

C_effective = float(scores_n.mean())

ts = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

state = {
  "protocol": "AzothUniversalSensoryOptima",
  "version": "2.1",
  "timestamp": ts,
  "H7": 0.70,
  "channels": channels,
  "C_effective": C_effective
}

regime_material = "2.1|" + "|".join(sorted(channels.keys())) + "|USO"
state["regime_hash"] = hashlib.sha256(regime_material.encode()).hexdigest()

raw = json.dumps(state, sort_keys=True).encode()
state["sha256"] = hashlib.sha256(raw).hexdigest()
state["bytes"]  = len(raw)

json.dump(state, open("azoth_state.json","w"), indent=2)
