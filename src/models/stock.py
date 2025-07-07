"""
Stock Movement and Inventory Tracking Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from . import Base

class MovementType(enum.Enum):
    STOCK_IN = "stock_in"           # Manual stock addition
    STOCK_OUT = "stock_out"         # Manual stock removal
    SALE = "sale"                   # Stock reduction from sale
    RETURN = "return"               # Stock increase from return
    ADJUSTMENT = "adjustment"       # Stock adjustment (positive or negative)
    DAMAGE = "damage"               # Stock marked as damaged
    TRANSFER = "transfer"           # Stock transfer (future use)

class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Movement details
    movement_type = Column(SQLEnum(MovementType), nullable=False)
    quantity_change = Column(Integer, nullable=False)  # Positive for increase, negative for decrease
    previous_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)
    
    # Reference details
    reference_number = Column(String(100))  # Receipt number, adjustment reference, etc.
    reason = Column(String(200))            # Reason for manual adjustments
    notes = Column(Text)
    
    # Cost tracking
    unit_cost = Column(DECIMAL(10, 2))      # Cost per unit for this movement
    total_value = Column(DECIMAL(10, 2))    # Total value of movement
    
    # Timestamps
    movement_date = Column(DateTime, server_default=func.now(), index=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Foreign keys
    product_sku_id = Column(Integer, ForeignKey("product_skus.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who made the change
    
    # Relationships
    product_sku = relationship("ProductSKU", back_populates="stock_movements")
    user = relationship("User")
    
    @property
    def is_increase(self) -> bool:
        """Check if this movement increases stock"""
        return self.quantity_change > 0
    
    @property
    def is_decrease(self) -> bool:
        """Check if this movement decreases stock"""
        return self.quantity_change < 0
    
    def __repr__(self):
        direction = "+" if self.is_increase else ""
        return f"<StockMovement(sku='{self.product_sku.sku_code}', change={direction}{self.quantity_change})>"

class StockAdjustment(Base):
    """
    Batch stock adjustments for multiple SKUs at once
    """
    __tablename__ = "stock_adjustments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Adjustment details
    adjustment_number = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    reason = Column(Text)
    
    # Status
    is_finalized = Column(Boolean, default=False)
    
    # Timestamps
    adjustment_date = Column(DateTime, server_default=func.now())
    finalized_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    
    # Foreign keys
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    finalized_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    finalizer = relationship("User", foreign_keys=[finalized_by])
    
    def generate_adjustment_number(self) -> str:
        """Generate unique adjustment number"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"ADJ{timestamp}{self.id:04d}"
    
    def __repr__(self):
        return f"<StockAdjustment(number='{self.adjustment_number}', finalized={self.is_finalized})>"