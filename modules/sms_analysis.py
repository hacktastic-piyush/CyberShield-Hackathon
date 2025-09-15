import tkinter as tk
from tkinter import ttk, scrolledtext
from gui_config import text_strings

class SmsAnalysisFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.spam_keywords = ["winner", "prize", "free", "urgent", "cash", "claim now", "लॉटरी", "इनाम", "रुपये"] # English & Hindi keywords
        
        # Create widgets
        self.label = ttk.Label(self, text=text_strings["english"]["sms_input_label"])
        self.text_area = scrolledtext.ScrolledText(self, width=70, height=10)
        self.analyze_btn = ttk.Button(self, text=text_strings["english"]["sms_analyze_button"], command=self.analyze_sms)
        self.result_label = ttk.Label(self, text=text_strings["english"]["result_label"])
        self.result_text = tk.StringVar(value="Analysis will appear here.")
        self.result_display = ttk.Label(self, textvariable=self.result_text, wraplength=600, foreground="red")
        
        # Layout widgets
        self.label.pack(pady=(20, 5))
        self.text_area.pack(pady=5)
        self.analyze_btn.pack(pady=5)
        self.result_label.pack(pady=(20, 5))
        self.result_display.pack(pady=5)
    
    def analyze_sms(self):
        # Get text from the text widget
        sms_text = self.text_area.get("1.0", tk.END).lower().strip()
        
        if not sms_text:
            self.result_text.set("Please enter some text to analyze.")
            return
        
        # Simple logic: Check for spam keywords
        found_keywords = []
        for keyword in self.spam_keywords:
            if keyword in sms_text:
                found_keywords.append(keyword)
        
        if found_keywords:
            result = f"WARNING: Potential spam detected.\nSuspicious keywords found: {', '.join(found_keywords)}"
            self.result_display.config(foreground="red")
        else:
            result = "This message appears to be safe. No obvious spam keywords detected."
            self.result_display.config(foreground="green")
        
        self.result_text.set(result)
    
    def update_text(self, language):
        # This is called when the language is switched
        self.label.config(text=text_strings[language]["sms_input_label"])
        self.analyze_btn.config(text=text_strings[language]["sms_analyze_button"])
        self.result_label.config(text=text_strings[language]["result_label"])
        # Note: The result text itself wouldn't be auto-translated in this simple version.
        # You would need to use a translation API for that.