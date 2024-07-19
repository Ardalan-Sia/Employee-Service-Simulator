import numpy as np
from utils import QueueingPolicy

class Queue:
    def __init__(self, method):
        self.queue = []
        self.method = method

    def push(self, customer):
        self.queue.append(customer)

    def pop(self):
        if len(self.queue) == 0:
            return None
        
        if self.method == QueueingPolicy.SPT:
            best_index = None
            for index, customer in enumerate(self.queue):
                if best_index == None or customer.time_needs < self.queue[best_index].time_needs:
                    best_index = index
            return self.queue.pop(best_index)

        if self.method == QueueingPolicy.SIRO:
            best_index = np.random.randint(len(self.queue))
            return self.queue.pop(best_index)
        
        return self.queue.pop(0)
    
    def tick(self):
        for customer in self.queue:
            customer.tick()