"""Rigenera data.json dai JSON ufficiali FIPAV (calendario e classifica del girone H).
Uso: python3 scripts/gen.py cal.json cla.json data.json
Scrive solo se i dati sono cambiati (campo "firma")."""
import json, sys, datetime, hashlib
KEYS=[("ARZANO","us"),("ANGUILLARA","ang"),("MATESE","faam"),("FRIENDS","fri"),("POOLSTARS","pool"),("LUISS","luiss"),("GREEN","green"),
      ("BIZZAGLIA","biz"),("TERRACINA","ter"),("C.V.R","cvr"),("OPLONTI","opl"),("CARBONE","car"),("VOLLEYRO","vro"),("APRILIA","apr")]
def key(n):
    u=str(n).upper()
    for k,v in KEYS:
        if k in u: return v
    raise SystemExit("squadra sconosciuta: "+str(n))
cal=json.load(open(sys.argv[1]))["data"]["matches"]
cla=json.load(open(sys.argv[2]))["data"]["teams"]
assert len(cal)==182 and len(cla)==14, (len(cal),len(cla))
partite={}
for m in cal:
    pa,pb=m.get("pt_a") or [],m.get("pt_b") or []
    partite[str(m["id"])]={"g":int(m["giornata"]),"casa":key(m["team1"]["name"]),"ospite":key(m["team2"]["name"]),
        "data":m["date"],"ora":m["time"],"campo":str(m["stadium-code"]),"giocata":bool(m["played"]),
        "set_casa":int(m.get("team1-setwin") or 0),"set_ospiti":int(m.get("team2-setwin") or 0),
        "parziali":[f"{a}-{b}" for a,b in zip(pa,pb)] if m["played"] else []}
squadre=[{"pos":t["position"],"nome":t["team"]["name"],"pt":t["points"],"g":t["played"],"v":t["won"],"p":t["lost"],
          "sv":t["sets_won"],"sp":t["sets_lost"],"pf":t["points_won"],"ps":t["points_lost"]} for t in sorted(cla,key=lambda t:t["position"])]
firma=hashlib.sha1(json.dumps([partite,squadre],sort_keys=True).encode()).hexdigest()[:16]
from zoneinfo import ZoneInfo
now=datetime.datetime.now(ZoneInfo("Europe/Rome")).isoformat(timespec="seconds")
doc={"aggiornato":now,"firma":firma,"fonte":"https://media.myvolley.net/public/json/2026/B2/F/H/calendario.json","partite":partite,
     "classifica":{"aggiornato":now,"fonte":"https://media.myvolley.net/public/json/2026/B2/F/H/classifica.json","squadre":squadre}}
try:
    old=json.load(open(sys.argv[3]))
except Exception:
    old={}
if old.get("firma")==firma:
    print("Nessuna novità (firma",firma+")"); sys.exit(0)
json.dump(doc,open(sys.argv[3],"w"),ensure_ascii=False)
print(len(partite),"partite,",sum(p["giocata"] for p in partite.values()),"giocate; classifica",len(squadre),"squadre; firma",firma)
arz=sorted([p for p in partite.values() if p["giocata"] and "us" in (p["casa"],p["ospite"])],key=lambda p:p["g"])
if arz: l=arz[-1]; print("Ultima di Arzano: G%d %s-%s %d-%d"%(l["g"],l["casa"],l["ospite"],l["set_casa"],l["set_ospiti"]))
print("Arzano in classifica:",[t["pos"] for t in squadre if "ARZANO" in t["nome"].upper()][0])
