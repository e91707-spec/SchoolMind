# 📚 SchoolMind - AI Study Companion

An intelligent AI assistant designed specifically for students, featuring multiple models, web search integration, and both web and desktop interfaces.

## ✨ Features

### 🤖 Multiple AI Models
- **Hermes 2 (10.7B)** - Best for essays and detailed answers
- **Qwen 2.5 (14B)** - Fast and versatile all-rounder
- **Qwen 2.5 (7B)** - Quick answers and summaries

### 🎯 Smart Mode
- Automatically selects the best model based on your question type
- Essays & Writing → Hermes 2
- Complex Questions → Qwen 2.5 (14B)
- Quick Answers → Qwen 2.5 (7B)

### 🔍 Web Search Integration
- Automatically searches the web for factual questions
- Verifies information with current sources
- Helps with historical dates, statistics, and current events

### 🖥️ Dual Interface Options
- **Web Interface**: Modern browser-based UI
- **Desktop Application**: Standalone GUI application
- Both feature beautiful dark themes and full functionality

### 📝 Markdown Support
- **Bold text**: `**text**`
- **Italic text**: `*text*`
- **Code formatting**: `` `code` ``
- Proper rendering in both interfaces

## 🚀 Quick Start

### Prerequisites
1. **Ollama** - Install and run Ollama locally
2. **AI Models** - Pull required models:
   ```bash
   ollama pull nous-hermes2:10.7b
   ollama pull qwen2.5:14b
   ollama pull qwen2.5:7b
   ```
3. **Python 3.8+** - For running the applications

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/e91707-spec/SchoolMind.git
   cd SchoolMind
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Ollama (if not already running):
   ```bash
   ollama serve
   ```

## 🎮 Usage

### Web Interface
**Option 1: Auto-launch (Recommended)**
```bash
# Double-click or run:
start-schoolmind.bat
```

**Option 2: Manual launch**
```bash
python launch-ui.py
```

**Option 3: Direct server**
```bash
python ui_server.py
# Then open http://localhost:3000
```

### Desktop Application
**Option 1: One-click launch**
```bash
# Double-click or run:
start-desktop.bat
```

**Option 2: Manual launch**
```bash
python schoolmind_desktop.py
```

### Advanced Features

#### Web Search Server
For enhanced web search capabilities:
```bash
python search-server.py
# Runs on http://localhost:8000
```

#### Camoufox Integration
For JavaScript-heavy websites and advanced browser automation:
```bash
python camoufox-integration.py
# Runs on http://localhost:8001
```

## 📁 Project Structure

```
SchoolMind/
├── 📄 README.md                    # This file
├── 📄 requirements.txt              # Python dependencies
├── 🐍 schoolmind_desktop.py        # Desktop GUI application
├── 🐍 ui_server.py               # Web UI server
├── 🐍 search-server.py            # Web search functionality
├── 🐍 camoufox-integration.py     # Advanced browser automation
├── 🐍 launch-ui.py               # Web UI launcher (hidden console)
├── 🐍 start-schoolmind.bat        # One-click web UI launcher
├── 🐍 start-desktop.bat          # One-click desktop launcher
├── 🐍 restart-web-ui.bat         # Restart web UI with cache clear
├── 🐍 README-UI.md              # UI-specific documentation
├── 🐍 SETUP_GUIDE.md            # Detailed setup instructions
└── 📄 school-ai-assistant.html   # Original HTML interface
```

## ⚙️ Configuration

### Model Selection
- Use the radio buttons to manually select a model
- Enable Smart Mode for automatic model selection
- Each model is optimized for different types of questions

### Web Search
- Toggle "Search web for facts" to enable/disable
- Automatically activates for factual questions
- Uses DuckDuckGo for privacy-focused search

### Customization
- Dark theme optimized for long study sessions
- Responsive design works on all screen sizes
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)

## 🔧 Technical Details

### Architecture
- **Backend**: FastAPI (web), Tkinter (desktop)
- **AI Integration**: Ollama local models
- **Web Search**: DuckDuckGo API + Camoufox automation
- **Frontend**: HTML/CSS/JavaScript (web), Python GUI (desktop)

### Dependencies
- `fastapi` - Web server framework
- `uvicorn` - ASGI server
- `httpx` - HTTP client
- `playwright` - Browser automation (optional)
- `tkinter` - Desktop GUI (built-in)

### Model Information
- **Hermes 2**: 10.7B parameters, optimized for creative writing
- **Qwen 2.5**: 14B/7B parameters, balanced performance
- All models run locally for privacy and speed

## 🎯 Use Cases

### 📝 Writing & Essays
- Brainstorming ideas
- Structuring essays
- Improving writing style
- Creative writing assistance

### ❓ Homework Help
- Math problem explanations
- Science concepts
- Historical information
- Literature analysis

### 📚 Learning & Study
- Complex topic explanations
- Study strategies
- Exam preparation
- Research assistance

## 🛠️ Troubleshooting

### Common Issues

**"Model not found" error**
- Ensure Ollama is running: `ollama serve`
- Check installed models: `ollama list`
- Pull missing models with commands above

**Web search not working**
- Start search server: `python search-server.py`
- Check internet connection
- Verify DuckDuckGo accessibility

**Desktop app won't start**
- Install tkinter: usually included with Python
- Check Python version: requires 3.8+
- Run as administrator if needed

**Browser UI not loading**
- Clear browser cache (Ctrl+F5)
- Check if port 3000 is available
- Try different browser

### Getting Help
1. Check this README for solutions
2. Review SETUP_GUIDE.md for detailed instructions
3. Open an issue on GitHub
4. Check existing issues and discussions

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution
- 🎨 UI/UX improvements
- 🤖 Additional model integrations
- 🔍 Enhanced search capabilities
- 📱 Mobile responsiveness
- 🌍 Multi-language support

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Ollama** - Local AI model hosting
- **Qwen** - High-quality language models
- **Nous Research** - Hermes model series
- **DuckDuckGo** - Privacy-focused search
- **FastAPI** - Modern web framework

## 📞 Contact

- **GitHub**: https://github.com/e91707-spec/SchoolMind
- **Issues**: https://github.com/e91707-spec/SchoolMind/issues

---

**🎓 Made with ❤️ for students everywhere**
