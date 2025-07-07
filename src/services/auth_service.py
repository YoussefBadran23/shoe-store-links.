"""
Authentication Service for User Management
"""
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.models import User, Role, UserRole, AuditLog, AuditAction
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling user authentication and authorization"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def login(self, username: str, password: str, ip_address: str = None) -> Tuple[bool, Optional[User], str]:
        """
        Authenticate user login
        
        Returns:
            (success, user, message)
        """
        try:
            # Find user by username
            user = self.session.query(User).filter(User.username == username).first()
            
            if not user:
                logger.warning(f"Login attempt with non-existent username: {username}")
                return False, None, "Invalid username or password"
            
            # Check if account is locked
            if user.is_locked():
                logger.warning(f"Login attempt on locked account: {username}")
                return False, None, f"Account is locked due to too many failed attempts"
            
            # Check if account is active
            if not user.is_active:
                logger.warning(f"Login attempt on inactive account: {username}")
                return False, None, "Account is not active"
            
            # Verify password
            if not user.verify_password(password):
                user.increment_failed_attempts()
                self.session.commit()
                
                logger.warning(f"Failed login attempt for user: {username}")
                
                # Log failed login attempt
                AuditLog.log_action(
                    self.session, 
                    user.id, 
                    AuditAction.LOGIN,
                    f"Failed login attempt for user {username}",
                    ip_address=ip_address
                )
                self.session.commit()
                
                return False, None, "Invalid username or password"
            
            # Successful login
            user.reset_failed_attempts()
            user.last_login = datetime.utcnow()
            self.session.commit()
            
            logger.info(f"Successful login for user: {username}")
            
            # Log successful login
            AuditLog.log_action(
                self.session,
                user.id,
                AuditAction.LOGIN,
                f"User {username} logged in successfully",
                ip_address=ip_address
            )
            self.session.commit()
            
            return True, user, "Login successful"
            
        except Exception as e:
            logger.error(f"Login error for user {username}: {e}")
            self.session.rollback()
            return False, None, "An error occurred during login"
    
    def logout(self, user: User, ip_address: str = None):
        """Log user logout"""
        try:
            logger.info(f"User logout: {user.username}")
            
            # Log logout
            AuditLog.log_action(
                self.session,
                user.id,
                AuditAction.LOGOUT,
                f"User {user.username} logged out",
                ip_address=ip_address
            )
            self.session.commit()
            
        except Exception as e:
            logger.error(f"Logout error for user {user.username}: {e}")
            self.session.rollback()
    
    def change_password(self, user: User, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password
        
        Returns:
            (success, message)
        """
        try:
            # Verify old password
            if not user.verify_password(old_password):
                return False, "Current password is incorrect"
            
            # Validate new password
            from config.settings import PASSWORD_MIN_LENGTH
            if len(new_password) < PASSWORD_MIN_LENGTH:
                return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
            
            # Set new password
            user.set_password(new_password)
            self.session.commit()
            
            logger.info(f"Password changed for user: {user.username}")
            
            # Log password change
            AuditLog.log_action(
                self.session,
                user.id,
                AuditAction.PASSWORD_CHANGE,
                f"Password changed for user {user.username}"
            )
            self.session.commit()
            
            return True, "Password changed successfully"
            
        except Exception as e:
            logger.error(f"Password change error for user {user.username}: {e}")
            self.session.rollback()
            return False, "An error occurred while changing password"
    
    def create_default_roles(self):
        """Create default system roles"""
        try:
            # Check if roles already exist
            if self.session.query(Role).count() > 0:
                return
            
            # Admin role
            admin_role = Role(
                name=UserRole.ADMIN,
                description="System Administrator - Full access to all features",
                can_manage_users=True,
                can_manage_products=True,
                can_process_sales=True,
                can_process_returns=True,
                can_view_reports=True,
                can_manage_settings=True,
                can_edit_prices=True,
                can_void_transactions=True
            )
            
            # Manager role
            manager_role = Role(
                name=UserRole.MANAGER,
                description="Store Manager - Can manage products, view reports",
                can_manage_users=False,
                can_manage_products=True,
                can_process_sales=True,
                can_process_returns=True,
                can_view_reports=True,
                can_manage_settings=False,
                can_edit_prices=True,
                can_void_transactions=True
            )
            
            # Cashier role
            cashier_role = Role(
                name=UserRole.CASHIER,
                description="Cashier - Can process sales and returns",
                can_manage_users=False,
                can_manage_products=False,
                can_process_sales=True,
                can_process_returns=True,
                can_view_reports=False,
                can_manage_settings=False,
                can_edit_prices=False,
                can_void_transactions=False
            )
            
            self.session.add_all([admin_role, manager_role, cashier_role])
            self.session.commit()
            
            logger.info("Default roles created successfully")
            
        except Exception as e:
            logger.error(f"Error creating default roles: {e}")
            self.session.rollback()
            raise
    
    def create_admin_user(self, username: str, password: str, full_name: str) -> Tuple[bool, str]:
        """
        Create default admin user
        
        Returns:
            (success, message)
        """
        try:
            # Check if admin user already exists
            existing_user = self.session.query(User).filter(User.username == username).first()
            if existing_user:
                return False, f"User with username '{username}' already exists"
            
            # Get admin role
            admin_role = self.session.query(Role).filter(Role.name == UserRole.ADMIN).first()
            if not admin_role:
                return False, "Admin role not found. Please create default roles first."
            
            # Create admin user
            admin_user = User(
                username=username,
                full_name=full_name,
                email=f"{username}@store.local",
                role_id=admin_role.id,
                is_active=True
            )
            admin_user.set_password(password)
            
            self.session.add(admin_user)
            self.session.commit()
            
            logger.info(f"Admin user '{username}' created successfully")
            return True, f"Admin user '{username}' created successfully"
            
        except Exception as e:
            logger.error(f"Error creating admin user: {e}")
            self.session.rollback()
            return False, f"Error creating admin user: {str(e)}"