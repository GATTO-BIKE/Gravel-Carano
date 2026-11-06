# Gravel Carano 2027 — backend richieste con verifica email e pannello admin.
import csv
import hmac
import io
import os
import re
import secrets
import smtplib
import sqlite3
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import quote
from flask import Flask, jsonify, request, send_from_directory, Response, redirect

ROOT = Path(__file__).resolve().parent.parent
DB = Path(os.environ.get('GC_DB_PATH', str(ROOT / 'private' / 'registrations.sqlite3')))
DB.parent.mkdir(parents=True, exist_ok=True)
APP_URL = os.environ.get('GC_PUBLIC_URL', 'http://127.0.0.1:5000').rstrip('/')
ADMIN_USER = os.environ.get('GC_ADMIN_USER', '')
ADMIN_PASSWORD = os.environ.get('GC_ADMIN_PASSWORD', '')
MAIL_HOST = os.environ.get('GC_SMTP_HOST', '')
MAIL_PORT = int(os.environ.get('GC_SMTP_PORT', '587'))
MAIL_USER = os.environ.get('GC_SMTP_USER', '')
MAIL_PASS = os.environ.get('GC_SMTP_PASSWORD', '')
MAIL_FROM = os.environ.get('GC_SMTP_FROM', MAIL_USER)
NOTIFY_TO = os.environ.get('GC_NOTIFY_TO', 'gattobiketeam@gmail.com')
app = Flask(__name__, static_folder=None)
app.config['MAX_CONTENT_LENGTH'] = 12000
attempts = {}

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

with connect() as con:
    con.execute('''CREATE TABLE IF NOT EXISTS registrations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT, message TEXT,
      token TEXT NOT NULL UNIQUE, status TEXT NOT NULL DEFAULT 'in_attesa',
      created_at TEXT NOT NULL, confirmed_at TEXT, privacy_accepted_at TEXT NOT NULL
    )''')

def send_mail(to, subject, body):
    if not (MAIL_HOST and MAIL_FROM):
        return False
    msg = EmailMessage()
    msg['From'] = MAIL_FROM
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)
    with smtplib.SMTP(MAIL_HOST, MAIL_PORT, timeout=12) as smtp:
        smtp.starttls()
        if MAIL_USER: smtp.login(MAIL_USER, MAIL_PASS)
        smtp.send_message(msg)
    return True

def check_admin():
    auth = request.authorization
    if not ADMIN_USER or not ADMIN_PASSWORD or not auth:
        return False
    return hmac.compare_digest(auth.username or '', ADMIN_USER) and hmac.compare_digest(auth.password or '', ADMIN_PASSWORD)

def unauthorized():
    return Response('Accesso riservato', 401, {'WWW-Authenticate':'Basic realm="Gravel Carano Admin"'})

@app.after_request
def security_headers(resp):
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['Cache-Control'] = 'no-store' if request.path.startswith('/api/') or request.path.startswith('/admin') else 'public, max-age=3600'
    return resp

@app.post('/api/register')
def register():
    # Basic abuse throttling; use a reverse proxy/rate-limiter for public deployment.
    ip = request.remote_addr or 'unknown'
    now = time.monotonic()
    attempts[ip] = [x for x in attempts.get(ip, []) if now - x < 3600]
    if len(attempts[ip]) >= 8:
        return jsonify(message='Troppe richieste. Riprova più tardi.'), 429
    data = request.get_json(silent=True) or {}
    if data.get('website'):
        return jsonify(message='Richiesta ricevuta.'), 200
    name = str(data.get('name','')).strip()[:100]
    email = str(data.get('email','')).strip().lower()[:150]
    phone = str(data.get('phone','')).strip()[:40]
    message = str(data.get('message','')).strip()[:1000]
    if len(name) < 3 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email) or data.get('privacy') is not True:
        return jsonify(message='Controlla nome, email e consenso privacy.'), 400
    if not MAIL_HOST:
        return jsonify(message='Servizio email non ancora configurato: usa il contatto diretto.'), 503
    attempts[ip].append(now)
    token = secrets.token_urlsafe(32)
    timestamp = datetime.now(timezone.utc).isoformat()
    with connect() as con:
        cur = con.execute('INSERT INTO registrations (name,email,phone,message,token,created_at,privacy_accepted_at) VALUES (?,?,?,?,?,?,?)', (name,email,phone,message,token,timestamp,timestamp))
        rowid = cur.lastrowid
    confirm_url = APP_URL + '/api/confirm?token=' + quote(token)
    try:
        send_mail(email, 'Conferma la tua richiesta — Gravel Carano 2027',
            f'Ciao {name},\n\nper verificare il tuo indirizzo email e confermare la richiesta di interesse, apri:\n{confirm_url}\n\nNon si tratta di iscrizione definitiva né di pagamento.\n\nGatto Bike Team')
    except Exception:
        with connect() as con: con.execute('DELETE FROM registrations WHERE id=?',(rowid,))
        app.logger.exception('SMTP failed')
        return jsonify(message='Invio email non riuscito. Contatta gli organizzatori.'), 503
    return jsonify(message='Richiesta ricevuta! Controlla la tua email e clicca sul link per verificarla. La partecipazione non è ancora confermata.'), 201

@app.get('/api/confirm')
def confirm():
    token = request.args.get('token','')
    if len(token) > 128 or len(token) < 20: return 'Link non valido.', 400
    with connect() as con:
        row = con.execute('SELECT id,name,email,status FROM registrations WHERE token=?',(token,)).fetchone()
        if not row: return 'Link non valido o scaduto.', 404
        if row['status'] == 'in_attesa':
            con.execute("UPDATE registrations SET status='email_verificata', confirmed_at=? WHERE id=?", (datetime.now(timezone.utc).isoformat(),row['id']))
            try:
                send_mail(NOTIFY_TO, 'Nuova richiesta verificata — Gravel Carano 2027', f"Richiesta #{row['id']} verificata: {row['name']} ({row['email']}). Consulta il pannello admin.")
            except Exception: app.logger.exception('Admin notification failed')
    return redirect('/conferma.html', code=303)

@app.get('/admin')
def admin():
    if not check_admin(): return unauthorized()
    with connect() as con:
        rows = con.execute('SELECT id,name,email,phone,message,status,created_at,confirmed_at FROM registrations ORDER BY id DESC LIMIT 1000').fetchall()
    from html import escape
    tr = ''.join('<tr>' + ''.join(f'<td>{escape(str(r[k] or ""))}</td>' for k in ('id','name','email','phone','message','status','created_at','confirmed_at')) + '</tr>' for r in rows)
    return Response('''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Gatto Bike — richieste</title><style>body{font:15px system-ui;background:#101b16;color:#fff;padding:24px}a{color:#d8ff50}table{border-collapse:collapse;background:#fff;color:#17231c;width:100%}td,th{padding:10px;border:1px solid #ccc;text-align:left}div{overflow:auto}</style><h1>Gravel Carano — richieste di interesse</h1><p>Le richieste verificate NON sono iscrizioni definitive. <a href="/admin/export.csv">Esporta CSV</a></p><div><table><thead><tr><th>ID</th><th>Nome</th><th>Email</th><th>Telefono</th><th>Messaggio</th><th>Stato</th><th>Data richiesta UTC</th><th>Verifica UTC</th></tr></thead><tbody>''' + tr + '</tbody></table></div></html>', mimetype='text/html')

@app.get('/admin/export.csv')
def export_csv():
    if not check_admin(): return unauthorized()
    out = io.StringIO()
    writer = csv.writer(out)
    fields = ['id','name','email','phone','message','status','created_at','confirmed_at']
    writer.writerow(fields)
    with connect() as con:
        for row in con.execute('SELECT id,name,email,phone,message,status,created_at,confirmed_at FROM registrations ORDER BY id'):
            writer.writerow([("'" + str(row[k]) if str(row[k] or '').startswith(('=','+','-','@')) else row[k]) for k in fields])
    return Response(out.getvalue(), mimetype='text/csv', headers={'Content-Disposition':'attachment; filename="gravel-carano-richieste.csv"'})

@app.get('/')
def homepage(): return send_from_directory(ROOT,'index.html')

@app.get('/<path:filename>')
def static_files(filename):
    if filename.startswith(('server/','private/','.')) or '..' in Path(filename).parts:
        return 'Non trovato', 404
    return send_from_directory(ROOT,filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=int(os.environ.get('PORT','5000')),debug=False)
