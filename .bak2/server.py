from http.server import BaseHTTPRequestHandler, HTTPServer
import pyautogui
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Remote Keyboard</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #f4f4f4;
                    }
                    .container {
                        text-align: center;
                    }
                    button {
                        padding: 10px 20px;
                        font-size: 16px;
                        margin: 10px;
                        cursor: pointer;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <button onclick="sendText('Hello World')">Type 'Hello World'</button>
                    <button onclick="sendText('Goodbye')">Type 'Goodbye'</button>
                </div>

                <script>
                    function sendText(text) {
                        fetch('/type', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ text: text })
                        })
                        .then(response => response.json())
                        .then(data => alert(data.message))
                        .catch(error => console.error('Error:', error));
                    }
                </script>
            </body>
            </html>
        ''')

    def do_POST(self):
        if self.path == '/type':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data)
                text = data.get('text', '')
                if text:
                    pyautogui.typewrite(text)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "message": "Text typed successfully!"}).encode('utf-8'))
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "No text provided!"}).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "Invalid JSON!"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
