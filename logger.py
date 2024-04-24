import os


class Logger:
    """
    Utility class for logging messages to a file.

    Methods:
    - clear_log(): Clears the log file.
    - log(message): Appends a message to the log file.

    Attributes:
    None
    """

    @staticmethod
    def clear_log():
        """
        Clears the log file by creating an empty file.

        Returns:
        None
        """
        # Create 'logs' directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Clear the log file in the 'logs' directory
        with open(os.path.join('logs', 'log.txt'), 'w') as f:
            pass

    @staticmethod
    def log(message):
        """
        Appends a message to the log file.

        Args:
        - message (str): The message to be logged.

        Returns:
        None
        """
        # Write the log message in the log file in the 'logs' directory
        with open(os.path.join('logs', 'log.txt'), 'a') as f:
            f.write(f"{message}\n")
