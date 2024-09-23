from http.server import BaseHTTPRequestHandler, HTTPServer
import pyautogui
import json
import os

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as file:
                self.wfile.write(file.read().encode('utf-8'))

        elif self.path == '/image':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('album.png', 'rb') as file:
                self.wfile.write(file.read())

        elif self.path.startswith('/control'):
            os.system("cp /tmp/audacious-* album.png")
            query = self.path.split('?')[1]
            params = dict(p.split('=') for p in query.split('&'))

            command = params.get('command')
            value = params.get('value')

            response = {"status": "success", "message": "Command executed!"}

            if command == 'prev':
                pyautogui.hotkey('alt', 'm')  # Example for 'Prev'
            elif command == 'playpause':
                pyautogui.hotkey('alt', 'n')  # Example for 'Play/Pause'
            elif command == 'next':
                pyautogui.hotkey('alt', 'apps')  # Example for 'Next'
            elif command == 'volumeup':
                pyautogui.hotkey('alt', '.')  # Example for Volume Up
            elif command == 'volumedown':
                pyautogui.hotkey('alt', ',')  # Example for Volume Down
            elif command == 'volume' and value:
                # Example for Volume Control (volume change as a placeholder)
                response['message'] = f"Volume set to {value}%"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
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
