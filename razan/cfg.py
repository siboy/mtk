import pymysql
import mysql.connector 
pymysql.install_as_MySQLdb()
import MySQLdb
import pandas as pd
# import mariadb 
import boto3 
import sys
import os.path
import os
import pathlib
import urllib3
from pathlib import Path
from dotenv import load_dotenv
from minio import Minio
import random
import uuid
from functools import wraps
from pytz import timezone
from datetime import datetime, timedelta
jkt = timezone('Asia/Jakarta') 

from dateutil.relativedelta import relativedelta

import logging
import socket

import traceback
import subprocess
try:
    from obs import ObsClient
except ImportError:
    print("Module obs not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "esdk-obs-python"])
    from obs import ObsClient  # Retry import after installation
    
try:
    import tos
except ImportError:
    print("Module py7zr not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tos"])
    import tos  # Retry import after installation


# os.environ.clear()
# from threading import RLock

# print("load module lengkap " + str(os.path.basename(__file__))+" in folder --> "+ str(os.path.dirname(os.path.realpath(".")))+" dir "+ os.path.basename(__file__))
# ff = str(os.path.basename(__file__))+" ===> "+os.path.join( os.path.dirname(sys.argv[0]), os.path.basename(__file__))
# print("load module lengkap " + str(ff))

# env = os.environ

# if '/var/snap' in os.path.dirname(os.path.realpath(".")): 
#     from konfigurasi import config as env
#     env2 = {kk: str(vv) for kk, vv in env.items()}
#     os.environ.update(env2)    
#     env = os.environ

# if '/var/snap' in os.path.dirname(os.path.realpath(".")): 
#     ifget_env('DB_USER_ac') is None: 
#         from dotenv import load_dotenv
#         from pathlib import Path 
#         dotenv_path = Path('.env')
#         print("-"*66)
#         print(dotenv_path)
#         print("-"*66)
#         load_dotenv(dotenv_path=dotenv_path) 
#         env = os.environ
# else:
# from dotenv import load_dotenv
# from pathlib import Path 
# ff='.env'
# dotenv_path = Path(ff)
# load_dotenv(dotenv_path=dotenv_path) 
# env = os.environ


###reload env
# import os
# os.environ.clear()
# from minio import Minio
# import urllib3
# ff=".env"
# dotenv_path = Path(ff)
# print(ff)
# load_dotenv(dotenv_path=dotenv_path) 
# env = os.environ


# --- 1. Tentukan lokasi .env ---
# Cari .env di beberapa lokasi umum (untuk dev lokal)
# possible_env_paths = [
#     Path(".env"),
#     Path.home() / ".env",
#     Path("/home/script/.env"),
#     Path(os.getenv("FOLDER_DATA", ".")) / ".env",
# ]

# Cari .env di lokasi prioritas
possible_env_paths = [Path(".env")]

# Lokasi khusus container/startup
if os.path.exists("/home/startup/.env"):
    possible_env_paths.append(Path("/home/startup/.env"))
    
# Lokasi khusus container/script
if os.path.exists("/home/script/.env"):
    possible_env_paths.append(Path("/home/script/.env"))

# Lokasi dari env FOLDER_DATA
folder_data = os.getenv("FOLDER_DATA")
if folder_data and os.path.isdir(folder_data):
    possible_env_paths.append(Path(folder_data) / ".env")

# Lokasi home user (opsional, aman)
try:
    home = Path.home()
    home_env = home / ".env"
    if home_env.exists():
        possible_env_paths.append(home_env)
except (RuntimeError, OSError):
    pass  # Tidak bisa tentukan home → skip

env_path = None
for p in possible_env_paths:
    if p.exists():
        env_path = p
        break

# --- 2. Muat .env hanya jika ada (tidak wajib) ---
if env_path:
    print(f"[cfg] Loading .env from: {env_path}")
    load_dotenv(dotenv_path=env_path, override=False)  # override=False: env system > .env

# --- 3. Helper: ambil env dengan fallback aman ---
def get_env(key: str, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise EnvironmentError(f"Environment variable '{key}' is required but not set.")
    return value


# os.environ.clear() to change new env
# userubuntu = os.getenv("HOME").split("/")[-1]
userubuntu = get_env('USER')
# if os.path.exists("/home/script/.env"):
#     ff='/home/script/.env'
#     dotenv_path = Path(ff)
#     print("LINE 45 cfg env di " + ff+ " < ---- > "*4)
# elif os.path.exists(f"/home/{userubuntu}/flask/notebook/data/.env"):
#     ff= f"/home/{userubuntu}/flask/notebook/data/.env"
#     dotenv_path = Path(ff)
#     print("LINE 49 cfg env di " + ff+ " < ---- > "*4)
# else:
#     ff='.env'
#     dotenv_path = Path(ff)
#     print("LINE 53 cfg env di " + ff+ " < ---- > "*4)

modelgemini="gemini-2.0-flash-exp"
modelgemini="gemini-2.5-flash"

def get_container_name():
    return socket.gethostname()

def get_mode():
    return os.getenv("SCHEDULER_MODE", get_container_name())

# dotenv_path = Path(ff)
# load_dotenv(dotenv_path=dotenv_path) 
# env = os.environ
# print(env)

def gethome():
    ff = str(os.getcwd())
    home = str(Path.home())
    if "\\" in home:
        cwd = ff.split("\\")[-1]
        onx= home.split("\\")[-1]+""+cwd
        return onx.replace(" ","")
    else:
        cwd = ff.split("/")[-1]
        onx = home.split("/")[-1]+""+cwd
        return onx.replace(" ","")

headers = {'accept':'application/json', 'Content-Type':'application/json', 'Referer':'https://satudata.kemenag.go.id/dataset/detail/jumlah-rumah-ibadah','User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

def headers(referer='https://www.idx.co.id/'):
    return {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
    f'Referer': {referer},
    f'Origin': {referer},
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }

apikey_bpsus = get_env('apikey_bpsus')
ACCESS_KEY_AWS = get_env('ACCESS_KEY_AWS')
SECRET_KEY_AWS = get_env('SECRET_KEY_AWS')
bucketnas = 'katadata-s3-nas'
bucketdata = 'cdn4.katadata.co.id'
bucketpublic = 'cdn1.katadata.co.id'
remote_grid=get_env('remote_grid')

ACCESS_KEY_obs=get_env('ACCESS_KEY_obs')
SECRET_KEY_obs=get_env('SECRET_KEY_obs')
server_obs =get_env('OBS_SERVER')

kode_prov = [11,12,13,14,15,16,17,18,19,21,31,32,33,34,35,36,51,52,53,61,62,63,64,71,72,73,74,75,81,82,94,91,65,76]
id_cms =get_env('id_cms')
pass_cms =get_env('pass_cms')

host=get_env('DB_HOST')
port = int(get_env('DB_PORT'))
user=get_env('DB_USER')
passwd=get_env('DB_PASSWORD')
database=get_env('DB_NAME')

gemini=get_env('token_gemini')
gemini_dev=get_env('token_gemini_dev')

user_monitoring=get_env('DB_USER_monitoring')
passwd_monitoring=get_env('DB_PASSWORD_monitoring')
host_monitoring=get_env('DB_HOST_monitoring')
port_monitoring = int(get_env('DB_PORT_monitoring'))
database_monitoring=get_env('DB_NAME_monitoring')
# try:
#     port = int(get_env('DB_PORT'))
# except:
#     port = 3306

user_db3=get_env('DB_USER')
passwd_db3=get_env('DB_PASSWORD')

user_ac=get_env('DB_USER_ac')
passwd_ac=get_env('DB_PASSWORD_ac')

user_foto=get_env('DB_USER_foto')
passwd_foto=get_env('DB_PASSWORD_foto')

database_folder =get_env('FOLDER_DATA') + '/sqlite/'
folder_sqlite =get_env('FOLDER_DATA') + '/sqlite/'
chatid =get_env('BOT_TOKEN')
baseurl =get_env('BASE_URL')
    
host_demo=get_env('DB_HOST_demo')
port_demo = int(get_env('DB_PORT_demo'))
user_demo=get_env('DB_USER_demo')
passwd_demo=get_env('DB_PASSWORD_demo')
database_demo=get_env('DB_NAME_demo')

host_dbs=get_env('host_databoks')
port_dbs = int(get_env('port_databoks'))
user_dbs=get_env('user_databoks')
passwd_dbs=get_env('pass_databoks')
database_dbs='databoks' #get_env('database_databoks')

host_docker=get_env('MYSQL_HOST_L')
port_docker= int(get_env('MYSQL_PORT_L'))
user_docker=get_env('MYSQL_USER_L')
passwd_docker=get_env('MYSQL_PASSWORD_L')
data_docker='databoks_development' #get_env('MYSQL_DB_NAME_L')

host_lcl=get_env('MYSQL_HOST_lcl')
port_lcl = int(get_env('MYSQL_PORT_lcl'))
user_lcl=get_env('MYSQL_USER_lcl')
passwd_lcl=get_env('MYSQL_PASSWORD_lcl')
database_lcl=get_env('MYSQL_DB_NAME_lcl')

host_local=get_env('MYSQL_HOST_local')
port_local =get_env('MYSQL_PORT_local')
user_local=get_env('MYSQL_USER_local')
passwd_local=get_env('MYSQL_PASSWORD_local')
database_local=get_env('MYSQL_DB_NAME_local')

##series psotgre
host_series=get_env('POSTGRE_HOST_series')
port_series =get_env('POSTGRE_PORT_series')
user_series=get_env('POSTGRE_USER_series')
passwd_series=get_env('POSTGRE_PASSWORD_series')
database_series=get_env('POSTGRE_DB_NAME_series')

userfb=get_env('FBuser')
passfb=get_env('FBpass')
twtuser=get_env('Twtuser')
twtpass=get_env('Twtpass')
bpsapi_token=get_env('BPS_KEY')

lls = ['World', 'Cura?ao', "C?te d'Ivoire", 'Europe Othr. Nes', 'European Union Nes', 'Area Nes','Serbia and Montenegro','United States Minor Outlying Islands']
premium=['Jawa Barat', 'Lampung', 'Sulawesi Selatan', 'Sumatera Selatan', 'Maluku', 'Jambi', 'Sumatera Utara', 'Nusa Tenggara Timur','Sulawesi Tengah', 'Kalimantan Barat', 'Kalimantan Utara', 'Kalimantan Timur', 'Gorontalo', 'Sumatera Barat',  'Bengkulu', 'Kalimantan Tengah', 'Sulawesi Barat', 'Bali', 'Papua Barat']
replace_values = {"China (RRC - Tiongkok)":"China",
                  "Russian Federation":"Russia",
                  "America":"USA",
                  "Croatia (Hrvatska)":"Croatia",
                  "Réunion":"Reunion",
                  "Brunei Darussalam":"Brunei", 
                  "Virgin Islands (U.S.)":"U.S. Virgin Islands",
                  "Moldova, Republic of":"Moldova",
                  "Bahamas":"The Bahamas",
                  "East Timor":"Timor-Leste",
                  "Iran (Islamic Republic of)":"Iran",
                  "Saint Vincent and The Grenadines":"Saint Vincent and the Grenadines",
                  "Virgin Islands (British)":"British Virgin Islands",
                  "Syrian Arab Republic":"Syria",
                  "Slovak Republic":"Slovakia",
                  "Libyan Arab Jamahiriya":"Libya",
                  "Cape Verde":"Cabo Verde"}

mapinstitusi = {'BKN':'https://www.bkn.go.id/publikasi/statistik-pns/',
    '':'https://wwww.bps.go.id/','bps':'https://wwww.bps.go.id/','BPS':'https://wwww.bps.go.id/','tabel dinamis':'https://wwww.bps.go.id/',
    'OJK':'https://www.ojk.go.id/id/kanal/perbankan/data-dan-statistik/laporan-keuangan-perbankan/Default.aspx',
    'Dikti':'https://pddikti.kemdikbud.go.id/',      
    'BI':'https://www.bi.go.id/',
    'PIHPS BI':'https://www.bi.go.id/hargapangan',
    'PIHPS':'https://www.bi.go.id/hargapangan',
    'Pusat Informasi Harga Pangan Strategis Nasional':'https://www.bi.go.id/hargapangan',
    'bi/hargapangan':'https://www.bi.go.id/hargapangan',
    'PIHPS Nasional':'https://www.bi.go.id/hargapangan',
    'PUPR':'https://data.pu.go.id/search/type/dataset',
    'Kemenkes':'dashboard.kemkes.go.id',
    'Kementan':'https://satudata.pertanian.go.id/',
    'Profil Kesehatan Indonesia':'Profil Kesehatan Indonesia',
    'kemenkes':'https://www.bankdata.depkes.go.id/propinsi/public/report/',
    'Buku Statistik Indonesia':'Buku Statistik Indonesia',
    'Laporan Perekonomian Indonesia':'Laporan Perekonomian Indonesia',
    'Statistika Indonesia':'Statistika Indonesia',
    'Buku Statistik Lingkungan Hidup 2019':'Buku Statistik Lingkungan Hidup',
    'Statistik Keuangan Pemprov':'Statistik Keuangan Pemprov',
    'Provinsi dalam Angka':'Provinsi dalam Angka',
    'Statistik Kesejahteraan Rakyat 2017-2019':'Statistik Kesejahteraan Rakyat',
    '2011-2018':'https://wwww.bps.go.id/',
    'Statistik Pemprov 2018':'Statistik Pemprov',
    'APBD 2018':'https://djpk.kemenkeu.go.id/portal/data/apbd',
    'Statistik Air Bersih 2013-2018':'Statistik Air Bersih',
    'Publikasi Kementerian PU - Statistik Pekerjaan Umum 2013':'Statistik Pekerjaan Umum',
    'Statistik Indonesia 2019':'Statistik Indonesia',
    'Profil Industri Mikro dan Kecil':'Profil Industri Mikro dan Kecil',
    'Profil Industri Mikro dan Kecil 2017-2018':'Profil Industri Mikro dan Kecil',
    'Kementerian Pertanian':'https://satudata.pertanian.go.id/',
    'Direktorat Jenderal Perkebunan':'https://satudata.pertanian.go.id/',
    'statistik keadaan tenaga kerja feb2020':'statistik keadaan tenaga kerja',
    'Sakernas':'statistik Keadaan Angkatan Kerja',
    'statistik Keadaan Angkatan Kerja':'statistik Keadaan Angkatan Kerja',
    'Buku Statistik Kriminal 2019':'Buku Statistik Kriminal',
    'Statistik Indonesia':'Statistik Indonesia',
    'Kemendagri':'https://e-database.kemendagri.go.id/',
    'pv_mahasiswa digital menurut provinsi.csv':'https://pddikti.kemdikbud.go.id/',
    'KLHK':'KLHK',
    'Statistik LHK 2017':'Statistik LHK',
    'Keadaan Angkatan Kerja Feb 2020':'statistik Keadaan Angkatan Kerja',
    'Pusdatin Kementerian PUPR':'Pusdatin Kementerian PUPR',
    'BPS & Kemenkeu':'kemenkeu.go.id',
    'Buku Statistik Indonesia 2019':'Buku Statistik Indonesia',
    'BNPB':'http://bnpb.cloud/dibi/tabel2a',
    'Statistik Lingkungan Hidup 2017-2019':'Statistik Lingkungan Hidup',
    'Statistik Kesehatan 20014-2018':'Statistik Kesehatan',
    'Keadaan Pekerja di Indonesia 2015-2019':'Keadaan Pekerja di Indonesia',
    'Kemenkeu':'kemenkeu.go.id',
    'None':'https://wwww.bps.go.id/',
    'Neraca Perdagangan Provinsi':'https://wwww.bps.go.id/',
    'Statistik Mobilitas Penduduk dan Tenaga Kerja':'Statistik Mobilitas Penduduk dan Tenaga Kerja',
    'Statistik Transportasi Udara':'Statistik Transportasi Udara',
    'Profil kesehatan Indonesia':'Profil kesehatan Indonesia',
    'Statistik Kesejahteraan Rakyat 2015-2019':'Statistik Kesejahteraan Rakyat',
    'Tabel Dinamis':'Tabel Dinamis BPS',
    'Rilis':'Rilis',
    'Statistik Mobilitas penduduk dan pekerja':'Statistik Mobilitas penduduk dan pekerja',
    'Indeks Kualitas Lingkungan Hidup 2015-2018':'Indeks Kualitas Lingkungan Hidup',
    'Statistik Perdagangan Luar Negeri Impor':'Statistik Perdagangan Luar Negeri Impor',
    'tabel Dinamis':'https://wwww.bps.go.id/',
    'Direktorat Jenderal Peternakan dan Kesehatan Hewan':'https://ditjenpkh.pertanian.go.id/',
    'ESDM':'www.migas.esdm.go.id',
    'Buku Statistik Indonesia 2018-2019':'Buku Statistik Indonesia',
    'Kemendag':'https://satudata.kemendag.go.id/',
    'westmetall':'https://www.westmetall.com/en/markdaten.php'}
                  
service_account_api=get_env('service_account_api') 
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
if '/home/irfanfadh43' in os.path.dirname(os.path.realpath(".")):
    executable_path = "/home/irfanfadh43/flask/.wdm/drivers/chromedriver"
    folder = '/home/irfanfadh43/flask/data'
    foldermaster = folder
    chrome = folder+ "/selenium/chromedriver"
    credentials_token  =get_env('credentials_token') 
    chromedriver =get_env('chromedriver')
elif '/opt' in os.path.dirname(os.path.realpath(".")):
    executable_path = "/opt/code/.wdm/drivers/chromedriver"
    folder = '/opt/code/data'
    chrome =get_env('chromedriver')
    foldermaster = folder
    credentials_token  =get_env('credentials_token') 
    chromedriver =get_env('chromedriver')
elif '/content/drive' in os.path.dirname(os.path.realpath(".")):  
    executable_path=r"/content/drive/MyDrive/Colab Notebooks/chrome/chromedriver" 
    folder = r"/content/drive/Othercomputers/Dell/flask/data"
    folder = r"/content/drive/Shareddrives/Tim Data/User/Agus D Darmawan/download/data"
    credentials = r"/content/drive/MyDrive/Colab Notebooks/python/sniping-78972632ad85.json"
    credentials_gsheet = folder+ "/agus/data/"+get_env('credentials_gsheet')
    credentials_token =get_env('credentials_token')
    chrome =get_env('chromedriver')
    memori = "/content/drive/MyDrive/Presentasi/Sync/python/data/training" 
    chrome = "/content/drive/Shareddrives/Tim Data/User/Agus D Darmawan/download/data/chrome"
    foldermaster = folder
    chromedriver =get_env('chromedriver')
else:
    executable_path= f'/home/{userubuntu}/flask/.wdm/drivers/chromedriver'
    folder =get_env('FOLDER_DATA') 
    credentials_gsheet = folder+ "/agus/data/"+get_env('credentials_gsheet')
    credentials_token  =get_env('credentials_token') 
    foldermaster = folder
    chrome =get_env('chromedriver')
    chromedriver =get_env('chromedriver')
    # foldermaster = '/home/ssm-user/.local/pyfile/agus/data'

folderinstalasi = "flask/data"
folder_cache = get_env('FOLDER_CACHE')

# Pastikan folder cache ada
CACHE_DIR = Path(folder_cache)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_TTL = 600  # 10 menit
CACHE_TTL_HOURS = 48  # 2 hari
# folder =get_env('FOLDER_DATA')
# /content/drive/My Drive/Data/training/sms/
cachefile = 10000
# keras_model, keras_token, keras_label
keras_model = f'{folder}/model/model_kategori.keras'
keras_token= f'{folder}/model/tokenizer.pickle'
keras_label= f'{folder}/model/label_text.pickle'

if os.path.exists(folder):
    pass
else:
    path = pathlib.Path(folder)
    path.mkdir(parents=True, exist_ok=True)

# https://github.com/huaweicloud/huaweicloud-sdk-python-obs/issues/31/
obs_client = ObsClient(
    access_key_id=ACCESS_KEY_obs,    
    secret_access_key=SECRET_KEY_obs,
    server= server_obs, is_secure=False
)
# # functions here
# obs_client.close()
    
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY_AWS,
    aws_secret_access_key=SECRET_KEY_AWS
)
s3s = session.resource('s3')

s3 = boto3.client(
        's3', region_name= 'ap-southeast-1',
        aws_access_key_id=ACCESS_KEY_AWS,
        aws_secret_access_key=SECRET_KEY_AWS
    )

# for name in logging.root.manager.loggerDict:
#     print(name)
koneksi_object='tos'
logging.getLogger('tos').setLevel(logging.WARNING)
tosclient = tos.TosClientV2(get_env('TOS_ACCESS_KEY'),
                         get_env('TOS_SECRET_KEY'),
                         get_env('TOS_ENDPOINT'),
                         get_env('TOS_REGION'))

mclo=get_env('DATABASE_VM_HOST')
# print(f"LINE xx :: {mclo}")
# print(f"LINE xx :: {get_env('MINIO_access_key')}")

def s3_minio():
    return Minio(f"{mclo}:{get_env('MINIO_PORT')}",
        #    get_env('MINIO_hostp') +":"+ str(get_env('MINIO_PORT')),
            access_key=get_env('MINIO_access_key') , 
            secret_key=get_env('MINIO_secret_key') ,
            secure=False,
            cert_check=False,
            http_client=urllib3.poolmanager.PoolManager(
                timeout=800,
                retries=urllib3.Retry(
                    total=1,
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504]
                )
            )
    )

mcoo=get_env('SCRAPING_VM_HOST')
# print(f"LINE yy_ :: {mcoo}")
# print(f"PORT ::: {get_env('MINIO_PORT')}")
# print(f"LINE yy_ :: {get_env('MINIO_access_key_contabo')}")
# from minio import Minio

def s3_minio_contabo(koneksi: str = 'docker'):
    host_dict = {
        "local": "localhost",
        "docker": get_env('MINIO_HOST'),
        "remote": get_env('DATABASE_VM_HOST'),
    }
    # print(host_dict)
    credentials = {
        "access_key": get_env('MINIO_ROOT_USER'),
        "secret_key": get_env('MINIO_ROOT_PASSWORD'),
        "hostminiop": f"{host_dict[koneksi]}:{ get_env('MINIO_PORT')}",
    }
    hostp=credentials["hostminiop"]
    # print(credentials)
    # print(hostp)
    return Minio(f"{hostp}",
            access_key=get_env('MINIO_access_key_contabo') , 
            secret_key=get_env('MINIO_secret_key_contabo') ,
            secure=False,
            cert_check=False,
            http_client=urllib3.poolmanager.PoolManager(
                timeout=800,
                retries=urllib3.Retry(
                    total=1,
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504]
                )
            )
    )

log_buffer = []
def log_fct_tomysql(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        status = "SUCCESS"
        message = f"{func.__name__} executed successfully"
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = None
            status = "FAILED"
            message = f"Error in {func.__name__}: {str(e)}"
        finally:
            log_buffer.append((
                func.__name__,
                status,
                message,
                datetime.now()
            ))
        return result
    return wrapper

def flush_logs_to_mysql():
    if not log_buffer:
        return
    try:
        engine = dbse("databoks")
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO logs_fct (function_name, status, message, timestamp)
            VALUES (%s, %s, %s, %s)
        """, log_buffer)
        conn.commit()
    except Exception as e:
        print(f"Batch logging failed: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def pro(database= database):
    return pymysql.connect(
        user = user,
        password = passwd,
        host = host,
        port = port,
        database = database 
    )

def foto():    
    connection = pymysql.connect(
        user = user_foto,
        password = passwd_foto,
        host = host,
        port = port,
        database = database 
    ) 
    cursor = connection.cursor() 
    return connection

def db3(database= database):
    return pymysql.connect(
        user = user,
        password = passwd,
        host = host,
        port = port,
        database = database 
    ) 

def demo():
    return pymysql.connect(
        user = user_demo,
        password = passwd_demo,
        host = host_demo,
        port = int(port_demo),
        database = database_demo 
    ) 

def ac(database= database):
    return pymysql.connect(host = host,
                           user = user,
                           passwd = passwd,
                           db = database,
                           port = port)
    
def ac2(database= database):
    return pymysql.connect(host = host,
                           user = user_ac,
                           passwd = passwd_ac,
                           db = database,
                           port = port)

def dbs(database=database_dbs):
    """
    try:
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = cfg.dbs(os.environ.get('database_dev')) #get_db_de()
        with conn.cursor() as cur:
            sql = f"INSERT INTO de_logs_request (name, url, method, params, body, response, status, created_at) VALUES ('{name}', '{url}', '{method}', '{params}', '{body}', '{response}', '{status}', '{created_at}')"
            cur.execute(sql)
            conn.commit()
            cur.close()
    except Exception as e:
        print(str(e))
        traceback.print_exc()
    """
    return pymysql.connect(user = user_dbs,password = passwd_dbs,host = host_dbs,port = port_dbs,database = database) 

def dbse(database=database_dbs):
    return create_engine('mysql+pymysql://'+ user_dbs +':'+ passwd_dbs +'@'+host_dbs+':'+str(port_dbs)+'/'+database+'', pool_recycle=3600)  

def ace(database= database):
    return create_engine('mysql+pymysql://'+ user_ac +':'+ passwd_ac +'@'+host+':'+str(port)+'/'+database+'', pool_recycle=3600)  

def demoe():
    return create_engine('mysql+pymysql://'+ user_demo +':'+ passwd_demo +'@'+host_demo+':'+str(port_demo)+'/'+database_demo+'', pool_recycle=3600)  

def acdemoe():
    """
    koneksi='acdemoe'
    database=None
    slug='pengeluaran-perkapita-untuk-aneka-barang-dan-jasa-kab-puncak-sebulan-2024'
    q="select id from data_statistik where slug='"+slug+"'"
    print(f"LINE 5450 {q}")
    # df_ids = rzn.selectpd(q, koneksi)
    df_ids=ccg._select_withpandas(q, koneksi, database)
    df_ids
    """
    print(f"LInE cfg 462 ::: acdemoe")
    return create_engine('mysql+pymysql://'+ user_demo +':'+ passwd_demo +'@'+host_demo+':'+str(port_demo)+'/'+database_demo+'', pool_recycle=3600)  

def db3e(database= database):
    return create_engine('mysql+pymysql://'+ user +':'+ passwd +'@'+host+':'+str(port)+'/'+database+'', pool_recycle=3600) 

def proe(database= database):
    return create_engine('mysql+pymysql://'+ user +':'+ passwd +'@'+host+':'+str(port)+'/'+database+'', pool_recycle=3600) 

def local(database= database):
    return MySQLdb.connect(host = 'localhost',
                           user ='root',
                           passwd ='',
                           db = database) 

def locale(database= database_local):
    return create_engine('mysql+pymysql://'+ user_local +':'+ passwd_local +'@'+ host_local +':'+str(port_local)+'/'+ database, pool_recycle=3600) 

def lcs(database= database_local):
    return locale(database= database)

def lcl(database= database_lcl):
    return create_engine('mysql+pymysql://'+user_lcl+':'+passwd_lcl+'@'+host_lcl+':'+str(port_lcl)+'/'+database, pool_recycle=3600)

def lcd_sqlite():
    db_uri = 'sqlite:///'+folder_sqlite+"datasqlite.db"
    engine = create_engine(db_uri)
    return engine.raw_connection()

def lcd(database= data_docker):
    """
    q="DROP TABLE tmp"
    conn = cfg.lcd_sqlite()
    db = conn.cursor()
    db.execute(q)
    print("done") 
    conn.commit()
    conn.close()

    or 

    q="DROP TABLE namoni"
    conn = cfg.lcde_sqlite()
    conn.execute(q)
    print("done") 
    conn.close()
    """
    return pymysql.connect(
            user = user_docker,
            password = passwd_docker,
            host = host_docker,
            port = port_docker,
            database = database ,
            cursorclass=pymysql.cursors.DictCursor
        )
    # try:
    #     return pymysql.connect(
    #         user = user_docker,
    #         password = passwd_docker,
    #         host = host_docker,
    #         port = int(port_docker),
    #         database = data_docker ,
    #         cursorclass=pymysql.cursors.DictCursor
    #     )
    # except:
    #     # sql_lock = RLock()
    #     # try:
    #     #     sql_lock.acquire()
    #     #     session.add(lcd_sqlite)
    #     #     session.commit()
    #     # finally:
    #     #     sql_lock.release()            
    #     return lcd_sqlite

def lcde_sqlite():
    db_uri = 'sqlite:///'+folder_sqlite+"datasqlite.db"
    return create_engine(db_uri)

def lcdbackup():
    return create_engine('mysql+pymysql://'+user_docker+':'+passwd_docker+'@'+host_docker+':'+str(port_docker)+'/backup', pool_recycle=3600)

def cdce():
    return create_engine('mysql+pymysql://'+user_docker+':'+passwd_docker+'@'+host_docker+':'+str(port_docker)+'/cdc', pool_recycle=3600)

def lcde(database= data_docker):
    return create_engine('mysql+pymysql://'+user_docker+':'+passwd_docker+'@'+host_docker+':'+str(port_docker)+'/'+database, pool_recycle=3600)
    # try:
    #     return create_engine('mysql+pymysql://'+user_docker+':'+passwd_docker+'@'+host_docker+':'+str(port_docker)+'/'+data_docker, pool_recycle=3600)
    # except:
    #     return lcde_sqlite()

def dws():
    """
    engine = cfg.dws()
    connection = engine.raw_connection()
    cursor = connection.cursor()
    """
    return create_engine('mysql+pymysql://'+get_env('user_dws')+':'+get_env('pass_dws')+'@'+get_env('host_dws')+':'+str(get_env('port_dws'))+'/'+get_env('database_dws'), pool_recycle=3600) ##, encoding='utf-8'

def series():
    """
    engine = cfg.series()
    connection = engine.raw_connection()
    cursor = connection.cursor()
    """
    return create_engine('postgresql+psycopg2://'+user_series+':'+passwd_series+'@'+host_series+':'+port_series+'/'+database_series, pool_recycle=3600) ##, encoding='utf-8'

def dbf():
    return create_engine('mysql+pymysql://'+get_env('DB_USER_free')+':'+get_env('DB_PASSWORD_free')+'@'+get_env('DB_HOST_free')+':'+str(get_env('DB_PORT_free'))+'/'+get_env('DB_NAME_free'), pool_recycle=3600) 

def byt():
    return create_engine('mysql+pymysql://'+get_env('DB_USER_byteplus')+':'+get_env('DB_PASSWORD_byteplus')+'@'+get_env('DB_HOST_byteplus')+':'+str(get_env('DB_PORT_byteplus'))+'/'+get_env('DB_NAME_byteplus'), pool_recycle=3600)

def byt_select():
    return create_engine('mysql+pymysql://'+get_env('DB_USER_byteplus_select')+':'+get_env('DB_PASSWORD_byteplus_select')+'@'+get_env('DB_HOST_byteplus_select')+':'+str(get_env('DB_PORT_byteplus_select'))+'/'+get_env('DB_NAME_byteplus_select'), pool_recycle=3600) 

def koto():
    return create_engine('mysql+pymysql://'+get_env('DB_USER_koto')+':'+get_env('DB_PASSWORD_koto')+'@'+get_env('DB_HOST_koto')+':'+str(get_env('DB_PORT_koto'))+'/'+get_env('DB_NAME_koto'), pool_recycle=3600) 

def dws_bacth():
    return create_engine('mysql+pymysql://'+get_env('user_dws')+':'+get_env('pass_dws')+'@'+get_env('host_dws')+':'+str(get_env('port_dws'))+'/'+get_env('database_dws'),
    executemany_mode='values',
    executemany_values_page_size=10000, executemany_batch_page_size=500, pool_recycle=3600) ##, encoding='utf-8'

def koneksi(koneksi='pro', database=None):
    if isinstance(koneksi, str): 
        if koneksi: 
            if koneksi=='local':
                if database is None:
                    database= database_local
                conn = local(database)
            elif koneksi=='lokal':
                conn = local(database) 
            elif koneksi=='local_server':
                if database is None:
                    database= database_local
                conn = locale(database)
            elif koneksi=='lcs':
                if database is None:
                    database= database_local
                conn = locale(database)
            elif koneksi=='lokale':
                if database is None:
                    database= database_local
                conn = locale(database) 
            elif koneksi=='lcd':
                if database is None:
                    database= data_docker
                conn = lcd(database)
            elif koneksi=='dbf':
                conn = dbf()
            elif koneksi=='lcde':
                if database is None:
                    database= data_docker
                conn = lcde(database)
            elif koneksi=='db3':
                if database is None:
                    database= get_env('DB_NAME')
                conn = db3(database)
            elif koneksi=='dbs':
                if database is None:
                    database= get_env('DB_NAME')
                conn = dbs(database)
            elif koneksi=='dsc':
                if database is None:
                    database= get_env('database_dev')
                conn = dbs(database)
            elif koneksi=='series':
                conn = series()
            elif koneksi=='dws':
                conn = dws()
            elif koneksi=='pro':
                if database is None:
                    database= get_env('DB_NAME')
                conn = pro(database)
            elif koneksi=='byt':
                conn = byt()
            elif koneksi=='byts':
                conn = byt_select()
            elif koneksi=='demo':
                conn = demo() 
            elif koneksi=='foto':
                conn = foto() 
            elif koneksi=='ac':
                if database is None:
                    database= get_env('DB_NAME')
                conn = ac(database) 
            elif koneksi=='proe':
                if database is None:
                    database= get_env('DB_NAME')
                conn = proe(database)
            elif koneksi=='db3e':
                if database is None:
                    database= get_env('DB_NAME')
                conn = db3e(database)
            elif koneksi=='ace':
                if database is None:
                    database= get_env('DB_NAME')
                conn = ace(database)
            elif koneksi=='demoe':
                conn = demoe() 
            elif koneksi=='acdemoe':
                conn = acdemoe() 
        else:                
            if database is None:
                database= database_local
            conn = local(database)
        return conn
    else:
        return koneksi
def getuid():
    return str(uuid.uuid1().hex)

def monitoring():
    return create_engine(f"postgresql://{user_monitoring}:{passwd_monitoring}@{host_monitoring}:{port_monitoring}/{database_monitoring}")

def mtr():
    return monitoring()

# def pdconn(koneksi='pro', database=None):
#     return create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}") ###postgresql+psycopg2

def pdconn(koneksi='pro', database=None):
    if isinstance(koneksi, str): 
        if koneksi=='db3':
            if database is None:
                database= get_env('DB_NAME')
            conn = create_engine(f"mysql+pymysql://{user_db3}:{passwd_db3}@{host}:{port}/{database}") ###postgresql+psycopg2
        elif koneksi=='pro':
            if database is None:
                database= get_env('DB_NAME')
            conn = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}") ###postgresql+psycopg2
        elif koneksi=='byt':
            conn = byt()
        elif koneksi=='series':
            conn = series()
        elif koneksi=='monitoring':
            conn = monitoring()
        elif koneksi=='byts':
            conn = byt_select()
        elif koneksi=='koto':
            conn = koto()
        elif koneksi=='mtr':
            conn = mtr()
        elif koneksi=='foto':
            conn = fotoe() ###postgresql+psycopg2
        elif koneksi=='local_server':
            if database is None:
                database= database_local
            conn = locale(database) ###postgresql+psycopg2
        elif koneksi=='lcs':
            if database is None:
                database= database_local
            conn = locale(database) ###postgresql+psycopg2
        elif koneksi=='lokale':
            if database is None:
                database= database_local
            conn = locale(database) 
        elif koneksi=='lcd':
            if database is None:
                database= data_docker
            conn = lcde(database) ###postgresql+psycopg2
        elif koneksi=='lcde':
            if database is None:
                database= data_docker
            conn = lcde(database) ###postgresql+psycopg2
        elif koneksi=='cdc':
            conn = cdce() ###postgresql+psycopg2
        elif koneksi=='cdce':
            conn = cdce() ###postgresql+psycopg2
        elif koneksi=='lcdbackup':
            conn = lcdbackup() ###postgresql+psycopg2
        elif koneksi=='lcl':
            if database is None:
                database= database_lcl
            conn = lcl(database) ###postgresql+psycopg2
        elif koneksi=='dws':
            conn = dws() ###postgresql+psycopg2
        elif koneksi=='dbf':
            conn = dbf() ###postgresql+psycopg2
        elif koneksi=='dbs':
            if database is None:
                database= get_env('database_databoks')
            conn = dbse(database) ###postgresql+psycopg2
        elif koneksi=='dsc':
            if database is None:
                database= get_env('database_dev')
            conn = dbse(database) ###postgresql+psycopg2
        elif koneksi=='dbse':
            if database is None:
                database= get_env('database_databoks')
            conn = dbse(database) ###postgresql+psycopg2
        elif koneksi=='ac':
            if database is None:
                database= get_env('DB_NAME')
            conn = create_engine(f"mysql+pymysql://{user_ac}:{passwd_ac}@{host}:{port}/{database}")
        elif koneksi=='demo':
            # conn = create_engine(f"mysql+pymysql://{user_demo}:{passwd_demo}@{host_demo}:{port_demo}/{database_demo}")
            conn = acdemoe()
        elif koneksi=='proe':
            if database is None:
                database= get_env('DB_NAME')
            conn = proe(database)
        elif koneksi=='db3e':
            if database is None:
                database= get_env('DB_NAME')
            conn = db3e(database)
        elif koneksi=='ace':
            if database is None:
                database= get_env('DB_NAME')
            conn = ace(database)
        elif koneksi=='ac':
            if database is None:
                database= get_env('DB_NAME')
            conn = ace(database)
        elif koneksi=='demoe':
            conn = demoe() 
        elif koneksi=='acdemoe':
            conn = acdemoe() 
        else:
            if database is None:
                database= get_env('DB_NAME')
            conn = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}")
        # print(f"LInE cfg 769 {koneksi}")
        return conn
    else:
        if database is None:
            database= get_env('DB_NAME')
        return create_engine(f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}")

    
def fotoe():
    return create_engine(f"mysql+pymysql://{user_foto}:{passwd_foto}@{host}:{port}/{database}")

def select(sql, koneksi = 'pro'):   
    conn = pdconn(koneksi)
    data = pd.read_sql(sql, conn)
    conn.dispose()
    return data

import sqlite3
try:
    from sqlalchemy import create_engine 
except:
    print("Gagal import sqlalchemy create_engine")
    pass
import requests 
# import prettytable as pt
# from telegram.ext import ParseMode
# from telegram.ext import CallbackContext, Updater


#chat_id log_de_katadata // -678681241 

def logs_topik(message, format="html", apps=None, message_thread_id=None):
    """
    cfg.logs_topik("ini nyoba ac", message_thread_id=2)
    ##autocontent -100 message_thread_id 4
    ##cekdata -100 message_thread_id 9
    ##error -100 message_thread_id 8
    ##alert -100 message_thread_id 10
    ##connection -100 message_thread_id 11
    ##CPU usage -100 message_thread_id 12
    ##data tracker -100 message_thread_id 14462
    """
    base_url = baseurl
    if isinstance(message, pd.DataFrame):
        pesan = message.to_html(classes='table table-stripped')
        parameters = {
            "chat_id" : chatid,
            "message_thread_id": message_thread_id,
            "text" : "exec : "+ str(tdy()) +"<p>\n\n<p>"+pesan,
            "parse_mode" : 'html' #ParseMode.MARKDOWN_V2
        }
    else:
        if message_thread_id is None:
            parameters = {
                "chat_id" : chatid,
                "text" : "exec : "+ str(tdy()) +"<p>"+message
            }
        else:
            parameters = {
                "chat_id" : chatid,
                "message_thread_id": message_thread_id,
                "text" : "exec : "+ str(tdy()) +"<p>"+message
            }
    requests.get(base_url, data = parameters)

def logs(pesan, format="html", message_thread_id=None):
    """format html yg diterima 
    messageEntityBold => <b>bold</b>, <strong>bold</strong>, **bold**
    messageEntityItalic => <i>italic</i>, <em>italic</em> *italic*
    messageEntityCode => <code>code</code>, `code`
    messageEntityStrike => <s>strike</s>, <strike>strike</strike>, <del>strike</del>, ~~strike~~
    messageEntityUnderline => <u>underline</u>
    messageEntityPre => <pre language="c++">code</pre>,
    <b>bold</b>, <strong>bold</strong><i>italic</i>, <em>italic</em><u>underline</u>, <ins>underline</ins><s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del><span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler><b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b><a href="http://www.example.com/">inline URL</a><a href="tg://user?id=123456789">inline mention of a user</a><code>inline fixed-width code</code><pre>pre-formatted fixed-width code block</pre><pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>"""
    # base_url = "https://api.telegram.org/bot5452678967:AAEF6k8PTLyNA_u8IPYMVYnpxRjpqSFgiiQ/sendMessage"
    base_url = baseurl
    message = str(pesan)
    if format=="html":
        parameters = {
            "chat_id" : chatid,
            "text" : message +". exec : "+ str(tdy()),
            "parse_mode" : format
        }
    elif format == "log":
        parameters = {
            "chat_id" : chatid,
            "text" : message 
        }
    else:
        parameters = {
            "chat_id" : chatid,
            "text" : message +". exec : "+ str(tdy())
        }
    
    if message_thread_id is None:
        if "DATABASE" in message:
            logs_topik(message, message_thread_id=9)
        elif "gagal runjob" in message:
            logs_topik(message, message_thread_id=8)
        elif "Error on line" in message:
            logs_topik(message, message_thread_id=8)
        elif "transfer" in message:
            logs_topik(message, message_thread_id=8)
        elif "AttributeError" in message:
            logs_topik(message, message_thread_id=8)
        elif "IPTCInfo" in message:
            logs_topik(message, message_thread_id=4227)
        elif "tracker" in message:
            logs_topik(message, message_thread_id=14462)
        elif "cekdata" in message:
            logs_topik(message, message_thread_id=9)
        elif "https" in message:
            logs_topik(message, message_thread_id=4)
        elif "minio" in message:
            logs_topik(message, message_thread_id=11)
        elif "CPU" in message:
            logs_topik(message, message_thread_id=12)
        elif "restart" in message:
            logs_topik(message, message_thread_id=10)
        else:
            requests.get(base_url, data = parameters)
            pass
    else:
        logs_topik(message, message_thread_id= message_thread_id)

def replace_all(text, dic):
    """
    from collections import OrderedDict
    od = OrderedDict([("cat", "dog"), ("dog", "pig")])
    """
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def mysql2sqlite(filesql, datadb = "data.db"):
    """ filesql 'C:/Users/KATADATA INDONESIA/Documents/provinsi.sql' mysql"""
    with open(filesql, 'r') as sql_file:
        sql_script = sql_file.read()
    rplc = {
        "int(11) UNSIGNED NOT NULL AUTO_INCREMENT":"INTEGER PRIMARY KEY AUTOINCREMENT",
        "int(11) NOT NULL AUTO_INCREMENT":"INTEGER PRIMARY KEY AUTOINCREMENT",
        "tinyint(1) NULL DEFAULT NULL COMMENT '1 data satu hari current, 2 data histori'":"INTEGER DEFAULT 1",
        "date NULL DEFAULT NULL":"REAL DEFAULT (datetime('now', 'localtime'))",
        "text CHARACTER SET utf8 COLLATE utf8_general_ci NULL":"TEXT NULL",
        "text CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL":"TEXT NULL",
        "text CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL":"TEXT NULL",
        "varchar(4) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL":"VARCHAR NULL",
        "char(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL":"VARCHAR NULL",
        "char(4) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL":"VARCHAR NULL",
        "varchar(225) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL":"VARCHAR NULL",
        "varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL":"VARCHAR NULL",
        "varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL":"VARCHAR NULL",
        "varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL":"VARCHAR NULL",
        "varchar(225) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL":"VARCHAR NULL"
           }

    newsql = replace_all(sql_script.split(" ENGINE")[0], rplc)
    newsql
    nn = newsql.split(",\n")
    aa = [a for a in nn if ('USING' not in a) and ('INDEX' not in a)]
    acreate = aa[0].split(";\n")[-1].split(" (")[0]
    nsql = ",\n".join(aa) + "\n);"
    nsql

    aset = nsql.split(";")
    nnsql = [a for a in aset if 'SET ' not in a] 
    sql2lite = ";".join(nnsql)
    sql2lite

    db = sqlite3.connect('data/'+datadb)
    cursor = db.cursor()
    cursor.executescript(sql2lite)
    db.commit()
    db.close()
    print(acreate + " DONE")
    nlist = sql_script.split(" ENGINE")[1].replace("\\'","").split(";")[1:-2] 
    qinsert = ";".join(nlist) +";"
    try:
        db = sqlite3.connect('data/'+datadb)
        cursor = db.cursor()
        cursor.executescript(qinsert)
        db.commit()
        db.close()    
        print("INSERT Data ... ")
        print("Done")
        return nsql, nlist
    except:
        print("Insert data gagal")
        return nsql, nlist

def yearsago(from_date=None, years=5):
    if from_date is None:
        from_date = datetime.now()
    return from_date - relativedelta(years=years)

def tdy():
    # cc = datetime.now().astimezone() ##datetime.now(jkt)
    cc = datetime.now(jkt)
    return cc.replace(tzinfo=None)

def last_month(bulan=1):
    txweb = datetime.now() - relativedelta(months=bulan)
    return pd.to_datetime(txweb)

def lastyear(tahun=1):
    return tdy() - relativedelta(years= tahun, month= tdy().month, day=1)

def yst(hari=1):
    cc = datetime.now(jkt)-timedelta(days=hari)
    return cc.replace(tzinfo=None)

def get_folder_server(database="kemkes"): 
    return folder_home(database) 

def folder_home(folder='data'):
    nf= folderinstalasi
    image_path_input = os.path.dirname(os.path.realpath(nf+"/"+folder+"/tes/"))
    path = pathlib.Path(image_path_input)
    path.mkdir(parents=True, exist_ok=True)
    return image_path_input 

def get_folder(database="kemkes"): 
    return folder_home(database)

def get_dirdb(database="data.db"): 
    nf= folder_sqlite ##folderinstalasi+"/sqlite/"
    dbdir = os.path.dirname(os.path.realpath(nf+"/tes/"))  
    return 'sqlite:///'+dbdir+"/"+database

def create_sqlite3(db_file):
    """ create a database connection to a SQLite database """
    db_uri = folder_sqlite+db_file 
    conn = None
    try:
        conn = sqlite3.connect(db_uri)
        print(sqlite3.version)
        print("SUCCESSS ... "+ str(db_uri))
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

def sqll_engine(database="sql_berita.db"):
    """sql_berita.db"""
    db_uri = 'sqlite:///'+folder_sqlite+database 
    return create_engine(db_uri, echo=True) 

def sqll_conn(database="sqlite.db"): 
    """connect to sql_berita.db sqlite.db data.db"""
    engine = sqll_engine(database) 
    return engine.connect() 

def sqll_get_tablename(database="sqlite.db"): 
    nf= folder_sqlite ##folderinstalasi+"/sqlite/"
    dbdir = os.path.dirname(os.path.realpath(nf+"/tes/"))  
    db_uri = 'sqlite:///'+dbdir+"/"+database
    engine = create_engine(db_uri)
    return engine.table_names()

def sqll_select(query, database="sqlite.db"): 
    nf= folder_sqlite ##folderinstalasi+"/sqlite/"
    dbdir = os.path.dirname(os.path.realpath(nf+"/tes/"))  
    db_uri = 'sqlite:///'+dbdir+"/"+database
    print(db_uri)
    engine = create_engine(db_uri)
    rows = engine.execute(query).fetchall()
    available_tables = [{**row} for row in rows]
    return pd.DataFrame(available_tables)

def sqll_schema(tabel, database="sqlite.db"):    
#     cc = sqll_select("select * from "+tabel, database)
#     print(cc.shape)
#     print(cc.head(2))
    ff = sqll_select("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name", database)
    print(ff)
    return ff[ff['name']==tabel]['sql'].values[0]

def sqll_insertdf(df, sqlite_table, database="sqlite.db", action="append"): 
    nf= folder_sqlite ##folderinstalasi+"/sqlite/"
    dbdir = os.path.dirname(os.path.realpath(nf+"/tes/"))  
    db_uri = 'sqlite:///'+dbdir+"/"+database
    
    engine = create_engine(db_uri, echo=True)
    sqlite_connection = engine.connect()
    df.to_sql(sqlite_table, sqlite_connection, if_exists=action, index=False) ##if_exists='fail'
    sqlite_connection.close()
    
def to_dbs(df, sqlite_table, database="data.db", action="append"):
    return sqll_insertdf(df, sqlite_table, database, action)