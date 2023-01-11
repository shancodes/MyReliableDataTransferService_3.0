# MyReliableDataTransferService_3.0
In this project, rdt3.0 is implemented, the final version of the stop-and-wait approach. rdt3.0 can handle bit errors and packet loss. 
This rdt3.0 runs in the application layer, and uses UDP as the underlying transport service. 

The main functions are -

Numbers all the received packets from 1 on the receiver side 
Simulates timeout for all the packets whose number is divisible by 6 
For the 6th, 12th, 18th, 24th … packet, time.sleep() is used in receiver.py to intentionally sleep a while before responding back. This should be able to trigger a socket timeout on the sender side. 
Simulates packet corruption for all the packets whose number is divisible by 3 
Bit errors don’t happen quite a lot. Therefore, similar to the timeout simulation, for a packet whose number is divisible by 3, is considered as corrupted (even though  checksum is valid) and processess this ‘corrupted’ packet correspondingly. If its number is divisible by both 3 and 6, it simulates a timeout only. 

Packet Information -
The first 8 bytes always contain the value “COMPNETW”. The 9th and 10th bytes together are for the checksum of the packet, which is calculated exactly the same as the UDP checksum calculation. For the 11th and 12th bytes, the first 14 bits are used to save the length (header + data) of the current packet, the 15th bit is used to indicate if this packet is an ACK packet, and the 16th bit saves the sequence number of this packet. 

![image](https://user-images.githubusercontent.com/96903382/211912987-d75e6fca-dabd-436a-8a87-460b6c50594c.png)
