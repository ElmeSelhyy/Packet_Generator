# PacketGenerator

PacketGenerator is a packet generation tool written in Python. It allows you to generate bursts of packets based on specified configurations, including Ethernet and ECPRI packet types.

## Project Structure

The project consists of the following files:

- **generation.py**: Contains classes for packet generation, including EthernetGeneration and ECPRIGeneration.
- **packet.py**: Defines data classes for representing Ethernet and ECPRI packets.
- **files.py**: Implements file handling operations, including reading and writing configuration files.
- **logger.py**: Provides logging functionality for the application.
- **main.py**: Main entry point for the application. It reads configurations from an input file, generates packets based on the specified payload type, and writes them to an output file.
- **README.md**: Documentation file explaining the project and its components.

## Usage

To use the packet generation tool, follow these steps:

1. Install Python if you haven't already.
2. Clone or download the project repository.
3. Navigate to the project directory in your terminal.
4. Run the `main.py` file with the input and output file paths as arguments. For example:

    ```bash
    python main.py input.txt output.txt
    ```

    Replace `input.txt` and `output.txt` with the paths to your input configuration file and desired output file, respectively.

## Configuration File Format

The input configuration file should follow a specific format. Each parameter should be specified as key-value pairs in the format `key=value`. Comments can be added using the `//` symbol.

Here's an example configuration file:

```plaintext
STREAM_DURATION_MS = 30                      // Sreaming duration of ethernet packets (Total duration of generation)
BURST_SIZE = 5                              // Number of ethernet packets in one burst
BURST_PERIODICITY_US = 5000                  // The periodicity of the burst in micro seconds
IFGs_NUMBER = 30                            // Standard IFGs to be inserted after CRC, in bytes
SOURCE_ADDRESS = 0x102030405060             // Source address in hex format
DESTINATION_ADDRESS = 0x102030302010        // Source address in hex format
ETHER_TYPE = 0x0800                         // Constant value
PAYLOAD_TYPE = ETHERNET                    // Payload of ethernet packet, could be random or fixed value
MAX_PACKET_SIZE = 243     // Packet size in bytes, includes preamble, SoP, src add, dest add, etherType, payload and CRC
PROTOCOL_VERSION=0010
RESERVED=010
C=0




