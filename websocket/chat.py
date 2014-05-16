#!/usr/bin/env python
# -*- coding: utf-8 -*-

# chat.py file
import tornado.ioloop
import tornado.web
import tornado.websocket
import lookup

clients = []
lookup_table = []
broadcast_msg = [{'author':'admin','message':'wait','time':'t'}]

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("index.html")

class WebSocketChatHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args):
        print("open", "WebSocketChatHandler")
        clients.append(self)

    def on_message(self, message):
        message = eval(message)             # converge unicode to dictionary
        sender_ip = self.request.remote_ip  # find client's ip
        message['sender_ip'] = sender_ip    # add on dictionary
        lookup.add_and_search(message, lookup_table, broadcast_msg)     # find friend
        
        self.write_message(broadcast_msg[0]) # receive result
        
        #for client in clients:
            #client.write_message(message) #Broad cast to every clients
    
    def on_close(self):
        print("clinet gone")
        clients.remove(self)



app = tornado.web.Application([(r'/chat', WebSocketChatHandler), 
    (r'/', IndexHandler)])

app.listen(80)
tornado.ioloop.IOLoop.instance().start()
