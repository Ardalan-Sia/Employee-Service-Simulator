import numpy as np
from utils import Task, Location, time_unit

transition_matrix = {
    'A': {
        Task.SET_UP_A_COMPLAINT: {
            Task.SET_UP_A_COMPLAINT: 0.9,
            Task.WRITING_A_CONTRACT: 0.1
        },
        Task.WRITING_A_CONTRACT: {
            Task.SET_UP_A_COMPLAINT: 0.2,
            Task.WRITING_A_CONTRACT: 0.8
        }
    },
    'B': {
        Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: {
            Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: 0.85,
            Task.FILING_A_REVIEW_REQUEST: 0.15
        },
        Task.FILING_A_REVIEW_REQUEST: {
            Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: 0.05,
            Task.FILING_A_REVIEW_REQUEST: 0.95
        }
    },
    'C': {
        Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: {
            Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: 0.8,
            Task.FILING_A_REVIEW_REQUEST: 0.1,
            Task.DOCUMENTS_CONFIRMATION : 0.1
        },
        Task.FILING_A_REVIEW_REQUEST: {
            Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: 0.15,
            Task.FILING_A_REVIEW_REQUEST: 0.75,
            Task.DOCUMENTS_CONFIRMATION : 0.1
        },
        Task.DOCUMENTS_CONFIRMATION : {
            Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: 0.05,
            Task.FILING_A_REVIEW_REQUEST: 0.05,
            Task.DOCUMENTS_CONFIRMATION : 0.9
        }
    }
}

change_intervals = {
    'A': 5 * 60 * time_unit(),
    'B': 7 * 60 * time_unit(),
    'C': 10 * 60 * time_unit()
}

class Employee:
    def __init__(self, type):
        self.type = type
        self.current_customer = None
        self.time_to_change = change_intervals[type]
        self.current_task = np.random.choice(list(transition_matrix[type].keys()))

    def assign_customer(self, customer):
        if self.current_customer:
            raise Exception("Employee already has a customer")
        if self.current_task != customer.service_type:
            raise Exception("Employee can't accept this type of customers at the time")
        
        self.current_customer = customer
        customer.change_location(Location.SERVICE)

    def change_state(self):
        self.time_to_change = change_intervals[self.type]
        matrix = transition_matrix[self.type][self.current_task]
        self.current_task = np.random.choice(list(matrix.keys()), p=list(matrix.values()))

    def tick(self):
        self.time_to_change -= 1
        if self.time_to_change == 0:
            self.change_state()

        customer = None
        if self.current_customer:
            self.current_customer.tick()
            if self.current_customer.is_finished():
                customer = self.current_customer = None

        if self.current_customer and self.current_task != self.current_customer.service_type:
            customer = self.current_customer
            self.current_customer = None

        return customer