from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Mtk(db.Model):
    __tablename__ = 'mtk'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), nullable=False, index=True)
    nama_user = db.Column(db.String(100), nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=False)
    tanggal_mengerjakan = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    soal = db.Column(db.String(50), nullable=False)
    jawaban_user = db.Column(db.String(20), nullable=False)
    kunci_jawaban = db.Column(db.Integer, nullable=False)
    durasi_jawab = db.Column(db.Float, nullable=False)
    durasi_total = db.Column(db.Float, nullable=False)
    benar = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Mtk {self.session_id} - {self.soal}>'