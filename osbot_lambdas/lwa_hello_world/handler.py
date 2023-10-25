import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 8080

lwa_message = "Hello there, {name}"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed_path  = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            name_param = query_params.get('name')
            if name_param:
                name = name_param[0]
            else:
                name = 'World'
            message = lwa_message.format(name=name)
        except Exception as error:
            message = f"Error: {error}"

        self.send_response(200)
        self.send_header  ("Content-type", "text/html")
        self.end_headers  ()
        self.wfile.write  (message.encode())

def run():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

# This ensures the server only runs if this script is the main entry point
if __name__ == "__main__":
    run()
