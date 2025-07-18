import streamlit as st
import openai
import os
import tempfile
from dotenv import load_dotenv

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# App layout
st.set_page_config(page_title="Automated Notes Generator", layout="centered")
st.title("🎙️ Automated Notes Generator")
st.write("Upload an audio or video file and get instant transcription using OpenAI Whisper.")

# File upload
uploaded_file = st.file_uploader("Choose a file", type=["mp3", "mp4", "wav", "m4a", "mov", "avi"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    st.info("Transcribing...")

    try:
        with open(temp_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        st.subheader("🗒️ Transcribed Notes")
        st.markdown(transcript)

        st.download_button(
            label="📥 Download Notes",
            data=transcript,
            file_name="transcription.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")

    os.remove(temp_file_path)

st.markdown("---")
st.caption("🚀 Built with Streamlit + OpenAI Whisper API")
