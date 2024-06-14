import logging, datetime
from ._Color import Color

#logging.basicConfig(level=logging.INFO)

class Log:
    
    @staticmethod
    def info(message: str):
        date = f" {Color.YELLOW}" + str(datetime.datetime.now()).split('.')[0].split(' ')[1] + f"{Color.WHITE} "
        print(f'INFO:{date}: {Color.GREEN}{message}{Color.WHITE}')
        
    @staticmethod
    def error(message: str):
        date = f" {Color.YELLOW}" + str(datetime.datetime.now()).split('.')[0].split(' ')[1] + f"{Color.WHITE} "
        print(f'ERROR:{date}: {Color.RED}{message}{Color.WHITE}')
        
    @staticmethod
    def infos(message: str):
        date = f" {Color.YELLOW}" + str(datetime.datetime.now()).split('.')[0].split(' ')[1] + f"{Color.WHITE} "
        print(f'INFO:{date}: {Color.WHITE}{message}{Color.WHITE}')