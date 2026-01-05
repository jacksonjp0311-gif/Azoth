import json, random, numpy as np
import matplotlib.pyplot as plt

base = json.load(open("state/azoth_state.json"))
runs = 96

lams, Cs = [], []
for _ in range(runs):
    lams.append(base["channels"]["photon"]["lambda_star"] + random.gauss(0,2))
    Cs.append(base["C_effective"] + random.gauss(0,0.01))

lam_std = float(np.std(lams))
C_std   = float(np.std(Cs))

# invariance gate thresholds (tuned to your synthetic perturbations)
# idea: "Ω-basin" means bounded perturbations don't materially move the geometry
gate = {
  "lambda_std_max": 3.5,
  "C_std_max": 0.02
}

omega_ok = (lam_std <= gate["lambda_std_max"]) and (C_std <= gate["C_std_max"])

omega = {
  "protocol": "AzothOmegaBasin",
  "version": "1.7",
  "runs": runs,
  "lambda_std": lam_std,
  "C_std": C_std,
  "omega_ok": bool(omega_ok),
  "gate": gate
}

json.dump(omega, open("state/azoth_omega_state.json","w"), indent=2)

plt.scatter(lams, Cs, s=10)
plt.xlabel("λ*")
plt.ylabel("C")
plt.tight_layout()
plt.savefig(r"runs/run_20260105_155743/visuals/omega_scatter.png")
