#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import threading
import json
import pyttsx3

PORT = 8083

class LumaTest(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == "/":
            html = '''<!DOCTYPE html>
<html>
<head><title>LUMA Test</title></head>
<body style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-family: Arial; padding: 50px; text-align: center;">
    <h1>🤖 LUMA TEST VOCAL</h1>
    <button onclick="testVoice()" style="padding: 20px; font-size: 18px; background: #00ff88; border: none; border-radius: 10px; cursor: pointer;">🗣️ TEST VOIX</button>
    <script>
        function testVoice() {
            fetch('/speak', {method: 'POST'})
            .then(() => alert('LUMA a parlé !'));
        }
    </script>
</body>
</html>'''
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        
    def do_POST(self):
        if self.path == "/speak":
            try:
                self.tts.say("Bonjour ! Je suis LUMA et je peux maintenant parler !")
                self.tts.runAndWait()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), LumaTest) as httpd:
        print(f"Test LUMA sur http://localhost:{PORT}")
        threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
        httpd.serve_forever()
