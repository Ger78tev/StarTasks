#!/usr/bin/env python3
"""
Script para importar la base de datos existente a Railway
"""

import mysql.connector
from mysql.connector import Error
import os
import time

def import_existing_database():
    print("🚀 IMPORTANDO BASE DE DATOS EXISTENTE A RAILWAY...")
    
    # Configuración desde variables de entorno de Railway
    db_config = {
        'host': os.environ.get('MYSQLHOST'),
        'user': os.environ.get('MYSQLUSER'),
        'password': os.environ.get('MYSQLPASSWORD'),
        'database': os.environ.get('MYSQLDATABASE'),
        'port': int(os.environ.get('MYSQLPORT', 3306)),
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    try:
        # Conectar a la base de datos de Railway
        print("🔗 Conectando a la base de datos de Railway...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print(f"✅ Conectado a: {db_config['host']} - Base de datos: {db_config['database']}")
        
        # Leer y ejecutar el archivo SQL
        sql_file = 'startask_railway.sql'
        
        print(f"📖 Leyendo archivo SQL: {sql_file}")
        
        with open(sql_file, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Dividir el script en sentencias individuales
        statements = sql_script.split(';')
        
        print(f"🔧 Ejecutando {len(statements)} sentencias SQL...")
        
        success_count = 0
        error_count = 0
        
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.startswith('--') and not statement.startswith('/*'):
                try:
                    cursor.execute(statement)
                    success_count += 1
                    if i % 10 == 0:  # Mostrar progreso cada 10 sentencias
                        print(f"📊 Progreso: {i+1}/{len(statements)} sentencias")
                except Error as e:
                    error_count += 1
                    print(f"⚠️  Error en sentencia {i+1}: {e}")
                    # Continuar con las siguientes sentencias
                    continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n🎉 IMPORTACIÓN COMPLETADA!")
        print(f"✅ Sentencias exitosas: {success_count}")
        print(f"❌ Sentencias con error: {error_count}")
        
        # Verificar datos importados
        verify_imported_data(db_config)
        
        return True
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

def verify_imported_data(db_config):
    """Verifica que los datos se hayan importado correctamente"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        print("\n🔍 VERIFICANDO DATOS IMPORTADOS...")
        
        # Contar registros en cada tabla
        tables = ['usuarios', 'proyectos', 'tareas', 'mensajes_chat', 'historial_actividades']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = cursor.fetchone()
            print(f"   📊 {table}: {result['count']} registros")
        
        # Mostrar usuarios
        cursor.execute("SELECT id, nombre, email, rol FROM usuarios")
        usuarios = cursor.fetchall()
        
        print(f"\n👥 USUARIOS IMPORTADOS ({len(usuarios)}):")
        for usuario in usuarios:
            print(f"   👤 {usuario['nombre']} ({usuario['email']}) - {usuario['rol']}")
        
        # Mostrar proyectos
        cursor.execute("SELECT id, nombre, estado FROM proyectos")
        proyectos = cursor.fetchall()
        
        print(f"\n📋 PROYECTOS IMPORTADOS ({len(proyectos)}):")
        for proyecto in proyectos:
            print(f"   📁 {proyecto['nombre']} - {proyecto['estado']}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡Verificación completada! Tu base de datos está lista en Railway.")
        
    except Error as e:
        print(f"❌ Error en verificación: {e}")

if __name__ == "__main__":
    import_existing_database()
