#!/usr/bin/env python3
"""
SchoolMind Desktop Application
A standalone GUI application for the AI assistant
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import threading
import queue
import webbrowser
from typing import List, Dict, Optional
import sys
import os

class SchoolMindDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SchoolMind - AI Study Companion")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0f172a')
        
        # Variables
        self.conversation_history: List[Dict] = []
        self.current_model = tk.StringVar(value="nous-hermes2:10.7b")
        self.smart_mode = tk.BooleanVar(value=True)
        self.web_search = tk.BooleanVar(value=True)
        self.response_queue = queue.Queue()
        
        # Available models
        self.models = {
            "nous-hermes2:10.7b": "Hermes 2",
            "qwen2.5:14b": "Qwen 2.5 (14B)", 
            "qwen2.5:7b": "Qwen 2.5 (7B)"
        }
        
        self.setup_ui()
        self.setup_styles()
        self.add_welcome_message()
        
        # Start response processor
        self.root.after(100, self.process_responses)
    
    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background='#0f172a', 
                       foreground='#34d399', 
                       font=('Georgia', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background='#0f172a',
                       foreground='#cbd5e1',
                       font=('Georgia', 12, 'italic'))
        
        style.configure('Card.TFrame',
                       background='#1e293b',
                       relief='raised',
                       borderwidth=1)
        
        style.configure('Dark.TButton',
                       background='#10b981',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       relief='flat')
        
        style.map('Dark.TButton',
                 background=[('active', '#34d399')])
        
        style.configure('Chat.TFrame',
                       background='#1e293b',
                       relief='sunken',
                       borderwidth=1)
    
    def setup_ui(self):
        """Setup the main UI components"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#0f172a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="📚 SchoolMind", style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        subtitle = ttk.Label(main_frame, text="Your AI study companion for writing, questions & learning", style='Subtitle.TLabel')
        subtitle.pack(pady=(0, 20))
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg='#0f172a')
        content_frame.pack(fill='both', expand=True)
        
        # Left side - Chat area
        self.setup_chat_area(content_frame)
        
        # Right side - Controls
        self.setup_controls(content_frame)
        
        # Bottom - Input area
        self.setup_input_area(main_frame)
    
    def setup_chat_area(self, parent):
        """Setup the chat display area"""
        chat_frame = tk.Frame(parent, bg='#1e293b', relief='sunken', bd=1)
        chat_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Chat header
        header_frame = tk.Frame(chat_frame, bg='#0a0f1d', height=40)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="💬 Assistant", 
                               bg='#0a0f1d', fg='#34d399',
                               font=('Arial', 12, 'bold'))
        header_label.pack(side='left', padx=10, pady=10)
        
        self.model_display = tk.Label(header_frame, text="🤖 Hermes 2",
                                     bg='#0a0f1d', fg='#cbd5e1',
                                     font=('Arial', 10))
        self.model_display.pack(side='right', padx=10, pady=10)
        
        # Chat messages area
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            bg='#1e293b',
            fg='#f1f5f9',
            font=('Georgia', 11),
            wrap='word',
            state='disabled',
            relief='flat',
            bd=0,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Configure text tags for different message types
        self.chat_display.tag_config('user', foreground='#10b981', justify='right')
        self.chat_display.tag_config('assistant', foreground='#f1f5f9')
        self.chat_display.tag_config('model', foreground='#cbd5e1', font=('Courier', 9))
        
        # Markdown formatting tags
        self.chat_display.tag_config('bold', font=('Georgia', 11, 'bold'), foreground='#34d399')
        self.chat_display.tag_config('italic', font=('Georgia', 11, 'italic'), foreground='#60a5fa')
        self.chat_display.tag_config('code', font=('Courier', 10), foreground='#fbbf24', background='#1a1a1a')
    
    def setup_controls(self, parent):
        """Setup the control panel"""
        controls_frame = tk.Frame(parent, bg='#0f172a', width=250)
        controls_frame.pack(side='right', fill='y')
        controls_frame.pack_propagate(False)
        
        # Model Selection Card
        self.create_model_card(controls_frame)
        
        # Smart Mode Card
        self.create_smart_mode_card(controls_frame)
        
        # Web Search Card
        self.create_web_search_card(controls_frame)
        
        # Tips Card
        self.create_tips_card(controls_frame)
    
    def create_model_card(self, parent):
        """Create model selection card"""
        card = tk.Frame(parent, bg='#1e293b', relief='raised', bd=1)
        card.pack(fill='x', pady=(0, 10))
        
        title = tk.Label(card, text="⚙️ Select Model", 
                        bg='#1e293b', fg='#34d399',
                        font=('Arial', 12, 'bold'))
        title.pack(pady=(10, 5))
        
        # Model options
        for model_value, model_name in self.models.items():
            rb = tk.Radiobutton(card, text=model_name,
                               variable=self.current_model, value=model_value,
                               bg='#1e293b', fg='#f1f5f9',
                               selectcolor='#1e293b',
                               activebackground='#1e293b',
                               font=('Arial', 10))
            rb.pack(anchor='w', padx=15, pady=2)
        
        # Model descriptions
        descriptions = {
            "nous-hermes2:10.7b": "Best for essays & detailed answers",
            "qwen2.5:14b": "Fast & versatile all-rounder",
            "qwen2.5:7b": "Quick answers & summaries"
        }
        
        for model_value, desc in descriptions.items():
            desc_label = tk.Label(card, text=f"  {desc}",
                                bg='#1e293b', fg='#cbd5e1',
                                font=('Arial', 8))
            desc_label.pack(anchor='w', padx=15, pady=(0, 5))
    
    def create_smart_mode_card(self, parent):
        """Create smart mode card"""
        card = tk.Frame(parent, bg='#1e293b', relief='raised', bd=1)
        card.pack(fill='x', pady=(0, 10))
        
        title = tk.Label(card, text="🎯 Smart Mode", 
                        bg='#1e293b', fg='#34d399',
                        font=('Arial', 12, 'bold'))
        title.pack(pady=(10, 5))
        
        cb = tk.Checkbutton(card, text="Auto-select best model",
                           variable=self.smart_mode,
                           bg='#1e293b', fg='#f1f5f9',
                           selectcolor='#1e293b',
                           activebackground='#1e293b',
                           font=('Arial', 10))
        cb.pack(anchor='w', padx=15, pady=5)
        
        info_text = """When enabled, AI picks the best model:
• Essays & Writing → Hermes 2
• Complex Questions → Qwen 2.5 (14B)
• Quick Answers → Qwen 2.5 (7B)"""
        
        info_label = tk.Label(card, text=info_text,
                            bg='#1e293b', fg='#cbd5e1',
                            font=('Arial', 8),
                            justify='left')
        info_label.pack(anchor='w', padx=15, pady=(5, 10))
    
    def create_web_search_card(self, parent):
        """Create web search card"""
        card = tk.Frame(parent, bg='#1e293b', relief='raised', bd=1)
        card.pack(fill='x', pady=(0, 10))
        
        title = tk.Label(card, text="🔍 Web Verification", 
                        bg='#1e293b', fg='#34d399',
                        font=('Arial', 12, 'bold'))
        title.pack(pady=(10, 5))
        
        cb = tk.Checkbutton(card, text="Search web for facts",
                           variable=self.web_search,
                           bg='#1e293b', fg='#f1f5f9',
                           selectcolor='#1e293b',
                           activebackground='#1e293b',
                           font=('Arial', 10))
        cb.pack(anchor='w', padx=15, pady=5)
        
        info_text = """Auto-searches web to verify facts:
• Auto-enabled for factual Q&As
• Helps verify historical dates
• Finds current statistics"""
        
        info_label = tk.Label(card, text=info_text,
                            bg='#1e293b', fg='#cbd5e1',
                            font=('Arial', 8),
                            justify='left')
        info_label.pack(anchor='w', padx=15, pady=(5, 10))
    
    def create_tips_card(self, parent):
        """Create tips card"""
        card = tk.Frame(parent, bg='#1e293b', relief='raised', bd=1)
        card.pack(fill='x', pady=(0, 10))
        
        title = tk.Label(card, text="💡 Study Tips", 
                        bg='#1e293b', fg='#34d399',
                        font=('Arial', 12, 'bold'))
        title.pack(pady=(10, 5))
        
        tips = [
            "Be specific in your questions",
            "Ask for examples & explanations",
            "Request summaries for complex topics",
            "Use it to brainstorm essay ideas",
            "Verify important facts yourself"
        ]
        
        for tip in tips:
            tip_label = tk.Label(card, text=f"• {tip}",
                               bg='#1e293b', fg='#cbd5e1',
                               font=('Arial', 9),
                               justify='left')
            tip_label.pack(anchor='w', padx=15, pady=2)
        
        tk.Label(card, text="", bg='#1e293b').pack(pady=5)
    
    def setup_input_area(self, parent):
        """Setup the input area"""
        input_frame = tk.Frame(parent, bg='#1e293b', relief='raised', bd=1)
        input_frame.pack(fill='x', pady=(10, 0))
        
        # Input field
        self.input_var = tk.StringVar()
        self.input_field = tk.Entry(input_frame, 
                                   textvariable=self.input_var,
                                   bg='#0f172a', fg='#f1f5f9',
                                   font=('Georgia', 11),
                                   relief='flat',
                                   bd=10)
        self.input_field.pack(side='left', fill='x', expand=True, padx=10, pady=10)
        
        # Send button
        self.send_button = tk.Button(input_frame, text="Send",
                                    command=self.send_message,
                                    bg='#10b981', fg='white',
                                    font=('Arial', 10, 'bold'),
                                    relief='flat',
                                    padx=20, pady=10)
        self.send_button.pack(side='right', padx=10, pady=10)
        
        # Bind Enter key
        self.input_field.bind('<Return>', lambda e: self.send_message())
    
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome = """👋 Welcome to SchoolMind! I'm here to help you with:

✍️ Writing essays and creative content
❓ Answering homework questions  
📚 Explaining complex topics
💡 Providing study tips

Select a model, ask your question, and let's get learning!"""
        
        self.add_message_to_chat(welcome, 'assistant')
    
    def add_message_to_chat(self, message: str, role: str, model: str = None):
        """Add a message to the chat display"""
        self.chat_display.config(state='normal')
        
        # Apply markdown formatting
        formatted_parts = self.format_markdown(message)
        
        # Add message with formatting
        if role == 'user':
            self.chat_display.insert('end', "You: ", 'user')
            self.insert_formatted_text(formatted_parts)
            self.chat_display.insert('end', "\n\n")
        else:
            self.chat_display.insert('end', "Assistant: ", 'assistant')
            self.insert_formatted_text(formatted_parts)
            self.chat_display.insert('end', "\n")
            if model:
                self.chat_display.insert('end', f"Model: {self.models.get(model, model)}\n\n", 'model')
            else:
                self.chat_display.insert('end', "\n")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see('end')
    
    def insert_formatted_text(self, formatted_parts):
        """Insert formatted text parts into chat display"""
        for tag, text in formatted_parts:
            if tag == 'text':
                self.chat_display.insert('end', text)
            else:
                self.chat_display.insert('end', text, tag)
    
    def format_markdown(self, text: str) -> str:
        """Apply simple markdown formatting to text"""
        import re
        
        # Return formatted text with tkinter tags
        formatted_parts = []
        i = 0
        n = len(text)
        
        while i < n:
            # Check for bold **text**
            if text[i:i+2] == '**':
                end = text.find('**', i+2)
                if end != -1:
                    bold_text = text[i+2:end]
                    formatted_parts.append(('bold', bold_text))
                    i = end + 2
                    continue
            
            # Check for italic *text*
            elif text[i] == '*' and (i == 0 or text[i-1] != '*'):
                end = text.find('*', i+1)
                if end != -1:
                    italic_text = text[i+1:end]
                    formatted_parts.append(('italic', italic_text))
                    i = end + 1
                    continue
            
            # Check for code `text`
            elif text[i] == '`':
                end = text.find('`', i+1)
                if end != -1:
                    code_text = text[i+1:end]
                    formatted_parts.append(('code', code_text))
                    i = end + 1
                    continue
            
            # Regular text
            else:
                if not formatted_parts or formatted_parts[-1][0] == 'text':
                    if formatted_parts:
                        formatted_parts[-1] = ('text', formatted_parts[-1][1] + text[i])
                    else:
                        formatted_parts.append(('text', text[i]))
                else:
                    formatted_parts.append(('text', text[i]))
                i += 1
        
        return formatted_parts
    
    def send_message(self):
        """Send a message to the AI"""
        message = self.input_var.get().strip()
        if not message:
            return
        
        # Clear input
        self.input_var.set("")
        
        # Add user message to chat
        self.add_message_to_chat(message, 'user')
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Disable input while processing
        self.input_field.config(state='disabled')
        self.send_button.config(state='disabled')
        
        # Start processing in background thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message: str):
        """Process message in background thread"""
        try:
            # Select model
            model_to_use = self.current_model.get()
            if self.smart_mode.get():
                model_to_use = self.select_best_model(message)
            
            # Update model display
            self.response_queue.put(('update_model', model_to_use))
            
            # Generate response
            response = self.generate_response(message, model_to_use)
            
            # Add response to queue
            self.response_queue.put(('response', response, model_to_use))
            
        except Exception as e:
            self.response_queue.put(('error', str(e)))
    
    def process_responses(self):
        """Process responses from background thread"""
        try:
            while True:
                item = self.response_queue.get_nowait()
                
                if item[0] == 'response':
                    _, response, model = item
                    self.add_message_to_chat(response, 'assistant', model)
                    self.conversation_history.append({"role": "assistant", "content": response})
                    
                elif item[0] == 'error':
                    self.add_message_to_chat(f"Error: {item[1]}", 'assistant')
                    
                elif item[0] == 'update_model':
                    model_name = self.models.get(item[1], item[1])
                    self.model_display.config(text=f"🤖 {model_name}")
                
                # Re-enable input
                self.input_field.config(state='normal')
                self.send_button.config(state='normal')
                self.input_field.focus()
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_responses)
    
    def select_best_model(self, message: str) -> str:
        """Select the best model based on message content"""
        lower_msg = message.lower()
        
        # Essay/Writing detection
        if ('essay' in lower_msg or 'write' in lower_msg or 
            'poem' in lower_msg or 'story' in lower_msg or 
            'creative writing' in lower_msg or len(message) > 100):
            return 'nous-hermes2:10.7b'
        
        # Complex question detection
        if ('explain' in lower_msg or 'analyze' in lower_msg or 
            'discuss' in lower_msg or 'compare' in lower_msg or 
            'contrast' in lower_msg or 'how' in lower_msg or 
            'why' in lower_msg or len(message.split()) > 15):
            return 'qwen2.5:14b'
        
        # Default: quick answers
        return 'qwen2.5:7b'
    
    def generate_response(self, user_message: str, model: str) -> str:
        """Generate AI response"""
        # Build system prompt
        system_prompt = """You are SchoolMind, an AI tutor specializing in helping students with:
- Writing essays, stories, and creative content
- Answering homework questions
- Explaining complex topics clearly
- Providing study tips and learning strategies
- Discussing academic subjects in depth

Be helpful, clear, and educational. Encourage learning rather than just giving answers.
When you provide factual information, cite sources when available."""
        
        # Check if web search is needed
        web_context = ""
        if self.web_search.get() and self.is_factual_question(user_message):
            try:
                web_context = self.search_web(user_message)
            except:
                pass
        
        # Build enhanced prompt
        enhanced_prompt = system_prompt
        if web_context:
            enhanced_prompt += f"\n\nRecent web search results:\n{web_context}\n\nIncorporate this information and cite sources where relevant."
        
        # Format messages for API
        messages = [
            {"role": "system", "content": enhanced_prompt},
            *self.conversation_history[-10:]  # Keep last 10 messages
        ]
        
        # Make API request
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.9
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")
        
        data = response.json()
        return data["message"]["content"]
    
    def is_factual_question(self, text: str) -> bool:
        """Check if question requires factual verification"""
        factual_keywords = [
            'what is', 'who is', 'when', 'where', 'how many', 'what are',
            'define', 'explain', 'history of', 'current', 'latest', 'recent',
            'facts about', 'information about', 'statistics', 'data about'
        ]
        return any(keyword in text.lower() for keyword in factual_keywords)
    
    def search_web(self, query: str) -> str:
        """Search web for information"""
        try:
            response = requests.post(
                "http://localhost:8000/search",
                json={"query": query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    return f"Web Search Results for \"{query}\":\n{data['results']}"
        except:
            pass
        
        return ""
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = SchoolMindDesktop()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start SchoolMind: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
