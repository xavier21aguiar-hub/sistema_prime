import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sistema Prime", layout="centered")

st.title("🔥 Sistema Prime Dashboard")

# Conectar a la DB
conn = sqlite3.connect("prime.db")
df = pd.read_sql_query("SELECT * FROM progreso", conn)
conn.close()

# Convertir fechas
df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")

# ===== MÉTRICAS =====
st.subheader("📊 Métricas generales")

col1, col2, col3 = st.columns(3)

col1.metric("Gym %", f"{df['gym'].mean()*100:.1f}%")
col2.metric("Lectura %", f"{df['leer'].mean()*100:.1f}%")
col3.metric("Aprendizaje %", f"{df['aprendizaje'].mean()*100:.1f}%")

st.metric("📱 Horas pantalla promedio", f"{df['horas_pantalla'].mean():.1f}h")
st.metric("🧠 Estado mental promedio", f"{df['estado_mental'].mean():.1f}/10")

# ===== GRÁFICAS =====
st.subheader("📈 Progreso")

fig, ax = plt.subplots()
ax.plot(df["fecha"], df["estado_mental"])
ax.set_title("Estado mental en el tiempo")
ax.set_xlabel("Fecha")
ax.set_ylabel("Nivel")

st.pyplot(fig)

# ===== TABLA =====
st.subheader("📋 Historial")
st.dataframe(df.tail(10))