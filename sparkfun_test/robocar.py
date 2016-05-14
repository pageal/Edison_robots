import os
import time
import socket
import BaseHTTPServer

from camera.camera2D import Camera
from chassis.chassis_sparkfun import chassis

HOST_NAME = socket.gethostname() 
PORT_NUMBER = 8080  # Maybe set this to 9000.
print("hostname: " + HOST_NAME)
HOST_NAME = "192.168.1.4"

camera = Camera()
chassis = chassis()

class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        global camera
	global car
	self.html = ["Error loading main.html"]
        with open("main.html", "r") as html:
            self.html = html.readlines()
	
        #with open("favicon.ico", "rb") as favicon:
        #    self.favicon = favicon.read()
        
	self._camera = camera
        self._car = chassis
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        if '/favicon.ico' in self.path:
            #self.send_response(200)
            #self.send_header("Content-type", 'image/x-icon')
            #self.end_headers()
            #self.wfile.write(self.favicon)
            return
		
        if '/camera.jpg' in self.path:
	    try:
            	os.remove('camera.jpg')
	    except Exception as e:
		pass 

	    try:
                camera.create_image('camera.jpg')
	    except Exception as e:
		pass
            self.send_response(200)
            self.send_header("Content-type", 'image/jpg')
            self.end_headers()
	    try:
                with open("camera.jpg", "rb") as camera_file:
                    self.wfile.write(camera_file.read())
	    except Exception as e:
		pass
            return
		
        if self.path == "/up":
            self._car.go_forward(0.3)
        elif self.path == "/down":
            self._car.go_backward(0.3)
        elif self.path == "/right":
            self._car.turn_right(0.2)
	    time.sleep(0.5)
	    self._car.stop_gradually()
        elif self.path == "/left":
            self._car.turn_left(0.2)
	    time.sleep(0.5)
	    self._car.stop_gradually()
        elif self.path == "/":
            pass
        elif self.path == "/stop":
            self._car.stop_gradually()
            #self._car.stop_now()
        else:
            self.send_response(400)
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        for line in self.html:
            self.wfile.write(line)

			
httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), HTTPRequestHandler)
print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()
print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
