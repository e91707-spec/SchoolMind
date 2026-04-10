# SchoolMind - Setup & Usage Guide

Your AI-powered study companion with web search verification using local models.

## 🚀 Quick Start

### Prerequisites
- **Ollama** - Download from [ollama.ai](https://ollama.ai)
- **Local Models** - Already have these:
  - `nous-hermes2:10.7b`
  - `qwen2.5:14b`
  - `qwen5:7b`
- **Python 3.8+** (optional, for web search server)
- **Camoufox** (optional, for advanced browser automation)

---

## 📋 Installation Steps

### Step 1: Start Ollama
```bash
ollama serve
```
This starts the Ollama API on `http://localhost:11434`

### Step 2: Load Your Models (if not already loaded)
In a new terminal:
```bash
ollama pull nous-hermes2:10.7b
ollama pull qwen2.5:14b
ollama pull qwen5:7b
```

### Step 3: (Optional) Start Web Search Server
This enables web verification for factual answers.

**Install dependencies:**
```bash
pip install fastapi uvicorn httpx
```

**Run the server:**
```bash
python search-server.py
```
This starts on `http://localhost:8000`

### Step 4: Open the Interface
Open `school-ai-assistant.html` in your browser.

---

## ⚙️ Configuration

### Model Selection
Each model is optimized for different tasks:

| Model | Best For | Speed | Depth |
|-------|----------|-------|-------|
| **Hermes 2** (10.7b) | Essays, creative writing, detailed responses | Medium | Deep |
| **Qwen 2.5** (14b) | Complex analysis, explanations, homework | Medium | Deep |
| **Qwen 5** (7b) | Quick answers, summaries, brainstorming | Fast | Good |

### Web Search
- **Enabled by default** for factual questions
- Automatically detects: "what is", "when", "who", "statistics", "current", "history of", etc.
- Falls back to local knowledge if search unavailable
- Uses DuckDuckGo (no API key required)

### Smart Mode
When enabled, the AI automatically selects the best model:
- **Writing detected** → Uses Hermes 2
- **Complex questions** → Uses Qwen 2.5
- **Simple queries** → Uses Qwen 5

---

## 💡 Usage Tips

### For Essays & Writing
1. Select **Hermes 2** or enable Smart Mode
2. Be specific: "Write a 5-paragraph essay about..."
3. Ask for: structure, thesis statements, transitions
4. Request: examples, citations, formatting

### For Homework Help
1. Ask specific questions: "Explain photosynthesis" not just "help with homework"
2. Request: step-by-step explanations, examples, practice problems
3. Use web search to verify dates, statistics, historical facts
4. Disable web search for creative subjects where sources may not help

### For Test Prep
1. Ask for: key concepts, flashcard topics, common mistakes
2. Request: practice questions and answers
3. Use web search for current events/news questions
4. Create summary sheets by asking for comprehensive overviews

### Best Practices
- ✅ Be specific and detailed in questions
- ✅ Ask for examples and analogies
- ✅ Request step-by-step explanations
- ✅ Use web search for factual verification
- ✅ Verify important information independently
- ❌ Don't blindly copy responses
- ❌ Don't rely solely on this for critical grades
- ❌ Don't disable web search for fact-based questions

---

## 🔧 Troubleshooting

### "Failed to connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check that it's on `localhost:11434`
- Verify models are loaded: `ollama list`

### Web search not working
- Optional feature - still works without it
- Check search server is running on port 8000
- Try disabling/re-enabling web search toggle
- Check your internet connection

### Model not responding
- Wait a moment - first load takes time
- Check model is loaded: `ollama list`
- Try a different model
- Restart Ollama if stuck

### Slow responses
- Larger models (Hermes, Qwen 2.5) are slower but more detailed
- Try Qwen 5 for faster responses
- Close other applications using system resources
- Consider GPU acceleration in Ollama settings

---

## 🎯 Advanced Usage

### Custom System Prompts
Edit the system prompt in the JavaScript:
```javascript
const systemPrompt = `You are SchoolMind...`;
```

### Adding More Models
In the HTML, add to the model selection:
```html
<div class="model-option">
    <input type="radio" id="newModel" name="model" value="model-name:size">
    <label for="newModel">Model Name <br><span class="model-size">Description</span></label>
</div>
```

### Camoufox Integration
When ready to use Camoufox for advanced searching:
1. Install Camoufox
2. Modify `search-server.py` to use Camoufox backend
3. This enables JavaScript execution, form filling, and dynamic content

---

## 📊 Model Comparison

### When to Use Each Model

**Nous-Hermes 2** (Best Writer)
- Long-form content
- Creative writing
- Detailed explanations
- Complex narratives

**Qwen 2.5** (Best Analyzer)
- Complex reasoning
- Multi-part explanations
- Comparative analysis
- Deep dives into topics

**Qwen 5** (Best for Speed)
- Quick factual answers
- Summaries
- Simple explanations
- Brainstorming ideas

---

## 🌐 Web Search Details

### How It Works
1. Detects if question is factual (contains keywords like "what", "when", "current", etc.)
2. Searches DuckDuckGo API for relevant results
3. Feeds results to the model with instruction to cite sources
4. Model incorporates and cites the information

### Supported Questions
- Historical facts: "When was the French Revolution?"
- Current information: "What is the current population of..."
- Statistics: "How many people use..."
- Definitions: "What is photosynthesis?"
- News/events: "What happened in..."

### Privacy
- Uses DuckDuckGo (no tracking)
- Searches are not stored
- Local models process everything
- No data sent to external AI services

---

## 📚 Example Prompts

### Essay Writing
"Write a 5-paragraph essay about climate change. Include an introduction with a thesis, 3 body paragraphs with evidence, and a conclusion. Make it suitable for a high school student."

### Homework Help
"Explain photosynthesis in simple terms. Break it down step-by-step and give an analogy to help me understand it better."

### Test Prep
"Give me a quiz with 10 questions about the Industrial Revolution. Include answers and explanations."

### Concept Learning
"I'm struggling with calculus derivatives. Explain what derivatives mean, give examples, and show me how to calculate them step-by-step."

### Quick Reference
"Summarize the key points of World War 2 for a history test."

---

## 🔐 Privacy & Safety

- ✅ All processing happens locally on your computer
- ✅ Models run through Ollama (open source)
- ✅ Web searches go through DuckDuckGo (privacy-focused)
- ✅ No data sent to cloud AI services
- ✅ No accounts or logins required
- ✅ Conversation history stored only in browser (cleared on refresh)

---

## 🆘 Support & Resources

### If Something Breaks
1. Check the browser console (F12) for errors
2. Verify Ollama is running
3. Try a different model
4. Restart both Ollama and the web interface

### Learning Resources
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Nous Research](https://www.nouspseudonym.com/posts/nous-hermes/)
- [Qwen Documentation](https://github.com/QwenLM/Qwen)
- [DuckDuckGo API](https://duckduckgo.com/api)

---

## 🎓 Educational Philosophy

SchoolMind is designed to:
- **Support learning**, not replace it
- **Encourage critical thinking** - always verify answers
- **Explain concepts** - understand, don't memorize blindly
- **Provide tools** - not do work for you
- **Respect academic integrity** - use as a study aid, not to plagiarize

Remember: Use this as a learning tool, not a shortcut. The best learning happens when you engage with the material yourself.

Happy studying! 📚✨
