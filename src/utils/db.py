import os
import logging
import sqlite3
import hashlib
import base64
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage")
DB_PATH = os.path.join(STORAGE_DIR, "passwords.db")
MASTER_KEY = "myPassw0rd*1"

# Salt hardcodeado para derivar clave
SALT = b'Xy7s3l9kPm2qR8tU'

def _ensure_storage():
    """Crear directorio storage si no existe"""
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

def _derive_key() -> bytes:
    """Derivar clave de cifrado desde master_key"""
    raw = hashlib.pbkdf2_hmac(
        'sha256',
        MASTER_KEY.encode(),
        SALT,
        iterations=100000,
        dklen=32
    )
    return base64.urlsafe_b64encode(raw)

def init_db():
    """Inicializar base de datos"""
    try:
        _ensure_storage()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER NOT NULL PRIMARY KEY,
                key TEXT NOT NULL,
                value TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error("Error al inicializar BD: %s", e)

def save_password(password: str):
    """Guardar password cifrado con master_key"""
    try:
        key = _derive_key()
        f = Fernet(key)
        encrypted = f.encrypt(password.encode())
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO config (id, key, value) VALUES (?, ?, ?)", (1, "password", encrypted.decode()))
        conn.commit()
        conn.close()
        logger.info("Password guardado correctamente")
    except Exception as e:
        logger.error("Error al guardar password: %s", e)

def get_password() -> str | None:
    """Recuperar password descifrado con master_key"""
    if not os.path.exists(DB_PATH):
        return None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM config WHERE id = ?", (1,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        key = _derive_key()
        f = Fernet(key)
        password = f.decrypt(row[0].encode()).decode()
        logger.info("Password descifrado correctamente")
        return password
    except Exception as e:
        logger.error("Error al descifrar password: %s", e)
        return None

def has_password() -> bool:
    """Verificar si existe password guardado"""
    if not os.path.exists(DB_PATH):
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM config WHERE id = ?", (1,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def delete_all():
    """Eliminar base de datos"""
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            logger.info("Base de datos eliminada")
    except Exception as e:
        logger.error("Error al eliminar BD: %s", e)