from app import create_app
from app.utils.database import Database
import os

app = create_app()

def initialize_railway_app():
    """Función de inicialización específica para Railway"""
    print("🚀 INICIANDO STARTASK EN RAILWAY...")
    
    # Verificar variables críticas
    required_vars = ['MYSQLHOST', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLDATABASE']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"⚠️  Variables MYSQL* faltantes: {missing_vars}")
        print("💡 Asegúrate de haber añadido un servicio MySQL en Railway")
        print("📋 Variables disponibles:")
        for key, value in os.environ.items():
            if any(db_key in key for db_key in ['MYSQL', 'DB_']):
                print(f"   {key}: {'***' if 'PASSWORD' in key else value}")
    else:
        print("✅ Todas las variables MYSQL* están configuradas")
    
    # Verificar conexión a la base de datos
    db = Database()
    if db.verificar_conexion():
        print("✅ Conexión a la base de datos verificada")
        
        # Mostrar información de la base de datos
        conn = db.conectar()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            try:
                # Contar registros
                cursor.execute("SELECT COUNT(*) as total FROM usuarios")
                usuarios_count = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM proyectos")
                proyectos_count = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM tareas")
                tareas_count = cursor.fetchone()['total']
                
                print(f"📊 Base de datos cargada:")
                print(f"   👥 Usuarios: {usuarios_count}")
                print(f"   📋 Proyectos: {proyectos_count}")
                print(f"   ✅ Tareas: {tareas_count}")
                
            except Exception as e:
                print(f"⚠️  Error al leer datos: {e}")
                print("💡 La base de datos podría estar vacía")
            finally:
                cursor.close()
                conn.close()
    else:
        print("❌ No se pudo conectar a la base de datos")
        print("🔧 Ejecuta: railway run python test_connection.py para diagnosticar")
    
    return True

# Solo ejecutar en desarrollo local
if __name__ == '__main__':
    if initialize_railway_app():
        debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=debug_mode, host='0.0.0.0', port=port)
    else:
        print("❌ No se pudo iniciar la aplicación - Verifica la configuración")

