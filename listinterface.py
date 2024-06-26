"""
File: listinterface.py
Author: Ken Lambert

Interfaces for lists and list iterators
"""

from abc import ABC, abstractmethod

class ListInterface(ABC):
    """Interface for all list types."""

    # Constructor
    def __init__(self, sourceCollection = None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        pass

    # Accessor methods
    @abstractmethod
    def isEmpty(self):
        """Returns True if len(self) == 0, or False otherwise."""
        return True
    
    @abstractmethod
    def __len__(self):
        """-Returns the number of items in self."""
        return 0

    @abstractmethod
    def __str__(self):
        """Returns the string representation of self."""
        return ""

    @abstractmethod
    def __iter__(self):
        """Supports iteration over a view of self."""
        return None

    @abstractmethod
    def __add__(self, other):
        """Returns a new instance of the type of self
        containing the contents of self and other."""
        return None

    @abstractmethod
    def __eq__(self, other):
        """Returns True if self equals other,
        or False otherwise."""
        return False

    @abstractmethod
    def __getitem__(self, i):
        """Precondition: 0 <= i < len(self)
        Returns the item at position i.
        Raises: IndexError."""
        return None

    @abstractmethod
    def index(self, item):
        """Precondition: item is in the list.
        Returns the position of item.
        Raises: ValueError if the item is not in the list."""
        return 0

    # Mutator methods
    @abstractmethod
    def clear(self):
        """Makes self become empty."""
        pass

    @abstractmethod
    def add(self, item):
        """Inserts item at the end of the list."""
        pass

    @abstractmethod
    def append(self, item):
        """Inserts item at the end of the list."""
        pass

    @abstractmethod
    def remove(self, item):
        """Precondition: item is in self.
        Raises: ValueError if item in not in self.
        Postcondition: item is removed from self."""
        pass

    @abstractmethod
    def insert(self, i, item):
        """Inserts the item at position i."""
        pass

    @abstractmethod
    def pop(self, i = None):
        """Precondition: 0 <= i < len(self).
        Removes and returns the item at position i.
        If i is None, i is given a default of len(self) - 1.
        Raises: IndexError."""
        return None

    @abstractmethod
    def __setitem__(self, i, item):
        """Precondition: 0 <= i < len(self)
        Replaces the item at position i with item.
        Raises: IndexError."""
        pass

    @abstractmethod
    def listIterator(self):
        """Returns a list iterator on self."""
        return None

class ListIteratorInterface(ABC):
    """Interface for all list iterator types."""

    @abstractmethod
    def first(self):
        """Returns the cursor to the beginning of the backing store."""
        pass

    @abstractmethod
    def hasNext(self):
        """Returns True if the iterator has a next item or False otherwise."""
        return False
 
    @abstractmethod
    def next(self):
        """Preconditions: hasNext returns True
        The list has not been modified except by this iterator's mutators.
        Returns the current item and advances the cursor to the next item.
        Postcondition: lastItemPos is now defined.
        Raises: ValueError if no next item.
        AttributeError if illegal mutation of backing store."""
        return None

    @abstractmethod
    def last(self):
        """Moves the cursor to the end of the backing store."""
        pass

    @abstractmethod
    def hasPrevious(self):
        """Returns True if the iterator has a previous item or False otherwise."""
        return False

    @abstractmethod
    def previous(self):
        """Preconditions: hasPrevious returns True
        The list has not been modified except by this iterator's mutators.
        Returns the current item and moves the cursor to the previous item.
        Postcondition: lastItemPos is now defined.
        Raises: ValueError if no next item.
        AttributeError if illegal mutation of backing store."""
        return None

    @abstractmethod
    def replace(self, item):
        """Preconditions: the current position is defined.
        The list has not been modified except by this iterator's mutators.
        Replaces the items at the current position with item.
        Raises: AttibuteError if position is not defined.
        AttributeError if illegal mutation of backing store."""
        pass
    
    @abstractmethod
    def insert(self, item):         
        """Preconditions:
        The list has not been modified except by this iterator's mutators.
        Adds item to the end if the current position is undefined, or
        inserts it at that position.
        Raises: AttributeError if illegal mutation of backing store."""
        pass
    
    @abstractmethod
    def remove(self):         
        """Preconditions: the current position is defined.
        The list has not been modified except by this iterator's mutators.
        Pops the item at the current position.
        Raises: AttibuteError if position is not defined.
        AttributeError if illegal mutation of backing store."""
        pass

