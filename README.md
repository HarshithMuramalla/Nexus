# Nexus Chat Application

![Nexus Chat](https://via.placeholder.com/800x400?text=Nexus+Chat+Application)

Nexus Chat is a real-time chat application powered by Ollama's AI models, providing intelligent and responsive chat capabilities. Built with Flask and modern web technologies, it offers a seamless chat experience with AI-powered responses.

## ✨ Features

- 💬 Real-time AI-powered chat interface
- 🚀 Built with Flask backend and vanilla JavaScript frontend
- 🤖 Integration with Ollama's AI models
- 🎨 Clean and responsive user interface
- 🔄 Real-time message streaming
- 🛠️ Easy to deploy and customize

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Ollama server running locally (default: http://localhost:11434)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HarshithMuramalla/Nexus.git
   cd Nexus
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors requests
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   OLLAMA_API=http://localhost:11434/api/chat
   OLLAMA_MODEL=nexus  # or your preferred Ollama model
   ```

5. **Start the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Visit `http://localhost:8000` to access the chat application

## 🛠️ Project Structure

```
nexus_chat/
├── static/               # Static files (CSS, JS, images)
│   ├── chat.js          # Frontend JavaScript
│   ├── style.css        # Stylesheet
│   └── Genesisfile.py   # Additional Python utilities
├── templates/            # HTML templates
│   └── index.html       # Main application page
├── app.py               # Flask application
└── README.md            # This file
```

## 🔧 Configuration

You can configure the application using the following environment variables:

- `OLLAMA_API`: URL to your Ollama API (default: `http://localhost:11434/api/chat`)
- `OLLAMA_MODEL`: The Ollama model to use (default: `nexus`)
- `FLASK_ENV`: Set to `development` for debug mode
- `PORT`: Port to run the Flask app on (default: `8000`)

## 🤖 Customizing the AI Model

To use a different Ollama model:

1. Pull the desired model:
   ```bash
   ollama pull <model-name>
   ```

2. Update the `OLLAMA_MODEL` environment variable in your `.env` file

## 🌐 Deployment

### Local Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

### Production Deployment

For production deployment, consider using:

- Gunicorn or uWSGI as a WSGI server
- Nginx as a reverse proxy
- Environment variables for configuration
- Process manager like PM2 or Supervisor

Example with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for the AI models
- [Flask](https://flask.palletsprojects.com/) for the web framework
- All contributors and open-source libraries used

---

Made with ❤️ by Harshith Muramalla
