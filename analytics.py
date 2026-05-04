import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Conectar a la base de datos
conn = sqlite3.connect("prime.db")

# Leer datos
df = pd.read_sql_query("SELECT * FROM progreso", conn)

conn.close()

# Convertir fecha
df["fecha"] = pd.to_datetime(df["fecha"])

# Ordenar
df = df.sort_values("fecha")

print("\n=== RESUMEN ===")

print("Días registrados:", len(df))
print("Promedio lectura:", df["leer"].mean())
print("Promedio gym:", df["gym"].mean())
print("Promedio aprendizaje:", df["aprendizaje"].mean())
print("Horas pantalla promedio:", df["horas_pantalla"].mean())
print("Estado mental promedio:", df["estado_mental"].mean())
print("\nCorrelación:")
print(df.corr(numeric_only=True))

# 📈 Gráfica simple
plt.figure()
plt.plot(df["fecha"], df["estado_mental"])
plt.title("Estado mental en el tiempo")
plt.xlabel("Fecha")
plt.ylabel("Nivel (1-10)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()