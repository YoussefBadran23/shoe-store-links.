"""
Database Models Package
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL, DATABASE_ECHO

# Create database engine
engine = create_engine(DATABASE_URL, echo=DATABASE_ECHO)

# Create declarative base
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Initialize database by creating all tables"""
    # Import all models to ensure they are registered
    from .user import User, Role
    from .product import Brand, Category, Color, Size, ProductStyle, ProductSKU
    from .sales import Sale, SaleItem, Payment
    from .stock import StockMovement, StockAdjustment
    from .returns import Return, ReturnItem
    from .audit import AuditLog
    from .settings import Settings, StoreSettings
    
    Base.metadata.create_all(bind=engine)

def get_session():
    """Get database session"""
    session = SessionLocal()
    try:
        return session
    except Exception:
        session.close()
        raise

# Import all models for easy access
from .user import User, Role, UserRole
from .product import Brand, Category, Color, Size, ProductStyle, ProductSKU
from .sales import Sale, SaleItem, Payment, PaymentMethod, SaleStatus
from .stock import StockMovement, StockAdjustment, MovementType
from .returns import Return, ReturnItem, ReturnReason, ReturnStatus
from .audit import AuditLog, AuditAction
from .settings import Settings, StoreSettings

__all__ = [
    'Base', 'engine', 'SessionLocal', 'init_database', 'get_session',
    'User', 'Role', 'UserRole',
    'Brand', 'Category', 'Color', 'Size', 'ProductStyle', 'ProductSKU',
    'Sale', 'SaleItem', 'Payment', 'PaymentMethod', 'SaleStatus',
    'StockMovement', 'StockAdjustment', 'MovementType',
    'Return', 'ReturnItem', 'ReturnReason', 'ReturnStatus',
    'AuditLog', 'AuditAction',
    'Settings', 'StoreSettings'
]