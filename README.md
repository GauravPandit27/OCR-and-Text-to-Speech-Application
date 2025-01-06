
---

# OCR and Text-to-Speech Application

This project demonstrates the integration of Optical Character Recognition (OCR) and Text-to-Speech (TTS) technologies into a simple yet powerful web-based Python application. The application allows users to upload images or PDF files, extract text from them using OCR, and convert the extracted text into speech. This solution is designed with accessibility in mind, making it ideal for users with visual impairments or for document processing tasks.

## Key Features:
- **OCR Integration:** Extract text from image files (`PNG`, `JPG`, `JPEG`) using Tesseract OCR.
- **PDF Text Extraction:** Extract and clean text from PDF files.
- **Text-to-Speech Conversion:** Convert the extracted text into speech using Google Text-to-Speech (gTTS).
- **Playback Controls:** Play, pause, resume, and stop the audio playback with user-friendly controls.
- **Adjustable Playback Speed:** Customize the speech speed for better accessibility or personal preference.
- **Web Interface:** A Flask web app to upload files and interact with the TTS functionality.

## Technologies Used:
- **Flask:** Web framework for building the web application.
- **Tesseract OCR:** Optical character recognition for extracting text from images.
- **gTTS (Google Text-to-Speech):** Text-to-speech conversion for the extracted text.
- **PyPDF2:** Extract text from PDF files.
- **pygame:** For audio playback and control.
- **Python's PIL (Pillow):** For image processing and enhancement to improve OCR accuracy.
- **pydub:** For adjusting the playback speed of the audio.

## Installation:
1. Clone the repository:

```bash
git clone https://github.com/yourusername/ocr-and-text-to-speech.git
cd ocr-and-text-to-speech
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure you have **Tesseract OCR** installed. You can install it from [here](https://github.com/tesseract-ocr/tesseract).

4. Run the Flask application:

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

## Usage:
- **Upload Files:** Users can upload image files or PDFs from the main page to extract text.
- **Text-to-Speech Playback:** After text extraction, the user can press a button to convert the text to speech, with adjustable speed.
- **Playback Controls:** Users can play, pause, resume, and stop the speech audio using provided buttons.

## Example Use Case:
- **Accessibility:** Ideal for visually impaired users who want to listen to the contents of documents or images.
- **Document Processing:** Quickly convert scanned documents or PDF files into audible content for easier review.

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments:
- **Tesseract OCR**: An open-source OCR engine.
- **gTTS**: Google's Text-to-Speech library.
- **PyPDF2**: A Python library for PDF text extraction.

---
