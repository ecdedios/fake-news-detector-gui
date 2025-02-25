import tkinter as tk
from tkinter import scrolledtext, messagebox
import openai
import json

def analyze_news():
    """Send the entered text to OpenAI for fake news analysis."""
    news_text = text_area.get("1.0", tk.END).strip()
    api_key = api_key_entry.get().strip()
    
    if not news_text:
        messagebox.showwarning("Input Error", "Please enter a news headline or article.")
        return
    if not api_key:
        messagebox.showwarning("Input Error", "Please enter your OpenAI API key.")
        return
    
    try:
        client = openai.OpenAI(api_key=api_key)  # Initialize OpenAI client
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert fact-checker. Analyze the following text and determine if it sounds credible or suspicious. Provide reasoning, a confidence score from 0 to 100, and supporting details."},
                {"role": "user", "content": news_text}
            ]
        )
        result = response.choices[0].message.content
        
        # Extract confidence score and breakdown
        try:
            result_json = json.loads(result)
            analysis = result_json.get("analysis", "No analysis provided.")
            confidence = result_json.get("confidence", "Unknown confidence score.")
            reasoning = result_json.get("reasoning", "No reasoning provided.")
            
            output_label.config(text=f"Analysis Result (Confidence: {confidence}%)")
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"Reasoning:\n{reasoning}\n\nAnalysis:\n{analysis}")
        except json.JSONDecodeError:
            output_label.config(text="Analysis Result:")
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze text: {e}")

# Set up Tkinter GUI
root = tk.Tk()
root.title("AI Fake News Detector")
root.geometry("600x500")

# API Key Input
tk.Label(root, text="Enter OpenAI API Key:", font=("Arial", 12)).pack(pady=5)
api_key_entry = tk.Entry(root, width=50, show="*")
api_key_entry.pack(pady=5)

# Label
tk.Label(root, text="Enter a News Headline or Article:", font=("Arial", 12)).pack(pady=5)

# Text Area
text_area = scrolledtext.ScrolledText(root, height=5, width=70, wrap=tk.WORD)
text_area.pack(pady=5)

# Analyze Button
tk.Button(root, text="Analyze", font=("Arial", 12), command=analyze_news).pack(pady=10)

# Output Label
output_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
output_label.pack()

# Output Text Area
output_text = scrolledtext.ScrolledText(root, height=7, width=70, wrap=tk.WORD)
output_text.pack(pady=5)

root.mainloop()
