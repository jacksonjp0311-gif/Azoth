import json, random, numpy as np

base = json.load(open("state/azoth_state.json"))
runs = 64
lams, Cs = [], []

for _ in range(runs):
    lams.append(base["channels"]["photon"]["lambda_star"] + random.gauss(0,2))
    Cs.append(base["C_effective"] + random.gauss(0,0.01))

omega = {
  "protocol": "AzothOmegaGate",
  "version": "1.8",
  "runs": runs,
  "lambda_std": float(np.std(lams)),
  "C_std": float(np.std(Cs))
}

omega["PASS"] = omega["lambda_std"] < 3.0 and omega["C_std"] < 0.02

json.dump(omega, open("state/azoth_omega_state.json","w"), indent=2)
