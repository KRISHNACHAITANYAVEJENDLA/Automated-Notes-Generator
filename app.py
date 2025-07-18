import streamlit as st
import whisper
import os
import tempfile

# Load Whisper model (base is a good balance of speed + accuracy)
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Page layout
st.set_page_config(page_title="Note Gen", layout="centered")
st.title("📝 Note Gen – Offline Audio Transcription")
st.write("Upload an audio file (.mp3, .wav, .m4a) and get instant transcribed notes — 100% offline, no API key needed.")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_path = temp_file.name

    st.info("Transcribing with Whisper...")

    try:
        result = model.transcribe(temp_path)
        transcript = result["text"]

        st.subheader("🗒️ Transcribed Notes")
        st.markdown(transcript)

        st.download_button(
            label="📥 Download Notes",
            data=transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Transcription failed: {e}")

    os.remove(temp_path)

st.caption("🚀 Built with Whisper | 100% offline | Audio-only (.mp3, .wav, .m4a)")
