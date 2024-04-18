"""
LinkedList implementing a list.
The LinkedListIterator ala Turing was also implemented to manipulate the list as a ribbon.
"""

__author__ = "Bertrand Blanc (Alan Turing)"
__all__ = ["LinkedList", "ListIterator"]

from abstractlist import AbstractList
from listinterface import ListInterface, ListIteratorInterface
from node import TwoWayNode

class LinkedList(AbstractList,ListInterface):
    # Constructor
    def __init__(self, sourceCollection = None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self.head = None
        self.tail = None
        AbstractList.__init__(self,sourceCollection)

    # Accessor methods

    def __iter__(self):
        """Supports iteration over a view of self."""
        probe = self.head
        while probe:
            yield probe.data
            probe = probe.next

    def __getitem__(self, i):
        """Precondition: 0 <= i < len(self)
        Returns the item at position i.
        Raises: IndexError."""
        if not (0 <= i < len(self)):
            raise IndexError(f'index {i} out of range [0,{len(self)}[')
        
        probe = self.head
        counter = 0
        while counter < i:
            counter += 1
            probe = probe.next
        return probe.data

    def __setitem__(self, i, item):
        """Precondition: 0 <= i < len(self)
        Replaces the item at position i with item.
        Raises: IndexError."""
        if not (0 <= i < len(self)):
            raise IndexError(f'index {i} out of range [0,{len(self)}[')
        
        probe = self.head
        counter = 0
        while counter < i:
            counter += 1
            probe = probe.next
        probe.data = item


    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert(self, i, item):
        """Inserts the item at position i."""
        if not (0 <= i <= len(self)):
            raise IndexError(f'index {i} out of range [0,{len(self)}[')
        
        if not self.head:
            self.head = TwoWayNode(item)
            self.tail = self.head
            self.size += 1
            return

        if i == len(self):
            self.tail.next = TwoWayNode(item,self.tail)
            self.tail = self.tail.next
            self.size += 1
            return
        
        if i == 0:
            self.head = TwoWayNode(item,None,self.head)
            self.head.next.previous = self.head
            self.size += 1
            return

        probe = self.head
        counter = 0
        while counter < i-2:
            counter += 1
            probe = probe.next
        probe.next = TwoWayNode(item,probe,probe.next.next)
        self.size += 1


    def pop(self, i = None):
        """Precondition: 0 <= i < len(self).
        Removes and returns the item at position i.
        If i is None, i is given a default of len(self) - 1.
        Raises: IndexError."""

        if i is None:
            if self.isEmpty():
                raise IndexError(f'the list is empty')

            if len(self) == 1:
                data = self.head.data
                self.clear()
                return data

            data = self.tail.data
            self.tail = self.tail.previous
            self.tail.next = None
            self.size -= 1
            return data
        

        if not (0 <= i < len(self)):
            raise IndexError(f'index {i} out of range [0,{len(self)}[')
        
        if i == 0:
            data = self.head.data
            self.head = self.head.next
            self.size -= 1
            return data

        probe = self.head
        counter = 0
        while counter < i-1:
            counter += 1
            probe = probe.next
        data = probe.next.data
        probe.next = probe.next.next
        self.size -= 1
        return data


    def listIterator(self):
        """Returns a list iterator on self."""
        return ListIterator(self)

class ListIterator(ListIteratorInterface):
    """Interface for all list iterator types."""

    def __init__(self, ll):
        self.ll = ll
        self.cursor = None

    def first(self):
        """Returns the cursor to the beginning of the backing store."""
        self.cursor = self.ll.head

    def hasNext(self):
        """Returns True if the iterator has a next item or False otherwise."""
        return self.cursor and self.cursor.next is not None
 
    def next(self):
        """Preconditions: hasNext returns True
        The list has not been modified except by this iterator's mutators.
        Returns the current item and advances the cursor to the next item.
        Postcondition: lastItemPos is now defined.
        Raises: ValueError if no next item.
        AttributeError if illegal mutation of backing store."""
        
        if not self.hasNext():
            raise ValueError('no next item')
        
        data = self.cursor.data
        self.cursor = self.cursor.next
        return data

    def last(self):
        """Moves the cursor to the end of the backing store."""
        self.cursor = self.ll.tail

    def hasPrevious(self):
        """Returns True if the iterator has a previous item or False otherwise."""
        return self.cursor and self.cursor.previous is not None

    def previous(self):
        """Preconditions: hasPrevious returns True
        The list has not been modified except by this iterator's mutators.
        Returns the current item and moves the cursor to the previous item.
        Postcondition: lastItemPos is now defined.
        Raises: ValueError if no next item.
        AttributeError if illegal mutation of backing store."""
        
        if not self.hasPrevious():
            raise ValueError('no previous item')
        data = self.cursor.data
        self.cursor = self.cursor.previous
        return data


    def replace(self, item):
        """Preconditions: the current position is defined.
        The list has not been modified except by this iterator's mutators.
        Replaces the items at the current position with item.
        Raises: AttibuteError if position is not defined.
        AttributeError if illegal mutation of backing store."""
        
        if not self.cursor:
            raise AttributeError('cursor not initialized')
        
        self.cursor.data = item
    
    def insert(self, item):         
        """Preconditions:
        The list has not been modified except by this iterator's mutators.
        Adds item to the end if the current position is undefined, or
        inserts it at that position.
        Raises: AttributeError if illegal mutation of backing store."""

        if not self.cursor:
            if self.ll.isEmpty():
                self.ll.insert(0,item)
            else:
                self.ll.append(item)
            return
        
        if self.cursor is self.ll.head:
            self.ll.insert(0,item)
            self.first()
            return
        
        node = TwoWayNode(item, self.cursor.previous, self.cursor)
        self.cursor.previous.next = node
        self.cursor.previous = node
        self.cursor = node

    
    def remove(self):         
        """Preconditions: the current position is defined.
        The list has not been modified except by this iterator's mutators.
        Pops the item at the current position.
        Raises: AttibuteError if position is not defined.
        AttributeError if illegal mutation of backing store."""
        
        if not self.cursor:
            raise AttributeError('undefined cursor')
        
        if self.cursor is self.ll.head:
            self.ll.pop(0)
            self.first()
            return

        if self.cursor.next is None:
            previous = self.cursor.previous
            previous.next = None
            self.cursor = previous
            self.ll.size -= 1
            return

        previous = self.cursor.previous
        previous.next = self.cursor.next
        self.cursor = previous.next
        self.ll.size -= 1


    def __str__(self):
        if self.ll.isEmpty():
            return []
        
        probe = self.ll.head
        buf = '['
        buf += '>' + str(probe.data) + '<' if probe is self.cursor else str(probe.data)
        probe = probe.next
        while probe:
            if probe is self.cursor:
                buf += ', >' + str(probe.data) + '<'
            else:
                buf += ', ' + str(probe.data)
            probe = probe.next
        buf += ']'
        return buf
        


