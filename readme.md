# 🌸 Local File Uploader & Tester (Python)

A clean and educational **Python Desktop application** that allows users to browse and load files locally, then run structured tests on them — **without using any server or internet connection**.

This project also includes **unit tests (pytest)** inside the same file to validate the core logic independently of the GUI.

---

## ✨ Features

- 📂 Browse and select files from your computer
- 📥 Load files locally into the program (no server, no upload)
- 🧪 Run automatic tests on the selected file
- 📊 Display detailed results in the GUI
- 🌸 Cute and clean **Pink UI** built with Tkinter
- ✅ Built-in **Unit Tests** using pytest
- 🧠 Clear separation between logic and interface

---

## 🧠 What “Upload” Means Here

The term **Upload** in this project does **NOT** mean uploading files to the internet.

It means:

> Loading a file from disk into the program’s memory for analysis and testing.

This makes the project safe, offline, and ideal for learning and experimentation.

---

## 🧪 File Tests Performed

The program performs several checks, including:

- File is not empty
- File size is under 5 MB
- File extension is allowed
- File type detection (text vs binary)
- Text content length validation
- Forbidden word detection (configurable)

All results are shown clearly in the application interface.

---

## 🖥️ Running the Desktop Application

```bash
python pink_file_tester.py
