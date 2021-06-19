class CoordsIterator:

    def __iter__(self):
        return self

    def __init__(self, coords):
        self.input_coords = coords
        self.counter = 0

    def __next__(self):
        if len(self.input_coords) != self.counter:
            self.counter += 2
            try:
                return int(self.input_coords[self.counter - 2]), int(self.input_coords[self.counter - 1])
            except ValueError as e:
                # вылет, если в массиве есть текст
                raise e
        else:
            raise StopIteration

def get_or_none(classmodel, **kwargs):
    # часто не хватает, а вот в SQLAlchemy имеется
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        if classmodel.objects.filter(**kwargs).count() > 1:
            return False
    except ValueError:
        return None
    return None