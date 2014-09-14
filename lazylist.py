import itertools

class List:
    def __init__(self, iterable):
        self._iterable = iter(iterable)
        self._list = list()

    @property
    def _exhausted(self):
        try:
            self._consume_next()
            return False
        except IndexError:
            return True

    def _slice_max(self, sl):
        start, stop, step = sl.start, sl.stop, sl.step
        if step == None:
            step = 1
        if step > 0 and stop > start:
            return stop - ((stop - start) % step)
        elif step < 0 and stop < start:
            return stop + ((start - stop) % (-step))
        else:
            return 0

    def _positive_index(self, value):
        '''Returns positive list index for value

        If value is None, returns None
        If value is positive, it is returned.
        If value is negative, it is converted to a positive index referring to
        the same position
        
        '''
        if value is None: return None
        if value >= 0: return value
        self._consume_rest()
        pos = len(self._list) - abs(value)
        if pos < 0:
            raise IndexError('list index out of range')
        return pos

    def _consume_next(self):
        exhausted = False
        try:
            self._list.append(next(self._iterable))
        except StopIteration:
            exhausted = True
        if exhausted:
            raise IndexError

    def _consume_rest(self):
        self._list.extend(self._iterable)

    def _consume_up_to_value(self, value):
        if value < 0:
            self._consume_rest()
            return
        to_consume = value - len(self._list) + 1
        for i in range(to_consume):
            self._consume_next()
    
    def _consume_up_to_slice(self, sl):
        if sl.start < 0 or sl.stop < 0:
            self._consume_rest()
        else:
            self._consume_up_to(self._slice_max(sl))

    def _consume_up_to(self, index):
        if isinstance(index, slice):
            self._consume_up_to_slice(index)
        else:
            self._consume_up_to_value(index)

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

    def extend(self, rest):
        self._iterable = itertools.chain(self._iterable, iter(rest))

    def __iadd__(self, rest):
        self.extend(rest)
        return self
    
    def __repr__(self):
        self._consume_rest()
        return '[' + ', '.join(repr(item) for item in self._list) + ']'

    def __eq__(self, other):
        return (all(a == b for a, b in zip(self, other))
                and self._exhausted
                and (isinstance(other, list) or other._exhausted)
                and len(self) == len(other))

    def sort(self):
        self._consume_rest()
        self._list.sort()

    def reverse(self):
        self._consume_rest()
        self._list.reverse()

    def pop(self, index=-1):
        self._consume_up_to(index)
        item = self._list[index]
        del self._list[index]
        return item

    def index(self, item, start=0, stop=None):
        start = self._positive_index(start)
        stop = self._positive_index(stop)
        for i, e in enumerate(itertools.islice(self, start, stop)):
            if e == item:
                return i + start

        raise ValueError('{} is not in list'.format(item))

    def count(self, item):
        self._consume_rest()
        return self._list.count(item)

    def remove(self, item):
        del self[self.index(item)]
