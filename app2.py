
from flask import Flask, Response, jsonify, redirect, make_response, request, url_for, render_template, session, abort, flash, stream_with_context, send_file, abort, g as gprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

import io, os, sys, re, random, json, time, html, uuid, sqlite3, logging
from functools import lru_cache
from datetime import datetime, timedelta
import urllib.parse
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text as sqltext
from models import db, Mtk
from razan import cfg
app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)
DATABASE = os.path.join(app.instance_path, 'mtk.db')
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(cfg.folder_cache, exist_ok=True)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

limiter = Limiter(app, key_func=get_remote_address)
# Konfigurasi MySQL (dari cfg)
# Di bagian konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('user_databoks')}:{os.getenv('pass_databoks')}"
    f"@{os.getenv('host_databoks')}:{os.getenv('port_databoks')}/{os.getenv('database_dev')}"
)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.getenv('REDIS_URL'))
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'max_overflow': 30
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi SQLAlchemy
db.init_app(app)
# Tambahkan command CLI untuk create tables
@app.cli.command()
def create_tables():
    """Buat tabel di database."""
    db.create_all()
    print("✅ Tabel berhasil dibuat!")

def get_user_ip():
    # Cek header proxy (X-Forwarded-For, X-Real-IP, dll)
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers['X-Real-IP']
    else:
        ip = request.remote_addr
    return ip or 'unknown'

@app.template_filter('urlencode')
def urlencode_filter(s):
    if isinstance(s, str):
        return urllib.parse.quote(s.encode('utf-8'))
    return s

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        # Buat tabel jika belum ada
        conn.execute('''
            CREATE TABLE IF NOT EXISTS mtk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                nama_user TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                tanggal_mengerjakan TEXT NOT NULL,
                soal TEXT NOT NULL,
                jawaban_user TEXT NOT NULL,
                kunci_jawaban INTEGER NOT NULL,
                durasi_jawab REAL NOT NULL,
                durasi_total REAL NOT NULL,
                benar INTEGER NOT NULL
            )
        ''')
        conn.commit()

        # Pastikan kolom yang diperlukan ada
        cur = conn.execute("PRAGMA table_info(mtk)")
        kolom_ada = {row[1] for row in cur.fetchall()}
        kolom_wajib = {'session_id', 'benar','ip_address'}

        for kolom in kolom_wajib:
            if kolom not in kolom_ada:
                tipe = "TEXT" if kolom == "session_id" else "INTEGER"
                conn.execute(f"ALTER TABLE mtk ADD COLUMN {kolom} {tipe}")
                conn.commit()
                print(f"✅ Kolom '{kolom}' ditambahkan ke tabel mtk.")

# Setup sekali pakai (ganti before_first_request)
_setup_done = False
_setup_lock = None

@app.before_request
def setup_once():
    global _setup_done, _setup_lock
    if not _setup_done:
        if _setup_lock is None:
            import threading
            _setup_lock = threading.Lock()
        with _setup_lock:
            if not _setup_done:
                init_db()
                _setup_done = True

@app.before_request
def create_tables():
    db.create_all()

@app.route('/mtk_lama', methods=['GET', 'POST'])
def mtk_lama():
    if request.method == 'POST':
        session.clear()
        session['nama_user'] = request.form.get('nama_user', 'Anonim').strip() or 'Anonim'
        session['mode'] = request.form['mode']
        session['operasi'] = request.form.get('operasi') or '+'  # 🔹 fallback ke penjumlahan
        session['batas_a'] = int(request.form.get('batas_a', 12))
        session['batas_b'] = int(request.form.get('batas_b', 2))
        session['session_id'] = str(uuid.uuid4())
        session['start_time_total'] = time.time()
        return redirect(url_for('mtk_latihan'))
    else:        
        nama_default = session.get('nama_user', 'Anonim')
        with sqlite3.connect(DATABASE) as conn:
            seminggu_lalu = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            cur = conn.cursor()
            cur.execute('''
                SELECT durasi_jawab, benar
                FROM mtk
                WHERE nama_user = ? AND tanggal_mengerjakan >= ? AND durasi_jawab <= 70.0 
                ORDER BY tanggal_mengerjakan ASC
            ''', (nama_default, seminggu_lalu))
            rows = cur.fetchall()
            durasi_7hari = [round(row[0], 2) for row in rows]
            status_7hari = [bool(row[1]) for row in rows]
        
        return render_template(
            'mtk.html', 
            step='config', 
            durasi_7hari_preview=durasi_7hari,
            status_7hari_preview=status_7hari  # 🔹 Ubah jadi _preview
        )

@app.route('/mtk', methods=['GET', 'POST'])
def mtk():
    if request.method == 'POST':
        session.permanent = True
        session.clear()
        session['nama_user'] = request.form.get('nama_user', 'Anonim').strip() or 'Anonim'
        session['mode'] = request.form['mode']
        session['operasi'] = request.form.get('operasi') or '+'
        session['batas_a'] = int(request.form.get('batas_a', 12))
        session['batas_b'] = int(request.form.get('batas_b', 2))
        session['session_id'] = str(uuid.uuid4())
        session['start_time_total'] = time.time()
        return redirect(url_for('mtk_latihan'))
    
    # Preview 7 hari (gunakan query ringan)
    nama_default = session.get('nama_user', 'Anonim')
    seminggu_lalu = datetime.utcnow() - timedelta(days=7)
    records = Mtk.query.filter(
        Mtk.nama_user == nama_default,
        Mtk.tanggal_mengerjakan >= seminggu_lalu,
        Mtk.durasi_jawab <= 70.0
    ).order_by(Mtk.tanggal_mengerjakan).limit(100).all()
    
    durasi_7hari = [round(r.durasi_jawab, 2) for r in records]
    status_7hari = [r.benar for r in records]
    
    return render_template('mtk.html', step='config', 
                         durasi_7hari_preview=durasi_7hari,
                         status_7hari_preview=status_7hari)

@app.route('/mtk/submit-batch', methods=['POST'])
@limiter.limit("5 per minute")  # Maks 5 submit per user per menit
def submit_batch():
    try:
        batch = request.get_json()
        if not batch or not isinstance(batch, list):
            return jsonify({"error": "Invalid data"}), 400

        session_id = session.get('session_id')
        nama_user = session.get('nama_user', 'Anonim')
        start_total = session.get('start_time_total', time.time())
        ip_address = get_user_ip()

        if not session_id:
            return jsonify({"error": "Session expired"}), 400

        records = []
        for item in batch:
            if 'soal' not in item or 'jawaban_user' not in item:
                continue

            try:
                # Ambil jawaban user
                jawaban_str = str(item['jawaban_user']).strip()
                jawaban_int = int(jawaban_str) if jawaban_str else 0
                
                # Hitung ulang kunci jawaban dari soal (lebih aman!)
                # Contoh: soal = "6 + 2"
                soal = item['soal']
                # Ganti '×' dengan '*' jika ada
                soal_eval = soal.replace('×', '*').replace('÷', '/')
                kunci_server = eval(soal_eval)  # ✅ Hitung ulang di server!
                
                # Validasi benar/salah di server
                benar = (jawaban_int == kunci_server)
                
                records.append(Mtk(
                    session_id=session_id,
                    nama_user=nama_user,
                    ip_address=ip_address,
                    tanggal_mengerjakan=datetime.utcnow(),
                    soal=soal,
                    jawaban_user=jawaban_str,
                    kunci_jawaban=kunci_server,  # Gunakan hasil server
                    durasi_jawab=min(float(item.get('durasi_jawab', 0)), 300.0),
                    durasi_total=time.time() - start_total,
                    benar=benar  # ✅ Gunakan hasil validasi server
                ))
            except Exception as e:
                print(f"Error processing item: {item}, error: {e}")
                continue

        if records:
            db.session.bulk_save_objects(records)
            db.session.commit()
            return jsonify({"status": "success", "count": len(records)})
        else:
            return jsonify({"status": "empty"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Batch submit error: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@app.route('/mtk/submit-batch_ori', methods=['POST'])
def submit_batch_ori():
    try:
        batch = request.get_json()
        if not batch or not isinstance(batch, list):
            return jsonify({"error": "Invalid data"}), 400

        # Ambil data dari session
        session_id = session.get('session_id')
        nama_user = session.get('nama_user', 'Anonim')
        start_total = session.get('start_time_total', time.time())
        ip_address = get_user_ip()

        if not session_id:
            return jsonify({"error": "Session expired"}), 400

        # Buat objek untuk disimpan
        records = []
        for item in batch:
            # Validasi minimal
            if 'soal' not in item or 'kunci_jawaban' not in item:
                continue
                
            records.append(Mtk(
                session_id=session_id,
                nama_user=nama_user,
                ip_address=ip_address,
                tanggal_mengerjakan=datetime.utcnow(),
                soal=item['soal'],
                jawaban_user=str(item.get('jawaban_user', '')),
                kunci_jawaban=item['kunci_jawaban'],
                durasi_jawab=min(float(item.get('durasi_jawab', 0)), 300.0),
                durasi_total=time.time() - start_total,
                benar=bool(item.get('benar', False))
            ))

        if records:
            db.session.bulk_save_objects(records)
            db.session.commit()
            return jsonify({"status": "success", "count": len(records)})
        else:
            return jsonify({"status": "empty"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error submitting batch: {str(e)}")  # 🔹 LOG ERROR!
        return jsonify({"error": "Server error"}), 500

@app.route('/mtk/latihan', methods=['GET'])
def mtk_latihan():
    if 'nama_user' not in session:
        return redirect(url_for('mtk'))

    # Generate soal baru
    mode = session['mode']
    batas_a = session['batas_a']
    batas_b = session['batas_b']

    if mode == 'random':
        operasi = random.choice(['+', '-', '*'])
    elif mode == 'add_sub':
        operasi = random.choice(['+', '-'])
    elif mode == 'add_div':
        operasi = random.choice(['+', '/'])
    elif mode == 'multi_div':
        operasi = random.choice(['*', '/'])
    else:
        operasi = session['operasi']

    # Generate angka berdasarkan operasi
    if operasi == '/':
        # Pastikan pembagian habis dan tidak nol
        b = random.randint(1, min(batas_b, 10))
        a = b * random.randint(1, max(1, batas_a // b))
    elif operasi == '-':
        # Hindari hasil negatif
        a = random.randint(1, batas_a)
        b = random.randint(1, min(batas_b, a))
    else:
        # Penjumlahan & perkalian
        a = random.randint(1, batas_a)
        b = random.randint(1, batas_b)

    # Acak posisi untuk operasi komutatif (+, *)
    if operasi in ['+', '*'] and random.choice([True, False]):
        a, b = b, a
    # Pastikan pengurangan tidak negatif
    elif operasi == '-' and a < b:
        a, b = b, a

    soal = f"{a} {operasi} {b}"
    kunci = eval(soal)  # Aman karena input terkontrol

    # Simpan ke session
    session['soal'] = soal
    session['kunci_jawaban'] = kunci
    session['start_time_soal'] = time.time()

    # 🔑 KIRIM kunci_jawaban ke template!
    return render_template('mtk.html', step='latihan', soal=soal, kunci_jawaban=kunci)

@app.route('/mtk/latihan_lama', methods=['GET', 'POST'])
def mtk_latihan_lama():
    if 'nama_user' not in session:
        return redirect(url_for('mtk'))

    if request.method == 'POST':
        if request.form.get('action') == 'selesai':
            return redirect(url_for('mtk_hasil'))

        # Proses jawaban
        jawaban_user = request.form.get('jawaban')
        soal = session.get('soal')
        kunci = session.get('kunci_jawaban')
        start_jawab = session.get('start_time_soal')
        start_total = session.get('start_time_total')

        try:
            jawaban_int = int(jawaban_user)
        except (TypeError, ValueError):
            jawaban_int = None

        benar = 1 if (jawaban_int == kunci) else 0
        # durasi_jawab = time.time() - start_jawab
        # durasi_total = time.time() - start_total

        durasi_jawab = float(request.form.get('client_duration', 0))
        durasi_total = time.time() - session.get('start_time_total', time.time())

        # Batasi maksimal 300 detik (5 menit)
        if durasi_jawab < 0 or durasi_jawab > 300:
            durasi_jawab = 300.0  # atau tolak request

        # Ambil IP
        user_ip = get_user_ip()

        # Simpan ke DB
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
                INSERT INTO mtk (
                    session_id, nama_user, ip_address, tanggal_mengerjakan, soal,
                    jawaban_user, kunci_jawaban, durasi_jawab, durasi_total, benar
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session['session_id'],
                session['nama_user'],
                user_ip,  # 🔹 Tambahkan ini
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                soal,
                str(jawaban_user),
                kunci,
                round(durasi_jawab, 2),
                round(durasi_total, 2),
                benar
            ))
            conn.commit()
        
        # Animasi
        if durasi_jawab < 1:
            animasi = 'transparan'
        elif 3 <= durasi_jawab <= 5:
            animasi = 'roket'
        elif durasi_jawab > 5:
            animasi = 'kembang_api'
        else:
            animasi = None

        return jsonify({
            'benar': bool(benar),
            'kunci': kunci,
            'animasi': animasi,
            'durasi': round(durasi_jawab, 2)
        })

    # Generate soal baru
    mode = session['mode']
    batas_a = session['batas_a']
    batas_b = session['batas_b']

    if mode == 'random':
        operasi = random.choice(['+', '-', '*'])
    elif mode == 'add_sub':
        operasi = random.choice(['+', '-'])
    elif mode == 'add_div':
        operasi = random.choice(['+', '/'])
    elif mode == 'multi_div':
        operasi = random.choice(['*', '/'])
    else:
        operasi = session['operasi']

    # Generate angka
    if operasi == '/':
        # Hindari pembagian dengan 0 dan hasil desimal
        b = random.randint(1, min(batas_b, 10))
        a = b * random.randint(1, batas_a // b)  # Pastikan a habis dibagi b
    elif operasi == '-':
        a = random.randint(1, batas_a)
        b = random.randint(1, min(batas_b, a))  # Hindari negatif
    else:
        a = random.randint(1, batas_a)
        b = random.randint(1, batas_b)

    # if operasi == '-' and a < b:
    #     a, b = b, a

    # 🔁 Acak posisi untuk operasi komutatif (+ dan *)
    if operasi in ['+', '*']:
        # 50% kemungkinan tukar posisi
        if random.choice([True, False]):
            a, b = b, a

    # Untuk pengurangan, pastikan tidak negatif
    elif operasi == '-':
        if a < b:
            a, b = b, a

    soal = f"{a} {operasi} {b}"
    kunci = eval(soal.replace('×', '*'))  # aman karena input terkontrol

    session['soal'] = soal
    session['kunci_jawaban'] = kunci
    session['start_time_soal'] = time.time()

    return render_template('mtk.html', step='latihan', soal=soal)

# Routes lain (users, user_chart) - disesuaikan dengan SQLAlchemy
@app.route('/mtk/users')
def mtk_users():
    users = db.session.query(
        Mtk.nama_user,
        db.func.count().label('total_sesi'),
        db.func.max(Mtk.tanggal_mengerjakan).label('terakhir')
    ).group_by(Mtk.nama_user).order_by(db.desc('terakhir')).all()
    return render_template('mtk_users.html', users=users)

@app.route('/mtk/users_lama')
def mtk_users_lama():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        # Ambil daftar user unik + jumlah sesi
        cur.execute('''
            SELECT nama_user, COUNT(*) as total_sesi, MAX(tanggal_mengerjakan) as terakhir
            FROM mtk
            GROUP BY nama_user
            ORDER BY terakhir DESC
        ''')
        users = cur.fetchall()
    return render_template('mtk_users.html', users=users)

@app.route('/mtk/user/<user_slug>')
def mtk_user_chart(user_slug):
    user_name = user_slug.replace('_', ' ')
    seminggu_lalu = datetime.utcnow() - timedelta(days=7)
    records = Mtk.query.filter(
        Mtk.nama_user == user_name,
        Mtk.tanggal_mengerjakan >= seminggu_lalu
    ).order_by(Mtk.id).limit(100).all()
    
    durasi = [round(r.durasi_jawab, 2) for r in records]
    status_benar = [r.benar for r in records]
    labels = [f"Soal {i+1}" for i in range(len(durasi))]
    
    return render_template('mtk_user_chart.html',
                         user_name=user_name,
                         durasi=durasi,
                         status_benar=status_benar,
                         labels=labels)

@app.route('/mtk/user_lama/<user_slug>')
def mtk_user_chart_lama(user_slug):
    user_name = user_slug.replace('_', ' ')
    with sqlite3.connect(DATABASE) as conn:
        seminggu_lalu = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cur = conn.cursor()
        cur.execute('''
            SELECT durasi_jawab, benar
            FROM mtk
            WHERE nama_user = ? AND tanggal_mengerjakan >= ?
            ORDER BY id ASC
        ''', (user_name, seminggu_lalu))
        rows = cur.fetchall()
        durasi_list = [round(row[0], 2) for row in rows]
        status_benar = [bool(row[1]) for row in rows]  # True = benar, False = salah

    labels = [f"Soal {i+1}" for i in range(len(durasi_list))]
    return render_template(
        'mtk_user_chart.html',
        user_name=user_name,
        durasi=durasi_list,
        status_benar=status_benar,
        labels=labels
    )

@app.route('/mtk/hasil')
def mtk_hasil():
    if 'session_id' not in session:
        return redirect(url_for('mtk'))

    session_id = session['session_id']
    records = Mtk.query.filter_by(session_id=session_id).order_by(Mtk.id).all()
    
    if not records:
        return redirect(url_for('mtk'))

    nama = records[0].nama_user
    total = len(records)
    benar_count = sum(1 for r in records if r.benar)
    salah_count = total - benar_count
    salah_list = [(r.soal, r.kunci_jawaban) for r in records if not r.benar]
    
    durasi_per_soal = [round(r.durasi_jawab, 2) for r in records]
    status_benar = [r.benar for r in records]

    # Statistik 7 hari
    seminggu_lalu = datetime.utcnow() - timedelta(days=7)
    durasi_7hari = [round(r.durasi_jawab, 2) for r in 
                    Mtk.query.filter(Mtk.nama_user == nama, 
                                   Mtk.tanggal_mengerjakan >= seminggu_lalu)
                    .order_by(Mtk.tanggal_mengerjakan).limit(100).all()]

    return render_template('mtk.html', step='hasil',
                         nama_user=nama,
                         total=total,
                         benar=benar_count,
                         salah=salah_count,
                         salah_list=salah_list,
                         durasi_per_soal=durasi_per_soal,
                         status_benar=status_benar,
                         durasi_7hari_global=durasi_7hari)


@app.route('/mtk/_lama')
def mtk_hasil_lama():
    if 'session_id' not in session:
        return redirect(url_for('mtk'))

    nama = session['nama_user']
    session_id = session['session_id']

    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT soal, kunci_jawaban, jawaban_user, durasi_jawab, benar
            FROM mtk
            WHERE session_id = ?
            ORDER BY id ASC
        ''', (session_id,))
        semua_soal = cur.fetchall()

        total = len(semua_soal)
        benar_count = sum(1 for row in semua_soal if row[4] == 1)
        salah_count = total - benar_count
        salah_list = [(row[0], row[1]) for row in semua_soal if row[4] == 0]

        # 🔹 Kirim durasi dan status benar/salah
        durasi_per_soal = [round(row[3], 2) for row in semua_soal]
        status_benar = [bool(row[4]) for row in semua_soal]  # True = benar

        # Data 7 hari terakhir (opsional, tidak dipakai di sini)
        seminggu_lalu = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cur.execute('''
            SELECT durasi_jawab
            FROM mtk
            WHERE nama_user = ? AND tanggal_mengerjakan >= ?
            ORDER BY tanggal_mengerjakan ASC
        ''', (nama, seminggu_lalu))
        durasi_7hari = [round(row[0], 2) for row in cur.fetchall()]
    jumlah_soal_sejauh_ini = session.get('jumlah_soal', 0)
    session['jumlah_soal'] = jumlah_soal_sejauh_ini + 1

    return render_template('mtk.html', step='hasil',
                           nama_user=nama,
                           total=total,
                           benar=benar_count,
                           salah=salah_count,
                           salah_list=salah_list,
                           durasi_per_soal=durasi_per_soal,
                           status_benar=status_benar, 
                           durasi_7hari_global=durasi_7hari, nomor_soal=session['jumlah_soal'])

