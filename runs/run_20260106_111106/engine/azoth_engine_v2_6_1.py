import numpy as np, json, hashlib, argparse
from datetime import datetime, timezone
from pathlib import Path

def channel(lam,c,w,n):
    F=np.exp(-0.5*((lam-c)/w)**2)
    T=np.exp(-0.001*(lam-c)**2)
    s=(F*T)/(0.1+n*(lam-c)**2)
    i=int(np.argmax(s))
    return float(lam[i]),float(s[i])

def sha(b): return hashlib.sha256(b).hexdigest()

ap=argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--window", type=int, required=True)
args=ap.parse_args()

lam=np.linspace(300,800,1200)
raw={
 "photon":channel(lam,550,90,0.0015),
 "vibration":channel(lam,420,70,0.002),
 "chemical":channel(lam,620,110,0.001)
}

scores=np.array([v[1] for v in raw.values()])
norm=(scores-scores.min())/(scores.max()-scores.min()+1e-12)

E=float(scores.mean())
I=float(norm.mean())
dphi=abs(I-0.70)
C=(E*I)/(1.0+abs(dphi))

state={
 "protocol":"AzothUniversalSensoryOptima",
 "version":"2.6.1",
 "timestamp":datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
 "H7":0.70,
 "window_size":args.window,
 "triad":{"E":E,"I":I,"C":C},
 "dphi_proxy":dphi,
 "channels":{k:{"lambda_star":v[0],"score_raw":v[1],"score_norm":float(norm[i])}
             for i,(k,v) in enumerate(raw.items())}
}

material=f"AZOTH|2.6.1|WINDOW={args.window}|LAM=300..800|N=1200"
state["regime_material"]=material
state["regime_hash"]=sha(material.encode())

b=json.dumps(state,sort_keys=True).encode()
state["sha256"]=sha(b)

out=Path(args.out)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(state,indent=2),encoding="utf-8")
