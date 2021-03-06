#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lookup.py file

import math

""" message encoded with Json, variable which are,
<JSON>
    From Android device
        0) send_id     : sender ID
        1) send_t   : sending message time
        2) gps(n)   : gps coordinates (longitudue, lartitude)
        3) cell_id(n)   : Cellular provider ID
        4) net_id(n)   : Network ID
        5) msg      : personal infomation

    From gear
        6) on_t     : gear on time
        7) acc_t (n): accelerator occurred time
        8) gy_x  (n): x coordinate occurred time
        9) gy_y  (n): y coordinate occurred time
        10)gy_z  (n): z

"""

def add_and_search(this_user, message, lookup_table):
    match_result = {'send_id' :'admin',
                        'send_t'    :'resend request',
                        'lart_gps'  :'',
                        'lont_gps'  :'',
                        'cell_id'   :'',
                        'net_id'    :'',
                        'msg'       :'',
                        'on_t'      :'',
                        'acc_t'     :'',
                        'gy_x'      :'',
                        'gy_y'      :'',
                        'gy_z'      :''
                        }
    
    for client_log in lookup_table[:]:# Search table with message
        # Second diff: miliseconds
        between_msg_t = (message['send_t'] - 
                        client_log['send_t'])/1000
        between_on_t = (message['on_t'] - 
                        client_log['on_t'])/1000
        on_to_s_msg = (message['send_t'] -
                        message['on_t'])/1000
        on_to_s_log = (clinet_log['send_t'] -
                        client_log['on_t'])/1000
        # GPS diff: 0.001 diff = 100 meters far, 1 = 100m
        lart_diff = abs((int(message['lart_gps']) - 
                        int(client_log['lart_gps']))*1000)
        lont_diff = abs((int(message['lont_gps']) - 
                        int(client_log['lont_gps']))*1000)

        if between_msg_t > 7:                   # passed 8 seconds
            lookup_table.remove(client_log)     # delete log
            continue

        #message['data'], client_log['data'] = possibility
        trustworthy = gps_trustworthy(on_to_s_msg) + 
                        gps_trustworthy(on_to_s_log)
        possibility = inital_possibility( trustworthy, 
                                            lart_diff, lont_diff)
        
        if message['acc_t'] != 0 && client_log['acc_t'] != 0:
            pass
        elif message['acc_t'] == 0 && client_log['acc_t'] == 0:
            possibility -= 20
        else:
            possibility -= 10

        if message['cell_id'] != client_log['cell_id']:
            possibility -= 5
        if message['net_id']  != client_log['net_id'] :
            possibility -= 7

        if possibility > 50:
            if message['send_id'] == client_log['send_id']:
                pass
            else:
                match_result = client_log
                this_user.write_message(match_result)

        print possibility 
        print match_result['send_id']
    print '--------------------'
    lookup_table.append(message)        # Add sender's message
    this_user.write_message(match_result)

def gps_trustworthy(time):
    if time >= 4:
        return 10
    if time >= 3:
        return 10
    if time >= 2:
        return 8
    if time >= 1:
        return 6
    return 2

def inital_possibility( trust_val, lart, lont ):
    dist = math.sqrt(pow(lart,2)+pow(lont,2))
    possibility = 0
    if dist <= 1.5:
        possibility = 100
    elif dist <= 3.0:
        possibility = 90
    elif dist <= 10.0:
        possibility = 70
    else:
        possibility = 50

    if trust_val == 20:
        return possibility - 20
    elif trust_val >= 16:
        return possibility - 30
    elif trust_val >= 12:
        return possibility
    else:
        return possibility - 10
