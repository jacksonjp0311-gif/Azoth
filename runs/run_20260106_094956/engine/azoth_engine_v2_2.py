import numpy as np, json, hashlib, os
from datetime import datetime, timezone

# ------------------------------------------
# AZOTH v2.2 — Universal Sensory Optima
# Fix: C_effective must be in [0,1] coherence space
# ------------------------------------------

lam = np.linspace(300, 800, 1200)

def channel(lam, c, w, n):
    F = np.exp(-0.5*((lam-c)/w)**2)
    T = np.exp(-0.001*(lam-c)**2)
    score = (F*T)/(0.1+n*(lam-c)**2)
    idx = int(np.argmax(score))
    return float(lam[idx]), float(score[idx])

channels_raw = {
  "photon": channel(lam,550,90,0.0015),
  "vibration": channel(lam,420,70,0.0020),
  "chemical": channel(lam,620,110,0.0010)
}

# Normalize scores to [0,1] for coherence semantics
scores = np.array([v[1] for v in channels_raw.values()], dtype=float)
scores_min = float(scores.min())
scores_max = float(scores.max())
scores_n = (scores - scores_min) / (scores_max - scores_min + 1e-12)

channels = {}
for i,(k,v) in enumerate(channels_raw.items()):
    channels[k] = {
        "lambda_star": v[0],
        "score_raw": float(v[1]),
        "score_norm": float(scores_n[i])
    }

C_effective = float(scores_n.mean())

ts = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

state = {
  "protocol": "AzothUniversalSensoryOptima",
  "version": "2.2",
  "timestamp": ts,
  "H7": 0.70,
  "coherence_space": {
    "range": [0.0, 1.0],
    "reference": "H7",
    "interpretation": "normalized score_norm average (ΔΦ-compatible coherence scalar)"
  },
  "normalization": {
    "method": "minmax",
    "scores_raw_min": scores_min,
    "scores_raw_max": scores_max,
    "epsilon": 1e-12
  },
  "channels": channels,
  "C_effective": C_effective
}

# Regime hash (identity of measurement regime, not outcome)
regime_material = "2.2|" + "|".join(sorted(channels.keys())) + "|USO"
state["regime_hash"] = hashlib.sha256(regime_material.encode()).hexdigest()

raw = json.dumps(state, sort_keys=True).encode()
state["sha256"] = hashlib.sha256(raw).hexdigest()
state["bytes"]  = len(raw)

out = os.path.join(os.getcwd(), "azoth_state.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2)

print("AZOTH_ENGINE_OK")
