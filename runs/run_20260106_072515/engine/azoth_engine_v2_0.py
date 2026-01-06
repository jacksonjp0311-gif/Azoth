import numpy as np, json, hashlib
from datetime import datetime, timezone

lam = np.linspace(300, 800, 1200)

def channel(lam, c, w, n):
    F = np.exp(-0.5*((lam-c)/w)**2)
    T = np.exp(-0.001*(lam-c)**2)
    score = (F*T)/(0.1+n*(lam-c)**2)
    idx = int(np.argmax(score))
    return float(lam[idx]), float(score[idx])

channels = {
  "photon": channel(lam,550,90,0.0015),
  "vibration": channel(lam,420,70,0.002),
  "chemical": channel(lam,620,110,0.001)
}

ts = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

state = {
  "protocol":"AzothUniversalSensoryOptima",
  "version":"2.0",
  "timestamp":ts,
  "H7":0.70,
  "channels":{},
}

scores=[]
for k,v in channels.items():
    state["channels"][k]={"lambda_star":v[0],"score":v[1]}
    scores.append(v[1])

state["C_effective"]=float(sum(scores)/len(scores))
raw=json.dumps(state,sort_keys=True).encode()
state["sha256"]=hashlib.sha256(raw).hexdigest()
state["bytes"]=len(raw)

json.dump(state,open("azoth_state.json","w"),indent=2)
