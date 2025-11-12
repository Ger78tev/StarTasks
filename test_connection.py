#!/usr/bin/env python3
"""
Script para probar la conexión a MySQL en Railway
"""

import mysql.connector
from mysql.connector import Error
import os

def test_mysql_connection():
    print("🧪 PROBANDO CONEXIÓN MYSQL EN RAILWAY...")
    
    # Mostrar todas las variables de entorno relevantes
    env_vars = [
        'MYSQLHOST', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLDATABASE', 'MYSQLPORT',
        'DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'DB_PORT',
        'RAILWAY_ENVIRONMENT'
    ]
    
    print("📋 Variables de entorno:")
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            masked_value = '***' if 'PASSWORD' in var else value
            print(f"   {var}: {masked_value}")
        else:
            print(f"   {var}: ❌ NO CONFIGURADA")
    
    # Configuración para Railway
    config = {
        'host': os.environ.get('MYSQLHOST', os.environ.get('DB_HOST', 'localhost')),
        'user': os.environ.get('MYSQLUSER', os.environ.get('DB_USER', 'root')),
        'password': os.environ.get('MYSQLPASSWORD', os.environ.get('DB_PASSWORD', '')),
        'database': os.environ.get('MYSQLDATABASE', os.environ.get('DB_NAME', 'startask')),
        'port': int(os.environ.get('MYSQLPORT', os.environ.get('DB_PORT', 3306))),
        'charset': 'utf8mb4',
        'connect_timeout': 10,
        'use_pure': True,  # Forzar conexión TCP
        'unix_socket': None  # Evitar socket local
    }
    
    print(f"\n🔗 Intentando conectar a: {config['host']}:{config['port']}")
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Probar consulta simple
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL Version: {version[0]}")
        
        # Listar tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📊 Tablas encontradas: {len(tables)}")
        
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡Conexión exitosa! MySQL está funcionando correctamente.")
        return True
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 SOLUCIÓN: Verifica que:")
        print("   1. Has añadido un servicio MySQL en Railway")
        print("   2. Las variables MYSQL* están configuradas automáticamente")
        print("   3. Estás usando las variables MYSQLHOST, MYSQLUSER, etc.")
        return False

if __name__ == "__main__":
    test_mysql_connection()
