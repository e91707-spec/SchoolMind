# SchoolMind UI - Python Version

## 🚀 Quick Start

### Option 1: Double-click (Recommended)
1. Double-click `start-schoolmind.bat`
2. Wait 2-3 seconds
3. Browser will open automatically with the UI

### Option 2: Command Line
```bash
python launch-ui.py
```

### Option 3: Direct Server
```bash
python ui_server.py
```
Then open http://localhost:3000 in your browser

## 📁 Files Created

- **`ui_server.py`** - Main UI server with embedded HTML/CSS/JS
- **`launch-ui.py`** - Launcher that hides console window
- **`start-schoolmind.bat`** - One-click launcher (Windows)
- **`requirements.txt`** - Python dependencies

## 🔧 Dependencies

Install with:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install fastapi uvicorn httpx playwright
```

## 🌐 How It Works

1. **ui_server.py** runs a FastAPI server on port 3000
2. **launch-ui.py** starts the server in background using pythonw (no console)
3. **start-schoolmind.bat** provides one-click launch
4. Browser opens automatically to http://localhost:3000

## 🎯 Features

- ✅ Same beautiful UI as the original HTML
- ✅ Model selection (Hermes 2, Qwen 2.5, Qwen 5)
- ✅ Smart mode auto-selection
- ✅ Web search integration
- ✅ No console window visible
- ✅ Auto-opens browser

## 🔗 Integration

The UI connects to:
- **Ollama** (localhost:11434) for AI models
- **Search Server** (localhost:8000) for web search
- **Camoufox** (localhost:8001) for advanced browser automation

Make sure these services are running for full functionality!

## 🛑 Stopping the Server

- Close the launcher window (if using `launch-ui.py`)
- Or press Ctrl+C in the launcher
- The UI server will stop automatically

## 🐛 Troubleshooting

**UI doesn't open:**
- Check if port 3000 is available
- Install dependencies: `pip install -r requirements.txt`

**Browser doesn't open:**
- Manually open http://localhost:3000
- Check your default browser settings

**Console still appears:**
- Use `start-schoolmind.bat` instead
- Make sure pythonw.exe is available

## 📝 Notes

- The original HTML file is still available as backup
- All functionality from the HTML version is preserved
- Server runs in background, no console window needed
