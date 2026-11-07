
from flask import Flask, render_template_string, request, redirect
from urllib.parse import quote
import json

app = Flask(__name__)

# رقم واتساب استقبال الطلبات
WHATSAPP = "201213690424"

# أسعار الشحن العادي
NORMAL_DATA = [
    (110,60),(231,115),(341,180),(460,230),
    (510,265),(583,290),(693,350),(814,410),
    (924,530),(1045,580),(1188,600),(1298,640),
    (1419,690),(1529,740),(1650,790),(1771,850),
    (1880,900),(2002,1000),(2233,1100),(2420,1200),
    (3000,1460),(3999,2000),(5000,2400),(5600,2800),
    (6028,3000),(7000,3500),(8000,4000),(9031,4300),
    (10021,4800)
]

NORMAL = [
    {
        "id": str(i),
        "name": f"{g} جوهرة",
        "gems": g,
        "price": p
    }
    for i, (g, p) in enumerate(NORMAL_DATA, 1)
]

# عرض التراكمي - شحنة واحدة
SINGLE = {
    "id": "single",
    "name": "عرض 1270 جوهرة - شحنة واحدة",
    "gems": 1270,
    "price": 240
}

# الشحن المتقطع
LEVELS = [
    {"id":"level_6","level":6,"gems":120,"price":30},
    {"id":"level_10","level":10,"gems":200,"price":40},
    {"id":"level_15","level":15,"gems":200,"price":40},
    {"id":"level_20","level":20,"gems":200,"price":40},
    {"id":"level_25","level":25,"gems":200,"price":40},
    {"id":"level_30","level":30,"gems":350,"price":60}
]

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MARO STORE</title>

<style>
*{box-sizing:border-box;margin:0;padding:0}

body{
 background:#080711;
 color:white;
 font-family:Arial,sans-serif;
}

header{
 padding:20px;
 background:#100c1c;
 display:flex;
 justify-content:space-between;
 border-bottom:1px solid #573477;
}

.logo{
 font-size:24px;
 font-weight:bold;
 color:#c18aff;
 text-shadow:0 0 15px #963dff;
}

.online{
 color:#70ffad;
 font-size:12px;
}

.hero{
 padding:35px 15px;
 text-align:center;
 background:radial-gradient(ellipse,#54227b,#080711 75%);
}

.character{
 font-size:75px;
 filter:drop-shadow(0 0 20px #ad5cff);
}

.hero h1{
 font-size:29px;
 margin:12px;
}

.hero span{color:#c28cff}

.hero p{
 color:#c5b5d4;
 line-height:2;
}

.container{
 max-width:850px;
 margin:auto;
 padding:20px;
}

.title{
 border-right:4px solid #b45bff;
 padding-right:12px;
 margin:25px 0 18px;
}

.tabs{
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:12px;
}

.tab{
 padding:18px 8px;
 border:1px solid #59406e;
 border-radius:13px;
 background:#191326;
 color:white;
 font-size:16px;
 font-weight:bold;
}

.tab.active{
 background:linear-gradient(135deg,#54218a,#26143c);
 border:2px solid #c083ff;
 box-shadow:0 0 15px #a34aff55;
}

.packages{
 display:grid;
 grid-template-columns:repeat(2,1fr);
 gap:12px;
}

.package{
 background:linear-gradient(145deg,#261638,#100d1b);
 border:1px solid #51336d;
 border-radius:15px;
 padding:17px 8px;
 text-align:center;
 cursor:pointer;
}

.package.active{
 border:2px solid #c083ff;
 box-shadow:0 0 18px #a34aff66;
}

.gem{
 font-size:32px;
 margin-bottom:10px;
}

.price{
 color:#d5aaff;
 margin-top:10px;
 font-weight:bold;
}

.note{
 font-size:11px;
 color:#aaa;
 margin-top:7px;
}

.panel{
 background:#191326;
 border:1px solid #422b5a;
 border-radius:15px;
 padding:20px;
 margin-top:25px;
}

label{
 display:block;
 margin:15px 0 8px;
}

input,select{
 width:100%;
 padding:14px;
 background:#0b0911;
 color:white;
 border:1px solid #59406e;
 border-radius:9px;
 font-size:15px;
}

button{cursor:pointer}

.total{
 background:#291a3d;
 padding:14px;
 border-radius:9px;
 margin-top:12px;
 display:flex;
 justify-content:space-between;
}

.total strong{color:#d6baff}

.warning{
 color:#ffc879;
 font-size:12px;
 line-height:2;
 margin-top:15px;
}

.submit{
 width:100%;
 padding:16px;
 margin-top:20px;
 border:0;
 border-radius:10px;
 background:linear-gradient(90deg,#7527d7,#bb65ff);
 color:white;
 font-size:17px;
 font-weight:bold;
}

.hidden{display:none}

.level{
 display:flex;
 align-items:center;
 gap:10px;
 background:#211630;
 padding:14px;
 border:1px solid #49345d;
 border-radius:10px;
 margin-bottom:10px;
}

.level input{
 width:20px;
 height:20px;
 accent-color:#b45bff;
}

.level-info{
 flex:1;
 line-height:1.8;
 font-size:14px;
}

.level-info small{color:#c8a6ff}

.offer{
 background:linear-gradient(135deg,#302044,#15101f);
 border:1px solid #a35bff;
 border-radius:14px;
 padding:18px;
 text-align:center;
 margin-bottom:17px;
}

.offer h3{margin:10px 0}

.offer p{
 color:#c9b5dc;
 line-height:1.8;
}

footer{
 text-align:center;
 padding:25px;
 color:#a89ab8;
}

@media(min-width:600px){
 .packages{grid-template-columns:repeat(3,1fr)}
}
</style>
</head>

<body>

<header>
 <div class="logo">MARO STORE</div>
 <div class="online">● ONLINE</div>
</header>

<section class="hero">
 <div class="character">🎮💎</div>
 <h1>WELCOME TO <span>MARO STORE</span></h1>
 <p>
 اشحن جواهر فري فاير بأفضل الأسعار<br>
 عروض مميزة وخدمة سريعة
 </p>
</section>

<div class="container">

<h2 class="title">اختار نوع الشحن</h2>

<div class="tabs">
 <button class="tab active" id="normalTab"
 onclick="changeMode('normal')">
 💎 شحن عادي
 </button>

 <button class="tab" id="cumulativeTab"
 onclick="changeMode('cumulative')">
 ⚡ شحن تراكمي
 </button>
</div>

<section id="normalSection">
 <h2 class="title">💎 باقات الجواهر</h2>
 <div class="packages" id="normalPackages"></div>
</section>

<section id="cumulativeSection" class="hidden">

 <h2 class="title">⚡ عروض المستويات</h2>

 <div class="offer">
  <div class="gem">💎</div>
  <h3>عرض 1270 جوهرة</h3>
  <p>
  شحن مرة واحدة فقط<br>
  <strong style="color:#d6aaff">240 جنيه</strong>
  </p>

  <button class="submit" type="button"
  onclick="selectSingle()">
  اختيار العرض
  </button>
 </div>

 <h3 class="title">أو اختار الشحن المتقطع</h3>

 <p style="color:#c6b6d6;margin-bottom:15px;font-size:13px">
 اختار المستويات التي تريد شحنها، ويمكنك اختيار أكثر من مستوى.
 </p>

 <div id="levels"></div>

</section>

<div class="panel">

 <h2 class="title">🎮 بيانات الشحن</h2>

 <form action="/order" method="POST"
 onsubmit="return validate()">

 <input type="hidden" name="mode" id="mode" value="normal">
 <input type="hidden" name="items" id="items">

 <label>Player ID</label>
 <input name="player_id" id="playerId"
 inputmode="numeric"
 placeholder="اكتب ID اللاعب" required>

 <label>اسم اللاعب (اختياري)</label>
 <input name="player_name"
 placeholder="اسم اللاعب">

 <label>طريقة الدفع</label>
 <select name="payment">
  <option>Orange Cash</option>
  <option>Vodafone Cash</option>
  <option>Instapay</option>
 </select>

 <label>رقم مرجع التحويل (اختياري)</label>
 <input name="transfer" placeholder="رقم العملية">

 <div class="total">
  <span>إجمالي الجواهر</span>
  <strong id="gemsTotal">0 💎</strong>
 </div>

 <div class="total">
  <span>الإجمالي</span>
  <strong id="priceTotal">0 جنيه</strong>
 </div>

 <p class="warning">
 ⚠️ لا ترسل كلمة سر المحفظة أو رمز OTP.
 يتم تأكيد الطلب بعد مراجعة التحويل.
 </p>

 <button class="submit" type="submit">
 اطلب الشحن عبر واتساب
 </button>

 </form>
</div>
</div>

<footer>
 <div class="logo">MARO STORE</div>
 شكراً لثقتك في متجرنا ❤️
 <p style="margin-top:10px">للتواصل: 01213690424</p>
</footer>

<script>
const normal = {{ normal|tojson }};
const single = {{ single|tojson }};
const levels = {{ levels|tojson }};

let mode = "normal";
let selectedNormal = null;
let selectedCumulative = null;
let selectedLevels = [];

function renderNormal(){

 document.getElementById("normalPackages").innerHTML =
 normal.map(p => `
 <div class="package" id="normal-${p.id}"
 onclick="selectNormal('${p.id}')">

  <div class="gem">💎</div>
  <h3>${p.gems} جوهرة</h3>
  <div class="price">${p.price} جنيه</div>
  <div class="note">FREE FIRE</div>

 </div>
 `).join("");

}

function renderLevels(){

 document.getElementById("levels").innerHTML =
 levels.map(p => `
 <label class="level">

  <input type="checkbox" value="${p.id}"
   onchange="toggleLevel('${p.id}')">

  <div class="level-info">
   <strong>المستوى ${p.level}</strong><br>
   ${p.gems} 💎
   <small> — ${p.price} جنيه</small>
  </div>

 </label>
 `).join("");

}

function changeMode(m){

 mode=m;

 document.getElementById("mode").value=m;

 document.getElementById("normalSection").classList.toggle(
  "hidden",m!=="normal");

 document.getElementById("cumulativeSection").classList.toggle(
  "hidden",m!=="cumulative");

 document.getElementById("normalTab").classList.toggle(
  "active",m==="normal");

 document.getElementById("cumulativeTab").classList.toggle(
  "active",m==="cumulative");

 updateTotal();
}

function selectNormal(id){

 selectedNormal=id;

 document.querySelectorAll("#normalPackages .package")
 .forEach(x=>x.classList.remove("active"));

 document.getElementById("normal-"+id).classList.add("active");

 updateTotal();
}

function selectSingle(){

 selectedCumulative="single";
 selectedLevels=[];

 document.querySelectorAll("#levels input")
 .forEach(x=>x.checked=false);

 updateTotal();

 alert("تم اختيار عرض 1270 جوهرة بسعر 240 جنيه");
}

function toggleLevel(id){

 selectedCumulative=null;

 const checkbox=document.querySelector(
  '#levels input[value="'+id+'"]');

 if(checkbox.checked){

  if(!selectedLevels.includes(id))
   selectedLevels.push(id);

 }else{

  selectedLevels=selectedLevels.filter(x=>x!==id);

 }

 updateTotal();
}

function updateTotal(){

 let gems=0,price=0,items=[];

 if(mode==="normal"){

  const p=normal.find(x=>x.id===selectedNormal);

  if(p){
   gems=p.gems;
   price=p.price;
   items=[p.id];
  }

 }else{

  if(selectedCumulative==="single"){

   gems=single.gems;
   price=single.price;
   items=["single"];

  }else{

   levels.filter(p=>selectedLevels.includes(p.id))
   .forEach(p=>{
    gems+=p.gems;
    price+=p.price;
    items.push(p.id);
   });

  }

 }

 document.getElementById("gemsTotal").textContent=
 gems+" 💎";

 document.getElementById("priceTotal").textContent=
 price+" جنيه";

 document.getElementById("items").value=
 JSON.stringify(items);

}

function validate(){

 const id=document.getElementById("playerId").value.trim();

 const items=document.getElementById("items").value;

 if(!/^\\d{5,20}$/.test(id)){
  alert("اكتب Player ID صحيح");
  return false;
 }

 if(!items || JSON.parse(items).length===0){
  alert("اختار باقة أو عرض الأول");
  return false;
 }

 return true;
}

renderNormal();
renderLevels();

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        normal=NORMAL,
        single=SINGLE,
        levels=LEVELS
    )

@app.route("/order", methods=["POST"])
def order():

    mode = request.form.get("mode")
    player_id = request.form.get("player_id", "").strip()
    player_name = request.form.get("player_name", "").strip()
    payment = request.form.get("payment", "")
    transfer = request.form.get("transfer", "").strip()

    if not player_id.isdigit() or not 5 <= len(player_id) <= 20:
        return "Player ID غير صحيح", 400

    try:
        ids = json.loads(request.form.get("items", "[]"))
    except (ValueError, TypeError):
        return "اختيار غير صحيح", 400

    if not isinstance(ids, list) or not ids or len(ids) != len(set(ids)):
        return "اختار باقة صحيحة", 400

    chosen = []

    if mode == "normal":

        for item_id in ids:

            p = next((x for x in NORMAL if x["id"] == item_id), None)

            if not p:
                return "باقة غير صحيحة", 400

            chosen.append(p)

    elif mode == "cumulative":

        if ids == ["single"]:

            chosen = [SINGLE]

        else:

            for item_id in ids:

                p = next((x for x in LEVELS if x["id"] == item_id), None)

                if not p:
                    return "مستوى غير صحيح", 400

                chosen.append(p)

    else:
        return "نوع شحن غير صحيح", 400

    gems = sum(x["gems"] for x in chosen)
    total = sum(x["price"] for x in chosen)

    details = "\n".join(
        f"- {x['name'] if 'name' in x else 'المستوى ' + str(x['level'])}: "
        f"{x['gems']} جوهرة / {x['price']} جنيه"
        for x in chosen
    )

    message = f"""
🔥 طلب جديد - MARO STORE

نوع الشحن: {"عادي" if mode == "normal" else "تراكمي"}

الباقات:
{details}

إجمالي الجواهر: {gems}
إجمالي السعر: {total} جنيه

Player ID: {player_id}
اسم اللاعب: {player_name or "غير محدد"}
طريقة الدفع: {payment}
مرجع التحويل: {transfer or "غير موجود"}

الطلب في انتظار مراجعة الدفع.
"""

    url = "https://wa.me/" + WHATSAPP + "?text=" + quote(message)

    return redirect(url)


if __name__ == "__main__":
    print("MARO STORE IS RUNNING")
    app.run(host="127.0.0.1", port=5000, debug=False)
