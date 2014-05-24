#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lookup.py file

import math

""" message encoded with Json, variable which are,
<JSON>
    From Android device
        0) send_id      : sender ID
        1) send_t       : sending message time
        2) lart_gps     : gps coordinates (longitudue, lartitude)
        2) lont_gps     : gps coordinates (longitudue, lartitude)
        3) cell_id(n)   : Cellular provider ID
        4) net_id(n)    : Network IP
        5) msg          : personal infomation

    From gear
        6) on_t     : gear on time
        7) acc_t (n): accelerator absolute value
        8) gy_x  (n): x coordinate occurred time
        9) gy_y  (n): y coordinate occurred time
        10)gy_z  (n): z

"""

def add_and_search(this_user, message, lookup_table):
    lookup_count = 0
    refresh = False
    match_result = {    'send_id' :'admin',
                        'send_t'    :'',
                        'lart_gps'  :'',
                        'lont_gps'  :'',
                        'cell_id'   :'',
                        'net_id'    :'',
                        'msg'       :'resend request',
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
        on_to_s_log = (client_log['send_t'] -
                        client_log['on_t'])/1000
        # GPS diff: 0.001 diff = 100 meters far, 1 = 100m
        lart_diff = abs((float(message['lart_gps']) - 
                        float(client_log['lart_gps']))*1000)
        lont_diff = abs((float(message['lont_gps']) - 
                        float(client_log['lont_gps']))*1000)

        if between_msg_t > 7:                   # passed 8 seconds
            lookup_table.remove(client_log)     # delete log
            continue

        # gps trustworthy: based on calcuating time
        trustworthy = (gps_trustworthy(on_to_s_msg) + 
                                    gps_trustworthy(on_to_s_log))
        # initial possibility: based on distance
        possibility = inital_possibility( trustworthy, 
                                            lart_diff, lont_diff)
        
        if message['acc_t'] != 0 and client_log['acc_t'] != 0:
            pass                # both gear acted
        elif message['acc_t'] == 0 and client_log['acc_t'] == 0:
            possibility -= 10   # both gear stayed still
        else:
            possibility -= 5    # one gear acted

        if message['net_id'][0:10] is client_log['net_id'][0:10] :
            possibility += 7    # if network ip is internal then +
        
        # possibility : arrived time
        possibility = possibility - 5 * between_msg_t
        if possibility > 45:
            if message['send_id'] == client_log['send_id']:
                client_log = message # refresh duplicated log
                refresh = True
            else:
                match_result = client_log
                this_user.write_message(match_result) # Find item
                lookup_count += 1         # increase lookup count
        print possibility 
        print match_result['send_id']
    print ('--------------------')
    print(len(lookup_table))                # lookup table length
    if lookup_count is 0:
        this_user.write_message(match_result) # Resend Request
    if refresh is True:
        pass
    else:
        lookup_table.append(message)    # Add sender's message

def gps_trustworthy(time):
    # Get gps trustworthy, this belongs to on time - send time
    #   difference.
    if time >= 4:
        return 7
    if time >= 3:
        return 10
    if time >= 2:
        return 9
    if time >= 1:
        return 6
    return 2

def inital_possibility( trust_val, lart, lont ):
    # Get initial exchange rationaility, it depends on
    #   GPS difference between points.
    dist = math.sqrt(pow(lart,2)+pow(lont,2))
    print "distance:" + str(dist)
    possibility = 0
    if dist <= 1.5:
        possibility = 100
    elif dist <= 3.0:
        possibility = 90
    elif dist <= 10.0:
        possibility = 70
    else:
        possibility = 50

    # Use GPS trustworthy to get reliable rational data.
    if trust_val == 20:
        return possibility - 20
    elif trust_val >= 16:
        return possibility - 30
    elif trust_val >= 12:
        return possibility
    else:
        return possibility - 10
