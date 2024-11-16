import os
import pytesseract
from PIL import Image, ImageEnhance
import gtts
import re
from PyPDF2 import PdfReader
from pydub import AudioSegment
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import pygame
import threading

# Initialize Flask app
app = Flask(__name__)

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Path for the generated audio file
AUDIO_FILE_PATH = "temp_output.mp3"

# Initialize pygame mixer
pygame.mixer.init()

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_image(image_path):
    """Extract text from an image file."""
    img = Image.open(image_path).convert("L")  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Adjust contrast for better OCR
    custom_config = r'--oem 1 --psm 3'  # Adjust the OCR settings for better recognition
    text = pytesseract.image_to_string(img, config=custom_config, lang="eng")
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text.strip()

def clean_text(text):
    """Clean extracted text to remove unnecessary spaces, unwanted characters, or extra punctuation."""
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    return text.strip()

def adjust_speed(audio_file_path, speed_factor):
    """Adjust playback speed of the audio using pydub."""
    sound = AudioSegment.from_mp3(audio_file_path)
    # Ensure speed_factor is reasonable (e.g., 0.5x to 2x)
    if speed_factor <= 0:
        raise ValueError("Speed factor must be greater than 0.")
    
    adjusted_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed_factor)
    }).set_frame_rate(sound.frame_rate)
    
    adjusted_sound.export(AUDIO_FILE_PATH, format="mp3")


def speak_text(text, speed_factor=1.0):
    """Convert text to speech, adjust speed, and save it as an audio file."""
    try:
        tts = gtts.gTTS(text=text, lang='en', slow=False)
        temp_audio_path = "temp_output.mp3"
        tts.save(temp_audio_path)

        # Adjust playback speed
        adjust_speed(temp_audio_path, speed_factor)
        os.remove(temp_audio_path)

    except Exception as e:
        print(f"Error during text-to-speech: {e}")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and text extraction."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text based on file type
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            text = extract_text_from_image(file_path)
        elif filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            return jsonify({'error': 'Unsupported file type'})

        # Clean extracted text
        cleaned_text = clean_text(text)

        # Return extracted and cleaned text
        return jsonify({'text': cleaned_text})
    else:
        return jsonify({'error': 'Invalid file format'})

playback_lock = threading.Lock()

@app.route('/play_text', methods=['POST'])
def play_text():
    """Start playing the audio."""
    try:
        text = request.form['text']  # Get the text from the form
        speed = float(request.form.get('speed', 1.0))  # Get playback speed from the slider (default 1.0)

        # Call the speak_text function with the adjusted speed
        speak_text(text, speed)

        # Load and play the generated audio file
        pygame.mixer.music.load(AUDIO_FILE_PATH)
        pygame.mixer.music.play()
        
        return jsonify({'status': 'playing', 'speed': speed})
    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/pause', methods=['POST'])
def pause_audio():
    """Pause the audio playback."""
    try:
        pygame.mixer.music.pause()
        return jsonify({'status': 'paused'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/resume', methods=['POST'])
def resume_audio():
    """Resume the audio playback."""
    try:
        pygame.mixer.music.unpause()
        return jsonify({'status': 'resumed'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/stop', methods=['POST'])
def stop_audio():
    """Stop the audio playback."""
    try:
        pygame.mixer.music.stop()
        return jsonify({'status': 'stopped'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

