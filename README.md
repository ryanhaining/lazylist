lazylist
========

Lazily evaluated lists in Python

A `lazylist.List` accepts a single iterable as its only constructor argument.
The intention is for this to be a generator.  The `lazylist.List` will
behave as a normal list does, but will only evaluate the iterable as it needs
to.  If there is a request for index `[5]`, then elements 0 - 5 will be
evaluated if they have not been yet. Certain operations like `len` and
negative indexing will force the list to be evaluated. This decision was made
to make the lazylist outwardly appear as much like a normal list as possible.
