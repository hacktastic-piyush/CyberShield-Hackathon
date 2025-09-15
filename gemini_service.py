# gemini_service.py
import os
import re
import json
import base64
import mimetypes
import requests
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class GeminiSMSAnalyzer:
    def __init__(self):
        self.spam_patterns = [
            r'(?i)win.*prize|free.*gift|cash.*reward',
            r'(?i)urgent|limited.*time|offer.*expire',
            r'(?i)click.*link|visit.*website|call.*now',
            r'(?i)congratulations|you.*won|selected',
            r'(?i)bank.*account|password|verify.*identity',
            r'(?i)\$[0-9,]+|million|billion|lakh|crore',
            r'(?i)lottery|raffle|draw|jackpot',
            r'(?i)guaranteed|risk.*free|no.*investment'
        ]
        self.api_key = os.getenv("GEMINI_API_KEY")

        # Models
        self.model_text = "gemini-1.5-flash"       # faster, for text-only (SMS)
        self.model_multimodal = "gemini-2.5-flash" # for images/audio
        self.api_url_base = "https://generativelanguage.googleapis.com/v1beta/models"

    # ---------------- SMS Analysis ----------------
    def analyze_sms(self, message: str) -> Dict[str, Any]:
        if not self.api_key:
            return self.basic_analysis(message)
        try:
            return self.analyze_with_gemini_text(message)
        except Exception as e:
            print(f"Gemini text analysis failed: {e}")
            return self.basic_analysis(message)

    def analyze_with_gemini_text(self, message: str) -> Dict[str, Any]:
        url = f"{self.api_url_base}/{self.model_text}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        prompt = f"""
Analyze this SMS message for spam characteristics:
\"{message}\"

Return JSON response with:
- is_spam: boolean
- spam_score: integer (0-10)
- reason: string explaining why
- confidence: float (0.0-1.0)
"""
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        resp = requests.post(url, headers=headers, json=data, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        return self.parse_gemini_response(result)

    def parse_gemini_response(self, response: Dict) -> Dict[str, Any]:
        try:
            text_response = response['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text_response)
        except (KeyError, json.JSONDecodeError):
            return {
                'is_spam': False,
                'spam_score': 0,
                'reason': 'Analysis failed, using fallback',
                'confidence': 0.0
            }

    def basic_analysis(self, message: str) -> Dict[str, Any]:
        spam_score = 0
        detected_patterns = []
        for pattern in self.spam_patterns:
            if re.search(pattern, message):
                spam_score += 1
                detected_patterns.append(pattern)
        return {
            'is_spam': spam_score >= 2,
            'spam_score': spam_score,
            'detected_patterns': detected_patterns,
            'reason': f'Detected {spam_score} spam patterns' if spam_score > 0 else 'No spam patterns detected',
            'confidence': min(spam_score / 5, 1.0),
            'analysis_method': 'basic_regex'
        }

    # ---------------- Image Sentiment Analysis ----------------
    def analyze_image_sentiment(self, image_path: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"sentiment": "unknown", "explanation": "No API key available."}
        url = f"{self.api_url_base}/{self.model_multimodal}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        prompt = "Analyze the sentiment expressed in this image. Classify as Positive, Negative, or Neutral and provide a short explanation."
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        data = {"contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}}]}]}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return {"sentiment": text_response}
        except Exception as e:
            return {"sentiment": "error", "explanation": str(e)}

    # ---------------- Fake Image Detection ----------------
    def analyze_fake_image(self, image_path: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"result": "unknown", "explanation": "No API key available."}
        url = f"{self.api_url_base}/{self.model_multimodal}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        prompt = """
Analyze this image and determine if it is likely AI-generated, manipulated, deepfake, or authentic.
Respond clearly with a classification (Fake / Real / Unsure) and provide a short explanation.
"""
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        data = {"contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}}]}]}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return {"result": text_response}
        except Exception as e:
            return {"result": "error", "explanation": str(e)}

    # ---------------- Fake Call Detection ----------------
    def analyze_fake_call(self, audio_path: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"result": "unknown", "explanation": "No API key available."}
        url = f"{self.api_url_base}/{self.model_multimodal}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        prompt = """
Analyze this audio call recording and determine if it is likely spoofed, AI-generated (deepfake voice), scam-related, or authentic.
Respond clearly with a classification (Fake / Real / Unsure) and provide a short explanation.
"""
        mime_type, _ = mimetypes.guess_type(audio_path)
        if not mime_type:
            mime_type = "audio/wav"
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        data = {"contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": mime_type, "data": b64_audio}}]}]}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return {"result": text_response}
        except Exception as e:
            return {"result": "error", "explanation": str(e)}

    # ---------------- Phone Number Analysis ----------------
    def analyze_phone_number(self, phone_number: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"result": "unknown", "explanation": "No API key available."}
        url = f"{self.api_url_base}/{self.model_text}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        prompt = f"""
Is the phone number {phone_number} likely a scam, safe, or unsure?
Answer with one word (Scam, Safe, Unsure) and a brief reason.
"""
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return {"result": text_response}
        except Exception as e:
            return {"result": "error", "explanation": str(e)}


# Singleton instance
gemini_analyzer = GeminiSMSAnalyzer()
