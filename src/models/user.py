"""
User and Role Models for Authentication and Authorization
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from passlib.hash import bcrypt
import enum
from . import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CASHIER = "cashier"

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(SQLEnum(UserRole), unique=True, nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    
    # Permissions
    can_manage_users = Column(Boolean, default=False)
    can_manage_products = Column(Boolean, default=False)
    can_process_sales = Column(Boolean, default=True)
    can_process_returns = Column(Boolean, default=False)
    can_view_reports = Column(Boolean, default=False)
    can_manage_settings = Column(Boolean, default=False)
    can_edit_prices = Column(Boolean, default=False)
    can_void_transactions = Column(Boolean, default=False)
    
    # Relationships
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100), nullable=False)
    password_hash = Column(String(128), nullable=False)
    
    # Status and security
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    last_login = Column(DateTime)
    password_changed_at = Column(DateTime, server_default=func.now())
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Foreign keys
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    sales = relationship("Sale", back_populates="cashier")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def set_password(self, password: str):
        """Hash and set password"""
        self.password_hash = bcrypt.hash(password)
        self.password_changed_at = func.now()
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.verify(password, self.password_hash)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        if not self.is_active or not self.role:
            return False
        return getattr(self.role, permission, False)
    
    def reset_failed_attempts(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0
    
    def increment_failed_attempts(self):
        """Increment failed login attempts"""
        self.failed_login_attempts += 1
    
    def is_locked(self) -> bool:
        """Check if account is locked due to failed attempts"""
        from config.settings import MAX_LOGIN_ATTEMPTS
        return self.failed_login_attempts >= MAX_LOGIN_ATTEMPTS
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role.name if self.role else None}')>"