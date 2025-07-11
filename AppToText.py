import streamlit as st
import whisper
import tempfile
import os

st.set_page_config(page_title="Convertidor de Audio a Texto", layout="centered")

st.markdown("<h1 style='text-align: center;'>🧠 Convertidor de Audio a Texto</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Convierte tu voz en texto con un solo clic</h4>", unsafe_allow_html=True)

modo = st.selectbox("Elige una opción", ["Convierte audio en texto", "Convierte tu voz en texto"])

# Función para cargar modelo Whisper (versión más ligera)
@st.cache_resource
def cargar_modelo():
    return whisper.load_model("tiny")  # Modelo más liviano que "base"

# Opción 1: Cargar archivo de audio
if modo == "Convierte audio en texto":
    audio_file = st.file_uploader("🔊 Sube tu archivo de audio", type=["mp3", "wav", "m4a", "mp4", "mpeg4"])
    st.markdown("⚠️ **Tamaño máximo recomendado: 200 MB. Archivos más grandes pueden fallar o demorar.**")

    if audio_file is not None:
        st.audio(audio_file, format="audio/mp3")

        file_size_mb = len(audio_file.getvalue()) / (1024 * 1024)
        st.markdown(f"📦 Tamaño del archivo: **{file_size_mb:.1f} MB**")
        st.markdown(f"⏱️ Tiempo estimado de transcripción: **{int(file_size_mb)} minuto(s)**")

        if file_size_mb > 200:
            st.error("❌ El archivo excede el límite permitido (200 MB). Reduce el tamaño.")
        else:
            if st.button("▶️ Convertir a texto"):
                with st.spinner("🔄 Cargando modelo..."):
                    modelo = cargar_modelo()

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tmp.write(audio_file.read())
                    tmp_path = tmp.name

                with st.spinner("🧠 Transcribiendo..."):
                    resultado = modelo.transcribe(tmp_path)
                    texto = resultado["text"]

                st.success("✅ Transcripción completada")
                st.text_area("📝 Texto transcrito:", texto, height=300)
                st.download_button("💾 Descargar texto", texto, file_name="transcripcion.txt", mime="text/plain")

                os.remove(tmp_path)

# Opción 2: Grabación con micrófono (a futuro)
elif modo == "Convierte tu voz en texto":
    st.info("🔧 Herramienta en construcción")
