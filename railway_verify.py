#!/usr/bin/env python3
"""
Script de verificación para Railway - Con base de datos existente
"""

import mysql.connector
from mysql.connector import Error
import os

def verify_railway_setup():
    print("🔍 VERIFICANDO CONFIGURACIÓN RAILWAY...")
    
    # Mostrar variables de entorno disponibles
    env_vars = {
        'MYSQLHOST': os.environ.get('MYSQLHOST'),
        'MYSQLUSER': os.environ.get('MYSQLUSER'),
        'MYSQLPASSWORD': '***' if os.environ.get('MYSQLPASSWORD') else None,
        'MYSQLDATABASE': os.environ.get('MYSQLDATABASE'),
        'MYSQLPORT': os.environ.get('MYSQLPORT'),
        'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT')
    }
    
    print("📋 Variables de entorno:")
    for key, value in env_vars.items():
        print(f"   {key}: {value}")
    
    # Verificar conexión a la base de datos
    print("\n🔗 Verificando conexión a la base de datos...")
    try:
        db_config = {
            'host': os.environ.get('MYSQLHOST'),
            'user': os.environ.get('MYSQLUSER'),
            'password': os.environ.get('MYSQLPASSWORD'),
            'database': os.environ.get('MYSQLDATABASE'),
            'port': int(os.environ.get('MYSQLPORT', 3306))
        }
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        
        print(f"✅ Conectado a la base de datos: {db_config['database']}")
        print(f"📊 Tablas encontradas: {len(tablas)}")
        
        for tabla in tablas:
            print(f"   - {tabla[0]}")
        
        # Verificar datos de usuarios
        cursor.execute("SELECT COUNT(*) as total_usuarios FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        cursor.execute("SELECT nombre, email, rol FROM usuarios WHERE estado = 'activo'")
        usuarios = cursor.fetchall()
        
        print(f"\n👥 Usuarios en la base de datos: {total_usuarios}")
        for usuario in usuarios:
            print(f"   - {usuario[0]} ({usuario[1]}) - {usuario[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡Verificación completada! La base de datos está lista.")
        return True
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    verify_railway_setup()
