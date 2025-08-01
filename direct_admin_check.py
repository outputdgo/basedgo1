#!/usr/bin/env python3
"""
Direct admin test - bypasses potential session issues
"""
import os
import sys
import sqlite3

def check_database_directly():
    db_path = '/home/ubuntu/basedgo1/db.sqlite3'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if admin user exists
        cursor.execute("SELECT username, is_active, is_staff, is_superuser, last_login FROM auth_user WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result:
            username, is_active, is_staff, is_superuser, last_login = result
            print(f"Admin user found:")
            print(f"  Username: {username}")
            print(f"  Active: {bool(is_active)}")
            print(f"  Staff: {bool(is_staff)}")
            print(f"  Superuser: {bool(is_superuser)}")
            print(f"  Last login: {last_login}")
        else:
            print("No admin user found in database")
        
        # Check sessions
        cursor.execute("SELECT COUNT(*) FROM django_session")
        session_count = cursor.fetchone()[0]
        print(f"\nTotal sessions in database: {session_count}")
        
        # Check if there are any current sessions
        cursor.execute("SELECT session_key, expire_date FROM django_session ORDER BY expire_date DESC LIMIT 3")
        sessions = cursor.fetchall()
        print(f"Recent sessions:")
        for session_key, expire_date in sessions:
            print(f"  {session_key[:10]}... expires: {expire_date}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False

def test_admin_login():
    """Test if we can authenticate the admin user"""
    
    # Set up Django
    sys.path.insert(0, '/home/ubuntu/basedgo1')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import authenticate
        from django.contrib.auth.models import User
        
        # Try to get admin user
        try:
            user = User.objects.get(username='admin')
            print(f"\nDjango ORM - Admin user found: {user.username}")
            print(f"  Is active: {user.is_active}")
            print(f"  Is staff: {user.is_staff}")
            print(f"  Is superuser: {user.is_superuser}")
        except User.DoesNotExist:
            print("\nDjango ORM - Admin user does not exist")
            return False
        
        return True
        
    except Exception as e:
        print(f"Django setup error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("DIRECT DATABASE ADMIN CHECK")
    print("=" * 50)
    
    # Check database directly
    if check_database_directly():
        print("\n" + "=" * 50)
        print("DJANGO ORM TEST")
        print("=" * 50)
        test_admin_login()
