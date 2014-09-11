class List:
    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._list = list()
        self._exhausted = False

    @property
    def consumed(self):
        return len(self._list)

    def _consume_next(self):
        try:
            self._list.append(next(self._iterable))
        except StopIteration:
            self._exhausted = True
            raise IndexError


    def _consume_rest(self):
        try:
            while True:
                self._consume_next()
        except IndexError:
            pass

    def _consume_up_to(self, index):
        if index < 0:
            raise ValueError('negative indices not supported')
        to_consume = index - self.consumed + 1
        for i in range(to_consume):
            self._consume_next()

    def __getitem__(self, index):
        self._consume_up_to(index)
        return self._list[index]

    def __setitem__(self, index, value):
        self._consume_up_to(index)
        self._list[index] = value
        

