import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
from gemini_service import gemini_analyzer

# ---------------- Translations ----------------
translations = {
    "en": {
        "sms_analysis": "SMS Analysis",
        "sentiment_analysis": "Sentiment Analysis",
        "fake_image": "Fake Image Detection",
        "fake_call": "Fake Call Detection",
        "usage": "Usage Instructions",
        "app_title": "Safety Toolkit - Security Suite",
        "ready": "Ready",
        "sms_title": "SMS Spam Detection",
        "sms_prompt": "SMS Analysis - Enter message to detect spam",
        "analyze_sms": "Analyze SMS",
        "clear": "Clear",
        "load_file": "Load from File",
        "results": "Analysis Results",
        "sentiment_title": "Image Sentiment Analysis",
        "sentiment_prompt": "Sentiment Analysis - Upload an image",
        "upload_image": "Upload Image",
        "fake_image_title": "Fake Image Detection",
        "fake_image_prompt": "Fake Image Detection - Upload an image",
        "upload_audio": "Upload Audio",
        "fake_call_title": "Fake Call Detection",
        "fake_call_prompt": "Fake Call Detection - Upload an audio file or enter a number",
        "phone_check": "Phone Number Check",
        "analyze_number": "Analyze Number",
        "call_audio": "Call Audio Analysis",
        "usage_text": """
Safety Toolkit - सुरक्षित उपकरण

📱 SMS Analysis: Detect spam and scam messages
❤️  Sentiment Analysis: Analyze emotional tone in images
🖼️  Fake Image Detection: Identify AI-generated images
📞 Fake Call Detection: Detect suspicious phone calls and numbers
"""
    },
    "hi": {
        "sms_analysis": "एसएमएस विश्लेषण",
        "sentiment_analysis": "भावना विश्लेषण",
        "fake_image": "नकली छवि पहचान",
        "fake_call": "नकली कॉल पहचान",
        "usage": "उपयोग निर्देश",
        "app_title": "सुरक्षा टूलकिट - सुरक्षा सूट",
        "ready": "तैयार",
        "sms_title": "एसएमएस स्पैम पहचान",
        "sms_prompt": "एसएमएस विश्लेषण - संदेश दर्ज करें और जांचें",
        "analyze_sms": "एसएमएस विश्लेषण करें",
        "clear": "साफ करें",
        "load_file": "फ़ाइल से लोड करें",
        "results": "विश्लेषण परिणाम",
        "sentiment_title": "छवि भावना विश्लेषण",
        "sentiment_prompt": "भावना विश्लेषण - छवि अपलोड करें",
        "upload_image": "छवि अपलोड करें",
        "fake_image_title": "नकली छवि पहचान",
        "fake_image_prompt": "नकली छवि पहचान - छवि अपलोड करें",
        "upload_audio": "ऑडियो अपलोड करें",
        "fake_call_title": "नकली कॉल पहचान",
        "fake_call_prompt": "नकली कॉल पहचान - ऑडियो अपलोड करें या नंबर दर्ज करें",
        "phone_check": "फ़ोन नंबर जांच",
        "analyze_number": "नंबर विश्लेषण करें",
        "call_audio": "कॉल ऑडियो विश्लेषण",
        "usage_text": """
सुरक्षा टूलकिट - सुरक्षित उपकरण

📱 एसएमएस विश्लेषण: स्पैम और धोखाधड़ी संदेशों का पता लगाएँ
❤️  भावना विश्लेषण: छवियों में भावनाओं का विश्लेषण करें
🖼️  नकली छवि पहचान: एआई द्वारा बनाई गई छवियों की पहचान करें
📞 नकली कॉल पहचान: संदिग्ध कॉल और नंबरों का पता लगाएँ
"""
    }
}


class SafetyToolkitApp:
    def __init__(self, root):
        self.root = root
        self.language = "en"  # default language
        self.analyzer = gemini_analyzer

        self.root.title(translations[self.language]["app_title"])
        self.root.geometry("1000x700")
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)

        # Language selector
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(lang_frame, text="Language / भाषा:").pack(side='left', padx=5)
        self.lang_var = tk.StringVar(value=self.language)
        lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["en", "hi"], width=5, state="readonly")
        lang_menu.pack(side='left')
        lang_menu.bind("<<ComboboxSelected>>", self.change_language)

        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill='x', pady=(0, 10))

        self.nav_buttons = []
        self.nav_frame = nav_frame
        self.build_nav_buttons()

        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill='both', expand=True)

        self.status_var = tk.StringVar()
        self.status_var.set(translations[self.language]["ready"])
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill='x', pady=(10, 0))

        self.show_sms_analysis()

    def build_nav_buttons(self):
        for btn in self.nav_buttons:
            btn.destroy()
        self.nav_buttons.clear()

        texts = translations[self.language]
        nav_items = [
            (texts["sms_analysis"], self.show_sms_analysis),
            (texts["sentiment_analysis"], self.show_sentiment_analysis),
            (texts["fake_image"], self.show_fake_image_detection),
            (texts["fake_call"], self.show_fake_call_detection),
            (texts["usage"], self.show_usage)
        ]
        for text, command in nav_items:
            btn = ttk.Button(self.nav_frame, text=text, command=command)
            btn.pack(side='left', padx=2)
            self.nav_buttons.append(btn)

    def change_language(self, event=None):
        self.language = self.lang_var.get()
        self.root.title(translations[self.language]["app_title"])
        self.status_var.set(translations[self.language]["ready"])
        self.build_nav_buttons()
        self.show_sms_analysis()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ---------------- SMS Analysis ----------------
    def show_sms_analysis(self):
        texts = translations[self.language]
        self.clear_content_frame()
        self.status_var.set(texts["sms_prompt"])
        title_label = ttk.Label(self.content_frame, text=texts["sms_title"], font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        input_frame = ttk.LabelFrame(self.content_frame, text=texts["sms_title"], padding="10")
        input_frame.pack(fill='x', padx=10, pady=5)
        self.sms_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD)
        self.sms_text.pack(fill='x', pady=5)
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill='x', pady=10)
        ttk.Button(btn_frame, text=texts["analyze_sms"], command=self.analyze_sms).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=texts["clear"], command=self.clear_text).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=texts["load_file"], command=self.load_from_file).pack(side='left', padx=5)
        results_frame = ttk.LabelFrame(self.content_frame, text=texts["results"], padding="10")
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.results_text = scrolledtext.ScrolledText(results_frame, height=12, wrap=tk.WORD, state=tk.DISABLED)
        self.results_text.pack(fill='both', expand=True)
    
    def analyze_sms(self):
    	message = self.sms_text.get("1.0", tk.END).strip()
    	if not message:
        	messagebox.showwarning("Input Error", "Please enter an SMS message to analyze.")
        	return
    	self.status_var.set("Analyzing SMS message...")
    	self.root.update()
    	result = self.analyzer.analyze_sms(message)

    	self.results_text.config(state=tk.NORMAL)
    	self.results_text.delete("1.0", tk.END)

    	status = "🚨 SPAM DETECTED!" if result.get('is_spam') else "✅ Legitimate Message"

    	result_text = f"""
	{status}

	📊 Spam Score: {result.get('spam_score', 0)}/10
	🎯 Confidence: {result.get('confidence', 0):.2%}
	📝 Reason: {result.get('reason', '')}
	🔍 Detected Patterns: {', '.join(result.get('detected_patterns', [])) if result.get('detected_patterns') else 'None'}
	"""

    	self.results_text.insert(tk.END, result_text.strip())
    	self.results_text.config(state=tk.DISABLED)
    	self.status_var.set("SMS analysis complete")

    

    def clear_text(self):
        self.sms_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.status_var.set("Cleared input and results")

    def load_from_file(self):
        file_path = filedialog.askopenfilename(title="Select SMS Text File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.sms_text.delete("1.0", tk.END)
                    self.sms_text.insert("1.0", content)
                self.status_var.set(f"Loaded content from {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    # ---------------- Sentiment Analysis ----------------
    def show_sentiment_analysis(self):
        texts = translations[self.language]
        self.clear_content_frame()
        self.status_var.set(texts["sentiment_prompt"])
        title_label = ttk.Label(self.content_frame, text=texts["sentiment_title"], font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        upload_btn = ttk.Button(self.content_frame, text=texts["upload_image"], command=self.upload_image_for_sentiment)
        upload_btn.pack(pady=10)
        self.sentiment_result = scrolledtext.ScrolledText(self.content_frame, height=12, wrap=tk.WORD, state=tk.DISABLED)
        self.sentiment_result.pack(fill='both', expand=True, padx=10, pady=10)

    def upload_image_for_sentiment(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.status_var.set("Analyzing sentiment in image...")
            self.root.update()
            result = self.analyzer.analyze_image_sentiment(file_path)
            self.sentiment_result.config(state=tk.NORMAL)
            self.sentiment_result.delete("1.0", tk.END)
            self.sentiment_result.insert(tk.END, f"Sentiment Analysis Result:\n\n{result}\n")
            self.sentiment_result.config(state=tk.DISABLED)
            self.status_var.set("Sentiment analysis complete")

    # ---------------- Fake Image Detection ----------------
    def show_fake_image_detection(self):
        texts = translations[self.language]
        self.clear_content_frame()
        self.status_var.set(texts["fake_image_prompt"])
        title_label = ttk.Label(self.content_frame, text=texts["fake_image_title"], font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        upload_btn = ttk.Button(self.content_frame, text=texts["upload_image"], command=self.upload_image_for_fake_detection)
        upload_btn.pack(pady=10)
        self.fake_result = scrolledtext.ScrolledText(self.content_frame, height=12, wrap=tk.WORD, state=tk.DISABLED)
        self.fake_result.pack(fill='both', expand=True, padx=10, pady=10)

    def upload_image_for_fake_detection(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.status_var.set("Analyzing image authenticity...")
            self.root.update()
            result = self.analyzer.analyze_fake_image(file_path)
            self.fake_result.config(state=tk.NORMAL)
            self.fake_result.delete("1.0", tk.END)
            self.fake_result.insert(tk.END, f"Fake Image Detection Result:\n\n{result}\n")
            self.fake_result.config(state=tk.DISABLED)
            self.status_var.set("Fake image analysis complete")

    # ---------------- Fake Call Detection ----------------
    def show_fake_call_detection(self):
        texts = translations[self.language]
        self.clear_content_frame()
        self.status_var.set(texts["fake_call_prompt"])
        title_label = ttk.Label(self.content_frame, text=texts["fake_call_title"], font=('Arial', 14, 'bold'))
        title_label.pack(pady=20)
        phone_frame = ttk.LabelFrame(self.content_frame, text=texts["phone_check"], padding="10")
        phone_frame.pack(fill='x', padx=10, pady=5)
        self.phone_entry = ttk.Entry(phone_frame, width=40)
        self.phone_entry.pack(side='left', padx=5)
        ttk.Button(phone_frame, text=texts["analyze_number"], command=self.analyze_phone_number).pack(side='left', padx=5)
        audio_frame = ttk.LabelFrame(self.content_frame, text=texts["call_audio"], padding="10")
        audio_frame.pack(fill='x', padx=10, pady=10)
        upload_btn = ttk.Button(audio_frame, text=texts["upload_audio"], command=self.upload_audio_for_fake_call)
        upload_btn.pack(pady=5)
        self.call_result = scrolledtext.ScrolledText(self.content_frame, height=12, wrap=tk.WORD, state=tk.DISABLED)
        self.call_result.pack(fill='both', expand=True, padx=10, pady=10)

    def upload_audio_for_fake_call(self):
        file_path = filedialog.askopenfilename(title="Select an Audio File", filetypes=[("Audio files", "*.wav *.mp3 *.m4a")])
        if file_path:
            self.status_var.set("Analyzing call authenticity...")
            self.root.update()
            result = self.analyzer.analyze_fake_call(file_path)
            self.display_fake_call_result("Fake Call Detection Result", result)

    def analyze_phone_number(self):
        phone_number = self.phone_entry.get().strip()
        if not phone_number:
            messagebox.showwarning("Input Error", "Please enter a phone number to analyze.")
            return
        self.status_var.set("Analyzing phone number...")
        self.root.update()
        result = self.analyzer.analyze_phone_number(phone_number)
        self.display_fake_call_result("Phone Number Analysis Result", result)

    def display_fake_call_result(self, title, result):
        self.call_result.config(state=tk.NORMAL)
        self.call_result.delete("1.0", tk.END)
        self.call_result.insert(tk.END, f"{title}:\n\n{result}\n")
        self.call_result.config(state=tk.DISABLED)
        self.status_var.set("Fake call analysis complete")

    # ---------------- Usage ----------------
    def show_usage(self):
        texts = translations[self.language]
        self.clear_content_frame()
        self.status_var.set(texts["usage"])
        ttk.Label(self.content_frame, text=texts["usage_text"], justify='left', font=('Arial', 11)).pack(pady=20)


def main():
    root = tk.Tk()
    app = SafetyToolkitApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
