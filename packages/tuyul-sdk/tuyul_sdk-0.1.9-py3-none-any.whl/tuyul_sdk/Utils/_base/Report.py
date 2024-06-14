class Report:

    def __str__(self) -> str:
        return str(self.__dict__)
    def __repr__(self) -> str:
        return str(self.__dict__)
    def json(self):
        return self.__dict__