import re, json, requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(name)

API yaha lagani hai (number ki jagah {number} rehne dena)

API_URL = "https://osint-apis-hub.onrender.com/api/num-info?key=1MonthFree&q={number}"

OWNER = "Monu Network"
NETWORK = "Monu Network"
TG = "https://t.me/MonuCyberLab"

HTML = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>{{ owner }}</title><style>  
*{box-sizing:border-box;margin:0;padding:0}  
html,body{height:100%;overflow:hidden;background:#000;font-family:'Courier New',monospace}  
canvas{position:fixed;inset:0;z-index:0}  
.scan{position:fixed;inset:0;z-index:2;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 1px,transparent 1px 3px)}  
.w{position:relative;z-index:1;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:16px;gap:14px}  
h1{color:#00ff41;font-size:30px;text-align:center;letter-spacing:2px;text-shadow:0 0 10px #00ff41,0 0 28px #00ff41;animation:fl 3s infinite}  
@keyframes fl{0%,90%,100%{opacity:1}93%{opacity:.35}96%{opacity:1}}  
.nw{color:#00ff41;opacity:.8;letter-spacing:6px;font-size:13px;text-transform:uppercase}  
.c{width:100%;max-width:520px;background:rgba(0,18,0,.88);border:1px solid #00ff41;border-radius:12px;box-shadow:0 0 25px rgba(0,255,65,.4);overflow:hidden}  
.bar{display:flex;align-items:center;gap:6px;padding:8px 12px;background:rgba(0,255,65,.1);border-bottom:1px solid #00ff41;color:#00ff41;font-size:12px}  
.dot{width:9px;height:9px;border-radius:50%}  
.in{padding:14px}  
.r{display:flex;gap:8px}  
input{flex:1;min-width:0;background:#000;color:#00ff41;border:1px solid #00ff41;border-radius:8px;padding:12px;font-size:16px;outline:none;font-family:inherit}  
input::placeholder{color:#0a7a22}  
button{background:#00ff41;color:#000;border:0;border-radius:8px;padding:12px 16px;font-weight:bold;font-family:inherit;box-shadow:0 0 12px #00ff41}  
#res{margin-top:12px;height:220px;overflow-y:auto;background:#000;color:#00ff41;border:1px dashed #0a7a22;border-radius:8px;padding:10px;font-size:14px;white-space:pre-wrap;word-break:break-word}  
#res::-webkit-scrollbar{width:6px}  
#res::-webkit-scrollbar-thumb{background:#00ff41;border-radius:3px}  
.t{display:block;text-align:center;text-decoration:none;color:#fff;padding:13px;border-radius:10px;font-weight:bold;width:100%;max-width:520px;text-shadow:0 0 6px #000;background:linear-gradient(90deg,#8b0000,#ff0000,#8b0000);background-size:200% 100%;animation:sh 3s linear infinite,pu 1.6s ease-in-out infinite}  
@keyframes sh{to{background-position:200% 0}}  
@keyframes pu{0%,100%{box-shadow:0 0 10px #f00}50%{box-shadow:0 0 26px #f00}}  
</style></head><body><canvas id="m"></canvas><div class="scan"></div>  
<div class="w"><h1>&#9889; {{ owner }} &#9889;</h1>  
<div class="nw">{{ network }}</div>  
<div class="c"><div class="bar"><span class="dot" style="background:#f33"></span><span class="dot" style="background:#fc3"></span><span class="dot" style="background:#00ff41"></span>&nbsp;root@monu-network:~#</div>  
<div class="in"><div class="r"><input id="n" type="tel" placeholder="Number dalo..."><button onclick="s()">SEARCH</button></div>  
<div id="res">// Result yaha dikhega...</div></div></div>  
<a class="t" href="{{ tg }}" target="_blank">&#128226; Telegram Channel Join Karo</a></div>  
<script>  
const c=document.getElementById('m'),x=c.getContext('2d');  
function rs(){c.width=innerWidth;c.height=innerHeight}rs();  
let d=[];function id(){d=Array(Math.ceil(c.width/16)).fill(0).map(()=>Math.random()*c.height/16)}id();  
addEventListener('resize',()=>{rs();id()});  
setInterval(()=>{x.fillStyle='rgba(0,0,0,.08)';x.fillRect(0,0,c.width,c.height);x.fillStyle='#00ff41';x.font='16px monospace';  
for(let i=0;i<d.length;i++){x.fillText(Math.floor(Math.random()*10),i*16,d[i]*16);if(d[i]*16>c.height&&Math.random()>.975)d[i]=0;d[i]++}},40);  
async function s(){const b=document.getElementById('res'),v=document.getElementById('n').value.trim();  
if(!v){b.textContent='[!] Pehle number dalo';return}b.textContent='[*] Searching...';  
try{const r=await fetch('/lookup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({number:v})});  
const j=await r.json();b.textContent=j.error?'[!] '+j.error:j.result}catch(e){b.textContent='[!] Server error'}}  
</script></body></html>"""  @app.route("/")
def home():
return render_template_string(HTML, owner=OWNER, network=NETWORK, tg=TG)

@app.route("/fake-api")
def fake_api():
return jsonify({
"status": "demo",
"number": request.args.get("number", ""),
"name": "Demo User",
"carrier": "Demo Telecom",
"country": "India",
"note": "Yeh sirf nakli test data hai",
})

@app.route("/lookup", methods=["POST"])
def lookup():
n = (request.get_json(silent=True) or {}).get("number", "")
n = re.sub(r"[\s-+]", "", n)
if not re.fullmatch(r"\d{7,15}", n):
return jsonify(error="Sahi number dalo")
try:
r = requests.get(API_URL.replace("{number}", n), timeout=15)
try:
t = json.dumps(r.json(), indent=2, ensure_ascii=False)
except ValueError:
t = r.text
return jsonify(result=t)
except requests.RequestException:
return jsonify(error="API se connect nahi ho paya")

app.run(host="0.0.0.0", port=5000)
