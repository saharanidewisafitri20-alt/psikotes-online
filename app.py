#!/usr/bin/env python3
import argparse, csv, html, io, json, os, secrets, sqlite3, urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / "data" / "packages.json"
DB_FILE = BASE / "data" / "results.sqlite3"
ADMIN_PIN = os.environ.get("PSIKOTES_ADMIN_PIN", "123456")
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8000"))

with open(DATA_FILE, encoding="utf-8") as f:
    PACKAGES = json.load(f)

def db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT,
        mode TEXT NOT NULL,
        package_no INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        submitted_at TEXT,
        score_json TEXT,
        answers_json TEXT
    )""")
    conn.commit()
    return conn

def esc(v):
    return html.escape(str(v), quote=True)

def page(title, body, extra_js=""):
    return f"""<!doctype html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Psikotes Online</title>
<style>
:root{{--ink:#122033;--muted:#65758b;--line:#dbe4ee;--brand:#135d8f;--brand2:#0d3b66;--soft:#eef6fb;--good:#107c55;--warn:#b7791f;--danger:#b42318;}}
*{{box-sizing:border-box}} body{{margin:0;background:#f5f8fb;color:var(--ink);font:15px/1.5 Arial,sans-serif}}
a{{color:var(--brand);text-decoration:none}} a:hover{{text-decoration:underline}}
.container{{max-width:1180px;margin:auto;padding:22px 18px}}
.top{{background:linear-gradient(135deg,#103b73,#1779a9 58%,#20a487);color:white;padding:24px 0;box-shadow:0 4px 18px #0d3b661c}}
.top h1{{margin:0;font-size:25px}} .top p{{margin:6px 0 0;color:#d9efff}}
.card{{background:white;border:1px solid var(--line);border-radius:16px;padding:22px;margin:18px 0;box-shadow:0 8px 24px #16324d0b}}
.grid2{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}
.grid3{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}
label{{display:block;font-weight:700;margin:8px 0 6px}} input,select,textarea{{width:100%;border:1px solid #b8c8d7;border-radius:9px;padding:11px;font:inherit;background:#fff}}
button,.btn{{border:0;border-radius:9px;background:var(--brand);color:white;padding:11px 16px;font-weight:700;cursor:pointer;display:inline-block}}
button:hover,.btn:hover{{background:var(--brand2);text-decoration:none}} .btn.secondary{{background:#e7eef5;color:var(--ink)}} .btn.danger{{background:var(--danger)}}
.badge{{display:inline-block;background:#e7f3fb;color:var(--brand2);border-radius:999px;padding:4px 10px;font-size:12px;font-weight:700}}
.muted{{color:var(--muted)}} .notice{{background:#fff8e6;border-left:4px solid #d69e2e;padding:12px 14px;border-radius:8px}}
.tabs{{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}} .tab{{background:#e8f0f6;color:var(--ink);padding:9px 12px;border-radius:999px;border:0;cursor:pointer}} .tab.active{{background:var(--brand);color:#fff}}
.section{{display:none}} .section.active{{display:block}}
.question{{border:1px solid var(--line);border-radius:12px;padding:15px;margin:12px 0;background:#fff}}
.question h3{{font-size:15px;margin:0 0 10px}} .option{{display:flex;gap:9px;align-items:flex-start;margin:8px 0;font-weight:400}}
.option input{{width:auto;margin-top:4px}} .qmeta{{color:var(--muted);font-size:12px;margin-bottom:5px}}
.kgrid{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}} .kcol{{border:1px solid var(--line);border-radius:10px;padding:8px;background:#fbfdff}}
.kcol b{{display:block;text-align:center;color:var(--brand)}} .digit{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px dotted #cbd5df;padding:2px 0;font-size:13px}}
.digit input{{width:34px;padding:3px;text-align:center;font-size:12px}}
.pair{{display:grid;grid-template-columns:1fr 1fr 90px;gap:10px;align-items:center;border-bottom:1px solid #edf1f5;padding:10px 0}}
.pair label{{margin:0;font-weight:400}} .pair input{{width:auto}}
.canvaswrap{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}} canvas{{width:100%;height:180px;border:1px solid #98aabd;border-radius:10px;background:#fff;touch-action:none}}
table{{width:100%;border-collapse:collapse;background:#fff}} th,td{{border:1px solid var(--line);padding:9px;text-align:left;vertical-align:top}} th{{background:#e7f1f8;color:var(--brand2)}} .scroll{{overflow:auto}}
.score{{font-size:24px;color:var(--brand2);font-weight:800}} .ok{{color:var(--good)}} .warn{{color:var(--warn)}} .footer{{padding:28px 0;color:var(--muted);text-align:center;font-size:13px}}
.hero-emoji{{font-size:34px;float:right}}.progress-wrap{{height:10px;background:#e7eef5;border-radius:99px;overflow:hidden;margin:12px 0}}.progress-bar{{height:100%;width:0;background:linear-gradient(90deg,#ffb703,#20a487);transition:width .25s}}.fun-card{{background:linear-gradient(135deg,#fff7df,#e9fbf6);border:0}}.review{{border-left:4px solid #20a487;padding:10px 14px;margin:8px 0;background:#f8fcfc;border-radius:8px}}.review small{{color:var(--muted)}}
@media(max-width:760px){{.grid2,.grid3,.canvaswrap{{grid-template-columns:1fr}}.pair{{grid-template-columns:1fr 1fr 60px}}.kgrid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.top h1{{font-size:20px}}}}
</style></head><body>
<header class="top"><div class="container"><span class="hero-emoji">🎯 ✨</span><h1>Psikotes Online</h1><p>Latihan psikotes umum dan CPNS dengan 30 paket berbeda</p></div></header>
<main class="container">{body}</main>
<footer class="footer">Aplikasi latihan mandiri. Untuk penggunaan resmi, sesuaikan materi dan ambang batas dengan ketentuan terbaru instansi.</footer>
<script>{extra_js}</script></body></html>"""

def clean_item(item, kind):
    out={"text":item["text"],"options":item["options"],"category":item.get("category","")}
    if kind=="tkp":
        out["scores_hint"] = None
    return out

def build_test_body(mode, package_no, attempt_id):
    pack=PACKAGES[mode][package_no-1]
    if mode=="general":
        sections=[
            ("verbal","Tes Kemampuan Verbal",pack["verbal"]),
            ("arithmetic","Logika Aritmatika dan Deret Angka",pack["arithmetic"]),
            ("logical","Penalaran Logis dan Analitik",pack["logical"]),
        ]
    else:
        sections=[
            ("twk","TWK Tes Wawasan Kebangsaan",pack["twk"]),
            ("tiu","TIU Tes Intelegensia Umum",pack["tiu"]),
            ("tkp","TKP Tes Karakteristik Pribadi",pack["tkp"]),
        ]
    tabs=[]; sections_html=[]
    for idx,(key,title,items) in enumerate(sections):
        tabs.append(f'<button class="tab {"active" if idx==0 else ""}" data-target="sec-{key}">{title} <span class="badge">{len(items)}</span></button>')
        qhtml=[]
        for i,item in enumerate(items):
            opts=[]
            for oi,opt in enumerate(item["options"]):
                opts.append(f'<label class="option"><input type="radio" name="{key}_{i}" value="{oi}"> <span><b>{chr(65+oi)}.</b> {esc(opt)}</span></label>')
            qhtml.append(f'<div class="question"><div class="qmeta">{esc(item.get("category",""))} · Soal {i+1}</div><h3>{esc(item["text"])}</h3>{"".join(opts)}</div>')
        if key=="tkp":
            intro="Pilih respons yang paling mencerminkan tindakan Anda. Penilaian TKP menggunakan bobot perilaku; semua pilihan tetap memiliki nilai."
        elif key=="twk":
            intro="Pilih satu jawaban yang paling tepat. Latihan ini berisi 30 soal."
        else:
            intro="Pilih satu jawaban yang paling tepat."
        sections_html.append(f'<section id="sec-{key}" class="section {"active" if idx==0 else ""}"><div class="notice">{intro}</div>{"".join(qhtml)}</section>')
    if mode=="general":
        epps_html=[]
        for i,pair in enumerate(pack["epps"]):
            epps_html.append(f'<div class="pair"><label><input type="radio" name="epps_{i}" value="A"> A. {esc(pair["a"])}</label><label><input type="radio" name="epps_{i}" value="B"> B. {esc(pair["b"])}</label><span class="muted">#{i+1}</span></div>')
        epps_section=f'<section id="sec-epps" class="section"><div class="notice">EPPS berisi 225 pasangan. Pilih pernyataan yang paling menggambarkan diri Anda. Tidak ada jawaban benar atau salah.</div>{"".join(epps_html)}</section>'
        kra_cols=[]
        for c,col in enumerate(pack["kraepelin"]):
            rows=[]
            for r,d in enumerate(col):
                if r==len(col)-1: continue
                rows.append(f'<div class="digit"><span>{d} + {col[r+1]}</span><input name="kra_{c}_{r}" maxlength="1" inputmode="numeric"></div>')
            kra_cols.append(f'<div class="kcol"><b>Kolom {c+1}</b>{"".join(rows)}</div>')
        kra_section=f'<section id="sec-kraepelin" class="section"><div class="notice">Jumlahkan dua angka berurutan dan tulis angka satuannya. Kerjakan sesuai waktu latihan.</div><div class="kgrid">{"".join(kra_cols)}</div></section>'
        canvas_items=[]
        for i in range(8):
            canvas_items.append(f'<div><label>Wartegg Kotak {i+1}</label><canvas data-canvas="wartegg_{i}"></canvas><input type="hidden" name="wartegg_{i}"></div>')
        for i,g in enumerate(pack["graphic"]):
            canvas_items.append(f'<div><label>{esc(g)}</label><canvas data-canvas="graphic_{i}"></canvas><input type="hidden" name="graphic_{i}"></div>')
        drawing_section=f'<section id="sec-drawing" class="section"><div class="notice">Lengkapi gambar pada canvas. Pada tes grafis, tidak ada jawaban benar atau salah.</div><div class="canvaswrap">{"".join(canvas_items)}</div></section>'
        extra_sections = epps_section + kra_section + drawing_section
        tab_extra = '<button class="tab" data-target="sec-epps">EPPS <span class="badge">225</span></button><button class="tab" data-target="sec-kraepelin">Kraepelin <span class="badge">45</span></button><button class="tab" data-target="sec-drawing">Wartegg dan Grafis</button>'
    else:
        extra_sections=""
        tab_extra=""
    body=f"""<div class="card fun-card"><span class="badge">{esc(pack["title"])}</span><h2>🎮 Kerjakan dengan santai dan teliti</h2>
<p class="muted">Pilih jawaban, lanjutkan ke bagian berikutnya, lalu kirim ketika selesai. Skor akhir muncul otomatis.</p><div class="progress-wrap"><div class="progress-bar" id="progressBar"></div></div><div class="muted" id="progressText">0 jawaban terisi</div>
<div class="tabs">{"".join(tabs)}{tab_extra}</div>
<form method="post" action="/submit" id="testForm"><input type="hidden" name="attempt_id" value="{attempt_id}">{"".join(sections_html)}{extra_sections}
<div class="card"><button type="submit">Kirim Jawaban dan Lihat Hasil</button> <button type="button" class="btn secondary" id="saveDraft">Simpan sementara di perangkat</button></div></form></div>"""
    js=r"""
const tabs=document.querySelectorAll('.tab');
tabs.forEach(t=>t.addEventListener('click',()=>{tabs.forEach(x=>x.classList.remove('active'));document.querySelectorAll('.section').forEach(x=>x.classList.remove('active'));t.classList.add('active');document.getElementById(t.dataset.target).classList.add('active');window.scrollTo({top:0,behavior:'smooth'});}));
const form=document.getElementById('testForm');
const progressBar=document.getElementById('progressBar'), progressText=document.getElementById('progressText');
function updateProgress(){const answered=form.querySelectorAll('input[type="radio"]:checked').length + [...form.querySelectorAll('input[type="text"]')].filter(x=>x.value.trim()).length; const total=form.querySelectorAll('input[type="radio"]').length/4 + form.querySelectorAll('input[type="text"]').length; const pct=Math.min(100,Math.round(answered/Math.max(1,total)*100)); if(progressBar)progressBar.style.width=pct+'%'; if(progressText)progressText.textContent=answered+' jawaban terisi · '+pct+'% selesai';}
form.addEventListener('change',updateProgress); form.addEventListener('input',updateProgress);
document.getElementById('saveDraft').addEventListener('click',()=>{localStorage.setItem('psikotes_draft_'+form.attempt_id.value,JSON.stringify(Object.fromEntries(new FormData(form))));alert('Jawaban sementara disimpan di perangkat ini.');});
const draft=JSON.parse(localStorage.getItem('psikotes_draft_'+form.attempt_id.value)||'{}');
Object.entries(draft).forEach(([k,v])=>{const el=form.elements[k]; if(!el) return; if(el.length && typeof el!=='string'){[...el].forEach(x=>{if(x.value==v)x.checked=true})}else el.value=v;});
updateProgress();
document.querySelectorAll('canvas').forEach(c=>{
 const ctx=c.getContext('2d'); let drawing=false;
 const pos=e=>{const r=c.getBoundingClientRect();const p=e.touches?e.touches[0]:e;return [p.clientX-r.left,p.clientY-r.top]};
 const down=e=>{drawing=true;ctx.beginPath();const [x,y]=pos(e);ctx.moveTo(x,y);e.preventDefault()};
 const move=e=>{if(!drawing)return;const [x,y]=pos(e);ctx.lineTo(x,y);ctx.stroke();e.preventDefault()};
 const up=()=>drawing=false;
 ctx.lineWidth=2;ctx.lineCap='round';ctx.strokeStyle='#123';
 c.addEventListener('pointerdown',down);c.addEventListener('pointermove',move);c.addEventListener('pointerup',up);c.addEventListener('pointerleave',up);
});
form.addEventListener('submit',()=>{document.querySelectorAll('canvas').forEach(c=>{const hidden=form.querySelector('input[name="'+c.dataset.canvas+'"]');if(hidden)hidden.value=c.toDataURL('image/png')});localStorage.removeItem('psikotes_draft_'+form.attempt_id.value);});
"""
    return body, js

class Handler(BaseHTTPRequestHandler):
    server_version="PsikotesOnline/1.0"
    def log_message(self, fmt,*args): print("%s - %s"%(self.address_string(),fmt%args))
    def send_html(self, content, status=200, headers=None):
        raw=content.encode("utf-8")
        self.send_response(status); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(raw)))
        if headers:
            for k,v in headers.items(): self.send_header(k,v)
        self.end_headers(); self.wfile.write(raw)
    def redirect(self, location, headers=None):
        self.send_response(303); self.send_header("Location",location)
        if headers:
            for k,v in headers.items(): self.send_header(k,v)
        self.end_headers()
    def parse_form(self):
        length=int(self.headers.get("Content-Length","0")); raw=self.rfile.read(length)
        return urllib.parse.parse_qs(raw.decode("utf-8"),keep_blank_values=True)
    def get_one(self, data, key, default=""):
        vals=data.get(key, [default]); return vals[0] if vals else default
    def do_GET(self):
        parsed=urllib.parse.urlparse(self.path); path=parsed.path; qs=urllib.parse.parse_qs(parsed.query)
        if path=="/":
            body="""<div class="card fun-card"><h2>🚀 Mulai latihan</h2><p>Pilih jenis latihan dan paket. Peserta dapat mengerjakan melalui Google Chrome atau browser lain.</p>
<form method="post" action="/start"><div class="grid2"><div><label>Nama peserta</label><input name="name" required placeholder="Nama lengkap"></div><div><label>Email atau identitas</label><input name="email" placeholder="Opsional"></div></div>
<div class="grid2"><div><label>Jenis paket</label><select name="mode" id="mode"><option value="general">Psikotes Umum</option><option value="cpns">CPNS TWK TIU TKP</option></select></div><div><label>Nomor paket</label><select name="package_no">"""+ "".join(f'<option value="{i}">Paket {i:02d}</option>' for i in range(1,16))+"""</select></div></div><br><button type="submit">Mulai Mengerjakan</button></form></div>
<div class="grid3"><div class="card"><h3>🧠 15 Paket Umum</h3><p>Verbal, aritmatika, penalaran, EPPS, Kraepelin, Wartegg dan grafis.</p></div><div class="card"><h3>🇮🇩 15 Paket CPNS</h3><p>TWK 30, TIU 35, TKP 45 pada setiap paket.</p></div><div class="card"><h3>🏆 Skor Langsung</h3><p>Setelah selesai, peserta langsung melihat skor dan kunci jawaban.</p></div></div>
<div class="card"><h3>Admin</h3><p>Gunakan halaman admin untuk melihat semua hasil peserta.</p><a class="btn secondary" href="/admin">Buka halaman admin</a></div>"""
            self.send_html(page("Mulai latihan",body)); return
        if path.startswith("/test/"):
            parts=path.strip("/").split("/")
            if len(parts)!=3: self.send_html(page("Tidak ditemukan","<div class='card'>Alamat tidak ditemukan.</div>"),404); return
            mode=parts[1]; pkg=int(parts[2]); attempt=self.get_one(qs,"attempt")
            if mode not in PACKAGES or not attempt: self.send_html(page("Sesi tidak ditemukan","<div class='card'>Sesi tidak ditemukan.</div>"),404); return
            body,js=build_test_body(mode,pkg,attempt)
            self.send_html(page(PACKAGES[mode][pkg-1]["title"],body,js)); return
        if path=="/admin":
            if self.is_admin():
                self.send_html(self.admin_page()); return
            body='<div class="card"><h2>Admin hasil peserta</h2><form method="post" action="/admin/login"><label>PIN admin</label><input name="pin" type="password" required><br><br><button>Masuk</button></form><p class="muted">PIN default dapat diganti dengan variabel PSIKOTES_ADMIN_PIN.</p></div>'
            self.send_html(page("Admin",body)); return
        if path=="/admin/export.csv":
            if not self.is_admin(): self.send_html(page("Akses ditolak","<div class='card'>Akses admin diperlukan.</div>"),403); return
            conn=db(); rows=conn.execute("select * from attempts order by id desc").fetchall(); conn.close()
            out=io.StringIO(); w=csv.writer(out); w.writerow(["id","nama","email","jenis","paket","dibuat","dikirim","skor"])
            for r in rows:w.writerow([r["id"],r["name"],r["email"],r["mode"],r["package_no"],r["created_at"],r["submitted_at"],r["score_json"]])
            raw=out.getvalue().encode(); self.send_response(200); self.send_header("Content-Type","text/csv; charset=utf-8"); self.send_header("Content-Disposition","attachment; filename=hasil_psikotes.csv"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw); return
        if path=="/admin/detail":
            if not self.is_admin(): self.send_html(page("Akses ditolak","<div class='card'>Akses admin diperlukan.</div>"),403); return
            aid=self.get_one(qs,"id")
            conn=db(); row=conn.execute("select * from attempts where id=?",(aid,)).fetchone(); conn.close()
            if not row:self.send_html(page("Tidak ditemukan","<div class='card'>Data tidak ditemukan.</div>"),404);return
            self.send_html(self.detail_page(row)); return
        self.send_html(page("Tidak ditemukan","<div class='card'><h2>Halaman tidak ditemukan</h2><a href='/'>Kembali</a></div>"),404)
    def do_POST(self):
        path=urllib.parse.urlparse(self.path).path; data=self.parse_form()
        if path=="/start":
            name=self.get_one(data,"name").strip(); email=self.get_one(data,"email").strip(); mode=self.get_one(data,"mode"); pkg=int(self.get_one(data,"package_no","1"))
            if not name or mode not in PACKAGES or pkg not in range(1,16): self.send_html(page("Data tidak valid","<div class='card'>Data belum lengkap.</div>"),400); return
            token=secrets.token_urlsafe(16); conn=db(); cur=conn.execute("insert into attempts(token,name,email,mode,package_no,created_at) values(?,?,?,?,?,?)",(token,name,email,mode,pkg,datetime.now(timezone.utc).isoformat())); conn.commit(); aid=cur.lastrowid; conn.close()
            self.redirect(f"/test/{mode}/{pkg}?attempt={aid}"); return
        if path=="/submit":
            aid=self.get_one(data,"attempt_id")
            conn=db(); row=conn.execute("select * from attempts where id=?",(aid,)).fetchone()
            if not row:self.send_html(page("Sesi tidak ditemukan","<div class='card'>Sesi tidak ditemukan.</div>"),404);return
            pack=PACKAGES[row["mode"]][row["package_no"]-1]; scores={}; correct=0; total=0; tkp_score=0; answers={}
            sections=["verbal","arithmetic","logical"] if row["mode"]=="general" else ["twk","tiu","tkp"]
            for sec in sections:
                items=pack[sec]; sec_correct=0; sec_total=len(items); sec_score=0
                for i,item in enumerate(items):
                    val=self.get_one(data,f"{sec}_{i}",""); answers[f"{sec}_{i}"]=val
                    if sec=="tkp":
                        try: sec_score += int(item["scores"][int(val)])
                        except: pass
                    else:
                        total+=1
                        if val!="" and int(val)==item["answer"]: correct+=1;sec_correct+=1
                if sec=="tkp": scores[sec]={"score":sec_score,"max":sec_total*5,"passing":166}
                else:
                    passing = 65 if sec=="twk" else 80
                    scores[sec]={"correct":sec_correct,"total":sec_total,"points":sec_correct*5,"passing":passing}
            for k,vals in data.items():
                if k not in answers and k not in ("attempt_id",): answers[k]=vals[0] if len(vals)==1 else vals
            if row["mode"]=="general": scores["objective"]={"correct":correct,"total":total}
            else: scores["total_objective"]={"correct":correct,"total":total}
            conn.execute("update attempts set submitted_at=?,score_json=?,answers_json=? where id=?",(datetime.now(timezone.utc).isoformat(),json.dumps(scores,ensure_ascii=False),json.dumps(answers,ensure_ascii=False),aid)); conn.commit(); conn.close()
            self.send_html(self.result_page(row,scores)); return
        if path=="/admin/login":
            if self.get_one(data,"pin")==ADMIN_PIN:self.redirect("/admin",{"Set-Cookie":"admin=1; HttpOnly; SameSite=Lax"});return
            self.send_html(page("PIN salah","<div class='card'><h2>PIN salah</h2><a href='/admin'>Coba lagi</a></div>"),403);return
        self.send_html(page("Tidak ditemukan","<div class='card'>Alamat tidak ditemukan.</div>"),404)
    def is_admin(self):
        return "admin=1" in self.headers.get("Cookie","")
    def review_html(self,row):
        """Build the answer key shown only after a participant submits."""
        answers=json.loads(row["answers_json"] or "{}")
        pack=PACKAGES[row["mode"]][row["package_no"]-1]
        sections=["verbal","arithmetic","logical"] if row["mode"]=="general" else ["twk","tiu","tkp"]
        blocks=[]
        for sec in sections:
            rows=[]
            for i,item in enumerate(pack[sec]):
                raw=answers.get(f"{sec}_{i}","")
                try: idx=int(raw)
                except: idx=-1
                selected=item["options"][idx] if 0 <= idx < len(item["options"]) else "Belum dijawab"
                if sec=="tkp":
                    score=item.get("scores",[])[idx] if 0 <= idx < len(item.get("scores",[])) else 0
                    key=f"Nilai respons: {score}/5"
                    status="Respons tersimpan"
                else:
                    correct=item.get("answer",0)
                    key=f"{chr(65+correct)}. {item['options'][correct]}"
                    status="Benar" if idx==correct else "Perlu dipelajari lagi"
                explanation=item.get("explanation","")
                extra=f'<div class="review"><b>{esc(sec.upper())} {i+1}.</b> {esc(item["text"])}<br><small>Jawaban Anda: {esc(selected)} · Kunci: {esc(key)} · {esc(status)}</small>'
                if explanation:
                    extra += f'<br><small><b>Cara:</b> {esc(explanation)}</small>'
                extra += '</div>'
                rows.append(extra)
            blocks.append(f'<h3>{esc(sec.upper())}</h3>{"".join(rows)}')
        return '<details><summary>📘 Lihat kunci jawaban dan pembahasan</summary><p class="muted">Pembahasan cara hitung ditampilkan pada soal aritmatika, deret, dan numerik.</p>'+''.join(blocks)+'</details>'
    def result_page(self,row,scores):
        if row["mode"]=="general":
            obj=scores["objective"]; pct=round((obj["correct"]/obj["total"])*100,1) if obj["total"] else 0; emoji="🎉" if pct>=70 else "💪"
            lines=f'<p class="score">{emoji} {obj["correct"]} / {obj["total"]} benar</p><p><b>Skor akhir: {pct}%</b></p><p>EPPS, Kraepelin, Wartegg, dan grafis ikut tersimpan sebagai jawaban latihan.</p>'
        else:
            twk=scores["twk"];tiu=scores["tiu"];tkp=scores["tkp"]; total=tkp["score"]
            twk_state="LULUS LATIHAN" if twk["points"]>=twk["passing"] else "Belum mencapai ambang"
            tiu_state="LULUS LATIHAN" if tiu["points"]>=tiu["passing"] else "Belum mencapai ambang"
            tkp_state="LULUS LATIHAN" if total>=tkp["passing"] else "Belum mencapai ambang"
            lines=f'<div class="grid3"><div><h3>🇮🇩 TWK</h3><p class="score">{twk["points"]} poin</p><span class="muted">{twk["correct"]}/{twk["total"]} benar · Ambang {twk["passing"]}<br>{twk_state}</span></div><div><h3>🧠 TIU</h3><p class="score">{tiu["points"]} poin</p><span class="muted">{tiu["correct"]}/{tiu["total"]} benar · Ambang {tiu["passing"]}<br>{tiu_state}</span></div><div><h3>🤝 TKP</h3><p class="score">{total} poin</p><span class="muted">Maksimal {tkp["max"]} · Ambang {tkp["passing"]}<br>{tkp_state}</span></div></div>'
        review=self.review_html(row)
        return page("Hasil latihan",f'<div class="card fun-card"><span class="badge">{esc(row["name"])}</span><h2>🏆 Hasil {esc(row["mode"].upper())} paket {row["package_no"]:02d}</h2>{lines}<p class="muted">Jawaban Anda sudah tersimpan. Gunakan pembahasan di bawah untuk belajar dari kesalahan.</p>{review}<br><a class="btn" href="/">🔁 Kerjakan paket lain</a></div>')
    def admin_page(self):
        conn=db(); rows=conn.execute("select * from attempts order by id desc").fetchall(); conn.close()
        tr=[]
        for r in rows:
            sc=esc(r["score_json"] or "Belum dikirim")
            tr.append(f'<tr><td>{r["id"]}</td><td>{esc(r["name"])}</td><td>{esc(r["email"])}</td><td>{esc(r["mode"])}</td><td>{r["package_no"]:02d}</td><td>{esc(r["submitted_at"] or "Belum")}</td><td><a href="/admin/detail?id={r["id"]}">Lihat jawaban</a><details><summary>Skor</summary><small>{sc}</small></details></td></tr>')
        body=f'<div class="card"><h2>Hasil semua peserta</h2><p><a class="btn" href="/admin/export.csv">Unduh CSV</a> <a class="btn secondary" href="/">Halaman peserta</a></p><div class="scroll"><table><tr><th>ID</th><th>Nama</th><th>Identitas</th><th>Jenis</th><th>Paket</th><th>Dikirim</th><th>Rincian</th></tr>{"".join(tr) or "<tr><td colspan=7>Belum ada peserta.</td></tr>"}</table></div></div>'
        return page("Admin hasil peserta",body)
    def detail_page(self,row):
        ans=json.loads(row["answers_json"] or "{}"); scores=esc(row["score_json"] or "")
        pack=PACKAGES[row["mode"]][row["package_no"]-1]; sections=["verbal","arithmetic","logical"] if row["mode"]=="general" else ["twk","tiu","tkp"]; rows=[]
        for sec in sections:
            for i,item in enumerate(pack[sec]):
                submitted=ans.get(f"{sec}_{i}",""); correct=item.get("answer",""); iftext=""
                if sec=="tkp": iftext=f"Nilai pilihan: {item.get('scores',[1,2,3,4,5])[int(submitted)] if str(submitted).isdigit() and int(submitted)<5 else '-'}"
                else: iftext=f"Kunci: {chr(65+correct)}" if isinstance(correct,int) else ""
                if item.get("explanation"):
                    iftext += " | Cara: " + item["explanation"]
                rows.append(f"<tr><td>{esc(sec.upper())} {i+1}</td><td>{esc(item['text'])}</td><td>{esc(submitted)}</td><td>{esc(iftext)}</td></tr>")
        body=f'<div class="card"><h2>Jawaban peserta</h2><p><b>Nama:</b> {esc(row["name"])}<br><b>Jenis:</b> {esc(row["mode"])} paket {row["package_no"]:02d}<br><b>Skor:</b> {scores}</p><div class="scroll"><table><tr><th>Bagian</th><th>Soal</th><th>Jawaban</th><th>Kunci/nilai</th></tr>{"".join(rows)}</table></div><br><a class="btn secondary" href="/admin">Kembali</a></div>'
        return page("Rincian jawaban",body)

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--host",default=HOST); ap.add_argument("--port",type=int,default=PORT); args=ap.parse_args()
    db().close()
    print(f"Psikotes Online berjalan di http://{args.host}:{args.port}")
    print(f"PIN admin: {ADMIN_PIN} (ubah dengan PSIKOTES_ADMIN_PIN)")
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()

