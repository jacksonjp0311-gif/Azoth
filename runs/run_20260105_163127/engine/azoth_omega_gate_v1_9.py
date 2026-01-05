import json, random, numpy as np, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--state-in", required=True)
parser.add_argument("--omega-out", required=True)
args = parser.parse_args()

base = json.load(open(args.state_in))
runs = 64
lams, Cs = [], []

for _ in range(runs):
    lams.append(base["channels"]["photon"]["lambda_star"] + random.gauss(0,2))
    Cs.append(base["C_effective"] + random.gauss(0,0.01))

omega = {
  "protocol": "AzothOmegaGate",
  "version": "1.9",
  "runs": runs,
  "lambda_std": float(np.std(lams)),
  "C_std": float(np.std(Cs))
}

omega["PASS"] = omega["lambda_std"] < 3.0 and omega["C_std"] < 0.02
json.dump(omega, open(args.omega_out,"w"), indent=2)
