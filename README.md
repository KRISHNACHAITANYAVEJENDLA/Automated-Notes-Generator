# Automated-Notes-Generator


# 🎥 Lecture Video Analyzer

Upload a lecture video, and this tool will:
- Extract audio
- Transcribe it with Whisper
- Summarize it using a transformer model
- Extract important keywords

## 🛠️ Tech Stack
- Whisper (speech-to-text)
- MoviePy (audio extraction)
- Hugging Face Transformers
- YAKE (keyword extraction)
- Streamlit

## 🚀 Deployment
You can deploy this app on [Streamlit Cloud](https://streamlit.io/cloud)

## 🖥️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
