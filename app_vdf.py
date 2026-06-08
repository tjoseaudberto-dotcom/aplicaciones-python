import streamlit as st
import math

st.set_page_config(page_title="ConfigVFD", layout="centered")

st.title("⚡ Configurador de Variadores de Frecuencia (VFD)")
st.subheader("Instructor: Automatización Industrial")

# -------------------------------
# Entrada de datos
# -------------------------------
marca = st.selectbox("Selecciona la marca", 
                     ["Allen Bradley", "Siemens", "ABB", "Schneider", "Delta"])

modelo = st.selectbox("Selecciona el modelo", 
                      ["PowerFlex 40", "Sinamics V20", "ACS355", "ATV320", "VFD-M"])

hp = st.number_input("Potencia del motor (HP)", min_value=0.1)
voltaje = st.number_input("Voltaje del motor (V)", value=220)
modo = st.radio("Modo de operación", ["Local", "Remoto"])
aceleracion = st.number_input("Rampa de aceleración (s)", value=5.0)
desaceleracion = st.number_input("Rampa de parada (s)", value=5.0)
velocidad_max = st.number_input("Velocidad máxima (Hz)", value=60.0)

# -------------------------------
# Cálculo
# -------------------------------
if st.button("🔧 Calcular parámetros"):

    # cálculo de corriente
    corriente = (hp * 746) / (math.sqrt(3) * voltaje * 0.85)

    parametros = []

    # ---------------- PowerFlex 40 ----------------
    if marca == "Allen Bradley" and modelo == "PowerFlex 40":
        parametros = [
            ("P031", "Voltaje nominal", voltaje),
            ("P032", "Frecuencia nominal", 60),
            ("P033", "Corriente nominal", round(corriente,2)),
            ("P034", "Frecuencia mínima", 5),
            ("P035", "Frecuencia máxima", velocidad_max),
            ("P039", "Tiempo de aceleración", aceleracion),
            ("P040", "Tiempo de desaceleración", desaceleracion),
        ]

        if modo == "Local":
            parametros.append(("P036", "Fuente de arranque", "Keypad"))
        else:
            parametros.append(("P036", "Fuente de arranque", "Remoto (2 hilos)"))

    # ---------------- Siemens V20 ----------------
    elif marca == "Siemens":
        parametros = [
            ("P0304", "Voltaje motor", voltaje),
            ("P0310", "Frecuencia nominal", 60),
            ("P0335", "Corriente nominal", round(corriente,2)),
            ("P1080", "Frecuencia mínima", 5),
            ("P1082", "Frecuencia máxima", velocidad_max),
            ("P1120", "Aceleración", aceleracion),
            ("P1121", "Deceleración", desaceleracion),
        ]

    # ---------------- ABB ----------------
    elif marca == "ABB":
        parametros = [
            ("9905", "Voltaje motor", voltaje),
            ("9906", "Corriente nominal", round(corriente,2)),
            ("9907", "Frecuencia nominal", 60),
            ("2202", "Velocidad máxima", velocidad_max),
            ("2203", "Aceleración", aceleracion),
            ("2204", "Desaceleración", desaceleracion),
        ]

    # ---------------- Schneider ----------------
    elif marca == "Schneider":
        parametros = [
            ("UnS", "Voltaje motor", voltaje),
            ("FrS", "Frecuencia nominal", 60),
            ("nCr", "Corriente nominal", round(corriente,2)),
            ("HSP", "Velocidad máxima", velocidad_max),
            ("ACC", "Aceleración", aceleracion),
            ("DEC", "Desaceleración", desaceleracion),
        ]

    # ---------------- Delta ----------------
    elif marca == "Delta":
        parametros = [
            ("01-00", "Voltaje motor", voltaje),
            ("01-01", "Frecuencia nominal", 60),
            ("01-02", "Corriente nominal", round(corriente,2)),
            ("01-05", "Velocidad máxima", velocidad_max),
            ("00-09", "Aceleración", aceleracion),
            ("00-10", "Desaceleración", desaceleracion),
        ]

    # -------------------------------
    # Mostrar resultados
    # -------------------------------
    st.success("✅ Parámetros generados correctamente")

    st.table({
        "Parámetro": [p[0] for p in parametros],
        "Descripción": [p[1] for p in parametros],
        "Valor": [p[2] for p in parametros],
    })

    # Explicación técnica
    st.subheader("🧠 Interpretación técnica")
    st.info("""
    Estos parámetros configuran el variador según los datos del motor:
    
    - Voltaje y frecuencia → placa del motor  
    - Corriente → protección y control  
    - Rampas → evitan esfuerzos mecánicos  
    - Frecuencia máxima → define velocidad  
    
    Esto sigue la lógica estándar de configuración de VFD.
    """)