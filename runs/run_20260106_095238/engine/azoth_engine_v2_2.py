import numpy as np, json, hashlib
from datetime import datetime, timezone

lam = np.linspace(300, 800, 1200)

def channel(lam, c, w, n):
    F = np.exp(-0.5*((lam-c)/w)**2)
    T = np.exp(-0.001*(lam-c)**2)
    score = (F*T)/(0.1+n*(lam-c)**2)
    i = int(np.argmax(score))
    return float(lam[i]), float(score[i])

raw = {
  "photon": channel(lam,550,90,0.0015),
  "vibration": channel(lam,420,70,0.002),
  "chemical": channel(lam,620,110,0.001)
}

scores = np.array([v[1] for v in raw.values()])
norm = (scores - scores.min()) / (scores.max() - scores.min() + 1e-12)

channels = {}
for i,(k,v) in enumerate(raw.items()):
    channels[k] = {
        "lambda_star": v[0],
        "score_raw": v[1],
        "score_norm": float(norm[i])
    }

C = float(norm.mean())

ts = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

state = {
  "protocol": "AzothUniversalSensoryOptima",
  "version": "2.2",
  "timestamp": ts,
  "H7": 0.70,
  "channels": channels,
  "C_effective": C
}

regime_material = "AZOTH|2.2|" + "|".join(sorted(channels.keys()))
state["regime_hash"] = hashlib.sha256(regime_material.encode()).hexdigest()

raw = json.dumps(state, sort_keys=True).encode()
state["sha256"] = hashlib.sha256(raw).hexdigest()
state["bytes"]  = len(raw)

json.dump(state, open("azoth_state.json","w"), indent=2)
