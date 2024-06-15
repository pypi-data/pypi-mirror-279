from typing import List
from .message_header import MessageHeader
from .io_device_data import IoDeviceData

class RequestMsg:
    """
    Represents a Request message containing various attributes like version, 
    header, payload, response, and a list of devices.
    
    Attributes:
        version (int): The version number for the Request message.
        header (MessageHeader): An instance of MessageHeader containing various metadata.
        payload (dict): A dictionary to hold payload information.
        response (dict): A dictionary to hold response information.
        device (List[IoDeviceData]): A list of IoDeviceData instances.
    """

    def __init__(self, requestName: str = "", version: int = -1):
        """
        Initialize a RequestMsg instance with default attributes.

        Args:
            requestName (str, optional): The name of the request. Defaults to an empty string.
            version (int, optional): The version number for the Request message. Defaults to -1.
        """

        # Initialize version and header
        self.version = version
        self.header = MessageHeader()
        
        # Update header attributes
        self.header.Compressed = False
        self.header.MessageType = requestName
        self.header.ConfigVersion = self.version
        
        # Initialize payload and response dictionaries
        self.payload = dict()
        self.response = dict()

        # Initialize a list of devices
        self.device: List[IoDeviceData] = []
