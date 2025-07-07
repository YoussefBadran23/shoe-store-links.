"""
Product Models for Inventory Management
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    product_styles = relationship("ProductStyle", back_populates="brand")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    parent = relationship("Category", remote_side=[id])
    children = relationship("Category", overlaps="parent")
    product_styles = relationship("ProductStyle", back_populates="category")

class Color(Base):
    __tablename__ = "colors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    hex_code = Column(String(7))  # For future UI color display
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    product_skus = relationship("ProductSKU", back_populates="color")

class Size(Base):
    __tablename__ = "sizes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    sort_order = Column(Integer, default=0)  # For ordering (XS, S, M, L, XL)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    product_skus = relationship("ProductSKU", back_populates="size")

class ProductStyle(Base):
    __tablename__ = "product_styles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    image_path = Column(String(500))  # Path to product image
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Foreign keys
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # Relationships
    brand = relationship("Brand", back_populates="product_styles")
    category = relationship("Category", back_populates="product_styles")
    skus = relationship("ProductSKU", back_populates="style", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ProductStyle(name='{self.name}', brand='{self.brand.name if self.brand else None}')>"

class ProductSKU(Base):
    __tablename__ = "product_skus"
    
    id = Column(Integer, primary_key=True, index=True)
    sku_code = Column(String(50), unique=True, nullable=False, index=True)
    barcode = Column(String(100), unique=True, index=True)  # Manually entered
    
    # Pricing
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    
    # Inventory
    current_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=5)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Foreign keys
    style_id = Column(Integer, ForeignKey("product_styles.id"), nullable=False)
    color_id = Column(Integer, ForeignKey("colors.id"), nullable=False)
    size_id = Column(Integer, ForeignKey("sizes.id"), nullable=False)
    
    # Relationships
    style = relationship("ProductStyle", back_populates="skus")
    color = relationship("Color", back_populates="product_skus")
    size = relationship("Size", back_populates="product_skus")
    stock_movements = relationship("StockMovement", back_populates="product_sku")
    sale_items = relationship("SaleItem", back_populates="product_sku")
    
    @property
    def is_low_stock(self) -> bool:
        """Check if product is below reorder level"""
        return self.current_stock <= self.reorder_level
    
    @property
    def profit_margin(self) -> float:
        """Calculate profit margin percentage"""
        if self.cost_price <= 0:
            return 0.0
        return float((self.selling_price - self.cost_price) / self.cost_price * 100)
    
    @property
    def display_name(self) -> str:
        """Get display name combining style, color, and size"""
        return f"{self.style.name} - {self.color.name} - {self.size.name}"
    
    def generate_sku_code(self) -> str:
        """Generate SKU code based on style, color, and size"""
        from config.settings import BARCODE_PREFIX
        style_code = self.style.name[:3].upper() if self.style else "STY"
        color_code = self.color.name[:2].upper() if self.color else "COL"
        size_code = self.size.name[:2].upper() if self.size else "SZ"
        return f"{BARCODE_PREFIX}{style_code}{color_code}{size_code}{self.id:04d}"
    
    def __repr__(self):
        return f"<ProductSKU(sku_code='{self.sku_code}', stock={self.current_stock})>"