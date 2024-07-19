from enum import Enum

class Task(Enum):
    WRITING_A_CONTRACT = 'Writing a Contract'
    SET_UP_A_COMPLAINT = 'Set up a Complaint'
    DOCUMENTS_CONFIRMATION = 'Documents Confirmation'
    REGISTRATION_OF_UNDERGRADUATE_APPLICATION = 'Registration of Undergraduate Application'
    FILING_A_REVIEW_REQUEST = 'Filing a Review Request'

class QueueingPolicy(Enum):
    FIFO = 'First-In-First-Out'
    SPT = 'Shortest-Proccesing-Time'
    SIRO = 'Select-In-Random-Order'

class Location(Enum):
    NEW = 'New'
    QUEUE = 'Queue'
    SERVICE = 'Service'
    FINISHED = 'Finished'

def time_unit():
    return 10 ** 1