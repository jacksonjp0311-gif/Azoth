import numpy as np, json, hashlib, datetime, random, matplotlib.pyplot as plt

def channel(lam, center, width, noise):
    F = np.exp(-0.5*((lam-center)/width)**2)
    T = np.exp(-0.001*(lam-center)**2)
    Nr = 0.1 + noise*(lam-center)**2
    Ne = 0.1 + noise*np.abs(lam-center)
    score = (F*T)/(Nr+Ne)
    idx = int(np.argmax(score))
    return float(lam[idx]), float(score[idx])

lam = np.linspace(300, 800, 1200)

channels = {
    "photon": channel(lam, 550, 90, 0.0015),
    "vibration": channel(lam, 420, 70, 0.002),
    "chemical": channel(lam, 620, 110, 0.001)
}

state = {
  "protocol": "AzothUniversalSensoryOptima",
  "version": "1.6",
  "timestamp": datetime.datetime.utcnow().isoformat()+"Z",
  "channels": {},
  "H7": 0.70
}

scores = []
for k,v in channels.items():
    state["channels"][k] = {"lambda_star": v[0], "score": v[1]}
    scores.append(v[1])

state["C_effective"] = sum(scores)/len(scores)

raw = json.dumps(state, sort_keys=True).encode()
state["hash"] = hashlib.sha256(raw).hexdigest()

json.dump(state, open("state/azoth_state.json","w"), indent=2)
