import os
import sys
import random

from enum import Enum
from logger import Logger


def convert_to_enum(PAYLOAD_TYPE):
    """
    Converts a string representation of payload type to its corresponding enum value.

    Args:
    - PAYLOAD_TYPE (str): String representation of the payload type.

    Returns:
    - Payload_Type: Enum value corresponding to the given payload type.

    Raises:
    - ValueError: If the payload type string is invalid.
    """
    try:
        return Payload_Type[PAYLOAD_TYPE.upper()]
    except KeyError:
        raise ValueError(f"No such PAYLOAD: {PAYLOAD_TYPE}")


class Payload_Type(Enum):
    """
    Enum class representing different payload types.

    Attributes:
    - ETHERNET: Ethernet payload type.
    - ECPRI: ECPRI payload type.
    - RANDOM: Randomly chosen payload type between Ethernet and ECPRI.
    """
    ETHERNET = 1
    ECPRI = 2
    RANDOM = random.randint(1, 2)


class FileHandler:
    """
    Utility class for file operations.

    Methods:
    - readfile(file): Reads configuration from a file.
    - has_read_permission(file): Checks read permission for a file.
    - has_write_permission(file): Checks write permission for a file.
    - writefile(file, config): Writes configuration to a file.
    - write_buffer(buffer, file): Writes packet buffer to a file.

    Attributes:
    None
    """
    @staticmethod
    def parse_config(file):
        config = {}
        with open(file, 'r') as f:
            for line in f:
                line = line.strip().split('//')[0]
                if not line:
                    continue
                key, value = line.strip().split('=')
                key = key.strip()
                value = value.strip()
                if value.startswith('0x'):
                    value = value[2:]
                if key in ['STREAM_DURATION_MS', 'BURST_SIZE', 'BURST_PERIODICITY_US', 'IFGs_NUMBER']:
                    config[key] = int(value)
                if key == 'MAX_PACKET_SIZE':
                    config[key] = value
                if key in 'PROTOCOL_VERSION':
                    # Treat value as a binary string
                    config[key] = value.zfill(4)
                if key == 'RESERVED':
                    config[key] = value.zfill(3)
                if key == 'C':
                    config[key] = value.zfill(1)
                if key == 'PAYLOAD_SIZE':
                    config[key] = value.zfill(16)
                if key in ['MESSAGE_TYPE', 'PAYLOAD_SIZE', 'SOURCE_ADDRESS', 'DESTINATION_ADDRESS', 'ETHER_TYPE']:
                    # Convert hexadecimal string to byte array
                    config[key] = bytes.fromhex(value)
                if key == 'PAYLOAD_TYPE':
                    PAYLOAD_ENUM = convert_to_enum(value)
                    config[key] = PAYLOAD_ENUM

        return config

    @staticmethod
    def readfile(file):
        """
        Reads configuration from a file.

        Args:
        - file (str): Path to the input configuration file.

        Returns:
        dict: Configuration parameters read from the file.
        """
        return FileHandler.parse_config(file)

    @staticmethod
    def has_read_permission(file):
        """
        Checks read permission for a file.

        Args:
        - file (str): Path to the file.

        Returns:
        None
        """
        if os.access(file, os.R_OK):
            Logger.log(f"Read permission granted for file: {file}")
        else:
            Logger.log("No read permission for file: {file}")
            sys.exit(1)

    @staticmethod
    def has_write_permission(file):
        """
        Checks write permission for a file.

        Args:
        - file (str): Path to the file.

        Returns:
        None
        """
        if os.access(file, os.W_OK):
            Logger.log(f"Write permission granted for file: {file}")
        else:
            Logger.log(f"No write permission for file: {file}")
            sys.exit(1)

    @staticmethod
    def write_buffer(buffer, file):
        with open(file, 'ab') as f:
            for packet in buffer:
                for item in packet:
                    if isinstance(item, int):
                        # Write byte as hexadecimal
                        f.write('{:02x}'.format(item).encode())
                    else:
                        # Write bit string as it is
                        f.write(item.encode())
