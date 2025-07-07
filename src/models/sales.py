"""
Sales and Transaction Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DECIMAL
import enum
from . import Base

class PaymentMethod(enum.Enum):
    CASH = "cash"
    CARD = "card"
    MOBILE_WALLET = "mobile_wallet"

class SaleStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    VOIDED = "voided"
    RETURNED = "returned"

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    receipt_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Sale details
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    discount_amount = Column(DECIMAL(10, 2), default=0)
    discount_percentage = Column(DECIMAL(5, 2), default=0)
    tax_amount = Column(DECIMAL(10, 2), default=0)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    
    # Payment details
    amount_paid = Column(DECIMAL(10, 2), nullable=False)
    change_amount = Column(DECIMAL(10, 2), default=0)
    
    # Status and timestamps
    status = Column(SQLEnum(SaleStatus), default=SaleStatus.PENDING)
    sale_date = Column(DateTime, server_default=func.now(), index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Notes
    notes = Column(Text)
    
    # Foreign keys
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    cashier = relationship("User", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="sale", cascade="all, delete-orphan")
    returns = relationship("Return", back_populates="original_sale")
    
    @property
    def total_items(self) -> int:
        """Calculate total quantity of items in sale"""
        return sum(item.quantity for item in self.items)
    
    @property
    def total_profit(self) -> float:
        """Calculate total profit from this sale"""
        return sum(item.profit for item in self.items)
    
    def generate_receipt_number(self) -> str:
        """Generate unique receipt number"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"REC{timestamp}{self.id:04d}"
    
    def can_be_returned(self) -> bool:
        """Check if sale can be returned"""
        return self.status == SaleStatus.COMPLETED
    
    def __repr__(self):
        return f"<Sale(receipt_number='{self.receipt_number}', total={self.total_amount})>"

class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Item details
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)  # Price at time of sale
    unit_cost = Column(DECIMAL(10, 2), nullable=False)   # Cost at time of sale
    discount_amount = Column(DECIMAL(10, 2), default=0)
    line_total = Column(DECIMAL(10, 2), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Foreign keys
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_sku_id = Column(Integer, ForeignKey("product_skus.id"), nullable=False)
    
    # Relationships
    sale = relationship("Sale", back_populates="items")
    product_sku = relationship("ProductSKU", back_populates="sale_items")
    
    @property
    def profit(self) -> float:
        """Calculate profit for this line item"""
        return float((self.unit_price - self.unit_cost - self.discount_amount) * self.quantity)
    
    @property
    def profit_margin(self) -> float:
        """Calculate profit margin percentage for this item"""
        if self.unit_cost <= 0:
            return 0.0
        effective_price = self.unit_price - (self.discount_amount / self.quantity if self.quantity > 0 else 0)
        return float((effective_price - self.unit_cost) / self.unit_cost * 100)
    
    def __repr__(self):
        return f"<SaleItem(sku='{self.product_sku.sku_code}', qty={self.quantity}, total={self.line_total})>"

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Payment details
    method = Column(SQLEnum(PaymentMethod), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    reference_number = Column(String(100))  # For card/mobile payments
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Foreign keys
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    
    # Relationships
    sale = relationship("Sale", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(method='{self.method.value}', amount={self.amount})>"