from http.server import SimpleHTTPRequestHandler, HTTPServer
import logging

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/feed":
            self.send_response(200)
            self.send_header("Content-type", "application/rss+xml")
            self.end_headers()
            with open("output/feed.xml", "rb") as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

def start_server(cfg):
    server_address = ('', cfg["http_server_port"])
    httpd = HTTPServer(server_address, CustomRequestHandler)
    logging.info(f"Serving RSS feed on port {cfg['http_server_port']}")
    httpd.serve_forever()

if __name__ == "__main__":
    import argparse
    import config

    parser = argparse.ArgumentParser(description="Start RSS feed server")
    parser.add_argument("config_path", help="Path to the configuration file (YAML)")
    args = parser.parse_args()

    config_loader = config.ConfigLoader(args.config_path)
    cfg = config_loader.load_config()

    start_server(cfg)