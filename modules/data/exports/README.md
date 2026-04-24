# 🎓 AI Smart Classroom v2.0

**Making education accessible for hearing-impaired and visually-impaired students using AI**

## 📋 Features

### For Hearing Impaired Students
✅ Real-time speech-to-text conversion  
✅ Automatic subtitle generation  
✅ Smart note generation  
✅ Key concept extraction  
✅ Live microphone & file upload support  

### For Visually Impaired Students
✅ Text-to-speech conversion  
✅ OCR (Board/Image text recognition)  
✅ Audio-based content delivery  

### General Features
✅ Multi-language support (English, Tamil, Hindi, Telugu)  
✅ Automatic session management  
✅ Student dashboard  
✅ Progress tracking  
✅ Easy export (TXT)  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Tesseract-OCR (for OCR feature)

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/shrawa26/ai-smart-classroom.git
cd ai-smart-classroom
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Tesseract (For OCR)**

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install and note the path

**macOS:**
```bash
brew install tesseract
```

5. **Download NLTK Data**
```bash
python -c "import nltk; nltk.download('punkt')"
```

6. **Run Application**
```bash
streamlit run main.py
```

Access at: `http://localhost:8501`

---

## 📂 Project Structure

```
ai-smart-classroom/
├── main.py                    # Main Streamlit app
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── README.md                  # This file
│
├── modules/
│   ├── database.py            # Database management
│   ├── speech_recognition.py  # Audio to text
│   ├── text_to_speech.py      # Text to audio
│   ├── ocr_processor.py       # Image to text
│   └── nlp_processor.py       # NLP processing
│
└── data/
    ├── uploads/               # Uploaded files
    └── exports/               # Exported files
```

---

## 💡 Usage Guide

### 1. Real-Time Lecture Processing
- Upload audio file or use microphone
- Get real-time subtitles
- Download transcript & smart notes

### 2. OCR Board Reader
- Upload board/classroom image
- Extract text automatically
- Listen to extracted text (if visually impaired)

### 3. Dashboard
- View lecture history
- Check progress metrics

---

## 🛠️ Technologies Used

- **Frontend:** Streamlit
- **Speech Recognition:** Google Speech-to-Text API
- **Text-to-Speech:** pyttsx3
- **OCR:** Tesseract/Pytesseract
- **NLP:** NLTK
- **Database:** SQLite
- **Image Processing:** OpenCV, Pillow

---

## 📄 License

MIT License - Free for educational use

---

## 👨‍💼 Author

**Shrawa26** - AI Researcher & Developer

---

## 🤝 Contributing

Contributions welcome! Please fork and submit PRs.

---

## 📞 Support

- 📧 Email: support@smartclassroom.edu
- 🐛 Issues: GitHub Issues

**Made with ❤️ for Inclusive Education**