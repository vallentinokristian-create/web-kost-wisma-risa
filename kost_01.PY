"""Wisma Risa — website kos sederhana dengan Python standard library.

Jalankan: python app.py
Lalu buka: http://127.0.0.1:8000
Tidak perlu memasang paket pihak ketiga.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from html import escape
from urllib.parse import quote
import json
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))

# Lengkapi data ini sebelum situs dibagikan.
BUSINESS = {
    "name": "Wisma Risa",
    "address": "[Alamat lengkap belum tersedia]",
    "city": "[Kota belum tersedia]",
    "phone": "[Nomor telepon belum tersedia]",
    "whatsapp": "",  # Contoh format: 6281234567890
    "hours": "[Jam layanan belum tersedia]",
    "map_url": "",
    "story": (
        "Wisma Risa hadir sebagai tempat tinggal yang nyaman untuk menemani "
        "hari-hari Anda. Kami percaya, tempat pulang yang baik membuat setiap "
        "langkah terasa lebih ringan."
    ),
}

ROOMS = [
    {
        "name": "Kamar Standard",
        "type": "Standard",
        "price": None,
        "area": "[Luas kamar belum tersedia]",
        "available": None,
        "facilities": [],
        "featured": True,
        "photos": [
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=1100&q=82",
            "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=1100&q=82",
        ],
    },
    {
        "name": "Kamar Comfort",
        "type": "Comfort",
        "price": None,
        "area": "[Luas kamar belum tersedia]",
        "available": None,
        "facilities": [],
        "featured": True,
        "photos": [
            "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=1100&q=82",
            "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=1100&q=82",
        ],
    },
    {
        "name": "Kamar Deluxe",
        "type": "Deluxe",
        "price": None,
        "area": "[Luas kamar belum tersedia]",
        "available": None,
        "facilities": [],
        "featured": False,
        "photos": [
            "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1100&q=82",
            "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=1100&q=82",
        ],
    },
]

FACILITIES = [
    ("Wi-Fi", "Konfirmasi ketersediaan kepada pengelola."),
    ("Kamar mandi", "Konfirmasi tipe kamar mandi kepada pengelola."),
    ("Area parkir", "Konfirmasi ketersediaan kepada pengelola."),
    ("Dapur bersama", "Konfirmasi ketersediaan kepada pengelola."),
    ("Keamanan", "Konfirmasi sistem keamanan kepada pengelola."),
    ("Area bersama", "Konfirmasi ketersediaan kepada pengelola."),
]

TESTIMONIALS = [
    {"quote": "[Kutipan testimoni penghuni belum tersedia.]", "name": "[Nama penghuni]"},
    {"quote": "[Kutipan testimoni penghuni belum tersedia.]", "name": "[Nama penghuni]"},
]

RULES = ["[Aturan kos belum tersedia. Minta informasi terbaru kepada pengelola.]"]
EXTRA_COSTS = "[Biaya listrik, deposit, dan biaya tambahan belum tersedia.]"


def safe(value):
    """Escape data sebelum dimasukkan ke dalam HTML."""
    return escape(str(value), quote=True)


def contact_url(message):
    number = "".join(char for char in BUSINESS["whatsapp"] if char.isdigit())
    if number:
        return "https://wa.me/{}?text={}".format(number, quote(message))
    return "mailto:?subject={}&body={}".format(
        quote("Informasi Wisma Risa"), quote(message)
    )


def make_page():
    rooms_json = json.dumps(ROOMS, ensure_ascii=False).replace("</", "<\\/")
    facilities_html = "".join(
        '<article class="facility"><span class="check">?</span><div><b>{}</b>'
        '<small>{}</small></div><span class="pending">Konfirmasi</span></article>'.format(
            safe(name), safe(description)
        )
        for name, description in FACILITIES
    )
    testimonials_html = "".join(
        '<article class="quote"><p>{}</p><small>{}</small></article>'.format(
            safe(item["quote"]), safe(item["name"])
        )
        for item in TESTIMONIALS
    )
    rules_html = "".join("<li>{}</li>".format(safe(rule)) for rule in RULES)
    chat_link = safe(contact_url("Halo, saya ingin bertanya tentang Wisma Risa."))
    address = safe(BUSINESS["address"])
    phone = safe(BUSINESS["phone"])
    hours = safe(BUSINESS["hours"])
    map_link = BUSINESS["map_url"]

    map_action = (
        '<a class="link" href="{}" target="_blank" rel="noreferrer">Buka peta ↗</a>'.format(
            safe(map_link)
        )
        if map_link
        else '<span class="muted">Tautan peta ditambahkan setelah alamat dikonfirmasi.</span>'
    )

    page = r"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f8f7f3">
<meta name="description" content="Temukan pilihan kamar di Wisma Risa. Lihat kamar, fasilitas, lokasi, dan tanyakan informasi kepada pengelola.">
<title>Wisma Risa — Hunian Nyaman, Berasa di Rumah</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#28352c;--green:#304839;--sage:#77866a;--cream:#f8f7f3;--line:#e6e5dc;--muted:#777b72;--serif:'Playfair Display',Georgia,serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:75px}
body{margin:0;background:var(--cream);color:var(--ink);font-family:'DM Sans',Arial,sans-serif}
a{color:inherit;text-decoration:none}
button,select,input,textarea{font:inherit}
.top{height:74px;padding:0 7%;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:#f8f7f3ee;backdrop-filter:blur(12px);z-index:4;border-bottom:1px solid #e6e5dc}
.brand{font-size:13px;letter-spacing:.13em}
.brand-mark{display:inline-grid;place-items:center;background:var(--green);color:white;border-radius:50%;width:32px;height:32px;margin-right:9px}
.nav{display:flex;gap:30px;font-size:12px;color:#61665e}
.nav a:hover,.link:hover{color:var(--sage)}
.button{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:13px 18px;background:var(--green);border:1px solid var(--green);color:white;font-size:11px;font-weight:600;cursor:pointer}
.button:hover{background:#49614e}
.button.outline{background:transparent;color:var(--ink);border-color:#d8d9d0}
.menu{display:none;background:none;border:0;font-size:22px}
.hero{padding:48px 7% 60px;display:grid;grid-template-columns:.9fr 1.1fr;gap:7%;align-items:center}
.eyebrow{font-size:9px;font-weight:700;letter-spacing:.19em;color:#79816e}
.hero h1,.heading{font-family:var(--serif);font-weight:500;letter-spacing:-.035em}
.hero h1{font-size:clamp(45px,5.5vw,72px);line-height:1.1;margin:18px 0}
.hero em,.heading em{color:#7b896c}
.hero p{font-size:13px;line-height:1.8;color:var(--muted);max-width:370px}
.actions{display:flex;gap:10px;margin-top:24px}
.hero-photo{height:420px;position:relative}
.hero-photo img{width:100%;height:100%;object-fit:cover}
.photo-note{position:absolute;bottom:16px;right:14px;background:#fff;padding:10px 12px;font-size:9px}
.highlights{padding:19px 7%;display:grid;grid-template-columns:repeat(3,1fr);border-block:1px solid var(--line);font-size:11px}
.highlights div{padding:6px 15px;border-right:1px solid var(--line)}
.highlights div:last-child{border:0}
.highlights b,.highlights small{display:block}
.highlights small{font-size:9px;color:var(--muted);margin-top:4px}
.section{padding:85px 9%}
.heading{font-size:42px;line-height:1.18;margin:12px 0}
.intro{font-size:12px;line-height:1.8;color:var(--muted);max-width:390px}
.filters{display:flex;gap:10px;margin:24px 0 18px}
.filters select{padding:10px 13px;border:1px solid var(--line);background:white;font-size:10px;color:#565b53}
.room-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.room{background:white;border:1px solid #eeede7}
.room-photo{position:relative;height:220px;overflow:hidden}
.room-photo img{width:100%;height:100%;object-fit:cover}
.badge{position:absolute;left:12px;top:12px;padding:6px 8px;background:#fff;font-size:8px;letter-spacing:.08em}
.status{position:absolute;right:10px;bottom:10px;background:#fff;padding:7px 9px;font-size:9px}
.room-info{padding:17px}
.type{font-size:8px;letter-spacing:.13em;color:#85877f}
.room h3{font:500 22px var(--serif);margin:9px 0}
.meta{font-size:9px;color:var(--muted);min-height:25px}
.room-bottom{border-top:1px solid var(--line);padding-top:12px;margin-top:11px;display:flex;justify-content:space-between;align-items:center}
.room-bottom b{font-size:12px}
.detail{border:1px solid var(--line);background:#fff;border-radius:50%;width:33px;height:33px;cursor:pointer}
.split{background:var(--green);color:#fff;padding:72px 9%;display:grid;grid-template-columns:.8fr 1.2fr;gap:9%}
.split .heading{font-size:39px}
.split p{color:#c7cec3;font-size:11px;line-height:1.8}
.facility{display:grid;grid-template-columns:33px 1fr auto;gap:10px;align-items:center;padding:15px 0;border-bottom:1px solid #ffffff30;font-size:11px}
.facility:first-child{border-top:1px solid #ffffff30}
.facility small{display:block;color:#c7cec3;font-size:9px;margin-top:4px}
.check{border:1px solid #ffffff55;border-radius:50%;width:30px;height:30px;display:grid;place-items:center;color:#c4d0b6}
.pending{font-size:8px;color:#e0cf9e}
.reviews{background:#f1f0e9}
.review-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:25px}
.quote{background:white;padding:22px;font-size:12px;line-height:1.8}
.quote small{color:var(--muted)}
.location{display:grid;grid-template-columns:1fr 1fr;gap:8%;align-items:center}
.location-image img{width:100%;height:330px;object-fit:cover}
.location p{font-size:12px;line-height:1.8}
.link{font-size:11px;text-decoration:underline}
.muted{font-size:10px;color:var(--muted)}
.contact{background:var(--green);color:white;padding:75px 9%;display:grid;grid-template-columns:1fr .8fr;gap:8%}
.contact .intro{color:#c7cec3}
.contact-info{display:grid;gap:15px;margin-top:30px;font-size:11px}
.contact-info small{display:block;color:#c7cec3;margin-bottom:5px}
.form{background:white;color:var(--ink);padding:25px;display:grid;gap:10px}
.form h3{font:500 23px var(--serif);margin:0 0 8px}
.form label{font-size:10px}
.form input,.form textarea{padding:11px;border:1px solid var(--line);width:100%;font-size:11px}
.form-note{color:var(--muted);font-size:9px;line-height:1.6}
.footer{padding:25px 7%;display:flex;justify-content:space-between;gap:15px;font-size:10px;color:var(--muted)}
.chat{position:fixed;right:20px;bottom:18px;z-index:5;background:var(--green);color:white;padding:13px 17px;font-size:10px}
.modal-bg{display:none;position:fixed;inset:0;background:#101710aa;z-index:8;padding:4vh 5%;overflow:auto}
.modal-bg.open{display:grid;place-items:center}
.modal{background:var(--cream);max-width:900px;width:100%;display:grid;grid-template-columns:1.1fr .9fr;position:relative}
.close{position:absolute;right:12px;top:12px;border:0;background:white;padding:9px;cursor:pointer}
.modal-image{width:100%;height:440px;object-fit:cover}
.thumbs{display:flex;gap:7px;padding:8px}
.thumbs button{width:60px;height:50px;padding:0;border:2px solid transparent;background:none;cursor:pointer}
.thumbs button.active{border-color:var(--sage)}
.thumbs img{width:100%;height:100%;object-fit:cover}
.modal-copy{padding:36px;max-height:85vh;overflow:auto}
.modal-copy h2{font:500 32px var(--serif)}
.modal-copy h3{font-size:12px;margin-top:25px}
.modal-copy p,.modal-copy li{font-size:11px;line-height:1.8;color:var(--muted)}
@media(max-width:760px){
 .nav{display:none;position:absolute;left:0;right:0;top:74px;background:var(--cream);padding:20px 7%;flex-direction:column;gap:17px}
 .nav.open{display:flex}.menu{display:block}
 .hero{grid-template-columns:1fr;padding-top:35px}.hero-photo{height:300px}
 .highlights{padding-inline:4%;font-size:9px}.highlights div{padding-inline:8px}
 .section{padding:58px 7%}.heading{font-size:35px}
 .room-grid{grid-template-columns:1fr}.room-photo{height:250px}
 .split,.contact,.location{grid-template-columns:1fr;padding:55px 7%;gap:30px}
 .review-grid{grid-template-columns:1fr}.footer{flex-wrap:wrap}
 .modal{grid-template-columns:1fr}.modal-image{height:260px}.modal-copy{padding:25px}
}
</style>
</head>
<body>
<header class="top">
<a class="brand" href="#"><span class="brand-mark">W</span><b>WISMA RISA</b></a>
<nav class="nav" id="nav">
<a href="#kamar">Pilihan Kamar</a><a href="#fasilitas">Fasilitas</a><a href="#lokasi">Lokasi</a><a href="#tentang">Tentang</a>
</nav>
<button class="menu" id="menu" aria-label="Buka menu">☰</button>
</header>

<main>
<section class="hero">
<div>
<div class="eyebrow">RUANG TINGGAL YANG TERASA SEPERTI RUMAH</div>
<h1>Hunian nyaman,<br><em>berasa di rumah.</em></h1>
<p>Temukan ruang yang pas untuk beristirahat, bertumbuh, dan menjalani hari dengan lebih nyaman.</p>
<div class="actions">
<a class="button" href="#kamar">Lihat pilihan kamar ↓</a>
<a class="button outline" href="#kontak">Hubungi kami</a>
</div>
</div>
<div class="hero-photo">
<img src="https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=1400&q=85" alt="Interior kamar yang nyaman">
<div class="photo-note">Ruang nyaman untuk cerita baru</div>
</div>
</section>

<section class="highlights">
<div><b>Hunian nyaman</b><small>Ruang untuk beristirahat dan beraktivitas</small></div>
<div><b>Pilihan kamar</b><small>Sesuaikan dengan kebutuhan Anda</small></div>
<div><b>Informasi transparan</b><small>Tanyakan detail kepada pengelola</small></div>
</section>

<section class="section" id="kamar">
<div class="eyebrow">PILIHAN KAMAR</div>
<h2 class="heading">Ruang yang pas<br><em>untuk Anda.</em></h2>
<p class="intro">Lihat pilihan kamar dan tanyakan informasi terbaru kepada pengelola.</p>
<div class="filters">
<label><span class="muted">Tipe kamar </span>
<select id="typeFilter"><option value="">Semua tipe</option><option>Standard</option><option>Comfort</option><option>Deluxe</option></select></label>
<label><span class="muted">Fasilitas </span><select id="facilityFilter"><option value="">Semua fasilitas</option></select></label>
</div>
<div id="roomGrid" class="room-grid"></div>
</section>

<section class="split" id="fasilitas">
<div><div class="eyebrow" style="color:#bdc8b1">KENYAMANAN SEHARI-HARI</div>
<h2 class="heading">Hal-hal kecil yang<br>membuat <em>betah.</em></h2>
<p>Fasilitas yang ditampilkan menunggu konfirmasi pengelola. Perbarui data di bagian atas app.py.</p></div>
<div>__FACILITIES__</div>
</section>

<section class="section reviews">
<div class="eyebrow">CERITA DARI PENGHUNI</div>
<h2 class="heading">Rasa nyaman<br><em>dimulai dari sini.</em></h2>
<p class="intro">Testimoni akan ditampilkan setelah tersedia.</p>
<div class="review-grid">__TESTIMONIALS__</div>
</section>

<section class="section location" id="lokasi">
<div class="location-image"><img src="https://images.unsplash.com/photo-1511818966892-d7d671e672a2?auto=format&fit=crop&w=1100&q=82" alt="Foto ilustrasi kawasan, ganti dengan foto sekitar kos"></div>
<div><div class="eyebrow">LOKASI & AKSES</div>
<h2 class="heading">Dekat dengan<br>yang <em>Anda butuhkan.</em></h2>
<p><b>Wisma Risa</b><br>__ADDRESS__</p>
<p class="intro">Akses kampus, kantor, transportasi, dan tempat umum: <b>[Informasi belum tersedia]</b></p>
__MAP_ACTION__</div>
</section>

<section class="section" id="tentang">
<div class="eyebrow">SEDIKIT TENTANG KAMI</div>
<h2 class="heading">Ruang tinggal, dengan<br><em>rasa yang lebih personal.</em></h2>
<p class="intro">__STORY__</p>
</section>

<section class="contact" id="kontak">
<div><div class="eyebrow" style="color:#bdc8b1">SENANG MENDENGAR DARI ANDA</div>
<h2 class="heading">Punya pertanyaan?<br><em>Kami siap membantu.</em></h2>
<p class="intro">Tanya kamar atau informasi lainnya kepada pengelola.</p>
<div class="contact-info">
<div><small>Telepon & WhatsApp</small>__PHONE__</div>
<div><small>Alamat</small>__ADDRESS__</div>
<div><small>Jam layanan</small>__HOURS__</div>
</div></div>

<form class="form" id="contactForm">
<h3>Kirim pertanyaan</h3>
<label for="name">Nama Anda</label><input id="name" name="name" required minlength="2" maxlength="80" placeholder="Nama lengkap">
<label for="email">Email</label><input id="email" type="email" required maxlength="120" placeholder="nama@email.com">
<label for="question">Pertanyaan</label><textarea id="question" required minlength="5" maxlength="1000" rows="3" placeholder="Apa yang ingin Anda ketahui?"></textarea>
<button class="button" type="submit">Siapkan pertanyaan ↗</button>
<small class="form-note">Formulir membuka WhatsApp atau draft email untuk pengelola.</small>
</form>
</section>

<section class="section" style="padding-top:30px;padding-bottom:30px;display:flex;justify-content:space-between;align-items:center;gap:15px">
<span><b>Temukan ruang yang terasa pas.</b><br><small class="muted">Obrolkan kebutuhan Anda dengan pengelola.</small></span>
<a class="button" href="__CHAT__">Tanya via WhatsApp ↗</a>
</section>
</main>

<footer class="footer"><b>WISMA RISA</b><span>Tempat nyaman untuk cerita baru.</span><span>© Wisma Risa</span></footer>
<a class="chat" href="__CHAT__">Tanya kami · WhatsApp</a>

<div class="modal-bg" id="modal" role="presentation">
<section class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
<button class="close" id="closeModal" aria-label="Tutup">✕</button>
<div><img class="modal-image" id="modalImage" alt="Foto kamar"><div class="thumbs" id="thumbs"></div></div>
<div class="modal-copy">
<div class="eyebrow">WISMA RISA</div><h2 id="modalTitle"></h2><b id="modalPrice"></b>
<p id="modalStatus"></p><p id="modalArea"></p><h3>Fasilitas kamar</h3><p id="modalFacilities"></p>
<h3>Aturan kos</h3><ul>__RULES__</ul><p>__EXTRA_COSTS__</p>
<a class="button" id="modalChat" href="__CHAT__">Tanya tipe kamar ini ↗</a>
</div>
</section>
</div>

<script id="roomData" type="application/json">__ROOMS_JSON__</script>
<script>
const rooms=JSON.parse(document.getElementById('roomData').textContent);
const chatBase=__CHAT_BASE__;
const grid=document.getElementById('roomGrid');
const typeFilter=document.getElementById('typeFilter');
const facilityFilter=document.getElementById('facilityFilter');

const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

function showRooms(){
 const type=typeFilter.value;
 const feature=facilityFilter.value;
 const matches=rooms.filter(r=>(!type||r.type===type)&&(!feature||r.facilities.includes(feature)));
 if(!matches.length){grid.innerHTML='<p class="empty">Belum ada kamar untuk filter ini.</p>';return}
 grid.innerHTML=matches.map(r=>`<article class="room">
 <div class="room-photo"><img loading="lazy" src="${esc(r.photos[0])}" alt="Foto ilustrasi ${esc(r.name)}">
 ${r.featured?'<span class="badge">PILIHAN HUNIAN</span>':''}
 <span class="status">${r.available===true?'Tersedia':r.available===false?'Penuh':'Konfirmasi ketersediaan'}</span></div>
 <div class="room-info"><span class="type">WISMA RISA · ${esc(r.type.toUpperCase())}</span>
 <h3>${esc(r.name)}</h3><div class="meta">${esc(r.area)} · ${r.facilities.length?esc(r.facilities.slice(0,2).join(' · ')):'Fasilitas perlu dikonfirmasi'}</div>
 <div class="room-bottom"><b>${r.price==null?'Tanyakan harga':'Rp'+Number(r.price).toLocaleString('id-ID')+(r.pricePeriod||' / bulan')}</b>
 <button class="detail" data-room="${esc(r.name)}" aria-label="Lihat detail ${esc(r.name)}">↗</button></div></div></article>`).join('');
 grid.querySelectorAll('[data-room]').forEach(b=>b.addEventListener('click',()=>openRoom(rooms.find(r=>r.name===b.dataset.room))))
}

function messageFor(room){
 return `Halo, saya ingin bertanya tentang ${room.name} di Wisma Risa. Apakah bisa mendapat informasi harga dan ketersediaannya?`
}

function contactHref(message){
 return chatBase
  ?`https://wa.me/${chatBase}?text=${encodeURIComponent(message)}`
  :`mailto:?subject=${encodeURIComponent('Informasi Wisma Risa')}&body=${encodeURIComponent(message)}`
}

function openRoom(r){
 if(!r)return;
 document.getElementById('modal').classList.add('open');
 document.getElementById('modalTitle').textContent=r.name;
 document.getElementById('modalPrice').textContent=r.price==null?'Tanyakan harga':'Rp'+Number(r.price).toLocaleString('id-ID')+' / bulan';
 document.getElementById('modalStatus').textContent='Status: '+(r.available===true?'Tersedia':r.available===false?'Penuh':'konfirmasi kepada pengelola');
 document.getElementById('modalArea').textContent='Luas: '+r.area;
 document.getElementById('modalFacilities').textContent=r.facilities.length?r.facilities.join(', '):'[Informasi fasilitas kamar belum tersedia.]';
 document.getElementById('modalImage').src=r.photos[0];
 document.getElementById('thumbs').innerHTML=r.photos.map((url,i)=>`<button class="${i===0?'active':''}" aria-label="Tampilkan foto ${i+1}" data-photo="${esc(url)}"><img src="${esc(url)}" alt=""></button>`).join('');
 document.querySelectorAll('#thumbs button').forEach(b=>b.addEventListener('click',()=>{
  document.getElementById('modalImage').src=b.dataset.photo;
  document.querySelectorAll('#thumbs button').forEach(t=>t.classList.remove('active'));
  b.classList.add('active')
 }));
 document.getElementById('modalChat').href=contactHref(messageFor(r));
 document.getElementById('closeModal').focus()
}

function closeModal(){document.getElementById('modal').classList.remove('open')}

typeFilter.addEventListener('change',showRooms);
facilityFilter.addEventListener('change',showRooms);
document.getElementById('closeModal').addEventListener('click',closeModal);
document.getElementById('modal').addEventListener('click',e=>{if(e.target.id==='modal')closeModal()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});
document.getElementById('menu').addEventListener('click',()=>document.getElementById('nav').classList.toggle('open'));
document.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',()=>document.getElementById('nav').classList.remove('open')));

document.getElementById('contactForm').addEventListener('submit',e=>{
 e.preventDefault();
 if(!e.currentTarget.reportValidity())return;
 const data=new FormData(e.currentTarget);
 const body=`Halo, saya ingin bertanya tentang Wisma Risa.\n\nNama: ${data.get('name')}\nEmail: ${document.getElementById('email').value}\nPertanyaan: ${document.getElementById('question').value}`;
 window.location.href=contactHref(body)
});

showRooms();
</script>
</body>
</html>"""

    return (
        page.replace("__CHAT__", chat_link)
        .replace(
            "__CHAT_BASE__",
            json.dumps("".join(c for c in BUSINESS["whatsapp"] if c.isdigit())),
        )
        .replace("__ADDRESS__", address)
        .replace("__PHONE__", phone)
        .replace("__HOURS__", hours)
        .replace("__FACILITIES__", facilities_html)
        .replace("__TESTIMONIALS__", testimonials_html)
        .replace("__STORY__", safe(BUSINESS["story"]))
        .replace("__RULES__", rules_html)
        .replace("__EXTRA_COSTS__", safe(EXTRA_COSTS))
        .replace("__ROOMS_JSON__", rooms_json)
        .replace("__MAP_ACTION__", map_action)
    )


class WebsiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Browser kadang meminta favicon otomatis. Jawab tanpa mengganggu halaman.
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # Website ini hanya memiliki satu halaman, jadi alamat lain juga diarahkan
        # ke halaman utama agar tidak menampilkan 404.
        page = make_page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(page)

    def log_message(self, fmt, *args):
        print("[Wisma Risa] {} - {}".format(self.address_string(), fmt % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), WebsiteHandler)
    print("Wisma Risa berjalan. Buka http://127.0.0.1:{} di browser (Ctrl+C untuk berhenti).".format(PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
    finally:
        server.server_close()

