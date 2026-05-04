import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sistema Prime", layout="centered")

st.title("🔥 Sistema Prime")

# ===== BASE DE DATOS =====
conn = sqlite3.connect("prime.db", check_same_thread=False)
cursor = conn.cursor()

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

conn.commit()

# ===== FORMULARIO =====
st.subheader("📥 Registrar día")

with st.form("registro"):
    leer = st.selectbox("¿Leíste?", [1, 0])
    gym = st.selectbox("¿Fuiste al gym?", [1, 0])
    aprendizaje = st.selectbox("¿Aprendiste algo?", [1, 0])
    horas = st.number_input("Horas pantalla", 0.0, 24.0, 4.0)
    estado = st.slider("Estado mental", 1, 10, 7)

    submit = st.form_submit_button("Guardar")

    if submit:
        hoy = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
        INSERT OR REPLACE INTO progreso 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (hoy, leer, gym, aprendizaje, horas, estado))

        conn.commit()
        st.success("✅ Guardado")

# ===== DATOS =====
df = pd.read_sql_query("SELECT * FROM progreso", conn)

if not df.empty:
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")

    st.subheader("📊 Métricas")

    st.metric("Gym %", f"{df['gym'].mean()*100:.1f}%")
    st.metric("Lectura %", f"{df['leer'].mean()*100:.1f}%")
    st.metric("Estado mental", f"{df['estado_mental'].mean():.1f}")

    st.subheader("📋 Historial")
    st.dataframe(df.tail(10))

conn.close()