# coding: utf-8
import socketserver, os

# Copyright 2013-2023 Abram Hindle, Eddie Antonio Santos, Jackson Z Chang, Mandy Meindersma, Andrew Rosario
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, solely version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not,
# see <https://www.gnu.org/licenses/>.
#
# Furthermore, it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved

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
BASE_URL = "http://127.0.0.1:8080"


def parse_web_file(file_path):
    file_name = os.path.split(file_path)[1]
    print(os.path.splitext(file_path))
    try:
        if not (os.path.isfile(file_path)):
            raise Exception("Does not exist.")
        elif (os.path.splitext(file_name)[1] != ".html") and (os.path.splitext(file_name)[1] != ".css"):
            raise NotAFileException
    except NotAFileException:
        print("Not a HTML/CSS file.")
    except Exception as e:
        print(f"Exception as: {e}")

    print("Yay! This is a HTML/CSS file.")
    with open(file_path, 'r') as file:
        data_to_send = file.read()
    return data_to_send


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
        if http_request[0] == "GET":
            path_to_thing = 'www' + http_request[1]
            if os.path.isdir(path_to_thing) and path_to_thing[-1] != "/":
                response = "HTTP/1.1 301 Moved Permanently\nDirection: " + path_to_thing + "/"
            else:
                response = self.handle_file_request(path_to_thing)
            print(response)
        else:
            response = "HTTP/1.1 405 Method Not Allowed"
        # response.rstrip('\n')
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
        split_path = path_to_file.split("/")

        #directory_exists = os.path.isdir(path_to_file)
        #print(f"Directory/file existence: {directory_exists}")
        if split_path[1] == "..": # do not allow paths that go up two directories; this is forbidden.
            request_to_send.append(NOT_EXIST_RESPONSE)
            return ''.join(request_to_send)

        #if os.path.isdir(path_to_file):
            #path_to_file += "/"

        if not file_path_components[1]:  # simply going into a directory
            index_path = os.path.join(file_path_components[0], "index.html")
            index_exists = os.path.isfile(index_path)
            print(f"Path joined: {index_path}")
            print(f"Index exists: {index_exists}")
            if index_exists:
                request_to_send.append(OK_RESPONSE)
                request_to_send.append(CONTENT_TYPE_HEADER + HTML_CONTENT_TYPE + "\n")
            else:
                request_to_send.append(NOT_EXIST_RESPONSE)
            request_to_send.append(parse_web_file(index_path))
        elif os.path.isfile(path_to_file):
            request_to_send.append(OK_RESPONSE)
            if os.path.splitext(file_path_components[1])[1] == ".html":
                request_to_send.append(CONTENT_TYPE_HEADER + HTML_CONTENT_TYPE + "\n")
                request_to_send.append(parse_web_file(path_to_file))
                # request_to_send.append(self.add_css_files(path_to_file))
            elif os.path.splitext(file_path_components[1])[1] == ".css":
                request_to_send.append(CONTENT_TYPE_HEADER + CSS_CONTENT_TYPE + "\n")
                request_to_send.append(parse_web_file(path_to_file))
        else:
            request_to_send.append(NOT_EXIST_RESPONSE)
        return ''.join(request_to_send)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
