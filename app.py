import os, re, tempfile
import streamlit as st

# ============= Page setup =============
st.set_page_config(page_title="AI Note Generator", page_icon="📝", layout="wide")
st.title("📝 AI Note Generator")
st.caption("Summarize pasted text, or (optionally) transcribe audio if OPENAI_API_KEY is set.")

# ============= Utilities =============
STOPWORDS = {
    "a","an","and","the","is","are","am","to","of","in","on","for","it","this","that","with","as","by","be","was","were",
    "or","at","from","but","about","into","than","then","so","if","out","up","down","over","under","we","you","your",
    "i","me","my","our","ours","their","they","them","he","she","his","her","its","not","no","yes","do","did","does",
    "have","has","had","can","could","would","should","will","just","more","most","some","any"
}

def summarize_text(text: str, num_points: int = 6):
    """Tiny extractive summarizer: rank sentences by word frequency (no external libs)."""
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)
    tokens = re.findall(r"[A-Za-z']+", text.lower())

    # word frequencies (ignore common words)
    freqs = {}
    for w in tokens:
        if w in STOPWORDS or len(w) <= 2:
            continue
        freqs[w] = freqs.get(w, 0) + 1

    scored = []
    for i, s in enumerate(sentences):
        words = re.findall(r"[A-Za-z']+", s.lower())
        score = sum(freqs.get(w, 0) for w in words)
        scored.append((score, i, s))

    # pick top-N by score, then restore original order
    top = [s for _, _, s in sorted(scored, reverse=True)[:num_points]]
    order = {s: idx for idx, s in enumerate(sentences)}
    top_sorted = sorted(top, key=lambda s: order.get(s, 0))
    return top_sorted

def bullets_md(lines):
    return "\n".join(f"- {line.strip()}" for line in lines if line.strip())

# ============= Sidebar =============
mode = st.sidebar.radio("Mode", ["Summarize text", "Transcribe audio (optional)"], index=0)
num_points = st.sidebar.slider("Bullet points", 3, 12, 6)

# ============= Main =============
if mode == "Summarize text":
    st.subheader("Summarize Text")
    text = st.text_area("Paste text here", height=220, placeholder="Paste your lecture notes, article, or transcript...")
    if st.button("Generate Notes", type="primary", use_container_width=True):
        if not text.strip():
            st.warning("Please paste some text.")
        else:
            pts = summarize_text(text, num_points)
            st.markdown("### Notes")
            st.markdown(bullets_md(pts))
            st.download_button("Download .txt", bullets_md(pts).encode("utf-8"),
                               file_name="notes.txt", mime="text/plain")

else:
    st.subheader("Transcribe Audio → Notes")
    st.caption("Requires `OPENAI_API_KEY` set in the Render service’s Environment.")
    uploaded = st.file_uploader("Upload audio (mp3, m4a, wav, mp4)", type=["mp3","m4a","wav","mp4"])

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        st.info("No OPENAI_API_KEY found. Set it in Render to enable transcription.")
    elif uploaded:
        # Save to a temp file
        suffix = os.path.splitext(uploaded.name)[1] or ".mp3"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded.read())
            audio_path = tmp.name

        try:
            # Use OpenAI Whisper API (no ffmpeg needed for basic uploads)
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            with open(audio_path, "rb") as f:
                resp = client.audio.transcriptions.create(model="whisper-1", file=f)
            transcript = getattr(resp, "text", "")
            if not transcript:
                st.error("Transcription API returned no text.")
            else:
                st.text_area("Transcript", transcript, height=180)
                pts = summarize_text(transcript, num_points)
                st.markdown("### Notes")
                st.markdown(bullets_md(pts))
                st.download_button("Download .txt", bullets_md(pts).encode("utf-8"),
                                   file_name="notes.txt", mime="text/plain")
        except Exception as e:
            st.error(f"Transcription failed: {e}")

    st.caption("Tip: if you don’t want to use the API, switch to **Summarize text** and paste any text.")

st.divider()
st.caption("Built with Streamlit • Deploy anywhere (Render ready)")
