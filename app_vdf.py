# ================= IMPORTACIONES =================
import streamlit as st
import math
from reportlab.pdfgen import canvas
from io import BytesIO
import matplotlib.pyplot as plt

# ================= ENCABEZADO =================
st.markdown("## 🏫 CEAI - Automatización Industrial")
st.markdown("👨‍🏫 Instructor: José Audberto Torres")
st.markdown("---")

st.title("⚡ Configurador de Variadores de Frecuencia")

# ================= ENTRADAS =================
st.subheader("📝 Datos del sistema")

hp = st.number_input("Potencia del motor (HP)", value=1.0)
voltaje = st.number_input("Voltaje del motor (V)", value=220)
aceleracion = st.number_input("Rampa de aceleración (s)", value=5.0)
desaceleracion = st.number_input("Rampa de parada (s)", value=5.0)
frecuencia = st.number_input("Frecuencia nominal (Hz)", value=60.0)

# ================= BOTON PRINCIPAL =================
if st.button("🔧 Calcular configuración"):

    # -------- CALCULO --------
    corriente = (hp * 746) / (math.sqrt(3) * voltaje * 0.85)

    parametros = [
        ("HP Motor", hp),
        ("Voltaje", voltaje),
        ("Frecuencia", frecuencia),
        ("Corriente calculada (A)", round(corriente, 2)),
        ("Aceleración (s)", aceleracion),
        ("Desaceleración (s)", desaceleracion),
    ]

    # -------- MOSTRAR RESULTADOS --------
    st.subheader("✅ Parámetros calculados")
    st.table(parametros)

    # ================= PDF =================
    def generar_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(80, 800, "CONFIGURACIÓN DE VARIADOR DE FRECUENCIA")

        c.setFont("Helvetica", 12)
        c.drawString(80, 780, "CEAI - Automatización Industrial")

        y = 740
        for p in parametros:
            c.drawString(80, y, f"{p[0]}: {p[1]}")
            y -= 20

        c.drawString(80, 650, "Observaciones:")
        c.drawString(80, 630, "Configurar parámetros según placa del motor")

        c.save()
        buffer.seek(0)
        return buffer

    pdf = generar_pdf()

    st.download_button(
        label="📄 Descargar reporte en PDF",
        data=pdf,
        file_name="configuracion_vfd.pdf",
        mime="application/pdf"
    )

    # ================= DIAGRAMA =================
    st.subheader("🔌 Diagrama básico de conexión")

    fig, ax = plt.subplots(figsize=(8,4))

    # BLOQUES
    ax.text(0.1, 0.5, "RED\nL1 L2 L3", ha='center',
            bbox=dict(boxstyle="round", facecolor="lightblue"))

    ax.text(0.5, 0.5, "VFD\nR/L1 S/L2 T/L3\nU/T1 V/T2 W/T3",
            ha='center', bbox=dict(boxstyle="round", facecolor="lightgreen"))

    ax.text(0.9, 0.5, "MOTOR\nU V W",
            ha='center', bbox=dict(boxstyle="round", facecolor="orange"))

    # CONEXIONES
    ax.plot([0.2, 0.4], [0.5, 0.5], linewidth=2)
    ax.plot([0.6, 0.8], [0.5, 0.5], linewidth=2)

    # TEXTO
    ax.text(0.3, 0.6, "Alimentación")
    ax.text(0.7, 0.6, "Salida al motor")

    ax.set_title("Conexión básica VFD")
    ax.axis('off')

    st.pyplot(fig)

    # ================= EXPLICACIÓN =================
    st.subheader("🧠 Interpretación técnica")

    st.info("""
    🔹 La RED alimenta el variador por R/L1, S/L2, T/L3  
    🔹 El VFD regula voltaje y frecuencia  
    🔹 La salida U/T1 V/T2 W/T3 se conecta al motor  
    🔹 Las rampas protegen el sistema mecánico  
    🔹 La corriente calculada debe ajustarse al parámetro de protección del variador  
    """)
