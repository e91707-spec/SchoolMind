#!/usr/bin/env python3
"""
SchoolMind UI Server
Serves the web interface for the AI assistant
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="SchoolMind UI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SchoolMind - Your Study Companion</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #0f172a;
            --secondary: #1e293b;
            --accent: #10b981;
            --accent-light: #34d399;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --border: #334155;
            --success: #10b981;
            --warning: #f59e0b;
            --info: #3b82f6;
        }

        body {
            font-family: 'Georgia', 'Garamond', serif;
            background: linear-gradient(135deg, var(--primary) 0%, #0a0f1d 100%);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            min-height: 100vh;
        }

        /* Header */
        header {
            text-align: center;
            padding: 40px 20px;
            border-bottom: 2px solid var(--border);
            margin-bottom: 20px;
            animation: slideDown 0.6s ease-out;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, var(--accent-light), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }

        .tagline {
            color: var(--text-secondary);
            font-size: 1.1em;
            font-style: italic;
            margin-bottom: 20px;
        }

        /* Main Grid */
        .main-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }

        @media (max-width: 900px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Chat Section */
        .chat-container {
            background: linear-gradient(135deg, var(--secondary) 20%, #2d3748 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 600px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .chat-header {
            padding: 15px 20px;
            background: rgba(0, 0, 0, 0.2);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chat-header h2 {
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-indicator {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            display: flex;
            gap: 10px;
            animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.user {
            justify-content: flex-end;
        }

        .message-bubble {
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 12px;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .message.user .message-bubble {
            background: linear-gradient(135deg, var(--accent), var(--accent-light));
            color: var(--primary);
            border-bottom-right-radius: 4px;
        }

        .message.assistant .message-bubble {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--border);
            border-bottom-left-radius: 4px;
            color: var(--text-primary);
        }

        .model-badge {
            font-size: 0.75em;
            opacity: 0.7;
            margin-top: 4px;
            font-family: 'Monaco', monospace;
            text-transform: uppercase;
        }

        /* Markdown styling */
        .message-bubble strong {
            font-weight: bold;
            color: #34d399;
        }

        .message-bubble em {
            font-style: italic;
            color: #60a5fa;
        }

        .message-bubble code {
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', monospace;
            font-size: 0.9em;
            color: #fbbf24;
        }

        /* Input Section */
        .input-section {
            padding: 15px 20px;
            background: rgba(0, 0, 0, 0.2);
            border-top: 1px solid var(--border);
            display: flex;
            gap: 10px;
        }

        .input-wrapper {
            flex: 1;
            display: flex;
            gap: 10px;
        }

        input[type="text"] {
            flex: 1;
            padding: 12px 16px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.95em;
            transition: all 0.2s;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
        }

        button {
            padding: 12px 24px;
            background: linear-gradient(135deg, var(--accent), var(--accent-light));
            border: none;
            border-radius: 8px;
            color: var(--primary);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(16, 185, 129, 0.2);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Sidebar */
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .card {
            background: linear-gradient(135deg, var(--secondary) 20%, #2d3748 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .card h3 {
            font-size: 1.05em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--accent-light);
        }

        .card-content {
            font-size: 0.95em;
            line-height: 1.6;
            color: var(--text-secondary);
        }

        .model-select {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 10px;
        }

        .model-option {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: rgba(15, 23, 42, 0.5);
            border: 2px solid transparent;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .model-option:hover {
            border-color: var(--accent);
            background: rgba(16, 185, 129, 0.1);
        }

        .model-option input[type="radio"] {
            cursor: pointer;
        }

        .model-option label {
            cursor: pointer;
            flex: 1;
            font-weight: 500;
        }

        .model-size {
            font-size: 0.8em;
            opacity: 0.6;
        }

        .tips-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .tips-list li {
            padding-left: 20px;
            position: relative;
            font-size: 0.9em;
        }

        .tips-list li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: var(--accent);
        }

        .loading {
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        .spinner {
            width: 16px;
            height: 16px;
            border: 2px solid var(--border);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 SchoolMind</h1>
            <p class="tagline">Your AI study companion for writing, questions & learning</p>
        </header>

        <div class="main-grid">
            <!-- Chat -->
            <div class="chat-container">
                <div class="chat-header">
                    <h2><span class="status-indicator"></span> Assistant</h2>
                    <span id="modelDisplay" style="font-size: 0.85em; opacity: 0.7;"></span>
                </div>
                <div class="messages" id="messages"></div>
                <div class="input-section">
                    <div class="input-wrapper">
                        <input 
                            type="text" 
                            id="userInput" 
                            placeholder="Ask a question, request an essay, need homework help..."
                            autocomplete="off"
                        />
                        <button id="sendBtn" onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </div>

            <!-- Sidebar -->
            <div class="sidebar">
                <!-- Model Selection -->
                <div class="card">
                    <h3>⚙️ Select Model</h3>
                    <div class="model-select">
                        <div class="model-option">
                            <input type="radio" id="hermes" name="model" value="nous-hermes2:10.7b" checked>
                            <label for="hermes">
                                Hermes 2 <br>
                                <span class="model-size">Best for essays & detailed answers</span>
                            </label>
                        </div>
                        <div class="model-option">
                            <input type="radio" id="qwen25" name="model" value="qwen2.5:14b">
                            <label for="qwen25">
                                Qwen 2.5 <br>
                                <span class="model-size">Fast & versatile all-rounder</span>
                            </label>
                        </div>
                        <div class="model-option">
                            <input type="radio" id="qwen7" name="model" value="qwen2.5:7b">
                            <label for="qwen7">
                                Qwen 2.5 (7B) <br>
                                <span class="model-size">Quick answers & summaries</span>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Smart Mode -->
                <div class="card">
                    <h3>🎯 Smart Mode</h3>
                    <div style="margin-top: 10px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                            <input type="checkbox" id="smartMode" checked>
                            <label for="smartMode" style="cursor: pointer;">Auto-select best model</label>
                        </div>
                        <p style="font-size: 0.85em; color: var(--text-secondary); line-height: 1.5;">
                            When enabled, the AI automatically picks the best model for your question:
                        </p>
                        <ul class="tips-list" style="margin-top: 10px;">
                            <li>Essays & Writing → Hermes 2</li>
                            <li>Complex Questions → Qwen 2.5 (14B)</li>
                            <li>Quick Answers → Qwen 2.5 (7B)</li>
                        </ul>
                    </div>
                </div>

                <!-- Web Search -->
                <div class="card">
                    <h3>🔍 Web Verification</h3>
                    <div style="margin-top: 10px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                            <input type="checkbox" id="webSearch" checked>
                            <label for="webSearch" style="cursor: pointer;">Search web for facts</label>
                        </div>
                        <p style="font-size: 0.85em; color: var(--text-secondary); line-height: 1.5;">
                            Automatically searches the web to verify factual questions and provide current information.
                        </p>
                        <ul class="tips-list" style="margin-top: 10px;">
                            <li>Auto-enabled for factual Q&As</li>
                            <li>Helps verify historical dates</li>
                            <li>Finds current statistics</li>
                        </ul>
                    </div>
                </div>

                <!-- Tips -->
                <div class="card">
                    <h3>💡 Study Tips</h3>
                    <div class="card-content">
                        <ul class="tips-list">
                            <li>Be specific in your questions</li>
                            <li>Ask for examples & explanations</li>
                            <li>Request summaries for complex topics</li>
                            <li>Use it to brainstorm essay ideas</li>
                            <li>Verify important facts yourself</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const messagesDiv = document.getElementById('messages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const modelDisplay = document.getElementById('modelDisplay');
        const smartModeCheckbox = document.getElementById('smartMode');
        const modelRadios = document.querySelectorAll('input[name="model"]');

        // Ollama API configuration
        const OLLAMA_BASE_URL = 'http://localhost:11434/api';

        let conversationHistory = [];
        let currentModel = 'nous-hermes2:10.7b';

        // Initialize
        updateModelDisplay();

        modelRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                currentModel = radio.value;
                updateModelDisplay();
            });
        });

        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            userInput.value = '';
            
            // Add user message to UI
            addMessageToUI(message, 'user');
            
            // Determine which model to use
            let modelToUse = currentModel;
            if (smartModeCheckbox.checked) {
                modelToUse = selectBestModel(message);
                updateModelDisplay(modelToUse);
            }

            // Add to history
            conversationHistory.push({ role: 'user', content: message });

            // Show loading state
            const loadingId = showLoading();
            
            try {
                const response = await generateResponse(message, modelToUse);
                removeLoading(loadingId);
                addMessageToUI(response, 'assistant', modelToUse);
                conversationHistory.push({ role: 'assistant', content: response });
            } catch (error) {
                removeLoading(loadingId);
                addMessageToUI(`Error: ${error.message}`, 'assistant');
            }
        }

        async function generateResponse(userMessage, model) {
            // Build context from conversation history
            const systemPrompt = `You are SchoolMind, an AI tutor specializing in helping students with:
- Writing essays, stories, and creative content
- Answering homework questions
- Explaining complex topics clearly
- Providing study tips and learning strategies
- Discussing academic subjects in depth

Be helpful, clear, and educational. Encourage learning rather than just giving answers.
When you provide factual information, cite sources when available.`;

            // Check if we should search the web for this question
            const shouldSearch = isFactualQuestion(userMessage);
            
            let webContext = '';
            if (shouldSearch && document.getElementById('webSearch').checked) {
                try {
                    webContext = await searchWeb(userMessage);
                } catch (error) {
                    console.warn('Web search failed:', error);
                }
            }

            // Build enhanced system prompt with web results
            let enhancedSystemPrompt = systemPrompt;
            if (webContext) {
                enhancedSystemPrompt += `\\n\\nRecent web search results:\\n${webContext}\\n\\nIncorporate this information and cite sources where relevant.`;
            }

            // Format messages for the API
            const messages = [
                { role: 'system', content: enhancedSystemPrompt },
                ...conversationHistory.slice(-10) // Keep last 10 messages for context
            ];

            const response = await fetch(`${OLLAMA_BASE_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: model,
                    messages: messages,
                    stream: false,
                    temperature: 0.7,
                    top_p: 0.9,
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Ollama error: ${errorData.error || 'Unknown error'}`);
            }

            const data = await response.json();
            return data.message.content;
        }

        function isFactualQuestion(text) {
            const factualKeywords = [
                'what is', 'who is', 'when', 'where', 'how many', 'what are',
                'define', 'explain', 'history of', 'current', 'latest', 'recent',
                'facts about', 'information about', 'statistics', 'data about'
            ];
            return factualKeywords.some(keyword => text.toLowerCase().includes(keyword));
        }

        async function searchWeb(query) {
            try {
                // Use the search server at port 8000
                const response = await fetch('http://localhost:8000/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });

                if (!response.ok) {
                    throw new Error('Search server unavailable');
                }

                const data = await response.json();
                
                if (data.results) {
                    return `Web Search Results for "${query}":\\n${data.results}`;
                }
                return '';
            } catch (error) {
                console.warn('Web search unavailable:', error);
                return '';
            }
        }

        function selectBestModel(message) {
            const lowerMsg = message.toLowerCase();
            
            // Essay/Writing detection
            if (lowerMsg.includes('essay') || lowerMsg.includes('write') || lowerMsg.includes('poem') || 
                lowerMsg.includes('story') || lowerMsg.includes('creative writing') || message.length > 100) {
                return 'nous-hermes2:10.7b'; // Best for detailed writing
            }
            
            // Complex question detection
            if (lowerMsg.includes('explain') || lowerMsg.includes('analyze') || lowerMsg.includes('discuss') ||
                lowerMsg.includes('compare') || lowerMsg.includes('contrast') || lowerMsg.includes('how') ||
                lowerMsg.includes('why') || message.split(' ').length > 15) {
                return 'qwen2.5:14b'; // Best for complex reasoning
            }
            
            // Default: quick answers
            return 'qwen2.5:7b'; // Best for speed
        }

        function addMessageToUI(text, role, model = null) {
            const messageEl = document.createElement('div');
            messageEl.className = `message ${role}`;
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            
            // Simple markdown rendering
            let formattedText = text
                .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')  // **bold**
                .replace(/\\*(.*?)\\*/g, '<em>$1</em>')              // *italic*
                .replace(/`([^`]+)`/g, '<code>$1</code>')             // `code`
                .replace(/#{1,6}\\s(.+)/g, '<strong>$1</strong>')    // # headers
                .replace(/\\n/g, '<br>');                           // line breaks
            
            bubble.innerHTML = `
                ${formattedText}
                ${model ? `<div class="model-badge">${model}</div>` : ''}
            `;
            
            messageEl.appendChild(bubble);
            messagesDiv.appendChild(messageEl);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function showLoading() {
            const id = Math.random().toString(36).substr(2, 9);
            const messageEl = document.createElement('div');
            messageEl.className = 'message assistant';
            messageEl.id = `loading-${id}`;
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <span>Thinking...</span>
                </div>
            `;
            
            messageEl.appendChild(bubble);
            messagesDiv.appendChild(messageEl);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            return id;
        }

        function removeLoading(id) {
            const element = document.getElementById(`loading-${id}`);
            if (element) element.remove();
        }

        function updateModelDisplay(model = null) {
            const displayModel = model || currentModel;
            const modelNames = {
                'nous-hermes2:10.7b': 'Hermes 2',
                'qwen2.5:14b': 'Qwen 2.5 (14B)',
                'qwen2.5:7b': 'Qwen 2.5 (7B)'
            };
            modelDisplay.textContent = `🤖 ${modelNames[displayModel] || displayModel}`;
        }

        // Welcome message
        window.addEventListener('load', () => {
            addMessageToUI(
                "👋 Welcome to SchoolMind! I'm here to help you with:\\n\\n" +
                "✍️ Writing essays and creative content\\n" +
                "❓ Answering homework questions\\n" +
                "📚 Explaining complex topics\\n" +
                "💡 Providing study tips\\n\\n" +
                "Select a model, ask your question, and let's get learning!",
                'assistant'
            );
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Serve the main UI"""
    # Add cache-busting headers
    from fastapi import Response
    response = Response(content=HTML_TEMPLATE, media_type="text/html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "SchoolMind UI"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")
