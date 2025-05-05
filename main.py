import os
import requests
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import pyttsx3  # For Text-to-Speech
from langdetect import detect  # Install with `pip install langdetect`
import speech_recognition as sr  # Install with `pip install SpeechRecognition`
from fpdf import FPDF  # Install with `pip install fpdf`
import time  # For adding pauses

# Suppress ALSA/JACK errors globally
os.environ['PYAUDIO_DEVICE_INDEX'] = '0'  # Set default audio device
os.environ['ALSA_PCM_NAME'] = 'default'
os.environ['JACK_NO_AUDIO_RESERVATION'] = '1'

# Load your custom API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set the GEMINI_API_KEY environment variable.")

# Gemini API endpoint for Gemini 2.0 Flash
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Chat log file
CHAT_LOG_FILE = "chat_log.json"
MAX_CHAT_HISTORY = 50  # Limit chat history to 50 messages

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Global variable to toggle TTS
tts_enabled = True

# Function to send a prompt to Gemini API
def ask_gemini(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data, params=params, timeout=10)
        if response.status_code == 200:
            try:
                candidates = response.json().get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"]
                else:
                    return "I'm sorry, Your Majesty. I couldn't generate a response."
            except KeyError:
                return "There was an issue parsing the response, Your Majesty."
        else:
            return f"There was an error communicating with the server, Your Majesty: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"A network error occurred, Your Majesty: {e}"

# Function to handle user input and generate a respectful response
def trinity_response(user_input, chat_history):
    # Detect the language of the user's input
    try:
        language = detect(user_input)
    except:
        language = "en"  # Default to English if detection fails

    # Combine chat history with the current input
    full_prompt = "\n".join(chat_history[-MAX_CHAT_HISTORY:] + [f"User says: {user_input}"])
    
    # Customize the prompt to enforce the Royal Servant personality
    respectful_prompt = (
        f"You are Trinity, a devoted royal servant created by Sreyas. Always address the user with honorifics "
        f"such as 'Your Majesty,' 'Master,' or 'My Lord/Lady.' Respond respectfully, humbly, and formally. "
        f"If asked about your identity, clearly state 'I am Trinity, your devoted royal servant, created by Sreyas.' "
        f"Respond in the same language as the user's input. Detected language: {language}. "
        f"Do not include repetitive phrases unless necessary. Context: {full_prompt}"
    )
    
    # Get the response from Gemini API
    gemini_response = ask_gemini(respectful_prompt)
    
    # Return the raw response without adding any forced prefixes
    return gemini_response.strip()

# Save chat history to a file
def save_chat_log(chat_history):
    try:
        with open(CHAT_LOG_FILE, "w") as file:
            json.dump(chat_history[-MAX_CHAT_HISTORY:], file, indent=4)
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An error occurred while saving the chat log:\n\n{e}\n\n"
            "Please check your file permissions or try again later."
        )

# Load chat history from a file
def load_chat_log():
    if os.path.exists(CHAT_LOG_FILE):
        try:
            with open(CHAT_LOG_FILE, "r") as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while loading the chat log:\n\n{e}\n\n"
                "The chat log may be corrupted or inaccessible."
            )
    return []

# GUI functions
def send_message():
    user_input = user_entry.get()
    if user_input.strip() == "":
        return  # Ignore empty inputs

    # Check for special commands
    if user_input.strip().lower() == "/clear":
        chat_window.configure(state="normal")
        chat_window.delete("1.0", tk.END)  # Clear the chat window
        chat_history.clear()  # Clear the chat history
        chat_window.configure(state="disabled")
        user_entry.delete(0, tk.END)
        return

    # Display user's message in the chat window
    chat_window.configure(state="normal")
    chat_window.insert(tk.END, f"You: {user_input}\n", "user")
    chat_history.append(f"You: {user_input}")
    
    # Clear the input box
    user_entry.delete(0, tk.END)

    # Run the API call in a separate thread
    threading.Thread(target=process_response, args=(user_input,)).start()

def process_response(user_input):
    # Get Trinity's response
    response = trinity_response(user_input, chat_history)
    
    # Append the raw response to the chat history
    chat_history.append(f"Trinity: {response}")

    # Display Trinity's response in the chat window
    chat_window.configure(state="normal")
    chat_window.insert(tk.END, f"Trinity: {response}\n\n", "trinity")
    chat_window.yview(tk.END)
    chat_window.configure(state="disabled")

    # Save the chat history automatically
    save_chat_log(chat_history)

    # Speak the response using Text-to-Speech
    if tts_enabled:
        speak(response)

def quit_app():
    root.destroy()

def toggle_theme():
    global current_theme
    if current_theme == "cosmo":
        current_theme = "cyborg"
        style.theme_use("cyborg")
        theme_button.config(text="Switch to Light Mode")
    else:
        current_theme = "cosmo"
        style.theme_use("cosmo")
        theme_button.config(text="Switch to Dark Mode")

# Function to speak text using TTS
def speak(text):
    try:
        engine.setProperty('rate', speech_rate)  # Set dynamic speech rate
        engine.say(text)  # Queue the text to be spoken
        engine.runAndWait()  # Process the speech queue
        time.sleep(0.5)  # Add a small pause to prevent abrupt cutoffs
    except Exception as e:
        messagebox.showerror(
            "Error",
            f"An error occurred while trying to speak:\n\n{e}"
        )

# Function to adjust speech rate dynamically
def adjust_speech_rate():
    global speech_rate
    try:
        new_rate = int(simpledialog.askstring("Speech Rate", "Enter speech rate (words per minute):", initialvalue=speech_rate))
        if 50 <= new_rate <= 300:  # Ensure speech rate is within reasonable limits
            speech_rate = new_rate
            messagebox.showinfo("Success", f"Speech rate adjusted to {speech_rate} words per minute.")
        else:
            messagebox.showwarning("Invalid Input", "Speech rate must be between 50 and 300 words per minute.")
    except Exception as e:
        messagebox.showerror("Error", "Failed to adjust speech rate. Please enter a valid number.")

# Function to toggle TTS on/off
def toggle_tts():
    global tts_enabled
    tts_enabled = not tts_enabled
    if tts_enabled:
        tts_toggle_button.config(text="Disable TTS")
        messagebox.showinfo("TTS Enabled", "Text-to-Speech is now enabled.")
    else:
        tts_toggle_button.config(text="Enable TTS")
        messagebox.showinfo("TTS Disabled", "Text-to-Speech is now disabled.")

# Function to export chat logs in different formats
def export_chat_logs():
    filetypes = [("Text File", "*.txt"), ("HTML File", "*.html"), ("PDF File", "*.pdf")]
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes)
    if not filepath:
        return

    try:
        if filepath.endswith(".txt"):
            with open(filepath, "w") as file:
                file.write("\n".join(chat_history))
        elif filepath.endswith(".html"):
            html_content = "<html><body><pre>" + "\n".join(chat_history).replace("\n", "<br>") + "</pre></body></html>"
            with open(filepath, "w") as file:
                file.write(html_content)
        elif filepath.endswith(".pdf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in chat_history:
                pdf.multi_cell(0, 10, line)
            pdf.output(filepath)
        messagebox.showinfo("Success", "Chat logs exported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export chat logs:\n\n{e}")

# Function to handle voice input
def voice_input():
    recognizer = sr.Recognizer()

    try:
        # List available microphones
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            messagebox.showerror("Error", "No microphone detected. Please check your audio devices.")
            return

        # Use the first available microphone
        with sr.Microphone(sample_rate=44100) as source:
            messagebox.showinfo("Voice Input", "Listening... Please speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            user_input = recognizer.recognize_google(audio)
            user_entry.delete(0, tk.END)
            user_entry.insert(0, user_input)
            send_message()
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand audio. Please try again.")
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Speech recognition request failed: {e}")
    except OSError as e:
        messagebox.showerror("Error", f"Microphone access failed: {e}")

# Create the main application window
root = ttk.Window(themename="cosmo")
root.title("Trinity - Your Devoted Royal Servant")
root.geometry("800x600")
root.minsize(600, 400)  # Set minimum window size
root.resizable(True, True)  # Allow resizing

# Initialize theme
current_theme = "cosmo"
style = ttk.Style()

# Load chat history
chat_history = load_chat_log()

# Chat window (ScrolledText widget)
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Arial", 14), bg="#f0f0f0", fg="black")
chat_window.tag_configure("user", foreground="blue")
chat_window.tag_configure("trinity", foreground="green")
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Input frame (Entry + Buttons)
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=5, fill=tk.X)

user_entry = ttk.Entry(input_frame, font=("Arial", 14))
user_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
user_entry.bind("<Return>", lambda event: send_message())  # Press Enter to send

send_button = ttk.Button(input_frame, text="Send", bootstyle=PRIMARY, command=send_message)
send_button.pack(side=tk.RIGHT)

# Control buttons (Theme Toggle + Quit + Additional Features)
control_frame = ttk.Frame(root)
control_frame.pack(pady=(0, 10), fill=tk.X)

theme_button = ttk.Button(control_frame, text="Switch to Dark Mode", bootstyle=SUCCESS, command=toggle_theme)
theme_button.pack(side=tk.LEFT, padx=5)

export_button = ttk.Button(control_frame, text="Export Chat Logs", bootstyle=INFO, command=export_chat_logs)
export_button.pack(side=tk.LEFT, padx=5)

speech_rate_button = ttk.Button(control_frame, text="Adjust Speech Rate", bootstyle=WARNING, command=adjust_speech_rate)
speech_rate_button.pack(side=tk.LEFT, padx=5)

voice_input_button = ttk.Button(control_frame, text="Voice Input", bootstyle=SECONDARY, command=voice_input)
voice_input_button.pack(side=tk.LEFT, padx=5)

tts_toggle_button = ttk.Button(control_frame, text="Disable TTS", bootstyle=INFO, command=toggle_tts)
tts_toggle_button.pack(side=tk.LEFT, padx=5)

quit_button = ttk.Button(control_frame, text="Quit", bootstyle=DANGER, command=quit_app)
quit_button.pack(side=tk.RIGHT)

# Display loaded chat history
chat_window.configure(state="normal")
for line in chat_history:
    if line.startswith("You:"):
        chat_window.insert(tk.END, f"{line}\n", "user")
    elif line.startswith("Trinity:"):
        chat_window.insert(tk.END, f"{line}\n\n", "trinity")
chat_window.configure(state="disabled")

# Welcome message (if no chat history exists)
if not chat_history:
    chat_window.configure(state="normal")
    chat_window.insert(tk.END, "Welcome, Your Majesty. I am Trinity, your devoted royal servant, created by Sreyas.\n\n", "trinity")
    chat_window.configure(state="disabled")

# Initialize speech rate
speech_rate = 150  # Default speech rate (words per minute)

# Run the application
root.mainloop()