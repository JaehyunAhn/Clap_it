#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lookup.py file

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

<Lookup Table>
    From client
       +11) sender_ip : server got ip address from the sender
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
    
    for client_log in lookup_table[:]:          # Search table with message
        matching_possibility = 100              # Possibility
        # Second diff: miliseconds
        passed_msg_t    = (message['send_t'] - client_log['send_t'])/1000
        passed_on_t     = (message['on_t'] - client_log['on_t'])/1000
        # GPS diff: 0.001 diff = 100 meters far
        lart_diff       = abs((message['lart_gps'] - client_log['lart_gps'])*1000)
        lont_diff       = abs((message['lont_gps'] - client_log['lont_gps'])*1000)

        if passed_msg_t > 7:                    # passed 8 seconds
            lookup_table.remove(client_log)     # delete log
            continue

        if (lart_diff < 2) and (lont_diff < 2): # within 200 square meters
            matching_possibility += 30
        else if (lart_diff < 10) and (lont_diff < 10):  # within 1 km squares
            matching_possibility += 10
        else if (lart_diff < 100) and (lont_diff < 100):# within 10km squares
            matching_possibility -= 20
        else:
            matching_possibility -= 50
        
        if passed_msg_t < 2:                    # excged within 2 seconds
            matching_possibility += 20
        else if passed_msg_t < 3:
            matching_possibility += 10
        else if passed_msg_t < 4:
            matching_possibility -= 30
        else:
            matching_possibility -= 50

        if message['sender_ip'] != client_log['sender_ip']:
            matching_possibility -= 5

        if message['cell_id'] != client_log['cell_id']:
            matching_possibility -= 5

        if message['net_id'] != client_log['net_id']:
            matching_possibility -= 5

        print matching_possibility
    lookup_table.append(message)                    # Add sender's message
    this_user.write_message(match_result)
