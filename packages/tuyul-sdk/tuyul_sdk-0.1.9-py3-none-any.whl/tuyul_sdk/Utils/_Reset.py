import os, platform

class Reset:
    
    def __init__(self) -> None:        
        if platform.system().lower() == "windows":
            os.system('color')
            os.system('cls')
        else:os.system('clear')