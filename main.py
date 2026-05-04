import sqlite3
from datetime import datetime

# Conectar a la base de datos (se crea sola)
conn = sqlite3.connect("prime.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS progreso (
    fecha TEXT PRIMARY KEY,
    leer INTEGER,
    gym INTEGER,
    aprendizaje INTEGER,
    horas_pantalla REAL,
    estado_mental INTEGER
)
""")

# Obtener fecha de hoy
hoy = datetime.now().strftime("%Y-%m-%d")

print("\n=== Registro Diario ===")

# Inputs
leer = int(input("¿Leíste hoy? (1 = sí, 0 = no): "))
gym = int(input("¿Fuiste al gym? (1 = sí, 0 = no): "))
aprendizaje = int(input("¿Aprendiste algo útil? (1 = sí, 0 = no): "))
horas_pantalla = float(input("Horas de pantalla: "))
estado_mental = int(input("Estado mental (1-10): "))

# Insertar o reemplazar datos del día
cursor.execute("""
INSERT OR REPLACE INTO progreso 
(fecha, leer, gym, aprendizaje, horas_pantalla, estado_mental)
VALUES (?, ?, ?, ?, ?, ?)
""", (hoy, leer, gym, aprendizaje, horas_pantalla, estado_mental))

conn.commit()
conn.close()

print("\n✅ Datos guardados correctamente.")