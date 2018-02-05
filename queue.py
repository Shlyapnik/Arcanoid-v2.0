class Queue:
    def __init__(self):
        self.size = 0

        self.first_stack = list()
        self.second_stack = list()


    def __iter__(self):
        #return self.QueueIterator(self)
        self.second_stack.reverse()
            
        for item in self.second_stack:
            yield item
        
        self.second_stack.reverse()

        for item in self.first_stack:
            yield item

        raise StopIteration


    def push(self, value):
        self.size += 1

        self.first_stack.append(value)

    def pop(self):
        if self.size == 0:
            # Neew throw exception
            pass

        self.size -= 1

        if len(self.second_stack) == 0:
            for i in range(len(self.first_stack)):
                self.second_stack.append(self.first_stack.pop())
        
        return self.second_stack.pop()

    def tail(self):
        if self.size == 0:
            raise RuntimeError
        
        if len(self.second_stack) != 0:
            return self.second_stack[-1]
        else:
            return self.first_stack[0]

    def front(self):
        if self.size == 0:
            raise RuntimeError
        
        if len(self.first_stack) != 0:
            return self.first_stack[-1]
        else:
            return self.second_stack[0]
    