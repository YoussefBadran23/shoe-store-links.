"""
Returns and Exchanges Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from . import Base

class ReturnReason(enum.Enum):
    DEFECTIVE = "defective"
    WRONG_SIZE = "wrong_size"
    WRONG_COLOR = "wrong_color"
    CUSTOMER_CHANGE_MIND = "customer_change_mind"
    DAMAGED_IN_TRANSIT = "damaged_in_transit"
    NOT_AS_DESCRIBED = "not_as_described"
    OTHER = "other"

class ReturnStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"

class Return(Base):
    __tablename__ = "returns"
    
    id = Column(Integer, primary_key=True, index=True)
    return_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Return details
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    refund_amount = Column(DECIMAL(10, 2), nullable=False)
    
    # Status and reason
    status = Column(SQLEnum(ReturnStatus), default=ReturnStatus.PENDING)
    reason = Column(SQLEnum(ReturnReason), nullable=False)
    customer_notes = Column(Text)
    staff_notes = Column(Text)
    
    # Timestamps
    return_date = Column(DateTime, server_default=func.now(), index=True)
    processed_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Foreign keys
    original_sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    processed_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    original_sale = relationship("Sale", back_populates="returns")
    processor = relationship("User")
    items = relationship("ReturnItem", back_populates="return_transaction", cascade="all, delete-orphan")
    
    @property
    def total_items(self) -> int:
        """Calculate total quantity of items being returned"""
        return sum(item.quantity for item in self.items)
    
    @property
    def days_since_purchase(self) -> int:
        """Calculate days since original purchase"""
        if self.original_sale and self.original_sale.sale_date:
            return (self.return_date - self.original_sale.sale_date).days
        return 0
    
    def generate_return_number(self) -> str:
        """Generate unique return number"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"RET{timestamp}{self.id:04d}"
    
    def can_be_processed(self) -> bool:
        """Check if return can be processed"""
        return self.status == ReturnStatus.PENDING
    
    def __repr__(self):
        return f"<Return(number='{self.return_number}', amount={self.refund_amount}, status='{self.status.value}')>"

class ReturnItem(Base):
    __tablename__ = "return_items"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Item details
    quantity = Column(Integer, nullable=False)
    original_unit_price = Column(DECIMAL(10, 2), nullable=False)  # Price from original sale
    refund_unit_price = Column(DECIMAL(10, 2), nullable=False)    # Actual refund price (may be different)
    line_total = Column(DECIMAL(10, 2), nullable=False)
    
    # Item condition
    is_damaged = Column(Boolean, default=False)
    return_to_stock = Column(Boolean, default=True)  # Whether to return to sellable stock
    condition_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Foreign keys
    return_id = Column(Integer, ForeignKey("returns.id"), nullable=False)
    product_sku_id = Column(Integer, ForeignKey("product_skus.id"), nullable=False)
    original_sale_item_id = Column(Integer, ForeignKey("sale_items.id"))  # Reference to original sale item
    
    # Relationships
    return_transaction = relationship("Return", back_populates="items")
    product_sku = relationship("ProductSKU")
    original_sale_item = relationship("SaleItem")
    
    @property
    def refund_difference(self) -> float:
        """Calculate difference between original price and refund price"""
        return float(self.original_unit_price - self.refund_unit_price) * self.quantity
    
    def __repr__(self):
        return f"<ReturnItem(sku='{self.product_sku.sku_code}', qty={self.quantity}, refund={self.line_total})>"