def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """
    s = 0
    for i in range(0, len(packet_wo_checksum), 2):
        w = (packet_wo_checksum[i] << 8) + packet_wo_checksum[i+1]
        s = carry_around_add(s, w)
    return (~s & 0xffff).to_bytes(2, "big")


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """

    packet_checksum = packet[8:10]
    data = packet[12:]
    length = packet[10:12]
    base = packet[:8]
    check = base + length + data

    calculated_checksum = create_checksum(check)
    csum = ""
    for i in packet_checksum:
        csum += bin(i)[2:]

    psum = ""
    for i in calculated_checksum:
        psum += bin(i)[2:]
    
    res = ""
    for i in psum:
        if(i == '0'):
            res += '1'
        else:
            res += '0'

    sum = (int(csum, 2) + int(res, 2))

    for i in bin(sum)[2:]:
        if i != '1':
            return False

    return True

def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    base_word = "COMPNETW"
    # checksum = create_checksum(data_str)

    base = bytes(base_word, "utf-8")
    data = bytes(data_str, "utf-8")
    s = 12 + len(data_str)

    c = bin(s << 2)
    lenstr = ''
    for i in range(len(c)):
        if i == len(c) - 1:
            lenstr += get_binary_char(seq_num)
        elif i == len(c) - 2:
            lenstr += get_binary_char(ack_num)
        else:
            lenstr += c[i]

    length = int(lenstr, 2).to_bytes(2, "big")

    to_checksum = base + length + data
    checksum2 = create_checksum(to_checksum)
    packet = base + checksum2 + length + data

    print(f'packet created: {packet}')
    return packet

def get_binary_char(num):
    """To get the Binary string representation of 1 and 0
    """
    if num == 1:
        return '1'
    else:
        return '0'

def carry_around_add(a, b):
    """calculate carry and handle addition while doing binary addition

    Args:
        a, b: numbers to be added
    
    Returns:
        the 
    """
    c = a + b
    return (c & 0xffff) + (c >> 16)

# make sure your packet follows the required format!


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should not make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  
