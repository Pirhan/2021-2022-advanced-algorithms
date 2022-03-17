from pickle import DICT


class heap:
    def __init__(self) -> None:
        self.dic = {}

    def insert(self, key : tuple, value : int):
        if key is not tuple:
            return False
        self.dic[(key[0], key[1])] = value
        return True
    
    def extractMin(self):
        keys = self.dic.keys
#TODO