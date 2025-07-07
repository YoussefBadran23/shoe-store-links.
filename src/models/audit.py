"""
Audit Log Model for Tracking System Changes
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from . import Base

class AuditAction(enum.Enum):
    # User actions
    LOGIN = "login"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    
    # Product actions
    PRODUCT_CREATE = "product_create"
    PRODUCT_UPDATE = "product_update"
    PRODUCT_DELETE = "product_delete"
    
    # Stock actions
    STOCK_ADJUSTMENT = "stock_adjustment"
    STOCK_ADD = "stock_add"
    STOCK_REMOVE = "stock_remove"
    
    # Sales actions
    SALE_CREATE = "sale_create"
    SALE_VOID = "sale_void"
    SALE_RETURN = "sale_return"
    
    # Settings actions
    SETTINGS_UPDATE = "settings_update"
    PRINTER_CONFIG = "printer_config"
    
    # System actions
    DATABASE_BACKUP = "database_backup"
    SYSTEM_RESTART = "system_restart"

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Action details
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    entity_type = Column(String(50))  # e.g., "Product", "Sale", "User"
    entity_id = Column(String(50))    # ID of the affected entity
    
    # Change details
    description = Column(String(500), nullable=False)
    old_values = Column(Text)         # JSON string of old values
    new_values = Column(Text)         # JSON string of new values
    
    # Request details
    ip_address = Column(String(45))   # IPv4 or IPv6
    user_agent = Column(String(500))
    
    # Timestamps
    timestamp = Column(DateTime, server_default=func.now(), index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    @classmethod
    def log_action(cls, session, user_id: int, action: AuditAction, 
                   description: str, entity_type: str = None, 
                   entity_id: str = None, old_values: str = None, 
                   new_values: str = None, ip_address: str = None):
        """
        Create an audit log entry
        """
        log_entry = cls(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address
        )
        session.add(log_entry)
        return log_entry
    
    def __repr__(self):
        return f"<AuditLog(action='{self.action.value}', user_id={self.user_id}, timestamp='{self.timestamp}')>"