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

"""

def add_and_search(this_user, message, lookup_table):
    match_result = {'send_id' :'admin',
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
    
    for client_log in lookup_table[:]:          # Search table with message
        matching_possibility = 100              # Possibility
        # Second diff: miliseconds
        passed_msg_t    = (message['send_t'] - client_log['send_t'])/1000
        passed_on_t     = (message['on_t'] - client_log['on_t'])/1000
        # GPS diff: 0.001 diff = 100 meters far
        lart_diff       = abs((int(message['lart_gps']) - 
                                int(client_log['lart_gps']))*1000)
        lont_diff       = abs((int(message['lont_gps']) - 
                                int(client_log['lont_gps']))*1000)

        if passed_msg_t > 7:                    # passed 8 seconds
            lookup_table.remove(client_log)     # delete log
            continue

        if (lart_diff < 1) and (lont_diff < 1): # within 100m^2 square
            matching_possibility += 30
        elif (lart_diff < 2) and (lont_diff < 2):  # within 200m^2 squares
            matching_possibility += 10
        elif (lart_diff < 10) and (lont_diff < 10):# within 1km squares
            matching_possibility -= 20
        else:
            matching_possibility -= 50               # more than 1 km
        
        if passed_msg_t < 2:                    # excged within 2 seconds
            matching_possibility += 20
        elif passed_msg_t < 3:
            matching_possibility += 10
        elif passed_msg_t < 4:                  # both of clients stay still
            matching_possibility -= 60
        else:
            matching_possibility -= 70

        if message['cell_id'] != client_log['cell_id']:
            matching_possibility -= 5

        if message['net_id'] != client_log['net_id']:
            matching_possibility -= 5

        if matching_possibility > 50:
            if message['send_id'] == client_log['send_id']:
                pass
            else:
                match_result = client_log
                this_user.write_message(match_result)

        print matching_possibility 
        print match_result['send_id']
    print '--------------------'
    lookup_table.append(message)                    # Add sender's message
    this_user.write_message(match_result)
