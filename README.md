# AI-Powered Interior Design Assistant

## Overview
This project is an AI-powered interior design assistant that analyzes images of interiors and suggests modifications to make them look modern. It utilizes Google's Generative AI (Gemini 1.5 Flash) for image analysis and Clipdrop API for text-to-image generation. The Flask web server provides API endpoints for image analysis, generation, and retrieval.

## Features
- **Image Analysis:** Analyzes interior images and provides suggestions for modern design, including furniture, colors, and layouts.
- **Text-to-Image Generation:** Generates AI-powered interior design images based on user prompts.
- **Logging:** Stores analysis results in a log file.
- **Ngrok Integration:** Exposes the local Flask server using a public Ngrok tunnel.

## Tech Stack
- **Backend:** Flask (Python)
- **AI Services:** Google Gemini AI, Clipdrop API
- **Image Processing:** PIL (Pillow)
- **Server Exposure:** Pyngrok
- **Deployment:** Local Flask server with Ngrok tunneling

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- Ngrok account with a static domain (if needed)

### Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kshitizsinghal13/interior-ai.git
   cd interior-ai
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Keys:**
   - Update `DEFAULT_API_KEY` with your Gemini API key in `app.py`.
   - Update `API_KEY` for Clipdrop API in `app.py`.

4. **Run the Flask Server:**
   ```bash
   python app.py
   ```

5. **Ngrok Setup:**
   - Ensure Ngrok is installed and linked to your account.
   - The script will automatically create a public URL for the server.

## API Endpoints
### `GET /`
- Loads the homepage (`index.html`).

### `POST /analyze`
- **Request:** JSON with base64-encoded image.
- **Response:** AI-generated design suggestions.

### `POST /generate`
- **Request:** JSON with a text prompt.
- **Response:** AI-generated interior design image.

### `GET /generated_images/<filename>`
- Retrieves the generated image from the server.

### `POST /stop`
- Stops speech synthesis.

## File Structure
```
interior-ai/
│── app.py                  # Main Flask application
│── requirements.txt        # Python dependencies
│── templates/
│   └── index.html          # Frontend UI
│── captured_images/        # Stores uploaded images
│── generated_images/       # Stores AI-generated images
│── responses.log           # Logs AI responses
└── README.md               # Documentation
```

## Troubleshooting
- **API Key Errors:** Ensure your API keys are correct and active.
- **Ngrok Connection Issues:** Check if your domain is set up correctly.
- **Image Processing Errors:** Ensure the base64 image data is correctly formatted.

## Future Enhancements
- Integrate additional AI models for design recommendations.
- Improve the UI for better user interaction.
- Add support for real-time voice-based recommendations.


