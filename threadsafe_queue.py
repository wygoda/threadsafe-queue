#! /usr/bin/python3
from threading import Lock, current_thread

class Threadsafe_queue:
    class Node:
        def __init__(self, data, next_node):
            self.data = data
            self.next_node = next_node

    def __init__(self):
        self.head = self.Node(None, None)
        self.tail = self.head
        self.head_lock = Lock()
        self.tail_lock = Lock()

    def try_pop(self):
        with self.head_lock:
            with self.tail_lock:
                if (self.head == self.tail): #EMPTY QUEUE
                    return
            old_head = self.head
            self.head = old_head.next_node
            print("{}, pop: {}".format(current_thread().name, old_head.data)) #this line is here just for tests
            return old_head.data

    def push(self, new_data):
        new_tail = self.Node(None, None)
        with self.tail_lock:
            self.tail.data = new_data
            self.tail.next_node = new_tail
            self.tail = new_tail
            print("{}, push: {}".format(current_thread().name, new_data)) #this line is here just for tests

    def __str__(self):
        result = []
        with self.head_lock:
            current = self.head
            while current.next_node is not None:
                result = [str(current.data)] + result
                current = current.next_node
        if result == []:
            return "Empty queue"
        return ", ".join(result)
