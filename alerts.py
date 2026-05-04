import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect("prime.db")

df = pd.read_sql_query("SELECT * FROM progreso", conn)
conn.close()

# Convertir fechas
df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")

print("\n=== ALERTAS DEL SISTEMA ===\n")

# 🚫 1. Detectar días sin gym consecutivos
sin_gym = 0
for val in reversed(df["gym"]):
    if val == 0:
        sin_gym += 1
    else:
        break

if sin_gym >= 3:
    print(f"⚠️ Llevas {sin_gym} días sin gym. Estás bajando nivel.")

# 📚 2. Detectar días sin leer
sin_leer = 0
for val in reversed(df["leer"]):
    if val == 0:
        sin_leer += 1
    else:
        break

if sin_leer >= 2:
    print(f"⚠️ Llevas {sin_leer} días sin leer. Estás perdiendo disciplina.")

# 📱 3. Pantalla alta reciente
if len(df) >= 3:
    ultimos = df.tail(3)
    if ultimos["horas_pantalla"].mean() > 6:
        print("⚠️ Estás usando demasiado el celular últimamente.")

# 🧠 4. Estado mental bajando
if len(df) >= 3:
    ultimos = df.tail(3)
    if ultimos["estado_mental"].iloc[-1] < ultimos["estado_mental"].iloc[0]:
        print("⚠️ Tu estado mental va a la baja. Ajusta tu rutina.")

print("\n--- Fin de alertas ---")