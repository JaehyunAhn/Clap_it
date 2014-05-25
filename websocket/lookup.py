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

    Data: if (possibility over threshold):
            excg contacts
"""

def add_and_search(this_user, message, lookup_table):
    lookup_count = 0
    threshold = 40
    refresh_mylog = False
    
    match_result = {    'send_id'   :'',
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
            pass                # if both gear acted
        elif message['acc_t'] == 0 and client_log['acc_t'] == 0:
            possibility -= 35   # if both gear's are stayed still
        else:
            possibility -= 10   # if only one gear acted

        if message['net_id'][0:10] is client_log['net_id'][0:10] :
            possibility += 7    # if network ip is internal then +
        
        # possibility : arrived time
        possibility = possibility - 3.5 * between_msg_t
        if possibility > trustworthy:
            # Refresh log with new message
            if message['msg'] == client_log['msg']:
                temp = 0.0
                temp = client_log['acc_t']
                client_log = message    # refresh duplicated log
                if client_log['acc_t'] > 0.0:
                    client_log['acc_t'] = temp
                    message['acc_t'] = temp
                refresh_mylog = True
            else:
                match_result = client_log
                lookup_count += 1       # increase lookup count
                this_user.write_message(match_result) # Find item
                print "I find you" + str(match_result['msg'])
    print ('--------------------')
    print "Table length: " + str(len(lookup_table))
    # lookup table length
    if lookup_count is 0:
        this_user.write_message(match_result)   # Resend Request
    if refresh_mylog is True:
        pass
    else:
        lookup_table.append(message)    # Add sender's message
    print "I send this msg: " + str(message['msg'])

def gps_trustworthy(time):
    # Get gps trustworthy, this belongs to on time - send time
    #   difference.
    if time >= 4:
        return 7
    if time >= 3:
        return 8
    if time >= 2:
        return 9
    if time >= 1:
        return 7
    return 2

def inital_possibility( trust_val, lart, lont ):
    # Get initial exchange rationaility, it depends on
    #   GPS difference between points. (float) 1.0 == 100 m
    dist = math.sqrt(pow(lart,2)+pow(lont,2))
    print "distance:" + str(dist)
    possibility = 0
    if   dist <= 0.1:       # 10 m
        possibility = 120 
    elif dist <= 0.2:       # 20 m
        possibility = 90
    elif dist <= 0.5:       # 50 m
        possibility = 75
    elif dist <= 1.0:       # 100 m
        possibility = 60
    elif dist <= 3.0:       # 300 m
        possibility = 55
    else:
        possibility = 40    # over

    # Use GPS trustworthy to get reliable rational data.
    print "Trust val: " + str(trust_val)
    print "Possibility: " + str(possibility)

    if trust_val == 20:
        return possibility - 20
    elif trust_val >= 16:
        return possibility
    elif trust_val >= 11:
        return possibility - 10
    elif trust_val >= 9:
        return possibility - 20
    elif trust_val >= 5:
        return possibility - 26
    else:
        return possibility - 25
