class OutOfBounds(Exception):
    pass

class RangedInteger: # An integer class that is useful for kee
    def __init__(self, min, max, value, raise_border_exceptions = False):
        self.min = min
        self.max = max
        self.value = value
        self.flag = raise_border_exceptions
    
    def __add__(self, val):
        if self.min <= self.value + val <= self.max:
            self.value += val
        elif self.flag:
            raise OutOfBounds
        return self
            

    def __iadd__(self, val):
        if self.min <= self.value + val <= self.max:
            self.value += val
        elif self.flag:
            raise OutOfBounds
        return self
        
    def __sub__(self, val):
        if self.min <= self.value - val <= self.max:
            self.value -= val
        elif self.flag:
            raise OutOfBounds
        return self
    
    def __isub__(self, val):
        if self.min <= self.value - val <= self.max:
            self.value -= val
        elif self.flag:
            raise OutOfBounds
        return self