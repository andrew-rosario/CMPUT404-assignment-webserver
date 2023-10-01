#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Righ        self.data
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

ROOT_FOLDER = 'www'
OK_RESPONSE = 'HTTP/1.1 200 OK\n'
NOT_EXIST_RESPONSE = 'HTTP/1.1 404 Not Found\n'
CONTENT_TYPE_HEADER = 'Content-Type: '
HTML_CONTENT_TYPE = 'text/html; charset=utf-8\n'
CSS_CONTENT_TYPE = 'text/css\n'
DEBUG_RESPONSE = OK_RESPONSE


class NotAFileException(Exception):
    pass


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        # self.request.sendall(bytearray("OK",'utf-8'))

        request_headers = self.data.decode().split("\r\n")
        print(request_headers)
        http_request = request_headers[0].split(" ")
        response = DEBUG_RESPONSE
        if http_request[0] == "GET":
            path_to_thing = 'www' + http_request[1]
            response = self.handle_file_request(path_to_thing)
            print(response)
        else:
            response = "HTTP/1.1 405 Method Not Allowed"
        #response.rstrip('\n')
        # with open(BASE_URL,'r') as html_page:
        #     html_content = html_page.read()
        # html_content = html_content.encode('ascii')
        # response = ok_base_response + content_type_header + html_content

        self.request.sendall(response.encode("utf-8"))

    def handle_file_request(self, path_to_file):
        request_to_send = []
        print(f"Path: {path_to_file}")
        file_path_components = os.path.split(path_to_file)
        print(f"File component index 1: {file_path_components[1]}")
        if not file_path_components[1]:  # simply going into a directory
            print(f"Directory. Does index exist")
            index_path = os.path.join(file_path_components[0], "index.html")
            index_exists = os.path.isfile(index_path)
            print(f"Path joined: {index_path}")
            print(f"Index exists: {index_exists}")
            if index_exists:
                request_to_send.append(OK_RESPONSE)
                request_to_send.append(CONTENT_TYPE_HEADER + HTML_CONTENT_TYPE + "\n")
            else:
                request_to_send.append(NOT_EXIST_RESPONSE)
            request_to_send.append(self.parse_web_file(index_path))
        elif os.path.exists(path_to_file):
            request_to_send.append(OK_RESPONSE)
            if os.path.splitext(file_path_components[1])[1] == ".html":
                request_to_send.append(CONTENT_TYPE_HEADER + HTML_CONTENT_TYPE + "\n")
                request_to_send.append(self.parse_web_file(path_to_file))
                #request_to_send.append(self.add_css_files(path_to_file))
            elif os.path.splitext(file_path_components[1])[1] == ".css":
                request_to_send.append(CONTENT_TYPE_HEADER + CSS_CONTENT_TYPE + "\n")
                request_to_send.append(self.parse_web_file(path_to_file))
        else:
            request_to_send.append(NOT_EXIST_RESPONSE)
        return ''.join(request_to_send)

    def parse_web_file(self, file_path):
        try:
            if not os.path.isfile(file_path) or os.path.splitext(file_path)[1] != ".html" or os.path.splitext(file_path)[1] != ".css":
                raise NotAFileException
        except NotAFileException:
            print("Not a HTML/CSS file.")

        with open(file_path, 'r') as file:
            file_to_send = file.read()
        return file_to_send

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
