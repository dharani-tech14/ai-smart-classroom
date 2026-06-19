import streamlit as st
import os
import pyttsx3
from modules.voice_guidance import VoiceGuidance
from modules.speech_to_text import SpeechRecognizer
from modules.text_to_speech import TextToSpeechConverter
from modules.ocr_processor import OCRProcessor
from modules.nlp_processor import NLPProcessor
import time

# Ensure voice_guidance exists

if "voice_guidance" not in st.session_state:
    st.session_state.voice_guidance = VoiceGuidance()

def speak_current_section(section_name):

    if st.session_state.voice_enabled:

        voice.speak(f"You are currently on {section_name}")

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Accessible Learning Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
            
    .stApp {
        background: linear-gradient(135deg, #193C4D, #2C6B8A, #3791BD);
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        padding: 20px;
    }

 /* 🌈 Background */
    body, .main {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        font-family: 'Poppins', 'Segoe UI', sans-serif;
        padding: 20px;
    }

/* 🎯 Header */
    .dashboard-header {
        text-align: center;
        margin-bottom: 40px;
        padding: 30px 20px;
    }

    .dashboard-header h1 {
        color: #00ffff; /* Bright cyan */
        font-size: 52px;
        font-weight: 800;
        text-shadow: 0 0 15px rgba(0,255,255,0.6);
    }

    .dashboard-header p {
        color: #ffdd57; /* Bright yellow */
        font-size: 20px;
        font-weight: 500;
        margin-top: 10px;
    }

/* 📚 Section Headings (Main Features, Tools) */
    h3 {
        color: #00ffcc !important;
        font-size: 26px !important;
        font-weight: 700;
        margin-bottom: 15px;
    }

/* 📦 Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 25px;
        margin-bottom: 40px;
    }

/* 🟪 Feature Cards (BIG + colorful) */
    .feature-card {
        border-radius: 18px;
        padding: 30px;
        color: white;
        min-height: 260px;   /* 🔥 increased size */
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 35px rgba(0,0,0,0.3);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

/* Hover effect */
    .feature-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }

/* 🎯 Card content */
    .card-icon {
        font-size: 45px;
    }  

    .card-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
    }

    .card-description {
        font-size: 14px;
        color: #f1f1f1;
    }

/* 🌈 UNIQUE COLORS FOR EACH CARD */
    .card-live-classes {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
    }

    .card-notes {
        background: linear-gradient(135deg, #00b09b, #96c93d);
    }

    .card-recorded {
        background: linear-gradient(135deg, #36d1dc, #5b86e5);
    }

    .card-quiz {
        background: linear-gradient(135deg, #f7971e, #ffd200);
    }

    .card-accessibility {
        background: linear-gradient(135deg, #8e2de2, #4a00e0);
    }

/* 🔽 Bottom Tools */
    .feature-grid-bottom {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
    }

/* Bottom cards */
    .card-text-speech {
        background: linear-gradient(135deg, #232526, #414345);
    }

    .card-speech-text {
        background: linear-gradient(135deg, #1d4350, #a43931);
    }

    .card-scan-book {
        background: linear-gradient(135deg, #11998e, #38ef7d);
    }

/* 🧾 Input box */
    .voice-input-area textarea {
        background: #ffffff;
        border-radius: 10px;
        padding: 15px;
        font-size: 15px;
        color: #333;
    }

/* 🔘 Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #ff7e5f, #feb47b);
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }

/* Accessibility panel */
    .accessibility-panel {
        background: rgba(255,255,255,0.08);
        border-left: 5px solid #00ffff;
        padding: 20px;
        border-radius: 12px;
    }

    .accessibility-panel h3 {
        color: #00ffff;
    }

/* Focus for keyboard users */
    button:focus,
    textarea:focus,
    input:focus {
        outline: 3px solid #00ffff;
    }

/* 📱 Responsive */
    @media (max-width: 1200px) {
        .feature-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 768px) {
        .feature-grid,
        .feature-grid-bottom {
            grid-template-columns: 1fr;
        }
    } 
    
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = True

if 'speech_rate' not in st.session_state:
    st.session_state.speech_rate = 150

if 'volume' not in st.session_state:
    st.session_state.volume = 0.9

if 'first_load' not in st.session_state:
    st.session_state.first_load = True

if 'last_voice_page' not in st.session_state:
    st.session_state.last_voice_page = ""

if 'last_announced_page' not in st.session_state:
    st.session_state.last_announced_page = ""

# ==================== VOICE GUIDANCE ====================
voice = VoiceGuidance()
if st.session_state.first_load and st.session_state.voice_enabled:
    voice.guidance_welcome()
    st.session_state.first_load = False

# ==================== ACCESSIBILITY FUNCTIONS ====================
def universal_voice_navigation():

    if st.session_state.get("voice_nav_help") != st.session_state.page:

        voice.speak(
            "Press tab until you hear speak command button. "
            "Then press enter and speak your command."
        )
        time.sleep(3)

        st.session_state.voice_nav_help = st.session_state.page


    if st.button(
        "🎙️ Speak Command", 
        key=f"voice_nav_{st.session_state.page}"
    ):

        recognizer = SpeechRecognizer()

        voice.speak("Listening for command")

        command = recognizer.recognize_from_microphone()

        if command:

            command = command.lower()

            st.success(f"Command: {command}")

        # 🔥 Navigation Commands

            if (
                "dashboard" in command or
                "go back" in command or
                "home" in command
            ):

                voice.speak("Opening Dashboard")
                time.sleep(2)

                st.session_state.page = "dashboard"
                st.rerun()

            elif (
                "notes" in command or
                "open notes" in command
            ):

                voice.speak("Opening Notes")
                time.sleep(2)

                st.session_state.page = "notes"
                st.rerun()
            elif (
                "quiz" in command or
                "open quiz" in command
            ):

                voice.speak("Opening Quiz")
                time.sleep(2)

                st.session_state.page = "quiz"
                st.rerun()

            elif (
                "live class" in command or
                "live classes" in command
            ):

                voice.speak("Opening Live Classes")
                time.sleep(2)

                st.session_state.page = "live_classes"
                st.rerun()

            elif (
                "recorded class" in command or
                "recorded classes" in command
            ):

                voice.speak("Opening Recorded Classes")
                time.sleep(2)

                st.session_state.page = "recorded_classes"
                st.rerun()

            elif (
                "accessibility" in command or
                "settings" in command
            ):

                voice.speak("Opening Accessibility Settings")
                time.sleep(2)
                
                st.session_state.page = "accessibility_settings"
                st.rerun()

            else:

                voice.speak("Command not recognized")
                st.warning("Command not recognized")
                   
def announce_page(page_name, message=None):

    if st.session_state.voice_enabled:

        current_page = st.session_state.page

        if st.session_state.get("last_announced_page") != current_page:

            if message:
                voice.speak(message)

            else:
                voice.speak(f"You are now in {page_name}")

            st.session_state.last_announced_page = current_page

# ==================== MAIN DASHBOARD ====================
def render_dashboard():
    """Render the main accessible learning dashboard."""
       # 🔊 Auto voice guidance on dashboard open
    announce_page(
        "Dashboard",
        "Welcome to Accessible Learning Dashboard. "
        "Press Tab key to move between features."
    )

    if (
        st.session_state.voice_enabled and
        st.session_state.last_voice_page != "dashboard_welcome"
    ):

        voice.speak(
        "Press Tab key until you reach Speak Command button. "
        "Then press Enter and speak your command."
    )

        # ✅ Speak aloud
        st.session_state.last_voice_page = "dashboard_welcome"

    universal_voice_navigation()

    
    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>🎓 Accessible Learning Dashboard</h1>
        <p>Inclusive platform for visually & hearing impaired students</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add screen reader text
    st.markdown("""
    <span class="sr-only">
    Welcome to Accessible Learning Dashboard. This is an inclusive platform for hearing and visually impaired students.
    </span>
    """, unsafe_allow_html=True)
    
    # ==================== TOP ROW: 5 FEATURE CARDS ====================
    st.markdown("### 📚 Main Features")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Feature 1: Live Classes
    with col1:
        if st.button(
            "🔴 Live Classes\n\nAttend live lectures with captions & audio support",
            key="live_classes",
            help="""
            Live Classes button.
            Press Enter to open.
            Use Tab key to move to next feature.
            """
        ):
            st.session_state.last_voice_page = ""
            speak_current_section("Live Classes")
            time.sleep(2)
            st.session_state.page = 'live_classes'
            if st.session_state.voice_enabled:
                voice.speak(
                    "Live Classes opened. Attend live lectures with real-time captions."
                    )
            st.rerun()
    
    # Feature 2: Notes
    with col2:
        if st.button(
            "🟢 Notes\n\nSubject-wise notes in text & audio format",
            key="notes",
            help="""
            Notes button.
            Press Enter to open.
            Use Tab key to move to next feature.
            """
        ):
            st.session_state.last_voice_page = ""   
            speak_current_section("Notes")
            time.sleep(2)
            st.session_state.page = 'notes'
            if st.session_state.voice_enabled:
                voice.speak(
                    "Notes opened.Access subject-wise notes available in both text and audio format for your learning needs. "
                )
            st.rerun()
    
    # Feature 3: Recorded Classes
    with col3:
        if st.button(
            "🔵 Recorded Classes\n\nDay-wise & subject-wise recordings",
            key="recorded_classes",
            help="""
            Recorded Classes button.
            Press Enter to open.
            Use Tab key to move to next feature.
            """
        ):
            st.session_state.last_voice_page = ""   
            speak_current_section("Recorded Classes")
            time.sleep(2)
            st.session_state.page = 'recorded_classes'
            if st.session_state.voice_enabled:
                voice.speak(
                    "Recorded Classes opened.Access previously recorded lectures organized by day and subject for flexible learning."
                )
            st.rerun()
    
    # Feature 4: Quiz
    with col4:
        if st.button(
            "🟠 Quiz\n\nVoice-enabled quizzes with instant audio feedback",
            key="quiz",
            help="""
            Quiz button.
            Press Enter to open.
            Use Tab key to move to next feature.
            """
        ):
            st.session_state.last_voice_page = ""   
            speak_current_section("Quiz")
            time.sleep(2)
            st.session_state.page = 'quiz'
            if st.session_state.voice_enabled:
                voice.speak(
                    "Quiz opened.Take voice-enabled quizzes with instant audio feedback to test your knowledge."
                )
            st.rerun()
    
    # Feature 5: Accessibility
    with col5:
        if st.button(
            "🟣 Accessibility\n\nText ↔ Speech, OCR & voice navigation",
            key="accessibility",
            help="""
            Accessibility Settings button.
            Configure voice and OCR settings.
            Press Enter to open.
            Use Tab key to move to next feature.
            """
        ):
            st.session_state.last_voice_page = ""
            speak_current_section("Accessibility Settings")
            time.sleep(2)
            st.session_state.page = 'accessibility_settings'
            if st.session_state.voice_enabled:
                voice.speak(
                    "Accessibility Settings opened.Configure text to speech, speech to text, OCR settings, and voice navigation preference."
                )
            st.rerun()
    
    st.markdown("---")

    
    
    # ==================== BOTTOM ROW: 3 FEATURE CARDS ====================
    st.markdown("### 🛠️ Conversion Tools")
    
    col1, col2, col3 = st.columns(3)
    
    # Feature 6: Text to Speech
    with col1:

        st.markdown("""
        <div class="feature-card card-text-speech">
            <div class="card-icon">🔊</div>
            <div class="card-title">Text → Speech</div>
            <div class="card-description">
            Enter text and we'll read it aloud
            </div>
        </div>
        """, unsafe_allow_html=True)
        
# Initialize session state
        if "text_input" not in st.session_state:
            st.session_state.text_input = ""

# Text Area
        text_input = st.text_area(
            "Enter text to speak",
            value=st.session_state.text_input,
            placeholder="Type your text here...",
            height=120,
            key="tts_input"
        )

# Buttons
        btn1, btn2, = st.columns(2)

        with btn1:

            if st.button("🔊 Speak", key="speak_btn_unique"):

                if text_input and text_input.strip():

                    try:
                        tts = TextToSpeechConverter()
                        tts.convert(text_input)

                        st.success("✅ Speech completed!")

                    except Exception as e:
                        st.error(f"Error: {e}")

                else:
                    st.warning("⚠️ Please enter text first")

        with btn2:

            if st.button("🗑️ Clear", key="clear_btn_unique"):

                st.session_state.text_input = ""
                st.rerun()
    
    # Feature 7: Speech to Text

    with col2:

        st.markdown("""
        <div class="feature-card card-speech-text">
            <div class="card-icon">🎙️</div>
            <div class="card-title">Speech → Text</div>
            <div class="card-description">
            Speak and we'll convert it to text
            </div>
        </div>
        """, unsafe_allow_html=True)

        if "speech_text" not in st.session_state:
            st.session_state.speech_text = ""

        if st.button("🎙️ Start Listening", key="listen_btn"):

            recognizer = SpeechRecognizer()

            text = recognizer.recognize_from_microphone()

            if text:

                st.session_state.speech_text = text

                st.success("✅ Speech-to-text conversion complete!")

                st.text_area(
                    "📝 Transcribed Text",
                    text,
                    height=100,
                    key="speech_output_area"
                )

                text_lower = text.lower()

                if "notes" in text_lower:
                    st.session_state.page = "notes"
                    st.rerun()

                elif "quiz" in text_lower:
                    st.session_state.page = "quiz"
                    st.rerun()

                elif "live classes" in text_lower:
                    st.session_state.page = "live_classes"
                    st.rerun()

            else:
                st.warning("⚠️ Could not recognize speech")

    
    # Feature 8: Scan Book
    with col3:

        st.markdown("""
        <div class="feature-card card-scan-book">
            <div class="card-icon">📄</div>
            <div class="card-title">Scan Book</div>
            <div class="card-description">
            Upload an image and we'll extract text using OCR
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png", "pdf"],
            key="ocr_upload",
            help="Upload an image or PDF to extract text using OCR"
        )

        if uploaded_file:

            if st.session_state.voice_enabled:
                voice.guidance_action(f"Processing {uploaded_file.name}")

            ocr = OCRProcessor()

    # 🔥 IMPORTANT: Convert uploaded file to PIL image
            from PIL import Image

# Handle image files
            if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:

                image = Image.open(uploaded_file)

                text = ocr.extract_text_from_pil_image(image)
        
                st.success("✅ OCR Completed")

                st.text_area(
                    "📄 Extracted Text", 
                    text, 
                    height=150,
                    key="ocr_output_area"
                )
            # PDF FILES

            elif uploaded_file.type == "application/pdf":

                st.warning("⚠️ PDF OCR support not added yet")

                text = "PDF uploaded successfully"

                st.text_area(
                    "📄 PDF Status",
                    text,
                    height=100,
                    key="pdf_status_area"
                )

            else: 
                st.error("❌ Unsupported file type")

            # READ ALOUD

            if "text" in locals():
            
                if st.button("🔊 Read Aloud", key="read_ocr_btn"):
                    tts = TextToSpeechConverter()
                    tts.convert(text)

                    if st.session_state.voice_enabled:
                        voice.guidance_action("Reading extracted text")

        # 🔥 NLP Processing
                nlp = NLPProcessor()

                
                summary = nlp.summarize_text(text)
                keywords = nlp.extract_keywords(text)

                st.write("📝 Summary:", summary)
                st.write("🔑 Keywords:", keywords)

                if st.button("🔊 Read Summary", key="read_ocr"):
                    tts = TextToSpeechConverter()
                    tts.set_rate(st.session_state.speech_rate)
                    tts.set_volume(st.session_state.volume)
                    tts.convert(summary)

                    if st.session_state.voice_enabled:
                        voice.guidance_action("Summary is being read aloud")
    
    st.markdown("---")
    
    # ==================== ACCESSIBILITY SETTINGS ====================
    st.markdown("### ⚙️ Accessibility Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.session_state.voice_enabled = st.checkbox(
            "🔊 Enable Voice Guidance",
            value=st.session_state.voice_enabled,
            help="Enable automatic voice guidance and feedback"
        )
        if st.session_state.voice_enabled:
            voice.guidance_action("Voice guidance enabled")
    
    with col2:
        new_rate = st.slider(
            "Speech Rate",
            min_value=100,
            max_value=200,
            value=st.session_state.speech_rate,
            step=10,
            help="Adjust how fast the text is read (100-200)"
        )
        if new_rate != st.session_state.speech_rate:
            st.session_state.speech_rate = new_rate
            voice.set_speech_rate(new_rate)
    
    with col3:
        new_volume = st.slider(
            "Volume",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.volume,
            step=0.1,
            help="Adjust voice volume"
        )
        if new_volume != st.session_state.volume:
            st.session_state.volume = new_volume
            voice.set_volume(new_volume)
    
    st.markdown("""
    <div class="accessibility-panel">
        <h3>♿ Screen Reader Compatibility</h3>
        <p style="color: #b8c5d6; margin-bottom: 10px;">
        This dashboard is fully compatible with screen readers like NVDA, JAWS, and VoiceOver.
        </p>
        <ul style="color: #b8c5d6; margin-left: 20px;">
            <li>Navigate using Tab key</li>
            <li>Activate features using Enter</li>
            <li>Get automatic voice feedback for all interactions</li>
            <li>Adjust speech rate and volume</li>
            <li>Use keyboard shortcuts for quick access</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Keyboard hints
    st.markdown("""
    <div style="background: rgba(100,100,100,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
        <p style="color: #95a5a6; font-size: 12px; margin: 0;">
            <strong>⌨️ Keyboard Shortcuts:</strong> Tab to navigate | Enter to select | Escape to go back | 
            Alt+V to toggle voice | Alt+H for help
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==================== PAGE ROUTING ====================
if st.session_state.page == 'dashboard':
    render_dashboard()
    

elif st.session_state.page == 'live_classes':

    universal_voice_navigation()

    st.title("🔴 Live Classes")
    announce_page(
        "Live Classes",
        "You are now in Live Classes page. "
        "Press Tab to move between controls."
    )

    if st.button("← Back to Dashboard", key="back_live"):
        st.session_state.last_announced_page = ""
        st.session_state.page = 'dashboard'
        st.rerun()

    # ================= HEADER =================
    st.markdown("### 📘 Physics - Motion and Forces")
    st.success("🔴 LIVE CLASS ACTIVE")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.info("👨‍🏫 Teacher: Arun Kumar")
    
    with col2:
        if st.button("❌ Leave Class"):
            if st.session_state.voice_enabled:
                voice.guidance_action("You left the class")
            st.warning("You left the class")

    st.markdown("---")

    # ================= VIDEO SECTION =================
   # ================= LIVE CLASS =================

    st.markdown("""
    <div style="
    background: linear-gradient(135deg,#1e3c72,#2a5298);
    padding:25px;
    border-radius:20px;
    margin-bottom:20px;
    ">

    <h1 style="color:white;">
    🎥 Live Classes
    </h1>

    <p style="color:#dfefff;font-size:18px;">
    Accessible live learning for visually and hearing impaired students
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

    st.markdown("## 📝 Live Captions")

    caption_text = st.empty()

    caption_text.info("""
    Teacher:
    Welcome students.
    Today's topic is Artificial Intelligence.
    Please listen carefully.
    """)

    st.markdown("## 🎤 Audio Controls")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button(
            "▶️ Play Audio",
            help="Press Enter to play lecture audio"
        )
    with col2:
        st.button(
            "⏸ Pause",
            help="Press Enter to pause lecture audio"
        )

    with col3:
        st.button(
            "🔊 Volume",
            help="Press Enter to volume up lecture audio"
        )
    # ================= CAPTIONS =================
    st.markdown("### 📝 Live Captions")

    caption_text = "Now, according to Newton's second law, Force is equal to mass into acceleration."

    st.text_area(
        "Real-time captions",
        caption_text,
        height=120
    )

    if st.session_state.voice_enabled:
        if st.button("🔊 Read Captions"):
            voice.speak(caption_text)

    st.markdown("---")

    # ================= CONTROLS =================
    st.markdown("### 🎛️ Controls")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.selectbox("🔊 Audio Quality", ["Low", "Medium", "High"])

    with col2:
        st.selectbox("📝 Caption Language", ["English", "Tamil"])

    with col3:
        st.slider("🔊 Volume", 0.0, 1.0, st.session_state.volume)

    st.markdown("---")

    # ================= CHAT =================
    st.markdown("### 💬 Class Chat")

    chat_display = """
    👩 Riya: Can you explain with example?
    👨‍🏫 Teacher: Sure, solving now.
    👨 Aman: Upload notes please.
    """

    st.text_area("Chat messages", chat_display, height=150)

    user_msg = st.text_input("Type your message")

    if st.button("📤 Send"):
        st.success("Message sent")

    # ================= ACCESSIBILITY =================
    st.markdown("---")
    st.markdown("### ♿ Accessibility Help")

    st.info("""
    - Press TAB to navigate  
    - Press ENTER to select  
    - Use voice guidance for assistance  
    """)

    
        
    # ================= NOTES =================

elif st.session_state.page == 'notes':

    universal_voice_navigation()

    st.title("🟢 Accessible Notes Center")
    announce_page(
        "Notes",
        "You are now in Notes section."
        "Press Tab to navigate through subjects and options."
    )
    
    # ================= BACK BUTTON =================
    if st.button("← Back to Dashboard", key="notes_back_btn"):

        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown("---")

    # ================= HEADER =================
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#11998e,#38ef7d);
        padding:25px;
        border-radius:20px;
        margin-bottom:20px;
    ">
    <h1 style="color:white;">
    📚 Smart Notes for Accessible Learning
    </h1>

    <p style="color:#f0fff0;font-size:18px;">
    Notes available in text, audio, and screen-reader friendly format
    </p>
    </div>
    """, unsafe_allow_html=True)

    # ================= SUBJECT LIST =================
    st.markdown("## 📘 Available Subjects")

    subjects = [
        "Mathematics",
        "Science",
        "English",
        "History",
        "Artificial Intelligence"
    ]

    selected_subject = st.selectbox(
        "Choose Subject",
        subjects,
        key="notes_subject_select"
    )

    # ================= SAMPLE NOTES =================
    notes_data = {

        "Mathematics":
        """
        Algebra is a branch of mathematics dealing with symbols and equations.
        Important formulas:
        a² + b² = (a+b)(a-b)
        """,

        "Science":
        """
        Force is equal to mass multiplied by acceleration.
        Newton's laws explain motion and forces.
        """,

        "English":
        """
        Communication skills improve reading, writing, speaking, and listening.
        Grammar helps form meaningful sentences.
        """,

        "History":
        """
        The Industrial Revolution transformed manufacturing and transportation.
        It began in the 18th century.
        """,

        "Artificial Intelligence":
        """
        Artificial Intelligence enables machines to simulate human intelligence.
        AI includes Machine Learning, NLP, and Computer Vision.
        """
    }

    note_text = notes_data[selected_subject]

    # ================= NOTES DISPLAY =================
    st.markdown("## 📝 Notes Content")

    st.text_area(
        "Accessible Notes",
        note_text,
        height=250,
        key="notes_text_area"
    )

    # ================= AUDIO FEATURES =================
    st.markdown("## 🔊 Audio Accessibility")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🔊 Read Notes Aloud", key="read_notes_btn"):

            tts = TextToSpeechConverter()

            tts.set_rate(st.session_state.speech_rate)

            tts.set_volume(st.session_state.volume)

            tts.convert(note_text)

            st.success("✅ Reading notes aloud")

            
            

    with col2:

        if st.button("⏸ Stop Audio", key="stop_notes_audio_btn"):

            st.warning("Audio stopped")

    # ================= DOWNLOAD SECTION =================
    st.markdown("---")

    st.markdown("## 📥 Download Notes")

    st.download_button(
        label="📄 Download Notes as TXT",
        data=note_text,
        file_name=f"{selected_subject}_notes.txt",
        mime="text/plain",
        key="download_notes_btn"
    )

    # ================= ACCESSIBILITY HELP =================
    st.markdown("---")

    st.markdown("## ♿ Accessibility Features")

    st.info("""
    ✔ Screen Reader Friendly  
    ✔ Keyboard Navigation Support  
    ✔ Adjustable Voice Speed  
    ✔ Audio Learning Support  
    ✔ Large Readable Text  
    ✔ Voice Guidance Enabled  
    """)

    # ================= VOICE COMMANDS =================
    st.markdown("---")

    st.markdown("## 🎙 Voice Commands")

    st.write("""
    You can say:
    - "Go to Dashboard"
    - "Open Quiz"
    - "Open Live Classes"
    - "Read Notes"
    """)



elif st.session_state.page == 'recorded_classes':

    universal_voice_navigation()

    st.title("🔵 Accessible Recorded Classes")
    announce_page(
        "Recorded Classes",
        "You are now in Recorded Classes section."
    )

    # ================= BACK BUTTON =================
    if st.button("← Back to Dashboard", key="recorded_back_btn"):
        st.session_state.last_announced_page = ""
        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown("---")

    # ================= HEADER =================
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#36d1dc,#5b86e5);
        padding:25px;
        border-radius:20px;
        margin-bottom:20px;
    ">

    <h1 style="color:white;">
    🎥 Recorded Classes Library
    </h1>

    <p style="color:#eef7ff;font-size:18px;">
    Access recorded lectures with captions, audio guidance, and accessible controls
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ================= SUBJECT SELECT =================
    st.markdown("## 📚 Select Subject")

    subjects = [
        "Mathematics",
        "Science",
        "English",
        "Artificial Intelligence"
    ]

    selected_subject = st.selectbox(
        "Choose Subject",
        subjects,
        key="recorded_subject_select"
    )

    # ================= VIDEO SELECT =================
    st.markdown("## 📹 Available Recorded Sessions")

    recorded_classes = {

        "Mathematics": [
            "Algebra Basics",
            "Trigonometry Introduction"
        ],

        "Science": [
            "Newton Laws",
            "Human Digestive System"
        ],

        "English": [
            "Communication Skills",
            "Grammar Basics"
        ],

        "Artificial Intelligence": [
            "Introduction to AI",
            "Machine Learning Basics"
        ]
    }

    selected_video = st.selectbox(
        "Choose Recorded Class",
        recorded_classes[selected_subject],
        key="recorded_video_select"
    )

    # ================= VIDEO PLAYER =================
    st.markdown("## ▶ Recorded Lecture")

    st.video("https://www.youtube.com/watch?v=jfKfPfyJRdk")

    # ================= CLASS INFO =================
    st.markdown("## Class Information")

    st.info(f"""
    📘 Subject: {selected_subject}

    🎥 Lecture: {selected_video}

    ⏱ Duration: 45 Minutes

    👨‍🏫 Instructor: Arun Kumar
    """)

    # ================= CAPTIONS =================
    st.markdown("## 📝 Lecture Captions")

    captions = f"""
    Welcome students.

    Today's recorded lecture is about {selected_video}.

    Please focus on the important concepts explained in this session.
    """

    st.text_area(
        "Accessible Captions",
        captions,
        height=180,
        key="recorded_captions_area"
    )

    # ================= AUDIO CONTROLS =================
    st.markdown("## 🔊 Accessibility Audio Controls")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🔊 Read Captions", key="read_recorded_caption_btn"):

            tts = TextToSpeechConverter()

            tts.set_rate(st.session_state.speech_rate)

            tts.set_volume(st.session_state.volume)

            tts.convert(captions)

            st.success("✅ Captions are being read aloud")

            if st.session_state.voice_enabled:
                voice.guidance_action("Reading lecture captions")

    with col2:

        if st.button("⏸ Pause Audio", key="pause_recorded_audio_btn"):

            st.warning("Audio paused")

    with col3:

        if st.button("🔁 Replay Lecture", key="replay_recorded_btn"):

            st.success("Lecture replay started")

    # ================= DOWNLOAD NOTES =================
    st.markdown("---")

    st.markdown("## 📥 Download Lecture Notes")

    lecture_notes = f"""
    Subject: {selected_subject}

    Lecture: {selected_video}

    Key Points:
    - Important concepts explained
    - Examples discussed
    - Summary included
    """

    st.download_button(
        label="📄 Download Notes",
        data=lecture_notes,
        file_name=f"{selected_video}_notes.txt",
        mime="text/plain",
        key="download_recorded_notes_btn"
    )

    # ================= ACCESSIBILITY =================
    st.markdown("---")

    st.markdown("## ♿ Accessibility Support")

    st.success("""
    ✔ Screen Reader Compatible  
    ✔ Keyboard Accessible  
    ✔ Voice Guidance Enabled  
    ✔ Caption Support  
    ✔ Adjustable Audio Speed  
    ✔ Accessible Learning Interface  
    """)

    # ================= VOICE COMMANDS =================
    st.markdown("---")

    st.markdown("## 🎙 Voice Commands")

    st.write("""
    Available voice commands:
            
    - "Go to dashboard"
    - "Open notes"
    - "Open quiz"
    - "Read captions"
    - "Replay lecture"
    """)

        

# ==================== QUIZ PAGE ====================
elif st.session_state.page == 'quiz':

    universal_voice_navigation()

    st.title("🟠 Accessible Quiz Center")
    announce_page(
        "Quiz",
        "You are now in Quiz section."
        "Press Tab to navigate through quiz options and controls."
    )

    # Back Button
    if st.button("← Back to Dashboard", key="back_quiz"):
        st.session_state.last_announced_page = ""
        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown("---")

    # Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#ff9966,#ff5e62);
        padding:25px;
        border-radius:18px;
        margin-bottom:20px;
    ">
        <h2 style="color:white;">🧠 Voice Enabled Quiz</h2>
        <p style="color:#fff;">
        Accessible quizzes for visually and hearing impaired students
        with voice guidance and instant feedback.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Subject Selection
    subject = st.selectbox(
        "📚 Select Quiz Subject",
        [
            "Artificial Intelligence",
            "Python Programming",
            "Data Structures",
            "Cloud Computing",
            "IoT"
        ],
        key="quiz_subject"
    )

    difficulty = st.selectbox(
        "🎯 Difficulty Level",
        ["Easy", "Medium", "Hard"],
        key="quiz_difficulty"
    )

    st.markdown("---")

    # Quiz Question
    st.markdown("## ❓ Question 1")

    question = """
    What is the full form of AI?
    """

    st.info(question)

    # Voice Read Question
    if st.button("🔊 Read Question", key="read_question"):

        if st.session_state.voice_enabled:
            voice.speak(question)

    # Options
    answer = st.radio(
        "Choose your answer",
        [
            "Artificial Integration",
            "Automated Interface",
            "Artificial Intelligence",
            "Advanced Internet"
        ],
        key="quiz_answer"
    )

    st.markdown("---")

    # Submit Button
    if st.button("✅ Submit Answer", key="submit_quiz"):

        if answer == "Artificial Intelligence":

            st.success("🎉 Correct Answer!")

            if st.session_state.voice_enabled:
                voice.speak("Correct answer. Well done.")

        else:

            st.error("❌ Wrong Answer")

            if st.session_state.voice_enabled:
                voice.speak("Wrong answer. Try again.")

    st.markdown("---")

    # Accessibility Features
    st.markdown("### ♿ Accessibility Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🔊 Voice Guidance Enabled")

    with col2:
        st.info("⌨️ Keyboard Navigation Supported")

    with col3:
        st.info("📝 Large Readable Text")

    st.markdown("---")

    # Quiz Instructions
    st.markdown("""
    ### 📋 Instructions

    - Press TAB to navigate between controls  
    - Press ENTER to select buttons  
    - Use voice guidance for assistance  
    - Questions can be read aloud  
    - Instant feedback provided after submission  
    """)
    
# ==================== ACCESSIBILITY SETTINGS PAGE ====================
elif st.session_state.page == 'accessibility_settings':

    universal_voice_navigation()

    st.title("🟣 Accessibility Settings")
    announce_page(
        "Accessibility Settings",
        "You are now in Accessibility Settings."
        "Press Tab to navigate through options and customize your experience."
    )
    # Back Button
    if st.button("← Back to Dashboard", key="back_accessibility"):
        st.session_state.last_announced_page = ""
        st.session_state.page = 'dashboard'
        st.rerun()

    st.markdown("---")

    # Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#7F00FF,#E100FF);
        padding:25px;
        border-radius:18px;
        margin-bottom:20px;
    ">
        <h2 style="color:white;">♿ Accessibility Control Center</h2>
        <p style="color:#fff;">
        Customize accessibility tools for visually and hearing impaired students.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==================== VOICE SETTINGS ====================
    st.markdown("## 🔊 Voice Guidance Settings")

    voice_enabled = st.checkbox(
        "Enable Voice Guidance",
        value=st.session_state.voice_enabled,
        key="voice_toggle_page"
    )

    st.session_state.voice_enabled = voice_enabled

    if voice_enabled:
        st.success("✅ Voice Guidance Enabled")

        if st.button("🔊 Test Voice", key="test_voice_btn"):
            voice.speak(
                "Voice guidance is enabled successfully."
            )

    else:
        st.warning("⚠️ Voice Guidance Disabled")

    st.markdown("---")

    # ==================== SPEECH RATE ====================
    st.markdown("## ⚡ Speech Rate")

    speech_rate = st.slider(
        "Adjust Speech Speed",
        min_value=100,
        max_value=250,
        value=st.session_state.speech_rate,
        step=10,
        key="speech_rate_slider"
    )

    st.session_state.speech_rate = speech_rate

    voice.set_speech_rate(speech_rate)

    st.info(f"Current Speech Rate: {speech_rate}")

    st.markdown("---")

    # ==================== VOLUME SETTINGS ====================
    st.markdown("## 🔊 Volume Control")

    volume = st.slider(
        "Adjust Volume",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.volume,
        step=0.1,
        key="volume_slider_page"
    )

    st.session_state.volume = volume

    voice.set_volume(volume)

    st.info(f"Current Volume Level: {volume}")

    st.markdown("---")

    # ==================== DISPLAY SETTINGS ====================
    st.markdown("## 🖥️ Display Accessibility")

    font_size = st.selectbox(
        "Choose Font Size",
        ["Small", "Medium", "Large", "Extra Large"],
        index=2,
        key="font_size_accessibility"
    )

    contrast_mode = st.selectbox(
        "Color Contrast",
        [
            "Normal",
            "High Contrast",
            "Dark Mode",
            "Light Mode"
        ],
        key="contrast_mode"
    )

    st.success(f"Selected Font Size: {font_size}")
    st.success(f"Selected Contrast Mode: {contrast_mode}")

    st.markdown("---")

    # ==================== KEYBOARD ACCESS ====================
    st.markdown("## ⌨️ Keyboard Navigation")

    st.info("""
    - Press TAB to move between controls  
    - Press ENTER to activate buttons  
    - Use Arrow Keys inside options  
    - Screen readers fully supported  
    """)

    st.markdown("---")

    # ==================== SCREEN READER ====================
    st.markdown("## 🗣️ Screen Reader Compatibility")

    st.success("""
    Compatible with:
    - NVDA
    - JAWS
    - VoiceOver
    - Narrator
    """)

    st.markdown("---")

    # ==================== SAVE SETTINGS ====================
    if st.button("💾 Save Accessibility Settings", key="save_accessibility"):

        st.success("✅ Accessibility settings saved successfully!")

        if st.session_state.voice_enabled:
            voice.speak(
                "Accessibility settings saved successfully"
            )

    st.markdown("---")

    # ==================== HELP SECTION ====================
    st.markdown("## 📘 Accessibility Help")

    st.write("""
    This platform is specially designed for:
    
    - 👁️ Visually impaired students  
    - 🦻 Hearing impaired students  
    - Keyboard-only navigation users  
    - Screen reader users  
    """)
        

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #95a5a6; padding: 20px; font-size: 12px;">
    <p>🎓 AI Smart Classroom v2.0 | Inclusive Education for All Students</p>
    <p>Made with ❤️ for accessibility | Screen Reader Compatible | Voice Guided Navigation</p>
</div>
""", unsafe_allow_html=True)