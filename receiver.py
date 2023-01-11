from socket import *
from time import sleep

exec(open('util.py').read())

class Receiver:
    def __init__(self, port = 10163):
        self.server_ip = ''
        self.port = port
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind((self.server_ip, self.port))
        self.received_packet = 0
        self.previous_packet = None

    def build_reply(self, packet):
        """Builds reply packet with correct ack

        Args:
            packet: Incoming Packet from the sender

        Returns:
            reply: packet to be sent back to sender
        """
        lenbits = packet[10:12]
        binarylen = bin(int.from_bytes(lenbits, "big"))[2:]
        seq_num = int(binarylen[-1], 2)
        ack_num = seq_num
        msgword = packet[12:].decode()

        reply = make_packet(msgword, ack_num, seq_num)
        return reply

    def start_server(self):
        """Starts the udp socket server for rdt 3.0 
        """

        print(f'RDT Receiver listening on 0.0.0.0:{self.port}')

        while True:
            packet, client_addr = self.server_socket.recvfrom(1024)
            self.received_packet += 1
            print(f'packet num.{self.received_packet} received: {packet}')
            
            if(verify_checksum(packet) is False):
                print("failed checksum verification")
                
            reply = self.build_reply(packet)

            if(self.received_packet % 6 == 0):
               self.simulate_packet_loss()
            elif(self.received_packet % 3 == 0):
                self.simulate_data_corruption(client_addr)
                continue
                
            print(f'packet is expected, message string delivered: {str(packet[12:])}')
            print(f'packet is delivered, now creating and sending the ack packet...')

            self.previous_packet = reply

            self.server_socket.sendto(reply, client_addr)
            print("all done for this packet!\n\n")


    def simulate_packet_loss(self):
        """ Function to simulate packet loss
        """
        
        print("Simulating packet loss: sleep a while to trigger timeout event on the send side...")
        sleep(5)

    def simulate_data_corruption(self, client_addr):
        """ Function to simulate data corruption

        Args:
        client_addr: client address to send the packet
        """
        print("Simulating packet bit errors/corruption: ACK the previous packet!")
        self.server_socket.sendto(self.previous_packet, client_addr)
        print("all done for this packet!\n\n")

r = Receiver()
r.start_server()