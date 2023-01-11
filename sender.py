from socket import *

exec(open('util.py').read())

class Sender:
    def __init__(self, port = 10163):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        self.server_ip = '0.0.0.0'
        self.server_port = port
        self.seq_num = 0
        self.rnum = 1

    def handle_success(self, response):
        """Handles the scenario where packet successfully sent to receiver and receiver sent correct ack

        Args: 
        response: hash with keys ack and seq, holding seq_num and ack from receiver as int values
        """
        #Update Next Sequence Number
        #Send Message
        print(f'packet is received correctly: seq num = {response["seq"]} ACK num = {response["ack"]}.all done!\n\n')

    def set_next_seq(self):
        """Sets the sequence number for the next packet
        """
        if self.seq_num == 0:
            self.seq_num = 1
        else:
            self.seq_num = 0

    def parse_receiver_response(self, received_message):
        """parses packet from receiver and build the hash with ack and seq

        Args:
            received_message: packet from receiver

        Returns:
            Hash with ack and seq values 
        """
        lenbits = received_message[10:12]
        binarylen = bin(int.from_bytes(lenbits, "big"))[2:]
        seq = int(binarylen[-1], 2)
        ack = int(binarylen[-2], 2)
        response = {
        'ack': ack,
        'seq': seq
        }

        return response
        #Fetch ACK and SEQ from Modified Message


    def validate_response(self, response):
        """validates the seq and ack from receiver

        Args:
            response: hash with ack and seq
        
        Returns:
            boolean that represents success or failure of verification
        """
        if(response['seq'] != str(self.seq_num)):
            return False
        elif (response['ack'] != str(self.seq_num)):
            return False
        else:
            return True

    # return (response['seq'] != str(self.seq_num)) and (response['ack'] != str(self.seq_num))

  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT Change the function name.                    #######                    
  ####### You can have other functions as needed.                             #######


    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

        Args:
        app_msg_str: the message string (to be put in the data field of the packet)

        """
        # print("sent")
        print(f'original message string: {app_msg_str}')

        packet = make_packet(app_msg_str, 0, self.seq_num)
        self.send_packet(app_msg_str, packet)
        self.set_next_seq()


    def handletimeout(self, app_msg_str, packet):
        """handles the case where fetching packet from receiver times out

        Args:
            app_msg_str: string to be sent to receiver
            packet: packet to be sent
        """
        print('socket timeout, resend!\n\n')
        print(f'[timeout retransmission]: {app_msg_str}')
        self.send_packet(app_msg_str, packet)

    def handle_corruption(self, app_msg_str, packet):
        """handles case where the receiver sends a packet that has corrupted data

        Args:
            app_msg_str: string to be sent to receiver
            packet: packet to be sent
        """
        print('receiver acked the previous pkt, resend!\n\n')
        print(f'[ACK-Previous retransmission]: {app_msg_str}')
        self.send_packet(app_msg_str, packet)

    def send_packet(self, app_msg_str, packet):
        """method to send packet to receiver and define the logic of how to handle the response

        Args:
            app_msg_str: string to be sent to receiver
            packet: packet to be sent
        """

        try:
            clientSocket = socket(AF_INET, SOCK_DGRAM)
            clientSocket.settimeout(3)
            clientSocket.sendto(packet,(self.server_ip, self.server_port))

            print(f'packet num.{self.rnum} is successfully sent to receiver')

            modified_msg, server_addr = clientSocket.recvfrom(2048)
            clientSocket.close()
            response = self.parse_receiver_response(modified_msg)
            self.rnum += 1

            if((self.seq_num == response['seq']) and (self.seq_num == response['ack'])):
                self.handle_success(response)
            else:
                self.handle_corruption(app_msg_str, packet)

        except Exception as e:
            self.rnum += 1
            self.handletimeout(app_msg_str, packet)
