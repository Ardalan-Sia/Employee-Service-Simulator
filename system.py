from scheduler import Scheduler
from employee import Employee
from utils import Location

class System:
    def __init__(self, num_employees):
        self.employees = {}
        self.queue = Scheduler()
        for employee_type in ['A', 'B', 'C']:
            self.employees[employee_type] = [Employee(employee_type) for _ in range(num_employees)]

    def add_customer(self, customer):
        self.queue.push(customer)
        customer.change_location(Location.QUEUE)
        self.check_employees()

    def tick(self):
        self.queue.tick()
        for employees in self.employees.values():
            for employee in employees:
                rejected_customer = employee.tick()
                if rejected_customer:
                    self.add_customer(rejected_customer)
        self.check_employees()

    def check_employees(self):
        for employees in self.employees.values():
            for employee in employees:
                if employee.current_customer == None:
                    customer = self.queue.pop(employee.current_task)
                    if customer:
                        employee.assign_customer(customer)