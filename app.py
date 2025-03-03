from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import google.generativeai as genai
from PIL import Image
import pyttsx3
from pyngrok import ngrok
import base64
from io import BytesIO
import time
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Set up directories for storing images and logs
IMAGE_DIR = 'captured_images'
GENERATED_IMAGES_DIR = 'generated_images'
LOG_FILE = 'responses.log'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
if not os.path.exists(GENERATED_IMAGES_DIR):
    os.makedirs(GENERATED_IMAGES_DIR)

DEFAULT_API_KEY ="Your gemini-1.5-flash-latest api"
DEFAULT_PROMPT = (
    "Analyze the image and suggest all the necessary changes to make interior modern looking "
    "and suggest all things like wall color furniture shape size color location carpet design "
    "and color and everything you can and provide all the color and location of furniture like "
    "what electronic or furniture should be placed where to look more modern and latest trends. "
    "Provide the exact color shade you can take reference from different sources like Sherwin-Williams and other. "
    "You have to suggest the particular furniture including brand design color etc. Use a communicable tone as you are directly talking to the client"
    "do not return the result in boldhighlight use plain text"
)

engine = pyttsx3.init()

def capture_and_analyze(apikey, prompt, image_path):
    genai.configure(api_key=apikey)
    generation_configuration = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048
    }
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config=generation_configuration, safety_settings=None)
    image = Image.open(image_path)
    
    try:
        response = model.generate_content([prompt, image])
        result = response.text
        
        return result
    except Exception as e:
        print(f"Error during analysis: {e}")
        return "Error analyzing the image."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_data = data.get('image_data')

    if not image_data:
        return jsonify({'error': 'Image data is required'}), 400

    image_data = image_data.split(",")[1]
    
    try:
        image_bytes = Image.open(BytesIO(base64.b64decode(image_data)))
    except Exception as e:
        return jsonify({'error': f'Failed to decode image: {str(e)}'}), 400

    timestamp = int(time.time())
    temp_image_path = os.path.join(IMAGE_DIR, f'captured_image_{timestamp}.png')
    
    image_bytes.save(temp_image_path)
    
    result = capture_and_analyze(DEFAULT_API_KEY, DEFAULT_PROMPT, temp_image_path)

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"Image: {temp_image_path}, Result: {result}\n")

    return jsonify({'result': result})

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
 
    # API_KEY='b1cdbf9355dafbb7a8756be973b2cd551f37dbc06147b80a05a77b5b8ae4cc971beadc1accd23572683475dbc19a7b6f'
    API_KEY="Your clip api key"
    try:
        r = requests.post(
            'https://clipdrop-api.co/text-to-image/v1',
            files={'prompt': (None, prompt, 'text/plain')},
            headers={'x-api-key': API_KEY}
        )
        
        r.raise_for_status()

        generated_image_path = os.path.join(GENERATED_IMAGES_DIR, 'generated_image.png')
        
        with open(generated_image_path, 'wb') as f:
            f.write(r.content)

        # Return the URL of the generated image
        public_url = f'/generated_images/generated_image.png'
        
        return jsonify({'image_url': public_url})

    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f"HTTP error occurred: {http_err}"}), 500  
    except requests.exceptions.ConnectionError:
        return jsonify({'error': "Connection error occurred. Please check your internet connection."}), 500
    except requests.exceptions.Timeout:
        return jsonify({'error': "The request timed out."}), 500
    except requests.exceptions.RequestException as err:
        return jsonify({'error': f"An error occurred: {err}"}), 500

@app.route('/generated_images/<filename>')
def view_generated_image(filename):
    return send_from_directory(GENERATED_IMAGES_DIR, filename)

@app.route('/stop', methods=['POST'])
def stop():
    stop_speech()
    return jsonify({'status': 'Speech stopped'})



if __name__ == '__main__':
        port = 5000
        
        # Connect ngrok using your static domain
        public_url = ngrok.connect(port, domain='marmot-clever-correctly.ngrok-free.app').public_url  
        print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")
        
        app.run(port=port)
        
        
        
       