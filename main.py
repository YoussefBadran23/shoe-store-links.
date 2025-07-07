#!/usr/bin/env python3
"""
RetailPOS - Main Application Entry Point
"""
import sys
import logging
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale
from config.settings import ensure_directories, LOGGING_CONFIG, DEFAULT_LANGUAGE, TRANSLATIONS_DIR
from src.models import init_database

def setup_logging():
    """Setup application logging"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Application starting...")
    return logger

def setup_translations(app: QApplication):
    """Setup application translations"""
    translator = QTranslator()
    
    # Load translation file based on default language
    if DEFAULT_LANGUAGE == "ar":
        translation_file = TRANSLATIONS_DIR / "retail_pos_ar.qm"
        if translation_file.exists():
            translator.load(str(translation_file))
            app.installTranslator(translator)
    
    return translator

def main():
    """Main application function"""
    try:
        # Ensure required directories exist
        ensure_directories()
        
        # Setup logging
        logger = setup_logging()
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("RetailPOS")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Your Store Name")
        
        # Setup translations
        translator = setup_translations(app)
        
        # Initialize database
        logger.info("Initializing database...")
        init_database()
        
        # TODO: Setup main window and services
        # from src.ui.main_window import MainWindow
        # from src.services.auth_service import AuthService
        
        # window = MainWindow()
        # window.show()
        
        # Temporary: Show a simple message
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("RetailPOS")
        msg.setText("Database initialized successfully!\n\nNext steps:\n- Create service layer\n- Build UI components\n- Setup authentication")
        msg.exec()
        
        logger.info("Application started successfully")
        return 0  # app.exec() when UI is ready
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())