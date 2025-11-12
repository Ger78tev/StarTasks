#!/usr/bin/env python3
"""
Verificación rápida de PostgreSQL en Railway
"""

import os
import psycopg2
from psycopg2 import Error

def check_postgres():
    print("🔍 VERIFICANDO POSTGRESQL EN RAILWAY...")
    
    # Mostrar variables
    print("📋 Variables PostgreSQL:")
    for var in ['PGHOST', 'PGUSER', 'PGDATABASE', 'PGPORT']:
        value = os.environ.get(var)
        print(f"   {var}: {value}")
    
    # Probar conexión
    try:
        conn = psycopg2.connect(
            host=os.environ.get('PGHOST'),
            user=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD'),
            database=os.environ.get('PGDATABASE'),
            port=int(os.environ.get('PGPORT', 5432))
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL Version: {version[0]}")
        
        # Listar tablas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"📊 Tablas encontradas: {len(tables)}")
        
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        conn.close()
        print("🎉 ¡PostgreSQL funciona correctamente!")
        return True
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    check_postgres()
