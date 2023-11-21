from http.server import BaseHTTPRequestHandler, HTTPServer
import re

# Constants
HOST = "localhost"
PORT = 8000

# Define the regular expressions to match the request path and HTTP headers
PATH_REGEX = re.compile(r"/tomcatwar\.jsp")
HEADERS_REGEX_LIST = [
    re.compile(r"suffix=%>//"),
    re.compile(r"c1=Runtime"),
    re.compile(r"c2=<%"),
    re.compile(r"DNT=1"),
    re.compile(r"Content-Type: application\/x-w>"),
]

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        self.handle_request()

    def do_POST(self):
        """Handle POST requests."""
        self.handle_request()

    def handle_request(self):
        """Handle the request based on path and headers."""
        if PATH_REGEX.search(self.path) or any(regex.search(str(self.headers)) for regex in HEADERS_REGEX_LIST):
            self.block_request()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = self.get_html_response(200, "OK", "Request successful")
            self.wfile.write(response.encode())

    def block_request(self):
        """Block the request and send a 403 Forbidden response."""
        print("Request blocked due to firewall")
        self.send_response(403)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = self.get_html_response(403, "Forbidden", "You don't have permission to access this resource.")
        self.wfile.write(response.encode())

    def get_html_response(self, status_code, title, message):
        """Generate HTML response."""
        return f"<html><head><title>{status_code} {title}</title></head>" \
               f"<body><h1>{status_code} {title}</h1><p>{message}</p></body></html>"

def run_server():
    """Run the HTTP server."""
    server_address = (HOST, PORT)
    server = HTTPServer(server_address, ServerHandler)
    print("[+] Firewall Server")
    print(f"[+] HTTP Web Server running on: {HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("[+] Server terminated. Exiting...")

if __name__ == "__main__":
    run_server()
