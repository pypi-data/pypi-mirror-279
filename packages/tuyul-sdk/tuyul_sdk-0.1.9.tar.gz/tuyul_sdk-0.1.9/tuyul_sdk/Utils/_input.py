class Input:
    
    @staticmethod
    def String(message: str):
        while True:
            try:
                Result = input(message).strip()
                if len(Result) > 5: return Result
            except KeyboardInterrupt:exit()
            except:pass
    
    @staticmethod
    def Integer(message: str):
        while True:
            try:
                return int(input(message).strip())
            except KeyboardInterrupt:exit()
            except:pass
            