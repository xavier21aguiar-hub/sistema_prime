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
col1, col2 = st.columns([1,1])

with col1:
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
    with col2:
        df["fecha"] = pd.to_datetime(df["fecha"])
        df = df.sort_values("fecha")

    # ===== XP SYSTEM =====
    def calcular_puntos(row):
        puntos = 0

        if row["leer"] == 1:
            puntos += 10
        if row["gym"] == 1:
            puntos += 20
        if row["aprendizaje"] == 1:
            puntos += 15

        if row["horas_pantalla"] < 4:
            puntos += 10
        if row["estado_mental"] >= 8:
            puntos += 10

        return puntos

    df["xp"] = df.apply(calcular_puntos, axis=1)
    xp_total = df["xp"].sum()

    def calcular_nivel(xp_total):
        return int(xp_total // 100)

    nivel = calcular_nivel(xp_total)

    # ===== RACHA =====
    streak = 0
    for val in reversed(df["gym"]):
        if val == 1:
            streak += 1
        else:
            break

    # ===== UI =====
    st.subheader("🎮 Progreso Gamer")

    col1, col2 = st.columns(2)
    col1.metric("Nivel", nivel)
    col2.metric("XP total", xp_total)

    st.metric("🔥 Racha Gym", streak)

    xp_actual = xp_total % 100
    st.progress(xp_actual / 100)
    st.write(f"XP para siguiente nivel: {100 - xp_actual}")

    # ===== MISIONES =====
    st.subheader("🎯 Misiones del día")

    ultimo = df.iloc[-1]

    misiones = []

    # Misión 1
    if ultimo["leer"] == 1:
        misiones.append(("📚 Leer", True, 10))
    else:
        misiones.append(("📚 Leer", False, 0))

    # Misión 2
    if ultimo["gym"] == 1:
        misiones.append(("🏋️ Gym", True, 20))
    else:
        misiones.append(("🏋️ Gym", False, 0))

    # Misión 3
    if ultimo["aprendizaje"] == 1:
        misiones.append(("🧠 Aprender", True, 15))
    else:
        misiones.append(("🧠 Aprender", False, 0))

    # Misión 4
    if ultimo["horas_pantalla"] < 4:
        misiones.append(("📵 Menos de 4h pantalla", True, 10))
    else:
        misiones.append(("📵 Control pantalla", False, -5))

    # Misión 5
    if ultimo["estado_mental"] >= 8:
        misiones.append(("😎 Estado mental alto", True, 10))
    else:
        misiones.append(("😴 Mejora tu estado", False, 0))

    # Mostrar misiones
    xp_misiones = 0

    for nombre, estado, recompensa in misiones:
        if estado:
            st.success(f"{nombre} ✔ (+{recompensa} XP)")
            xp_misiones += recompensa
        else:
            st.error(f"{nombre} ✖")

    st.subheader("💥 Bonus del día")
    st.write(f"XP ganado por misiones: {xp_misiones}")

    # ===== HISTORIAL =====
    st.subheader("📋 Historial")
    st.dataframe(df.tail(10))

    st.subheader("🏆 Logros")

    logros = []

    # ===== LOGROS DE RACHA GYM =====
    if streak >= 3:
        logros.append("🥉 3 días seguidos en el gym")
    if streak >= 7:
        logros.append("🥈 7 días seguidos en el gym")
    if streak >= 15:
        logros.append("🥇 15 días seguidos en el gym")

    # ===== LOGROS DE LECTURA =====
    lectura_streak = 0
    for val in reversed(df["leer"]):
        if val == 1:
            lectura_streak += 1
        else:
            break

    if lectura_streak >= 5:
        logros.append("📚 5 días seguidos leyendo")

    # ===== LOGROS DE APRENDIZAJE =====
    apr_streak = 0
    for val in reversed(df["aprendizaje"]):
        if val == 1:
            apr_streak += 1
        else:
            break

    if apr_streak >= 5:
        logros.append("🧠 5 días seguidos aprendiendo")

    # ===== LOGROS DE CONTROL DE PANTALLA =====
    if len(df) >= 3:
        ultimos = df.tail(3)
        if ultimos["horas_pantalla"].mean() < 4:
            logros.append("📵 Control total: bajo uso de pantalla 3 días")

    # ===== LOGROS DE ESTADO MENTAL =====
    if len(df) >= 3:
        ultimos = df.tail(3)
        if all(ultimos["estado_mental"] >= 8):
            logros.append("😎 Mente fuerte: 3 días con alto estado mental")

    # ===== LOGROS DE XP =====
    if xp_total >= 500:
        logros.append("🚀 500 XP alcanzados")
    if xp_total >= 1000:
        logros.append("🔥 1000 XP alcanzados")

    # ===== MOSTRAR =====
    if logros:
        for logro in logros:
            st.success(logro)
    else:
        st.info("Aún no desbloqueas logros… sigue avanzando 😈")

conn.close()