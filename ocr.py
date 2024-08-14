import http.server
import json
import base64
import io
import pytesseract
from PIL import Image
import requests
import tempfile
import os

PORT = 8081
API_KEY = 'your_secret_api_key'

class CAPTCHAHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        api_key = data.get('apikey')
        if api_key != API_KEY:
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Forbidden: Invalid API Key\nSai Apikey roi ban oi, Ib cho Minh de lay lai apikey moi nhe :)')
            return
        
        base64_image = data.get('image')
        if base64_image:
            ocr_text = read_capcha_from_base64(base64_image)
            response = ocr_text
        else:
            response = "'error': 'Base64 image data is missing'"
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def read_capcha_from_base64(base64_image):

    ocr_text = ""
    try:
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        for _ in range(1):  # Đọc CAPTCHA 1 lần
            ocr_text = pytesseract.image_to_string(image, lang='eng', config = ' --oem 3 --psm 7 ')

    except Exception as e:
        ocr_text = (f"Error processing image: {e}")
    

    
    print(ocr_text)
    return ocr_text

def run(server_class=http.server.HTTPServer, handler_class=CAPTCHAHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Starting on port {PORT}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
