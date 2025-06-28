
# 🎧 MP3/MP4 to Text & Subtitle Converter (GUI)

A simple, GPU-accelerated desktop app to transcribe `.mp3` or `.mp4` files into professional-quality text or `.srt` subtitles using OpenAI's Whisper model. Built with Python and `customtkinter` for a modern GUI.

---

## ✅ Features

* 🎙️ Convert **MP3** or **MP4** to clean, normalized `.wav`
* 🧠 Transcribe using **OpenAI Whisper** with GPU acceleration (if available)
* 🧼 Automatic volume normalization for clearer transcription
* 📜 Export transcription as `.txt` or `.srt` subtitle format
* 🔄 Background processing for smooth, non-blocking GUI

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/mp4-mp3-to-text-gui.git
cd mp4-mp3-to-text-gui
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**

* `customtkinter`
* `pydub`
* `whisper`
* `torch` (for GPU support)
* `ffmpeg` (must be installed and added to PATH)

### 3. Install `ffmpeg`

* 🔗 [FFmpeg download](https://ffmpeg.org/download.html)
* Add `ffmpeg` to your system's PATH for `pydub` to work correctly.

---

## 🧪 Usage

```bash
python app.py
```

1. Select an `.mp3` or `.mp4` file.
2. The tool will:

   * Normalize and clean the audio.
   * Use Whisper to transcribe the audio.
   * Display the result in a textbox.
3. Choose to save the result as:

   * `.txt` (plain transcription)
   * `.srt` (subtitle format with timestamps)

---

## 📂 Output Example

### `example.srt`

```srt
1
00:00:00,000 --> 00:00:02,300
Hello and welcome to our video.

2
00:00:02,300 --> 00:00:05,500
In this tutorial, we'll explore Whisper by OpenAI.
```

---

## ⚙️ Configuration

* Model used: `base` (you can change to `tiny`, `medium`, etc. in the code)
* GPU usage: Automatically uses GPU if available (`torch.cuda.is_available()`)

---

## 💡 Notes

* Works offline once Whisper is downloaded.
* Works best with clear audio.
* Subtitle formatting follows standard `.srt` convention.

---

## 📜 License

MIT License. Free to use and modify.

---

Let me know if you'd like badges, screenshots, or deployment info added to the README.
