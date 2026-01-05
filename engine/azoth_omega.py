import json, random, numpy as np, matplotlib.pyplot as plt

base = json.load(open("state/azoth_state.json"))
runs = 64

lams = []
Cs = []

for i in range(runs):
    lams.append(base["channels"]["photon"]["lambda_star"] + random.gauss(0,2))
    Cs.append(base["C_effective"] + random.gauss(0,0.01))

omega = {
  "protocol": "AzothOmegaBasin",
  "runs": runs,
  "lambda_std": float(np.std(lams)),
  "C_std": float(np.std(Cs))
}

json.dump(omega, open("state/azoth_omega_state.json","w"), indent=2)

plt.scatter(lams, Cs, s=10)
plt.xlabel("λ*")
plt.ylabel("C")
plt.tight_layout()
plt.savefig("visuals/omega_scatter.png")
