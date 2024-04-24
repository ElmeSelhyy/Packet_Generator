import binascii
import time
import os
from abc import ABC, abstractmethod

from file_handler import FileHandler
from logger import Logger


class Generation(ABC):
    """
    Base class for packet generation.

    Methods:
    - generate_packet(packet_config): Abstract method to generate a single packet.
    - generate_single_burst(packet_config): Abstract method to generate a single burst of packets.
    - generate_bursts(filename, packet_config): Generates bursts of packets and writes them to a file.

    Attributes:
    None
    """
    @abstractmethod
    def generate_packet(self, packet_config):
        pass

    @abstractmethod
    def generate_single_burst(self, packet_config):
        """
        abstract method

        """
        pass

    def generate_bursts(self, filename, packet_config):
        """
        Generates bursts of packets and writes them to a file.

        Args:
        - filename: Name of the file to write the packets to.
        - packet_config: Configuration object specifying packet parameters.

        Returns:
        None
        """
        start_time = time.time()
        file_handler = FileHandler()
        Burst = 1
        while time.time() - start_time < packet_config.stream_duration_ms / 1_000:
            Logger.log(f"Generating burst {Burst}")
            file_handler.write_buffer(
                self.generate_single_burst(packet_config), filename)
            Logger.log(f"Burst {Burst} finished generating")
            Burst += 1


class EthenetGeneration(Generation):
    """
    Subclass for Ethernet packet generation.

    Inherits from:
    - Generation

    Methods:
    - generate_packet(packet_config): Generates a single Ethernet packet.
    - generate_single_burst(packet_config): Generates a single burst of Ethernet packets.

    Attributes:
    None
    """

    def crc32(self, data: bytes):
        "convert list of bytes to string"
        data = ''.join([chr(byte) for byte in data])
        return binascii.crc32(data.encode('utf-8')) & 0xFFFFFFFF

    def generate_packet(self, packet_config):
        """
        Generates a single Ethernet packet.

        Args:
        - packet_config: Configuration object specifying packet parameters.

        Returns:
        A list representing the generated Ethernet packet content.
        """
        packet_content = []
        packet_content += packet_config.preamble
        packet_content += packet_config.SOF
        packet_content += packet_config.dest_address
        packet_content += packet_config.src_address
        packet_content += packet_config.EtherType
        packet_content += os.urandom(packet_config.payload_size)
        crc = self.crc32(packet_content)
        packet_content += crc.to_bytes(4, byteorder='big')

        return packet_content

    def generate_single_burst(self, packet_config):
        """
        Generates a single burst of Ethernet packets.

        Args:
        - packet_config: Configuration object specifying packet parameters.

        Returns:
        A list containing Ethernet packets generated in the burst.
        """
        buffer = []
        burst_start_time = time.time()
        while time.time() - burst_start_time < packet_config.burst_period_us / 1_000_000:
            for i in range(packet_config.burst_size):
                packet_buffer = self.generate_packet(packet_config)
                packet_end_time = time.time()
                if packet_end_time - burst_start_time >= packet_config.burst_period_us / 1_000_000:
                    buffer.append(packet_config.IFG)
                    Logger.log("Added IFG to buffer")
                    break
                else:
                    buffer.append(packet_buffer)
                    Logger.log("Added packet to buffer")
                    buffer.append(packet_config.IFG)
                    Logger.log("Added IFG to buffer")
            break
        return buffer


class ECPRIGeneration(Generation):
    """
    Subclass for ECPRI packet generation.

    Inherits from:
    - Generation

    Methods:
    - generate_packet(packet_config): Generates a single ECPRI packet.
    - generate_single_burst(packet_config): Generates a single burst of ECPRI packets.

    Attributes:
    None
    """

    def generate_packet(self, packet_config):
        """
        Generates a single ECPR Ipacket.

        Args:
        - packet_config: Configuration object specifying packet parameters.

        Returns:
        A list representing the generated ECPR Ipacket content.
        """
        packet_content = []
        packet_content += packet_config.ecpri_first_byte
        packet_content += packet_config.message_type
        packet_content += packet_config.max_packet_size_in_bytes
        packet_content += os.urandom(packet_config.payload_size)

        return packet_content

    def generate_single_burst(self, packet_config):
        """
        Generates a single burst of ECPR Ipackets.

        Args:
        - packet_config: Configuration object specifying packet parameters.

        Returns:
        A list containing ECPR Ipackets generated in the burst.
        """
        buffer = []
        burst_start_time = time.time()
        while time.time() - burst_start_time < packet_config.burst_period_us / 1_000_000:
            for i in range(packet_config.burst_size):
                packet_buffer = self.generate_packet(packet_config)
                packet_end_time = time.time()
                if packet_end_time - burst_start_time >= packet_config.burst_period_us / 1_000_000:
                    break
                else:
                    buffer.append(packet_buffer)
                    Logger.log("Added packet to buffer")
            break
        return buffer
