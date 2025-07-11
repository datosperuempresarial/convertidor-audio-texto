import streamlit as st
import whisper
import speech_recognition as sr
import tempfile
import time
import os

# -------------------------
# TÍTULO Y ENCABEZADO
# -------------------------
st.markdown("<h4 style='text-align: center; color: #007BFF; font-style: italic; '>Derechos reservados por Nilder Mori Fernández</h4>", unsafe_allow_html=True)

st.title("🎙️ Convertidor de Audio a Texto")
st.markdown("## Convierte tu voz en texto con un solo clic")

# -------------------------
# SELECCIÓN DE MODO
# -------------------------

modo = st.selectbox(
    "🎛️ Elige una opción",
    ["Convierte audio en texto", "Convierte tu voz en texto"],
    index=None,  # Ninguna opción preseleccionada
    placeholder="Selecciona una opción"  # Texto en gris
)
# -------------------------
# SI NO SE ELIGE NINGUNA OPCIÓN
# -------------------------
if modo == "Selecciona una opción":
    st.warning("🔽 Elige una opción del menú para comenzar.")

# -------------------------
# OPCIÓN 1: SUBIR ARCHIVO
# -------------------------
elif modo == "Convierte audio en texto":
    #st.markdown("🎧 Esta opción permite subir un archivo y convertirlo a texto.")

    # Modelo Whisper cargado solo una vez
    @st.cache_resource
    def cargar_modelo():
        return whisper.load_model("base")

    modelo = cargar_modelo()

    # Subida de archivo
    audio_file = st.file_uploader("📁 Sube tu archivo de audio", type=["mp3", "wav", "m4a", "mp4", "mpeg4"])
    st.markdown("⚠️ **Tamaño máximo recomendado: 200 MB. Archivos más grandes pueden fallar o demorar.**")

    if audio_file is not None:
        st.audio(audio_file, format="audio/mp3")

        file_size_mb = len(audio_file.getvalue()) / (1024 * 1024)
        #st.markdown(f"📦 Tamaño del archivo: **{file_size_mb:.1f} MB**")
        #st.markdown(f"⏱️ Tiempo estimado de transcripción: **{int(file_size_mb)} minuto(s)**")

        if file_size_mb > 200:
            st.error("❌ El archivo excede el límite permitido (200 MB). Reduce el tamaño.")
        else:
            if st.button("📝 Convertir a texto"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp.write(audio_file.read())
                    tmp_path = tmp.name

                with st.spinner("🔄 Transcribiendo..."):
                    resultado = modelo.transcribe(tmp_path)
                    texto = resultado["text"]

                st.success("✅ Transcripción completada")
                st.text_area("Texto transcrito", texto, height=300)
                st.download_button("⬇️ Descargar texto", texto, file_name="transcripcion.txt", mime="text/plain")

                os.remove(tmp_path)

# -------------------------
# OPCIÓN 2: GRABAR CON MICRÓFONO
# -------------------------
elif modo == "Convierte tu voz en texto":
    st.info("🎙️ Herramienta en construcción")


