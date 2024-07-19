from utils import Location

class Customer:
    def __init__(self, arrival_time, service_type, time_needs):
        self.arrival_time = arrival_time
        self.service_type = service_type
        self.time_needs = time_needs
        
        self.current_location = Location.NEW
        self.total_time_in_location = {
            Location.NEW: 0,
            Location.QUEUE: 0,
            Location.SERVICE: 0,
            Location.FINISHED: 0
        }
        self.in_location_intervals = {
            Location.NEW: [],
            Location.QUEUE: [],
            Location.SERVICE: [],
            Location.FINISHED: []
        }
        
    def change_location(self, location):
        if self.is_finished():
            raise Exception("Customer already finished")
        if self.current_location == location:
            return

        self.current_location = location
        self.in_location_intervals[location].append(0)

    def is_finished(self):
        return self.current_location == Location.FINISHED

    def tick(self):
        if self.is_finished():
            raise Exception("Customer already finished")
        
        self.in_location_intervals[self.current_location][-1] += 1
        self.total_time_in_location[self.current_location] += 1

        if self.current_location == Location.SERVICE:
            self.time_needs -= 1
            if self.time_needs == 0:
                self.change_location(Location.FINISHED)

    def get_total_time(self, location):
        return self.total_time_in_location[location]

    def get_total_time_in_system(self):
        return sum(self.total_time_in_location.values())
    
    def get_in_location_intervals(self, location):
        return self.in_location_intervals[location]