#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket

clients = []

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("index.html")

class WebSocketChatHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print("open", "WebSocketChatHandler")
        clients.append(self)

    def on_message(self, message):        
        print message
        for client in clients:
            print ("client ip: " + client.request.remote_ip)
            client.write_message(message)
            self.write_message({"author":"admin",
                "message":"this is return","time":client.request.remote_ip})

    def on_close(self):
        clients.remove(self)



app = tornado.web.Application([(r'/chat', WebSocketChatHandler), 
    (r'/', IndexHandler)])

app.listen(80)
tornado.ioloop.IOLoop.instance().start()
