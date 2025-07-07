"""
Application Configuration Settings
"""
import os
from pathlib import Path

# Application Info
APP_NAME = "RetailPOS"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Your Store Name"

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
TRANSLATIONS_DIR = ASSETS_DIR / "translations"

# Database
DATABASE_URL = f"sqlite:///{DATA_DIR}/pos_database.db"
DATABASE_ECHO = False  # Set to True for SQL logging

# Printer Settings
RECEIPT_PRINTER_NAME = "XP-233B"  # ESC/POS receipt printer
LABEL_PRINTER_NAME = "XP-80C"    # Label printer
PRINTER_ENCODING = "utf-8"

# Currency
CURRENCY_CODE = "EGP"
CURRENCY_SYMBOL = "ج.م"
DECIMAL_PLACES = 2

# UI Settings
DEFAULT_LANGUAGE = "ar"  # Arabic
FALLBACK_LANGUAGE = "en"  # English
UI_THEME = "dark"

# Security
PASSWORD_MIN_LENGTH = 6
SESSION_TIMEOUT_MINUTES = 480  # 8 hours
MAX_LOGIN_ATTEMPTS = 3

# Business Rules
LOW_STOCK_THRESHOLD = 10
RECEIPT_COPY_COUNT = 1
BARCODE_PREFIX = "SKU"

# File Paths
def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in [DATA_DIR, LOGS_DIR, IMAGES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'app.log',
            'mode': 'a',
        },
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}