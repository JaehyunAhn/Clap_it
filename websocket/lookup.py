#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lookup.py file
# this file used to find suitable user for """ message encoded with Json, variable
""" message encoded with Json, variable
1) send_t
2) gps (x,y)
3) cid
4) nid
5) msg

6) on_t
7) acc_t
8) gyxy_t
9) gyz_t

10) sender_ip : server got ip address from the sender
"""

def add_and_search(message, lookup_table, broadcast_msg):
    print message
    broadcast_msg[0] = {'author':'admin','message':'asdf','time':'t'}

    lookup_table.append(message)
    #else send re-request
    for client in lookup_table:
        print ("client!")
