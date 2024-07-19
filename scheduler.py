from queue import Queue
from utils import Task, QueueingPolicy

class Scheduler:
    def __init__(self):
        self.queues = {
            Task.WRITING_A_CONTRACT: Queue(QueueingPolicy.SPT),
            Task.SET_UP_A_COMPLAINT: Queue(QueueingPolicy.FIFO),
            Task.DOCUMENTS_CONFIRMATION: Queue(QueueingPolicy.FIFO),
            Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: Queue(QueueingPolicy.SPT),
            Task.FILING_A_REVIEW_REQUEST: Queue(QueueingPolicy.SIRO)
        }

    def push(self, customer):
        self.queues[customer.service_type].push(customer)

    def pop(self, service_type):
        return self.queues[service_type].pop()
    
    def tick(self):
        for queue in self.queues.values():
            queue.tick()