import numpy as np, json, hashlib
from datetime import datetime, timezone
from pathlib import Path
import argparse

def channel(lam, c, w, n):
    F = np.exp(-0.5*((lam-c)/w)**2)
    T = np.exp(-0.001*(lam-c)**2)
    score = (F*T)/(0.1+n*(lam-c)**2)
    idx = int(np.argmax(score))
    return float(lam[idx]), float(score[idx])

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output JSON path (run-scoped)")
    ap.add_argument("--window", type=int, default=5, help="Window size encoded into regime identity")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lam = np.linspace(300, 800, 1200)

    raw = {
      "photon": channel(lam,550,90,0.0015),
      "vibration": channel(lam,420,70,0.002),
      "chemical": channel(lam,620,110,0.001)
    }

    scores = np.array([v[1] for v in raw.values()], dtype=np.float64)
    norm = (scores - scores.min()) / (scores.max() - scores.min() + 1e-12)

    channels = {}
    for i,(k,v) in enumerate(raw.items()):
        channels[k] = {
            "lambda_star": v[0],
            "score_raw": float(v[1]),
            "score_norm": float(norm[i])
        }

    E = float(np.mean(scores))          # energy-like magnitude (raw)
    I = float(np.mean(norm))            # information-like magnitude (normalized mean)
    dphi = float(abs(I - 0.70))         # ΔΦ proxy vs H7 horizon target
    C = float((E * I) / (1.0 + abs(dphi)))

    state = {
      "protocol": "AzothUniversalSensoryOptima",
      "version": "2.5",
      "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
      "H7": 0.70,
      "window_size": int(args.window),
      "triad": {"E":E,"I":I,"C":C},
      "dphi_proxy": dphi,
      "channels": channels
    }

    # Regime identity must encode kernel+window; NOT just the channel names.
    regime_material = (
        "AZOTH|2.5|"
        f"WINDOW={int(args.window)}|"
        "LAM=300..800|N=1200|"
        "PHOTON(550,90,0.0015)|"
        "VIB(420,70,0.002)|"
        "CHEM(620,110,0.001)"
    )
    state["regime_hash"] = sha256_hex(regime_material.encode("utf-8"))
    state["regime_material"] = regime_material

    raw_bytes = json.dumps(state, sort_keys=True).encode("utf-8")
    state["sha256"] = sha256_hex(raw_bytes)
    state["bytes"]  = len(raw_bytes)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    main()
