#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import json
import subprocess


#Create custom HTTPRequestHandler class
class AlexaTTPRequestHandler(BaseHTTPRequestHandler):
  
  #handle GET command
  def do_POST(self):
    return self.do_GET()
  
  #handle GET command
  def do_GET(self):

    try:
        #send code 200 response
        self.send_response(200)

        #send header first
        self.send_header('Content-type','application/json')
        self.end_headers()
        
        import urlparse
        params = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('data')[0]
        params = json.loads(params)
        print params
        
        request = params['request']
        type = request['type']
        
        if type == 'IntentRequest':
            intent = request['intent']
            name = intent['name']
            if name == 'dimm':
                intensity = intent['slots']['intensity']['value']
                i_val = 0
                
                if intensity == "dunkel":
                    i_val = 45
                elif intensity == "sehr dunkel":
                    i_val = 0
                elif intensity == "mittel":
                    i_val = 90
                elif intensity == "hell":
                    i_val = 135
                elif intensity == "sehr hell":
                    i_val = 180
                
                subprocess.Popen(["python","/share/servocontrol/servocontrol.py", str(i_val)], shell=False)
                    
                self.wfile.write("{ \"version\": \"1.0\", \"response\": { \"outputSpeech\": { \"type\": \"PlainText\", \"text\": \"Ok, ich habe den Strahler auf " + intensity + " gestellt.\"} }}")
            else:
                self.wfile.write("{ \"version\": \"1.0\", \"response\": { \"outputSpeech\": { \"type\": \"PlainText\", \"text\": \"Diesen Befehl kenne ich nicht.\"} }}")


        #send file content to client
        else:
            self.wfile.write("{ \"version\": \"1.0\", \"response\": { \"outputSpeech\": { \"type\": \"PlainText\", \"text\": \"Ja mein Gebieter!\"} }}")
        
        return
      
    except Exception as e:
        print e
        self.wfile.write("{ \"version\": \"1.0\", \"response\": { \"outputSpeech\": { \"type\": \"PlainText\", \"text\": \"Den Befehl konnte ich nicht verstehen.\"} }}")
  
def run():
  print('http server is starting...')

  #ip and port of servr
  #by default http server port is 80
  server_address = ('0.0.0.0', 8000)
  httpd = HTTPServer(server_address, AlexaTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()