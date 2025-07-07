"""
Settings Model for Application Configuration
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.types import DECIMAL
from decimal import Decimal
from . import Base

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text)
    description = Column(String(500))
    is_system = Column(Boolean, default=False)  # System settings vs user preferences
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    @classmethod
    def get_setting(cls, session, key: str, default_value: str = None):
        """Get a setting value by key"""
        setting = session.query(cls).filter(cls.key == key).first()
        return setting.value if setting else default_value
    
    @classmethod
    def set_setting(cls, session, key: str, value: str, description: str = None, is_system: bool = False):
        """Set a setting value"""
        setting = session.query(cls).filter(cls.key == key).first()
        if setting:
            setting.value = value
            if description:
                setting.description = description
        else:
            setting = cls(
                key=key,
                value=value,
                description=description,
                is_system=is_system
            )
            session.add(setting)
        return setting
    
    def __repr__(self):
        return f"<Settings(key='{self.key}', value='{self.value[:50]}...')>"

class StoreSettings(Base):
    """
    Store-specific settings and configuration
    """
    __tablename__ = "store_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Store information
    store_name = Column(String(200), nullable=False)
    store_address = Column(Text)
    store_phone = Column(String(50))
    store_email = Column(String(100))
    store_website = Column(String(200))
    tax_number = Column(String(50))
    
    # Receipt settings
    receipt_header = Column(Text)
    receipt_footer = Column(Text)
    logo_path = Column(String(500))
    
    # Tax settings
    tax_rate = Column(DECIMAL(5, 2), default=0)
    tax_included = Column(Boolean, default=False)
    
    # Currency settings
    currency_code = Column(String(3), default="EGP")
    currency_symbol = Column(String(5), default="ج.م")
    decimal_places = Column(Integer, default=2)
    
    # Business hours
    opening_time = Column(String(8))  # HH:MM:SS format
    closing_time = Column(String(8))  # HH:MM:SS format
    business_days = Column(String(20), default="1,2,3,4,5,6,7")  # Comma-separated days (1=Monday)
    
    # Printer settings
    receipt_printer_name = Column(String(100))
    label_printer_name = Column(String(100))
    receipt_width = Column(Integer, default=58)  # mm
    
    # Return policy
    return_policy_days = Column(Integer, default=7)
    return_policy_text = Column(Text)
    
    # Inventory settings
    low_stock_threshold = Column(Integer, default=10)
    auto_generate_sku = Column(Boolean, default=True)
    require_barcode = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<StoreSettings(store_name='{self.store_name}')>"