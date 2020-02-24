# MAC_Address_Changer
There are 3 modes provided in the file:
1. We can change MAC address manually by selecting the network and choosing your own MAC address.

  eg.   python Mac_Changer.py -i eth0 -m 00:00:00:00:00:00
  
2. We can set a random MAC address of a network.

  eg.   python Mac_Changer.py -i wlan0 -r
  
3. Last one, or I should say most effective one. It gives random MAC address in the time interval provided.

  eg.   python Mac_Changer.py -i wlan0 -r -t 600
            (The time provided is in seconds)
            
            
  In case of doubt a help section is also added which says
  
  
       -h, --help            show this help message and exit
       -i INTERFACE, --interface=INTERFACE
                        Interface to change
       -m NEW_MAC, --mac=NEW_MAC
                        New MAC address                                                                                                                    
       -r, --random          Random MAC address                                                                                                                 
       -t TIME_INTERVAL, --time=TIME_INTERVAL                                                                                                                   
                        Time Interval(in sec) to change MAC address
  
