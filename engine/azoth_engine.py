import numpy as np, json, matplotlib.pyplot as plt, hashlib, datetime

lam = np.linspace(300, 800, 1200)

F  = np.exp(-0.5*((lam-550)/90)**2)
T  = np.exp(-0.001*(lam-550)**2)
Nr = 0.15 + 0.0015*(lam-550)**2
Ne = 0.10 + 0.002*np.abs(lam-550)

score = (F*T)/(Nr+Ne)
idx = int(np.argmax(score))

state = {
  "protocol": "AzothUniversalSensoryOptima",
  "version": "1.1",
  "timestamp": datetime.datetime.utcnow().isoformat()+"Z",
  "lambda_star": float(lam[idx]),
  "score": float(score[idx]),
  "H7": 0.70,
  "field": "spectral"
}

raw = json.dumps(state, sort_keys=True).encode()
state["hash"] = hashlib.sha256(raw).hexdigest()

json.dump(state, open("state/azoth_state.json","w"), indent=2)

plt.figure(figsize=(6,4))
plt.plot(lam, score)
plt.axvline(lam[idx], linestyle="--")
plt.xlabel("λ")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("visuals/optimum.png")
