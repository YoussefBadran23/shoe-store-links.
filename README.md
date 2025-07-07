# RetailPOS - Inventory & Point of Sale System

A comprehensive desktop Point of Sale and Inventory Management application built with Python and PySide6.

## 🚀 Project Status

**✅ Database Layer Complete**
- SQLAlchemy models for all entities
- Authentication and authorization system
- Audit logging functionality
- Multi-role user management

**🔧 In Progress**
- Service layer development
- PySide6 UI components
- Printer integration
- Localization support

## 📋 Features

### Core Functionality
- **No barcode scanner** - Manual entry only
- **Manual cash drawer** - No software control
- **Arabic UI** with English receipts/labels
- **Offline-first** SQLite database
- **Multi-user support** with role-based permissions

### User Roles
- **Admin**: Full system access
- **Manager**: Product management, reports, sales
- **Cashier**: Sales and returns only

### Inventory Management
- Product styles with multiple SKUs (color/size combinations)
- Stock movement tracking
- Low stock alerts
- Manual stock adjustments
- Brand and category management

### Point of Sale
- Product search by name, category, or SKU
- Manual price override and discounts
- Multiple payment methods (cash, card, mobile)
- Receipt printing via XP-233B
- Manual cash drawer operation

### Returns & Exchanges
- Return by receipt number
- Cash refunds only
- Stock return or damage marking
- Return reason tracking

### Reporting
- Z-Report (end of day summary)
- Sales reports by period/product/cashier
- Inventory reports and valuation
- Profit tracking and analysis

### Printer Integration
- **XP-233B**: ESC/POS receipt printer
- **XP-80C**: Barcode label printer
- English-only output formatting

## 🏗️ Project Structure

```
RetailPOS/
├── src/
│   ├── models/          # SQLAlchemy database models
│   │   ├── __init__.py  # Database setup and imports
│   │   ├── user.py      # User and Role models
│   │   ├── product.py   # Product, Brand, Category, SKU models
│   │   ├── sales.py     # Sale, SaleItem, Payment models
│   │   ├── stock.py     # StockMovement, StockAdjustment models
│   │   ├── returns.py   # Return and ReturnItem models
│   │   ├── audit.py     # AuditLog model
│   │   └── settings.py  # Settings and StoreSettings models
│   ├── services/        # Business logic services
│   │   ├── __init__.py
│   │   └── auth_service.py  # Authentication service
│   ├── ui/              # PySide6 UI components (TODO)
│   └── utils/           # Utility functions (TODO)
├── config/
│   └── settings.py      # Application configuration
├── assets/
│   ├── images/          # Product images, logos
│   ├── icons/           # UI icons
│   └── translations/    # Arabic translation files
├── data/                # SQLite database location
├── logs/                # Application logs
├── venv/                # Python virtual environment
├── requirements.txt     # Python dependencies
├── main.py              # Application entry point
├── test_setup.py        # Database and functionality tests
└── README.md            # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.13+
- Ubuntu/Linux environment
- System packages for Qt (for GUI when needed)

### Installation

1. **Clone and navigate to project:**
   ```bash
   cd /workspace  # or your project directory
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test setup:**
   ```bash
   python test_setup.py
   ```

5. **Run application (when UI is ready):**
   ```bash
   python main.py
   ```

## 🗄️ Database Schema

### Core Entities
- **Users & Roles**: Authentication and authorization
- **Products**: Hierarchical product management (Style → SKU)
- **Sales**: Transaction processing and payment tracking
- **Stock**: Inventory movement and adjustment tracking
- **Returns**: Return and exchange processing
- **Audit**: Complete system activity logging
- **Settings**: Configurable application settings

### Key Relationships
- User → Role (many-to-one)
- ProductStyle → Brand, Category (many-to-one)
- ProductSKU → ProductStyle, Color, Size (many-to-one)
- Sale → User (cashier), SaleItems, Payments (one-to-many)
- StockMovement → ProductSKU, User (many-to-one)

## 🔐 Security Features

- **Password hashing** with bcrypt
- **Failed login attempt tracking**
- **Account locking** after multiple failures
- **Role-based permissions** for all operations
- **Comprehensive audit logging** for all changes
- **Session management** with timeout

## 📊 Test Results

Latest test run shows all systems working:

✅ Database models created  
✅ Authentication service working  
✅ Default roles created  
✅ Admin user created  
✅ Login/logout functionality working  
✅ Model relationships working correctly  

**Default Admin Account:**
- Username: `admin`
- Password: `admin123`
- Role: System Administrator

## 🔄 Development Workflow

1. **Database Layer** ✅ Complete
2. **Service Layer** 🔧 In Progress
3. **UI Components** 📋 Planned
4. **Printer Integration** 📋 Planned
5. **Localization** 📋 Planned
6. **Testing & QA** 📋 Planned
7. **Packaging** 📋 Planned

## 📝 Next Steps

### Immediate (Service Layer)
- [ ] ProductService for catalog management
- [ ] SaleService for POS operations
- [ ] StockService for inventory management
- [ ] ReturnService for returns processing
- [ ] ReportService for analytics

### Short Term (UI Layer)
- [ ] Login screen
- [ ] Main dashboard
- [ ] Product management screens
- [ ] POS interface
- [ ] Reports interface

### Medium Term (Integration)
- [ ] ESC/POS printer driver
- [ ] Label printer integration
- [ ] Arabic localization
- [ ] Data export/import

### Long Term (Polish)
- [ ] PyInstaller packaging
- [ ] Installer creation
- [ ] User documentation
- [ ] Training materials

## 🤝 Contributing

This is a single-developer project following the detailed task breakdown provided. The architecture supports future expansion and maintenance.

## 📄 License

Private project for retail store implementation.

---

**Built with:** Python 3.13, SQLAlchemy 2.0, PySide6, SQLite  
**Target Platform:** Windows Desktop  
**Language Support:** Arabic UI, English receipts  
**Architecture:** Offline-first, role-based, audit-logged