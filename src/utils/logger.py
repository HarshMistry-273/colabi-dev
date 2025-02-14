import logging

# Create a logs in success and faild for all api's
def setup_logger(log_file):
    """
    Sets up a logger that writes log messages to a specified file.

    Args:
        log_file (str): The path to the log file where messages will be recorded.

    Returns:
        logging.Logger: The configured logger instance.

    Notes:
        - The logger is set to the DEBUG level, capturing all log messages at 
        this level and above.
        - A file handler is added to log messages to the specified file.
        - The formatter specifies the log message format, including the timestamp, 
        log level, filename, line number, and the message.
        - StreamHandler for console output is currently commented out but can be enabled if needed.
    """
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    # stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )

    file_handler.setFormatter(formatter)
    # stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    # logger.addHandler(stream_handler)

    return logger

logger_set = setup_logger(f"colabi.log")