import numpy as np
from system import System
from customer import Customer
from utils import Task, Location, time_unit
import matplotlib.pyplot as plt


mean_time_needs = {
    Task.DOCUMENTS_CONFIRMATION: 10 * 60 * time_unit(),
    Task.FILING_A_REVIEW_REQUEST: 10 * 60 * time_unit(),
    Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: 5 * 60 * time_unit(),
    Task.SET_UP_A_COMPLAINT: 25 * 60 * time_unit(),
    Task.WRITING_A_CONTRACT: 30 * 60 * time_unit()
}
tasks_distribution = {
    Task.DOCUMENTS_CONFIRMATION: ['gamma', 60 * 60 * time_unit(), 2, 1],
    Task.FILING_A_REVIEW_REQUEST: ['normal', 60 * time_unit(), 15, 36],
    Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: ['exponential', 60 * time_unit(), 1 / 0.06],
    Task.SET_UP_A_COMPLAINT: ['exponential', 60 * 60 * time_unit(), 1 / 0.5],
    Task.WRITING_A_CONTRACT: ['normal', 60 * time_unit(), 40, 36]
}
total_time_interval = 0
customers = []

def positive_rng(method, args):
    if method == 'normal':
        x = np.random.normal(args[0], args[1]) # Mu, Sigma
        return x if x > 0 else positive_rng(method, args)

    if method == 'gamma':
        x = np.random.gamma(args[0], args[1]) # Betha, Theta
        return x if x > 0 else positive_rng(method, args)
    
    return np.random.exponential(args[0]) # Mu = 1 / Lambda

def main():
    global total_time_interval
    num_employees = int(input('Enter number of employees for each category: '))
    total_time_interval = int(input('Enter total time interval of simulation (per minute): ')) * 60 * time_unit()
    
    system = System(num_employees)
    next_customers = {
        Task.DOCUMENTS_CONFIRMATION: None,
        Task.FILING_A_REVIEW_REQUEST: None,
        Task.REGISTRATION_OF_UNDERGRADUATE_APPLICATION: None,
        Task.SET_UP_A_COMPLAINT: None,
        Task.WRITING_A_CONTRACT: None
    }

    for time in range(1, total_time_interval + 1):
        system.tick()
        for task_type, next_customer in next_customers.items():
            if next_customer and next_customer.arrival_time == time:
                customers.append(next_customer)
                system.add_customer(next_customer)
                next_customers[task_type] = None
        for task_type in next_customers.keys():
            if next_customers[task_type] == None:
                arrival_time = time + round(positive_rng(tasks_distribution[task_type][0], tasks_distribution[task_type][2:]) * tasks_distribution[task_type][1])
                time_needs = round(positive_rng('exponential', [mean_time_needs[task_type]]))
                customer = Customer(arrival_time, task_type, time_needs)
                next_customers[task_type] = customer
        if time % (60 * 60 * time_unit()) == 0:
            print('Processing -', time // (60 * 60 * time_unit()), 'hours passed')

def analyse_result():
    plot_for_interariival_times()
    plot_for_service_times()
    plot_for_total_times()
    plot_for_queue_times()
    plot_for_num_customers()
    plot_for_num_customers_in_queue()

    print(f"Average of L(t) = {sum([customer.get_total_time_in_system() for customer in customers])/total_time_interval:.3f}")
    print(f"Average of LQ(t) = {sum([customer.get_total_time(Location.QUEUE) for customer in customers])/total_time_interval:.3f}")
    print(f"Average of W(t) = {sum([customer.get_total_time_in_system() for customer in customers])/len(customers)/(time_unit()*60):.3f}")
    print(f"Average of WQ(t) = {sum([customer.get_total_time(Location.QUEUE) for customer in customers])/len(customers)/(time_unit()*60):.3f}")

def plot_for_interariival_times():
    interarrival_times = [(customers[i].arrival_time - customers[i - 1].arrival_time)/(time_unit()*60) for i in range(1, len(customers))]
    event_numbers = list(range(1, len(interarrival_times) + 1))
    plt.plot(event_numbers, interarrival_times)  
    plt.title("Interarrival Times of The Simulation")
    plt.xlabel("Customers")
    plt.ylabel("Interarrival Time (minutes)")
    plt.show()

def plot_for_service_times():
    service_times = [customer.get_total_time(Location.SERVICE)/(time_unit()*60) for customer in customers]
    event_numbers = list(range(1, len(service_times) + 1))
    plt.plot(event_numbers, service_times)  
    plt.title("Service Times of The Simulation")
    plt.xlabel("Customers")
    plt.ylabel("Service Time (minutes)")
    plt.show()

def plot_for_total_times():
    total_times = [customer.get_total_time_in_system()/(time_unit()*60) for customer in customers]
    event_numbers = list(range(1, len(total_times) + 1))
    plt.plot(event_numbers, total_times)  
    plt.title("Total System Times of The Simulation")
    plt.xlabel("Customers")
    plt.ylabel("Total Time in System (minutes)")
    plt.show()  

def plot_for_queue_times():
    queue_times = [customer.get_total_time(Location.QUEUE)/(time_unit()*60) for customer in customers]
    event_numbers = list(range(1, len(queue_times) + 1))
    plt.plot(event_numbers, queue_times)  
    plt.title("Queue Times of The Simulation")
    plt.xlabel("Customers")
    plt.ylabel("Queue Time (minutes)")
    plt.show()     

def plot_for_num_customers():
    arrival_times = [customer.arrival_time for customer in customers]
    total_times = [customer.get_total_time_in_system() for customer in customers]

    departure_times = [arrival_times[i] + total_times[i] for i in range(len(arrival_times))]
    events = sorted([(t, 1) for t in arrival_times] + [(t, -1) for t in departure_times])
    customer_count = 0
    times, counts = [], []
    for time, change in events:
        time /= time_unit() * 60
        customer_count += change
        if len(times) and times[-1] == times:
            counts[-1] = customer_count
        else:
            if len(times):
                for i in (times[-1], time):
                    times.append(i)
                    counts.append(counts[-1])
            times.append(time)
            counts.append(customer_count)
    plt.plot(times, counts)
    plt.title("Number of Customers in the System Over Time")
    plt.xlabel("Time")
    plt.ylabel("Number of Customers")

    plt.show()

def plot_for_num_customers_in_queue():
    arrival_times = [customer.arrival_time for customer in customers]
    queue_times = [customer.get_in_location_intervals(Location.QUEUE) for customer in customers]
    service_times = [customer.get_in_location_intervals(Location.SERVICE) for customer in customers]

    start_times, end_times = [], []
    for index in range(len(customers)):
        queue_time = queue_times[index]
        service_time = service_times[index]

        current_time = arrival_times[index]
        for i in range(len(queue_time)):
            start_times.append(current_time)
            current_time += queue_time[i]
            end_times.append(current_time)
            if i < len(service_time):
                current_time += service_time[i]

    events = sorted([(t, 1) for t in start_times] + [(t, -1) for t in end_times])
    customer_count = 0
    times, counts = [], []
    for time, change in events:
        time /= time_unit() * 60
        customer_count += change
        if len(times) and times[-1] == times:
            counts[-1] = customer_count
        else:
            if len(times):
                for i in (times[-1], time):
                    times.append(i)
                    counts.append(counts[-1])
            times.append(time)
            counts.append(customer_count)
    plt.plot(times, counts)
    plt.title("Number of Customers in the System Queue Over Time")
    plt.xlabel("Time")
    plt.ylabel("Number of Customers")

    plt.show()
    
if __name__ == "__main__":
    main()
    analyse_result()