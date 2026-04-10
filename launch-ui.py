#!/usr/bin/env python3
"""
SchoolMind UI Launcher
Launches the UI server without showing console window
"""

import sys
import os
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    """Launch the UI server and open browser"""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Path to the UI server
    ui_server_path = script_dir / "ui_server.py"
    
    # Check if UI server exists
    if not ui_server_path.exists():
        print("Error: ui_server.py not found!")
        input("Press Enter to exit...")
        return
    
    try:
        # Launch UI server in hidden window
        if sys.platform == "win32":
            # Windows: use pythonw.exe and hide window
            pythonw_path = os.path.join(sys.executable.replace("python.exe", "pythonw.exe"))
            
            # Create process with hidden window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            process = subprocess.Popen(
                [pythonw_path, str(ui_server_path)],
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=str(script_dir)
            )
        else:
            # Linux/Mac: run in background
            process = subprocess.Popen(
                [sys.executable, str(ui_server_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=str(script_dir)
            )
        
        print("🚀 Starting SchoolMind UI...")
        print("📍 Server will be available at: http://localhost:3000")
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Open browser
        webbrowser.open("http://localhost:3000")
        print("🌐 Opening browser...")
        
        # Keep the launcher running
        print("\n✅ SchoolMind is running!")
        print("📝 The UI server is running in the background.")
        print("🔄 Close this window to stop the server.")
        print("\nPress Ctrl+C to stop...")
        
        try:
            # Keep running until user interrupts
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped.")
            
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
