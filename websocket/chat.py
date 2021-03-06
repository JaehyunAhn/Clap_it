#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat.py file

import tornado.ioloop
import tornado.web
import tornado.websocket
import lookup

clients = []
lookup_table = []

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
        print "acc time is " + str(message['acc_t'])

        this_user = self
        lookup.add_and_search(this_user, message, lookup_table)     # find friend
        
        #for client in clients:
            #client.write_message(message) #Broad cast to every clients
    
    def on_close(self):
        print("clinet gone")
        clients.remove(self)



app = tornado.web.Application([(r'/chat', WebSocketChatHandler), 
    (r'/', IndexHandler)])

app.listen(80)
tornado.ioloop.IOLoop.instance().start()
