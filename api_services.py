# api_services.py
import requests
import json
from textblob import TextBlob
import re
from translate import Translator
from gemini_service import gemini_analyzer

class SMSAnalyzer:
    def __init__(self):
        try:
            self.translator_en_to_hi = Translator(to_lang="hi", from_lang="en")
            self.translator_hi_to_en = Translator(to_lang="en", from_lang="hi")
        except:
            print("Translation service not available")
            self.translator_en_to_hi = None
            self.translator_hi_to_en = None
        
        # Basic keyword patterns for fallback
        self.spam_patterns = {
            "english": [
                "winner", "prize", "free", "urgent", "cash", "claim now", "congratulations",
                "lottery", "selected", "award", "limited time", "click here", "urgent",
                "account suspended", "verify your account", "password expired", "won",
                "million", "dollar", "reward", "offer", "limited offer", "bank alert",
                "security alert", "login required", "verify now", "immediate action"
            ],
            "hindi": [
                "जीत", "इनाम", "मुफ्त", "तुरंत", "नकद", "दावा करें", "बधाई", "लॉटरी",
                "चयनित", "पुरस्कार", "सीमित समय", "यहाँ क्लिक करें", "अत्यावश्यक",
                "खाता निलंबित", "अपना खाता सत्यापित करें", "पासवर्ड समाप्त", "जीते",
                "मिलियन", "डॉलर", "पुरस्कार", "ऑफर", "सीमित ऑफर", "बैंक अलर्ट",
                "सुरक्षा चेतावनी", "लॉगिन आवश्यक", "अभी सत्यापित करें", "तत्काल कार्रवाई"
            ]
        }
        
        self.phishing_indicators = {
            "english": [
                "bank", "paypal", "amazon", "netflix", "facebook", "login", "password",
                "verify", "security", "update", "information", "details", "click",
                "account", "secure", "confirm", "personal", "data", "credentials"
            ],
            "hindi": [
                "बैंक", "पेपैल", "अमेज़न", "नेटफ्लिक्स", "फेसबुक", "लॉगिन", "पासवर्ड",
                "सत्यापित", "सुरक्षा", "अपडेट", "जानकारी", "विवरण", "क्लिक", "खाता",
                "सुरक्षित", "पुष्टि", "व्यक्तिगत", "डेटा", "प्रमाणपत्र"
            ]
        }

    def analyze_message(self, text, target_language="english"):
        """Comprehensive SMS analysis"""
        try:
            # First try Gemini AI analysis
            gemini_result = gemini_analyzer.analyze_with_gemini(text, target_language)
            if gemini_result:
                return self._format_gemini_result(gemini_result, text)
            
            # Fallback to basic analysis
            return self.basic_analysis(text, target_language)
                
        except Exception as e:
            print(f"Analysis error: {e}")
            return self.basic_analysis(text, target_language)

    def _format_gemini_result(self, result, text):
        """Format Gemini result with additional metrics"""
        return {
            "risk_level": result.get("risk_level", "low"),
            "risk_score": result.get("risk_score", 0),
            "spam_confidence": result.get("spam_confidence", 0),
            "phishing_confidence": result.get("phishing_confidence", 0),
            "categories": result.get("categories", []),
            "key_indicators": result.get("key_indicators", []),
            "explanation": result.get("explanation", ""),
            "recommendation": result.get("recommendation", ""),
            "length": len(text),
            "word_count": len(text.split()),
            "contains_links": bool(re.search(r'http[s]?://|www\.', text)),
            "is_urgent": "urgent" in result.get("categories", [])
        }

    def basic_analysis(self, text, language):
        """Basic analysis fallback"""
        text_lower = text.lower()
        
        # Basic patterns
        spam_score = sum(1 for word in self.spam_patterns[language] if word in text_lower)
        phishing_score = sum(1 for word in self.phishing_indicators[language] if word in text_lower)
        
        risk_score = min(100, spam_score * 10 + phishing_score * 15)
        
        return {
            "risk_level": "high" if risk_score > 60 else "medium" if risk_score > 30 else "low",
            "risk_score": risk_score,
            "spam_confidence": spam_score * 10,
            "phishing_confidence": phishing_score * 15,
            "categories": ["spam"] if spam_score > 0 else [],
            "key_indicators": [],
            "explanation": "Basic analysis completed",
            "recommendation": "Use caution" if risk_score > 30 else "Appears safe",
            "length": len(text),
            "word_count": len(text.split()),
            "contains_links": bool(re.search(r'http[s]?://|www\.', text)),
            "is_urgent": any(word in text_lower for word in ["urgent", "immediate", "तुरंत", "अभी"])
        }

    def get_risk_level(self, risk_score):
        """Determine risk level based on score"""
        if risk_score >= 70:
            return "high"
        elif risk_score >= 40:
            return "medium"
        else:
            return "low"

    def format_results(self, results, language="english"):
        """Format analysis results in the specified language"""
        if not results:
            return "Error: Could not analyze message.", "", "low"

        risk_level = results["risk_level"]
        
        # Base message
        if risk_level == "high":
            message = "🚨 HIGH RISK: This message appears to be malicious!" if language == "english" else "🚨 उच्च जोखिम: यह संदेश दुर्भावनापूर्ण प्रतीत होता है!"
        elif risk_level == "medium":
            message = "⚠️ CAUTION: This message shows suspicious characteristics." if language == "english" else "⚠️ सावधानी: यह संदेश संदिग्ध विशेषताएं दिखाता है."
        else:
            message = "✅ This message appears to be safe." if language == "english" else "✅ यह संदेश सुरक्षित प्रतीत होता है."

        # Add AI explanation
        details = [
            f"🔍 {results['explanation']}",
            f"💡 {results['recommendation']}"
        ]

        # Add key indicators if available
        if results["key_indicators"]:
            indicators = ", ".join(results["key_indicators"][:3])
            details.append(f"⚠️ Suspicious patterns: {indicators}")

        # Add categories
        if results["categories"]:
            categories = ", ".join(results["categories"])
            details.append(f"📋 Categories: {categories}")

        # Combine message and details
        full_message = message + "\n\n" + "\n".join(details)
        
        # Format statistics
        if language == "english":
            stats_parts = [
                f"Message length: {results['length']} characters",
                f"Words: {results['word_count']}",
                f"Risk Score: {results['risk_score']}/100",
                f"Spam Confidence: {results['spam_confidence']}%",
                f"Phishing Confidence: {results['phishing_confidence']}%"
            ]
        else:
            stats_parts = [
                f"संदेश लंबाई: {results['length']} अक्षर",
                f"शब्द: {results['word_count']}",
                f"जोखिम स्कोर: {results['risk_score']}/100",
                f"स्पैम आत्मविश्वास: {results['spam_confidence']}%",
                f"फ़िशिंग आत्मविश्वास: {results['phishing_confidence']}%"
            ]
        
        stats_text = " | ".join(stats_parts)
        
        return full_message, stats_text, risk_level

# Singleton instance
sms_analyzer = SMSAnalyzer()