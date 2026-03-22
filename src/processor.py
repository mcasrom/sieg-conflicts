import json, os
import pandas as pd
from collections import defaultdict
from datetime import datetime
from utils import detect_country

IN="../data/raw/news.json"
OUT="../data/processed/conflicts.csv"
HIST="../data/processed/history.csv"

K={
 "alta":["war","missile","airstrike"],
 "media":["conflict","attack","troops"],
 "baja":["tension","sanctions"]
}

def score(t):
    t=t.lower()
    s=0
    for w in K["alta"]:
        if w in t: s+=3
    for w in K["media"]:
        if w in t: s+=2
    for w in K["baja"]:
        if w in t: s+=1
    return s

def lvl(v):
    return "ALTA" if v>2.5 else "MEDIA" if v>1.5 else "BAJA"

if not os.path.exists(IN):
    exit()

with open(IN) as f:
    d=json.load(f)

agg=defaultdict(list)

for a in d["articles"]:
    txt=a["title"]+" "+a["summary"]
    s=score(txt)
    if s==0: continue
    c=detect_country(txt)
    agg[c].append(s)

now=datetime.utcnow().strftime("%Y-%m-%d %H:%M")

rows=[]
for c,v in agg.items():
    avg=sum(v)/len(v)
    rows.append({
        "timestamp":now,
        "pais":c,
        "score":avg,
        "intensidad":lvl(avg),
        "menciones":len(v)
    })

df=pd.DataFrame(rows)
df.to_csv(OUT,index=False)

if os.path.exists(HIST):
    h=pd.read_csv(HIST)
    h=pd.concat([h,df]).tail(500)
else:
    h=df

h.to_csv(HIST,index=False)
print("[+] OK")
