import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from openai import OpenAI
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
# Set OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ""
    return text


def extract_text_from_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def text_to_speech(text, voice):
    max_length = 4096  # Maximum character length for OpenAI speech API
    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    audio_files = []

    for chunk in chunks:
        response = client.audio.speech.create(
            model="tts-1",
            input=chunk,
            voice=voice
        )
        audio_file = BytesIO(response.content)
        audio_files.append(audio_file)

    return audio_files


def main():
    st.set_page_config(page_title="PDF Voice Reader", page_icon="📑")  # Website icon as a book emoji

    st.title('PDF Voice Reader')

    with st.sidebar:
        st.title("Upload Document")
        uploaded_file = st.file_uploader("Upload PDF or Word document", type=["pdf", "docx"])
        voice = st.selectbox("Choose a voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])

        # Contact details as a dropdown
        with st.expander("Contact The Creator Of This App"):
            st.markdown("- Twitter: [EmarhNFT](https://twitter.com/EmarhNFT)")
            st.markdown("- Email: [Ezeokekemm016@gmail.com](mailto:Ezeokekemm016@gmail.com)")
            st.markdown("- LinkedIn: [Emma Ezeokeke](https://www.linkedin.com/in/emma-ezeokeke/)")

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file type")
            return

        if text:
            if st.button("Convert to Speech"):
                with st.spinner("Generating audio..."):
                    audio_files = text_to_speech(text, voice)
                    for audio_file in audio_files:
                        st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("No text found in the document.")


if __name__ == '__main__':
    main()
















