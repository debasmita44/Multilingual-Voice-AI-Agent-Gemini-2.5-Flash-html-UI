from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from backend.modules.speech_to_text import transcribe_audio
from backend.modules.language_detector import detect_language
from backend.modules.llm_handler import generate_response
from backend.modules.text_to_speech import text_to_speech

app = Flask(__name__, 
            static_folder='frontend',
            template_folder='frontend')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-voice', methods=['POST'])
def process_voice():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Save uploaded audio temporarily
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.webm')
        audio_file.save(audio_path)
        
        # Step 1: Transcribe audio to text
        transcribed_text = transcribe_audio(audio_path)
        if not transcribed_text:
            return jsonify({'error': 'Failed to transcribe audio'}), 500
        
        # Step 2: Detect language
        detected_language = detect_language(transcribed_text)
        
        # Step 3: Generate response using Gemini
        ai_response = generate_response(transcribed_text, detected_language)
        
        # Step 4: Convert response to speech
        output_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'response_audio.mp3')
        text_to_speech(ai_response, detected_language, output_audio_path)
        
        # Clean up input audio
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        return jsonify({
            'transcribed_text': transcribed_text,
            'detected_language': detected_language,
            'ai_response': ai_response,
            'audio_url': '/get-audio'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-audio', methods=['GET'])
def get_audio():
    try:
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'response_audio.mp3')
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/mpeg')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)