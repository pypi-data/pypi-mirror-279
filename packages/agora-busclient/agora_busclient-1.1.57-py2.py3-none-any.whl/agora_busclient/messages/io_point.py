class IoPoint:
    """ 
    Represents an individual Input/Output (IO) point. 
    Contains information about the value represented as either a flow or a str, 
       quality, and timestamp of the point.
    """
  
    def __init__(self,
                 value: float = None,
                 value_str: str = None,
                 quality_code: int = None,
                 timestamp: float = None):
        """
        Initialize an IoPoint instance.
        
        Args:
            value (float, optional): Numerical value of the IO point. Defaults to None.
            value_str (str, optional): String representation for non-numeric values. Defaults to None.
            quality_code (int, optional): Quality code indicating the reliability of the value. 
                0 signifies good quality, 1 signifies bad quality. Defaults to None.
            timestamp (float, optional): Timestamp indicating when the value was recorded, 
                expected to be in epoch time format (AgoraTimeStamp). Defaults to None.
        
        Attributes:
            value (float): Numerical value of the IO point.
            value_str (str): String representation for non-numeric values.
            quality_code (int): Quality code for the value.
            timestamp (float): Timestamp of the IO point, in epoch time format (msec since UTC epoch).
        """
        self.value: float = value
        self.value_str: str = value_str
        self.quality_code: int = quality_code
        self.timestamp: float = timestamp
