#  coding: utf-8 
import socketserver,os
from requests import get
import json

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

BASE_URL = './www/'
OK_RESPONSE = b'HTTP/1.1 200 OK\n'
NOT_EXIST_RESPONSE =b'HTTP/1.1 404 Not Found\n'
DEBUG_RESPONSE = OK_RESPONSE


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        #self.request.sendall(bytearray("OK",'utf-8'))
        base_response = b'HTTP/1.1 200 OK\n'
        
        request_headers = self.data.decode().split("\r\n")
        print(request_headers)
        http_request = request_headers[0].split(" ")
        if http_request[0] == "GET":
            path_to_thing = os.path.join(BASE_URL,http_request[1])
            self.handle_file_request(http_request[1])
            
        
        # with open(BASE_URL,'r') as html_page:
        #     html_content = html_page.read()
        # html_content = html_content.encode('ascii')
        # response = ok_base_response + content_type_header + html_content
        
        self.request.sendall(DEBUG_RESPONSE)

    def handle_file_request(self,path_to_file):
        request_to_send = []
        if path_to_file == :
            if os.path.exists(os.path.join(BASE_URL,"index.html")):
                request_to_send.append(OK_RESPONSE)
            else:
                request_to_send.append(NOT_EXIST_RESPONSE)
        elif os.path.splitext(os.path.join(BASE_URL,file_requested))[1] == ".html":
            pass
        
        
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
