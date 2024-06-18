class WorkFlow:
    """
    Represents a WorkFlow with a specific Type and Properties.
    
    Attributes:
        Type (str): The type of the WorkFlow. 
        Properties (dict): A dictionary holding various properties related to the WorkFlow.
    """
  
    def __init__(self):
        """
        Initialize a WorkFlow instance with default attributes.
        """
        # Initialize the type as an empty string
        self.Type = ""
        
        # Initialize an empty dictionary for properties
        self.Properties = dict()
