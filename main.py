import sys

from generation import EthenetGeneration, ECPRIGeneration
from packet import Ethernet, ECPRI
from file_handler import FileHandler
from logger import Logger


def main():
    """
    Main function to generate packets based on configuration and write them to an output file.

    Reads configuration from an input file specified as a command-line argument.
    Generates packets based on the specified payload type (Ethernet or ECPRI).
    Writes the generated packets to an output file specified as a command-line argument.
    """

    # Checking command-line argument validity
    if len(sys.argv) != 3:
        print("Usage: python test.py <inputfile> <outputfile>")
        sys.exit(1)

    # Clearing the log file
    Logger.clear_log()

    # Assigning file paths
    config_file = sys.argv[1]
    output_file = sys.argv[2]
    # clear the output file
    open(output_file, 'w').close()

    file_handler = FileHandler()

    # Check access permissions for input and output files
    file_handler.has_read_permission(config_file)
    file_handler.has_write_permission(output_file)

    # Read configuration from file
    config = file_handler.readfile(config_file)

    # Generate packets based on payload type
    if config['PAYLOAD_TYPE'].value == 1:
        # Assigning values to Ethernet packets
        ethernet_packets = Ethernet(
            config.get('STREAM_DURATION_MS'),
            config.get('BURST_SIZE'),
            config.get('BURST_PERIODICITY_US'),
            config.get('MAX_PACKET_SIZE'),
            config.get('IFGs_NUMBER'),
            config.get('SOURCE_ADDRESS'),
            config.get('DESTINATION_ADDRESS'),
            config.get('ETHER_TYPE')
        )

        # Generate Ethernet bursts
        gen = EthenetGeneration()
        gen.generate_bursts(output_file, ethernet_packets)
    elif config['PAYLOAD_TYPE'].value == 2:
        # Assigning values to ECPRI packets
        ecpri_packet = ECPRI(
            config.get('STREAM_DURATION_MS'),
            config.get('BURST_SIZE'),
            config.get('BURST_PERIODICITY_US'),
            config.get('MAX_PACKET_SIZE'),
            config.get('PROTOCOL_VERSION'),
            config.get('RESERVED'),
            config.get('C')
        )

        # Generate ECPRI bursts
        gen = ECPRIGeneration()
        gen.generate_bursts(output_file, ecpri_packet)
    else:
        print("Invalid payload_type. Use 'ETHERNET' or 'ECPRI' or 'RANDOM'")
        sys.exit(1)


if __name__ == "__main__":
    main()
