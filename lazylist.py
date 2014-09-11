class List:
    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._list = list()

    def _consume_next(self):
        exhausted = False
        try:
            self._list.append(next(self._iterable))
        except StopIteration:
            exhausted = True
        if exhausted:
            raise IndexError

    def _consume_rest(self):
        try:
            while True:
                self._consume_next()
        except IndexError:
            pass

    def _consume_up_to(self, index):
        if index < 0:
            self._consume_rest()
            return
        to_consume = index - len(self._list) + 1
        for i in range(to_consume):
            self._consume_next()

    def __getitem__(self, index):
        self._consume_up_to(index)
        return self._list[index]

    def __setitem__(self, index, value):
        self._consume_up_to(index)
        self._list[index] = value

    def __delitem__(self, index):
        self._consume_up_to(index)
        del self._list[index]
        
    def __len__(self):
        self._consume_rest()
        return len(self._list)

    def __bool__(self):
        if self._list:
            return True
        try:
            self._consume_next()
            return True
        except IndexError:
            return False
