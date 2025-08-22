from datetime import datetime
#!        RED        GREEN       BLUE        RESET
col = ['\033[91m', '\033[92m', '\033[94m', '\033[0m']

class custLogging:
    def __init__(self):
        return
    
    def log(self, type:str, log):
        date = datetime.now()
        date = date.strftime("%m-%d-%Y %I:%M:%S")
        print(f"{col[3]}({col[0]}{date}{col[3]}) [{col[2]}{type}{col[3]}]: {col[1]}{log}{col[3]}\n")