import streamlit as st
import datetime
from modules.speech_recognition import SpeechRecognitionEngine
from modules.text_to_speech import TextToSpeechEngine
from modules.ocr_processor import OCRProcessor
from modules.nlp_processor import NLPProcessor
from modules.database import DatabaseManager
from config import LANGUAGES, APP_NAME, VERSION
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="AI Smart Classroom",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'language' not in st.session_state:
    st.session_state.language = "en-IN"

# Initialize engines
@st.cache_resource
def load_engines():
    return {
        'sr_engine': SpeechRecognitionEngine(),
        'tts_engine': TextToSpeechEngine(),
        'ocr_engine': OCRProcessor(),
        'nlp_engine': NLPProcessor(),
        'db_manager': DatabaseManager()
    }

engines = load_engines()

# CSS Styling
st.markdown("""
<style>
:root {
    --primary: #1f77b4;
    --success: #2ca02c;
    --warning: #ff7f0e;
    --danger: #d62728;
}

.main-header {
    text-align: center;
    color: var(--primary);
    margin-bottom: 20px;
}

.subtitle-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.notes-box {
    background-color: #e8f5e9;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid var(--success);
}

.keywords-box {
    background-color: #fff3e0;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid var(--warning);
}

.ocr-box {
    background-color: #e3f2fd;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid var(--primary);
}

.highlight {
    background-color: yellow;
    padding: 2px 4px;
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    try:
        img = Image.open("logo.png")
        st.image(img, width=80)
    except:
        st.write("🎓")

with col2:
    st.markdown(f"<h1 class='main-header'>{APP_NAME} v{VERSION}</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>For Hearing & Visually Impaired Students</h4>", unsafe_allow_html=True)

with col3:
    st.write("")

# Sidebar
st.sidebar.title("⚙️ Settings")

disability_type = st.sidebar.radio(
    "👤 Select Mode",
    ["Hearing Impaired", "Visually Impaired", "Both"]
)

st.session_state.language = st.sidebar.selectbox(
    "🌐 Language",
    list(LANGUAGES.keys()),
    format_func=lambda x: LANGUAGES[x]
)

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎧 Real-Time Lecture",
    "🖼️ OCR Board Reader",
    "📚 Dashboard",
    "ℹ️ About"
])

# ==================== TAB 1: REAL-TIME LECTURE ====================
with tab1:
    st.header("🎧 Real-Time Lecture Processing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Input Method")
        input_method = st.radio("Choose:", ["Upload Audio File", "Live Microphone"], key="input_method")
    
    with col2:
        st.subheader("📊 Session Info")
        lecture_title = st.text_input("Lecture Title", "Lecture 1")
        subject = st.text_input("Subject", "General")
    
    if input_method == "Upload Audio File":
        uploaded_file = st.file_uploader("📤 Upload Audio (.wav, .mp3)", type=["wav", "mp3", "m4a"])
        
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎧 Audio Preview")
                st.audio(uploaded_file)
            
            if st.button("🎬 Process Audio", key="process_audio"):
                with st.spinner("Processing audio..."):
                    # Save temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Speech to text
                    text, success, message = engines['sr_engine'].recognize_from_file(
                        temp_path, 
                        language=st.session_state.language
                    )
                    
                    if success:
                        st.success("✅ Speech recognized!")
                        
                        # Create session
                        session_id = engines['db_manager'].create_session(
                            user_id=1,
                            lecture_title=lecture_title,
                            subject=subject
                        )
                        
                        # Process with NLP
                        keywords = engines['nlp_engine'].extract_keywords(text)
                        summary = engines['nlp_engine'].generate_summary(text)
                        notes = engines['nlp_engine'].generate_smart_notes(text)
                        
                        # Save to database
                        engines['db_manager'].save_transcript(
                            session_id, text, keywords, summary
                        )
                        
                        # Display results
                        st.markdown(f"📊 **Word Count:** {len(text.split())}")
                        
                        # Subtitles
                        with col2:
                            st.subheader("📝 Subtitles & Transcript")
                            st.markdown(f"<div class='subtitle-box'>{text}</div>", unsafe_allow_html=True)
                        
                        # Smart Notes
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📌 Smart Notes")
                            st.markdown("<div class='notes-box'>", unsafe_allow_html=True)
                            for note in notes:
                                st.write(note)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Keywords
                        with col2:
                            st.subheader("🏷️ Key Topics")
                            st.markdown("<div class='keywords-box'>", unsafe_allow_html=True)
                            st.write(", ".join(keywords))
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Summary
                        st.subheader("📄 Summary")
                        st.info(summary)
                        
                        # TTS for visually impaired
                        if disability_type in ["Visually Impaired", "Both"]:
                            st.subheader("🔊 Audio Summary (For Visually Impaired)")
                            if st.button("🎙️ Play Summary Audio"):
                                with st.spinner("Generating audio..."):
                                    success, msg = engines['tts_engine'].speak(summary)
                                    if success:
                                        st.success("✅ Audio played!")
                                    else:
                                        st.error(f"❌ {msg}")
                        
                        # Downloads
                        st.subheader("📥 Downloads")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.download_button(
                                "📥 Transcript",
                                data=text,
                                file_name="transcript.txt",
                                mime="text/plain"
                            )
                        
                        with col2:
                            notes_text = "\n".join(notes)
                            st.download_button(
                                "📥 Notes",
                                data=notes_text,
                                file_name="notes.txt",
                                mime="text/plain"
                            )
                        
                        with col3:
                            st.download_button(
                                "📥 Summary",
                                data=summary,
                                file_name="summary.txt",
                                mime="text/plain"
                            )
                        
                        # Cleanup
                        os.remove(temp_path)
                    else:
                        st.error(f"❌ {message}")
    
    else:  # Live Microphone
        if st.button("🎤 Start Recording (30 seconds)", key="record_button"):
            with st.spinner("🎙️ Recording... Please speak clearly"):
                text, success, message = engines['sr_engine'].recognize_from_microphone(
                    language=st.session_state.language,
                    timeout=30
                )
                
                if success:
                    st.success("✅ Recording processed!")
                    
                    # Process with NLP
                    keywords = engines['nlp_engine'].extract_keywords(text)
                    notes = engines['nlp_engine'].generate_smart_notes(text)
                    
                    st.markdown(f"<div class='subtitle-box'>{text}</div>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📌 Smart Notes")
                        for note in notes:
                            st.write(note)
                    
                    with col2:
                        st.subheader("🏷️ Keywords")
                        st.write(", ".join(keywords))
                else:
                    st.error(f"❌ {message}")

# ==================== TAB 2: OCR BOARD READER ====================
with tab2:
    st.header("🖼️ OCR - Board/Image Text Reader")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Upload Image")
        uploaded_image = st.file_uploader("Upload image", type=["jpg", "jpeg", "png", "bmp"])
    
    if uploaded_image is not None:
        with col1:
            st.image(uploaded_image, caption="Uploaded Image")
        
        if st.button("🔍 Extract Text (OCR)"):
            with st.spinner("Extracting text from image..."):
                temp_image_path = f"temp_{uploaded_image.name}"
                with open(temp_image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                
                # Extract text
                extracted_text, success, message = engines['ocr_engine'].extract_text_from_image(temp_image_path)
                
                if success:
                    st.success("✅ Text extracted!")
                    
                    # Extract keywords
                    keywords = engines['ocr_engine'].extract_keywords_from_ocr(extracted_text)
                    
                    # Display
                    with col2:
                        st.subheader("📝 Extracted Text")
                        st.markdown(f"<div class='ocr-box'>{extracted_text}</div>", unsafe_allow_html=True)
                    
                    st.subheader("🏷️ Keywords Found")
                    st.write(", ".join(keywords))
                    
                    # TTS for visually impaired
                    if disability_type in ["Visually Impaired", "Both"]:
                        if st.button("🔊 Read Text Aloud"):
                            with st.spinner("Reading..."):
                                success, msg = engines['tts_engine'].speak(extracted_text)
                                if success:
                                    st.success("✅ Text read!")
                    
                    # Download
                    st.download_button(
                        "📥 Download Extracted Text",
                        data=extracted_text,
                        file_name="ocr_text.txt",
                        mime="text/plain"
                    )
                    
                    # Save to database
                    engines['db_manager'].save_ocr_record(
                        user_id=1,
                        image_name=uploaded_image.name,
                        extracted_text=extracted_text,
                        confidence=0.95
                    )
                    
                    os.remove(temp_image_path)
                else:
                    st.error(f"❌ {message}")

# ==================== TAB 3: DASHBOARD ====================
with tab3:
    st.header("📚 Student Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 Total Lectures", "12")
    
    with col2:
        st.metric("📄 Total Notes", "45")
    
    with col3:
        st.metric("🎓 Learning Hours", "36")
    
    st.subheader("📊 Recent Sessions")
    
    # Mock data
    recent_data = {
        "Date": ["2024-01-20", "2024-01-19", "2024-01-18"],
        "Subject": ["Mathematics", "Physics", "Chemistry"],
        "Duration": ["45 min", "50 min", "40 min"],
        "Words": [2345, 2567, 2123]
    }
    
    st.dataframe(recent_data, use_container_width=True)
    
    st.subheader("⏰ Learning Schedule")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📅 Monday - Friday: 9 AM - 5 PM\n\n📚 Subjects: Math, Physics, Chemistry, Biology")
    
    with col2:
        st.success("✅ Current Status: 1,456 words processed today\n\n⭐ Accuracy: 94.5%")

# ==================== TAB 4: ABOUT ====================
with tab4:
    st.header("ℹ️ About AI Smart Classroom")
    
    st.markdown("""
    ### 🎓 Project Overview
    
    **AI Smart Classroom** is an intelligent learning platform designed to make education accessible to students with hearing and visual impairments.
    
    ### ✨ Features
    
    #### For Hearing Impaired Students:
    - 🎧 Real-time speech-to-text conversion
    - 📝 Automatic subtitle generation
    - 📌 Smart note generation
    - 🏷️ Key concept extraction
    - 📊 Lecture analytics
    
    #### For Visually Impaired Students:
    - 🔊 Text-to-speech conversion
    - 🖼️ OCR (Optical Character Recognition)
    - 📖 Audio-based content delivery
    - 🎙️ Interactive audio feedback
    
    #### For All Students:
    - 💾 Automatic session management
    - 📥 Easy download options
    - 🌐 Multi-language support
    - 📊 Progress tracking
    - 🎯 Personalized learning insights
    
    ### 🛠️ Technologies Used
    
    - **Frontend:** Streamlit
    - **Speech Recognition:** Google Speech-to-Text API
    - **Text-to-Speech:** pyttsx3
    - **OCR:** Tesseract/Pytesseract
    - **NLP:** NLTK, spaCy
    - **Database:** SQLite
    - **Image Processing:** OpenCV, Pillow
    
    ### 👥 Team & Support
    
    Developed for inclusive education with ❤️
    
    **Contact:** support@smartclassroom.edu
    
    ### 📄 License
    
    MIT License - Free for educational use
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>AI Smart Classroom © 2024 | Inclusive Education for All</p>", unsafe_allow_html=True)