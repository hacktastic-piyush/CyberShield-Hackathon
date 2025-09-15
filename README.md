# CyberShield-Hackathon
WiCys CyberShield Hackathon, conducted in September , 2025 at VIT - Bhopal, University
# Safety & Privacy Toolkit 🛡️

A comprehensive security suite for detecting spam SMS, analyzing image sentiment, identifying fake images, and detecting fraudulent calls. Built with Python and powered by Google's Gemini AI.

## 🌟 Features

### 📱 SMS Analysis
- **Advanced Spam Detection**: Uses AI-powered analysis to detect spam and phishing SMS messages
- **Multi-language Support**: Supports both English and Hindi text analysis
- **Risk Scoring**: Provides detailed risk scores and explanations
- **Pattern Recognition**: Identifies common spam patterns and suspicious keywords

### ❤️ Sentiment Analysis
- **Image Emotion Detection**: Analyzes emotional content in uploaded images
- **AI-Powered Analysis**: Uses Google Gemini Vision API for accurate sentiment detection
- **Detailed Reports**: Provides comprehensive emotional analysis with explanations

### 🖼️ Fake Image Detection
- **AI-Generated Image Detection**: Identifies AI-created or manipulated images
- **Deepfake Detection**: Detects potentially fake or altered visual content
- **Authenticity Scoring**: Provides confidence levels for image authenticity

### 📞 Fake Call Detection
- **Phone Number Analysis**: Analyzes phone numbers for potential scam indicators
- **Audio Analysis**: Processes call recordings to detect AI-generated or spoofed voices
- **Multi-format Support**: Supports various audio formats (WAV, MP3, M4A)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/hacktastic-piyush/CyberShield-Hackathon.git
cd CyberShield-Hackathon
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Getting your Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it in your `.env` file

### Step 5: Download NLTK Data (Optional)

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🎯 Usage

### Running the Application

```bash
python main.py
```

This will launch the GUI application with the following tabs:
- **SMS Analysis**: Paste or load SMS messages for spam detection
- **Sentiment Analysis**: Upload images for emotional content analysis  
- **Fake Image Detection**: Upload images to check for AI generation or manipulation
- **Fake Call Detection**: Analyze phone numbers or upload audio files
- **Usage Instructions**: Help and documentation

### Language Support

The application supports both English and Hindi:
- Switch between languages using the dropdown menu
- SMS analysis works with both English and Hindi text
- UI elements are localized for both languages

### File Formats Supported

- **Text Files**: `.txt` for SMS content
- **Images**: `.jpg`, `.jpeg`, `.png`
- **Audio**: `.wav`, `.mp3`, `.m4a`

## 🏗️ Project Structure

```
Shield Hackathon/
│
├── main.py                 # Main application entry point
├── api_services.py         # SMS analysis service with fallback logic
├── gemini_service.py       # Google Gemini AI integration
├── modules/sms_analysis.py # Original SMS analysis frame (legacy)
├── gui_config.py           # UI text translations and configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md              # This file
```

## 🔧 Configuration

### API Configuration

The application uses Google's Gemini AI for advanced analysis. Configure your API key in the `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### Customizing Spam Detection

You can customize spam detection patterns in `api_services.py`:

```python
self.spam_patterns = {
    "english": [
        "winner", "prize", "free", "urgent", "cash", 
        # Add your custom patterns here
    ],
    "hindi": [
        "जीत", "इनाम", "मुफ्त", "तुरंत", "नकद",
        # Add your custom Hindi patterns here
    ]
}
```

## 🛠️ API Integration

### SMS Analysis API

```python
from api_services import sms_analyzer

# Analyze SMS message
result = sms_analyzer.analyze_message(
    text="Your SMS message here",
    target_language="english"
)

print(f"Risk Level: {result['risk_level']}")
print(f"Risk Score: {result['risk_score']}")
print(f"Explanation: {result['explanation']}")
```

### Gemini Services

```python
from gemini_service import gemini_analyzer

# Analyze SMS
sms_result = gemini_analyzer.analyze_sms("Your message")

# Analyze image sentiment  
sentiment_result = gemini_analyzer.analyze_image_sentiment("path/to/image.jpg")

# Detect fake images
fake_result = gemini_analyzer.analyze_fake_image("path/to/image.jpg")

# Analyze phone numbers
phone_result = gemini_analyzer.analyze_phone_number("+1234567890")

# Analyze audio calls
audio_result = gemini_analyzer.analyze_fake_call("path/to/audio.wav")
```

## 🔍 Example Usage

### SMS Spam Detection

```python
# Example spam message
spam_message = "URGENT! You have won $1,000,000! Click here to claim now!"

result = sms_analyzer.analyze_message(spam_message, "english")
# Output: High risk, spam confidence: 95%
```

### Image Sentiment Analysis

```python
# Analyze emotional content in image
result = gemini_analyzer.analyze_image_sentiment("happy_family.jpg")
# Output: Positive sentiment with detailed explanation
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: No API key available
   ```
   **Solution**: Ensure your `.env` file contains a valid `GEMINI_API_KEY`

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'google-generativeai'
   ```
   **Solution**: Run `pip install -r requirements.txt`

3. **Tkinter Issues on Linux**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL
   sudo yum install tkinter
   ```

4. **Audio File Issues**
   - Ensure audio files are in supported formats (WAV, MP3, M4A)
   - Check file permissions and accessibility

### Performance Optimization

- For better performance, ensure stable internet connection for Gemini API calls
- Large audio files may take longer to process
- Consider implementing caching for frequently analyzed content

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Style

- Follow PEP 8 Python style guidelines
- Add docstrings to functions and classes
- Include error handling for API calls
- Add comments for complex logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful analysis capabilities
- Python community for excellent libraries
- Contributors and testers who helped improve this toolkit

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/safety-privacy-toolkit/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🔮 Future Enhancements

- [ ] Web-based interface
- [ ] Batch processing capabilities
- [ ] Additional language support
- [ ] Real-time monitoring dashboard
- [ ] Machine learning model training interface
- [ ] Integration with popular messaging platforms
- [ ] Advanced reporting and analytics

---

**⚠️ Disclaimer**: This tool is designed to assist in identifying potential security threats but should not be the sole method for security decisions. Always use multiple verification methods for critical security assessments.
