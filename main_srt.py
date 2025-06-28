import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import whisper
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def convert_mp3_to_wav(mp3_path, progress_bar, progress_label):
    progress_label.set("Converting MP3 to WAV...")
    progress_bar.set(20)
    wav_path = mp3_path.replace(".mp3", ".wav")
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    progress_bar.set(50)
    return wav_path

def convert_mp4_to_wav(mp4_path, progress_bar, progress_label):
    progress_label.set("Extracting audio from MP4 and converting to WAV...")
    progress_bar.set(20)
    wav_path = mp4_path.replace(".mp4", ".wav")
    audio = AudioSegment.from_file(mp4_path, format="mp4")
    audio.export(wav_path, format="wav")
    progress_bar.set(50)
    return wav_path

def transcribe_audio(wav_path, progress_bar, progress_label):
    progress_label.set("Loading Whisper model...")
    progress_bar.set(60)
    model = whisper.load_model("base")
    progress_label.set("Transcribing audio...")
    progress_bar.set(80)
    result = model.transcribe(wav_path)
    progress_bar.set(100)
    progress_label.set("Transcription completed.")
    return result['text']

def generate_srt_from_audio(wav_path):
    model = whisper.load_model("base")
    result = model.transcribe(wav_path, task="transcribe", verbose=False)
    segments = result.get("segments", [])

    srt_content = ""
    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"

    save_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
    if save_path:
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(srt_content)
        messagebox.showinfo("Success", f"Subtitle saved to {save_path}")

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def save_transcription(text):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(text)
        messagebox.showinfo("Success", f"Transcription saved to {save_path}")

def process_file(progress_bar, progress_label, text_widget):
    file_path = filedialog.askopenfilename(filetypes=[("MP3 or MP4 Files", "*.mp3 *.mp4")])
    if not file_path:
        return

    def process():
        try:
            progress_bar.set(0)
            if file_path.endswith(".mp3"):
                wav_path = convert_mp3_to_wav(file_path, progress_bar, progress_label)
            elif file_path.endswith(".mp4"):
                wav_path = convert_mp4_to_wav(file_path, progress_bar, progress_label)
            else:
                raise ValueError("Unsupported file format")
            transcription = transcribe_audio(wav_path, progress_bar, progress_label)
            text_widget.delete("1.0", ctk.END)
            text_widget.insert(ctk.END, transcription)
            messagebox.showinfo("Congratulations", "Transcription Completed!")
            save_transcription(transcription)
            generate_srt_from_audio(wav_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    threading.Thread(target=process, daemon=True).start()

def setup_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Audio/Video to Text Converter")
    root.geometry("500x400")
    progress_label = ctk.StringVar(value="Welcome! Select an MP3 or MP4 file to begin.")
    label = ctk.CTkLabel(root, textvariable=progress_label, wraplength=450, font=("Arial", 14))
    label.pack(pady=10)
    progress_bar = ctk.CTkProgressBar(root, width=400)
    progress_bar.pack(pady=10)
    progress_bar.set(0)
    text_widget = ctk.CTkTextbox(root, wrap="word", width=450, height=150, font=("Arial", 12))
    text_widget.pack(pady=10, padx=10)
    process_button = ctk.CTkButton(root, text="Select MP3 or MP4 File", command=lambda: process_file(progress_bar, progress_label, text_widget))
    process_button.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
