class CoordsIterator:

    def __iter__(self):
        return self

    def __init__(self, coords):
        self.input_coords = coords
        self.counter = 0

    def __next__(self):
        if len(self.input_coords) != self.counter:
            self.counter += 2
            return int(self.input_coords[self.counter - 2]), int(self.input_coords[self.counter - 1])
        else:
            raise StopIteration
