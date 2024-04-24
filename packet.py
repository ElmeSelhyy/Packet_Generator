import sys

from dataclasses import dataclass


@dataclass
class Packet:
    """
    Data class representing a generic packet.

    Attributes:
    - stream_duration_ms (int): Duration of the packet stream in milliseconds.
    - burst_size (int): Number of packets in a burst.
    - burst_period_us (int): Period between bursts in microseconds.
    - max_packet_size (str): Maximum size of the packet.
    """
    stream_duration_ms: int
    burst_size: int
    burst_period_us: int
    max_packet_size: str


@dataclass
class ECPRI(Packet):
    """
    Data class representing an ECPRI packet.

    Inherits from:
    - Packet

    Attributes:
    - protocol_version (bytearray): Version of the ECPRI protocol.
    - reserved (str): Reserved field.
    - C (str): C field.
    -
    """

    protocol_version: str
    reserved: str
    C: str

    @property
    def ecpri_first_byte(self):
        """
        Property representing the first byte of the ECPRI packet (protocol_version, reserved, C).

        Returns:
        bytes: First byte.
        """
        byte = self.protocol_version + self.reserved + self.C
        # Convert str to int then to int
        byte = int(byte, 2)
        # I want to return it in this shape b'\xstr'
        byte.to_bytes(1, byteorder='big')
        # return it as string
        # make the string one
        return str(byte)

    @ property
    def message_type(self):
        """
        Property representing the message type of the ECPRI packet.

        Returns:
        bytes: Message type represented as bytes.
        """
        return b"\x00"

    @ property
    def max_packet_size_in_bytes(self):
        """
        Property representing the max packet size in bytes.

        Returns:
        str: Max packet size in bytes.
        """
        # Convert max_packet_size to bytes
        return int(self.max_packet_size).to_bytes(2, byteorder='big')

    @ property
    def payload_size(self):
        """
        Property representing the payload size of the ECPRI packet.

        Returns:
        int: Size of the payload in bytes.
        """

        payload_size = int(self.max_packet_size)-len(self.protocol_version)-len(
            self.reserved)-len(self.C)-len(self.message_type)*4-len(self.max_packet_size)

        return payload_size


@ dataclass
class Ethernet(Packet):
    """
    Data class representing an Ethernet packet.

    Inherits from:
    - Packet

    Attributes:
    - IFGs_number (int): Number of Inter-Frame Gaps (IFGs) in the Ethernet packet.
    - src_address (bytearray): Source MAC address.
    - dest_address (bytearray): Destination MAC address.
    - EtherType (bytearray): Ethernet Type field.
    """

    IFGs_number: int
    src_address: bytearray
    dest_address: bytearray
    EtherType: bytearray

    @ property
    def payload_size(self):
        """
        Property representing the payload size of the Ethernet packet.

        Returns:
        int: Size of the payload in bytes.
        """
        payload_size = int(self.max_packet_size)-len(self.src_address)-len(self.dest_address)-len(
            self.EtherType)-len(self.SOF)-len(self.preamble)-4
        # 4 bytes for CRC
        return payload_size

    @ property
    def IFG(self):
        """
        Property representing the Inter-Frame Gap (IFG) of the Ethernet packet.

        Returns:
        bytes: IFG represented as bytes.
        """
        return b"\x07" * self.IFGs_number

    @ property
    def SOF(self):
        """
        Property representing the Start of Frame (SOF) of the Ethernet packet.

        Returns:
        bytes: SOF represented as bytes.
        """
        return b"\xFD"

    @ property
    def preamble(self):
        """
        Property representing the preamble of the Ethernet packet.

        Returns:
        bytes: Preamble represented as bytes.
        """
        return b"\x55"*8
