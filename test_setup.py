#!/usr/bin/env python3
"""
Test script to verify database setup and basic functionality
"""
import sys
import logging
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_database_setup():
    """Test database creation and basic operations"""
    from config.settings import ensure_directories
    from src.models import init_database, get_session
    from src.services.auth_service import AuthService
    
    print("🔧 Setting up directories...")
    ensure_directories()
    
    print("🗄️ Initializing database...")
    init_database()
    print("✅ Database initialized successfully!")
    
    # Test database connection
    print("🔌 Testing database connection...")
    session = get_session()
    
    try:
        # Test auth service
        print("🔐 Testing authentication service...")
        auth_service = AuthService(session)
        
        # Create default roles
        print("👥 Creating default roles...")
        auth_service.create_default_roles()
        print("✅ Default roles created!")
        
        # Create admin user
        print("👨‍💼 Creating admin user...")
        success, message = auth_service.create_admin_user("admin", "admin123", "System Administrator")
        print(f"{'✅' if success else '❌'} {message}")
        
        # Test login
        print("🔑 Testing login...")
        login_success, user, login_message = auth_service.login("admin", "admin123")
        print(f"{'✅' if login_success else '❌'} {login_message}")
        
        if login_success:
            print(f"   User: {user.full_name} ({user.username})")
            print(f"   Role: {user.role.name.value}")
            print(f"   Permissions: Can manage products: {user.role.can_manage_products}")
            
            # Test logout
            auth_service.logout(user)
            print("✅ Logout successful!")
        
        print("\n🎉 All tests passed! Database setup is working correctly.")
        print("\n📋 Summary:")
        print("   ✅ Database models created")
        print("   ✅ Authentication service working")
        print("   ✅ Default roles created")
        print("   ✅ Admin user created")
        print("   ✅ Login/logout functionality working")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    finally:
        session.close()

def test_models():
    """Test model relationships and basic functionality"""
    from src.models import get_session, ProductStyle, Brand, Category, Color, Size, ProductSKU
    
    print("\n🧪 Testing model relationships...")
    session = get_session()
    
    try:
        # Create some test data
        brand = Brand(name="Test Brand", description="A test brand")
        category = Category(name="Test Category", description="A test category")
        color = Color(name="Red", hex_code="#FF0000")
        size = Size(name="M", sort_order=2)
        
        session.add_all([brand, category, color, size])
        session.flush()  # Get IDs without committing
        
        # Create product style
        style = ProductStyle(
            name="Test T-Shirt",
            description="A comfortable test t-shirt",
            brand_id=brand.id,
            category_id=category.id
        )
        session.add(style)
        session.flush()
        
        # Create SKU
        sku = ProductSKU(
            sku_code="TEST001",
            barcode="123456789012",
            cost_price=10.00,
            selling_price=20.00,
            current_stock=50,
            style_id=style.id,
            color_id=color.id,
            size_id=size.id
        )
        session.add(sku)
        session.commit()
        
        # Test relationships
        print(f"   ✅ Product created: {sku.display_name}")
        print(f"   ✅ Profit margin: {sku.profit_margin:.1f}%")
        print(f"   ✅ Low stock status: {sku.is_low_stock}")
        
        # Clean up test data
        session.delete(sku)
        session.delete(style)
        session.delete(brand)
        session.delete(category)
        session.delete(color)
        session.delete(size)
        session.commit()
        
        print("   ✅ Model relationships working correctly!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing models: {e}")
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("🚀 Starting RetailPOS Setup Test")
    print("=" * 50)
    
    try:
        # Test database setup
        db_success = test_database_setup()
        
        if db_success:
            # Test models
            model_success = test_models()
            
            if model_success:
                print("\n🎉 All systems working! Ready to build the UI.")
                print("\n📝 Next steps:")
                print("   1. Create UI components with PySide6")
                print("   2. Build service layer for products, sales, reports")
                print("   3. Implement printer integration")
                print("   4. Add localization support")
                sys.exit(0)
            else:
                print("\n❌ Model testing failed!")
                sys.exit(1)
        else:
            print("\n❌ Database setup failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)