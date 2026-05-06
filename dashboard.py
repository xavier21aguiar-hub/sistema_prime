import pandas as pd
import streamlit as st
from datetime import datetime
from supabase import create_client

# ===== CONFIG =====
st.set_page_config(page_title="Sistema Prime", layout="centered")
st.title("🔥 Sistema Prime")

# ===== SUPABASE =====
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ===== LAYOUT PRINCIPAL =====
col_form, col_dash = st.columns([1,1])

# ===== FORMULARIO =====
with col_form:
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

            supabase.table("progreso").upsert({
                "fecha": hoy,
                "leer": leer,
                "gym": gym,
                "aprendizaje": aprendizaje,
                "horas_pantalla": horas,
                "estado_mental": estado
            }).execute()

            st.success("✅ Guardado en la nube")

# ===== DATOS =====
response = supabase.table("progreso").select("*").execute()
df = pd.DataFrame(response.data)

if df.empty:
    st.warning("⚠️ Aún no tienes registros")
    st.stop()

# ===== LIMPIEZA =====
df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")

# ===== XP SYSTEM =====
def calcular_puntos(row):
        puntos = 0
        if row["leer"]: puntos += 10
        if row["gym"]: puntos += 20
        if row["aprendizaje"]: puntos += 15
        if row["horas_pantalla"] < 4: puntos += 10
        if row["estado_mental"] >= 8: puntos += 10
        return puntos

df["xp"] = df.apply(calcular_puntos, axis=1)
xp_total = df["xp"].sum()
nivel = int(xp_total // 100)

# ===== RACHA =====
streak = 0
for val in reversed(df["gym"]):
    if val == 1:
        streak += 1
    else:
        break

# ===== UI =====
with col_dash:
        
    st.subheader("🎮 Progreso Gamer")

    colA, colB = st.columns(2)
    colA.metric("Nivel", nivel)
    colB.metric("XP total", xp_total)

    st.metric("🔥 Racha Gym", streak)

    xp_actual = xp_total % 100
    st.progress(xp_actual / 100)
    st.write(f"XP para siguiente nivel: {100 - xp_actual}")

        # ===== MISIONES =====
    st.subheader("🎯 Misiones del día")

    ultimo = df.iloc[-1]

    misiones = [
        ("📚 Leer", ultimo["leer"], 10),
        ("🏋️ Gym", ultimo["gym"], 20),
        ("🧠 Aprender", ultimo["aprendizaje"], 15),
        ("📵 Control pantalla", ultimo["horas_pantalla"] < 4, 10),
        ("😎 Estado mental", ultimo["estado_mental"] >= 8, 10),
    ]

    xp_misiones = 0

    for nombre, estado_m, xp in misiones:
        if estado_m:
            st.success(f"{nombre} ✔ (+{xp} XP)")
            xp_misiones += xp
        else:
            st.error(f"{nombre} ✖")

    st.subheader("💥 Bonus del día")
    st.write(f"XP ganado: {xp_misiones}")

# ===== HISTORIAL =====
st.subheader("📋 Historial")

ultimos = df.tail(10).sort_values("fecha", ascending=False)
for _, row in ultimos.iterrows():
    st.markdown("---")

    st.markdown(f"### 📅 {row['fecha'].strftime('%Y-%m-%d')}")

    st.write(f"📚 Leer: {'✅' if row['leer'] else '❌'}")
    st.write(f"🏋️ Gym: {'✅' if row['gym'] else '❌'}")
    st.write(f"🧠 Aprendizaje: {'✅' if row['aprendizaje'] else '❌'}")
    st.write(f"📱 Horas pantalla: {row['horas_pantalla']}")
    st.write(f"😎 Estado mental: {row['estado_mental']}/10")
    st.write(f"⚡ XP: {row['xp']}")

# ===== LOGROS =====
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

# ===== IA =====
st.subheader("🧠 Análisis Inteligente")

mensajes = []

# ===== ANALISIS RECIENTE =====
if len(df) >= 3:
    ultimos = df.tail(3)

    # 📱 Pantalla
    if ultimos["horas_pantalla"].mean() > 6:
        mensajes.append("📱 Estás usando demasiado el celular últimamente.")

    # 🧠 Estado mental
    if ultimos["estado_mental"].iloc[-1] < ultimos["estado_mental"].iloc[0]:
        mensajes.append("⚠️ Tu estado mental va bajando.")

    # 🏋️ Gym
    if ultimos["gym"].sum() == 0:
        mensajes.append("💀 No has ido al gym en varios días.")

# ===== CORRELACIONES SIMPLES =====
if df["gym"].sum() > 0:
    gym_promedio = df[df["gym"] == 1]["estado_mental"].mean()
    no_gym_promedio = df[df["gym"] == 0]["estado_mental"].mean()

    if gym_promedio > no_gym_promedio:
        mensajes.append("💡 Tu estado mental mejora cuando vas al gym.")

# ===== DISCIPLINA GENERAL =====
if df["leer"].mean() < 0.5:
    mensajes.append("📚 Estás leyendo muy poco.")

if df["aprendizaje"].mean() < 0.5:
    mensajes.append("🧠 Estás aprendiendo poco.")

# ===== MENSAJE FINAL =====
if mensajes:
    for m in mensajes:
        st.warning(m)
else:
    st.success("🔥 Buen trabajo, mantienes buenos hábitos.")
