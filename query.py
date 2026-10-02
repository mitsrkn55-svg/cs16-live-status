import socket, struct, json, time
HOST="95.173.173.13"; PORT=27015; TIMEOUT=4
def cstr(d,p):
    e=d.find(b"\0",p)
    if e<0: raise ValueError("bad response")
    return d[p:e].decode("utf-8","replace"),e+1
def query():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.settimeout(TIMEOUT); t=time.time()
        s.sendto(b"\xff\xff\xff\xffTSource Engine Query\0",(HOST,PORT))
        d,_=s.recvfrom(8192)
    ping=round((time.time()-t)*1000)
    if d[:4]!=b"\xff\xff\xff\xff": raise ValueError("bad header")
    typ=d[4:5]; p=5
    if typ not in (b"I",b"m"): raise ValueError("unsupported response "+repr(typ))
    p+=1
    name,p=cstr(d,p); mp,p=cstr(d,p); folder,p=cstr(d,p); game,p=cstr(d,p)
    if typ==b"I": p+=2
    players,maxp,bots=d[p],d[p+1],d[p+2]
    return {"online":True,"name":name,"map":mp,"players":players,"max_players":maxp,"bots":bots,"ping":ping,"checked_at":int(time.time())}
try: out=query()
except Exception as e: out={"online":False,"name":"","map":"","players":0,"max_players":32,"bots":0,"ping":None,"error":str(e),"checked_at":int(time.time())}
open("status.json","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(out,ensure_ascii=False))
