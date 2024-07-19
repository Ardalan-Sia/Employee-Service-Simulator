# Project overview
This project is a part of the Computer Simulation course at Sharif University of Technology, under the supervision of Professor Bardia Safaie. The aim of this simulation is to model a company's service system using Python, focusing on interactions between employees and customers. It categorizes employees into three distinct groups A, B, and C each with specific task-switching capabilities. The primary objective is to analyze and evaluate service efficiency through various performance metrics.

## Features
- **Employee Categories**:
  - **Group A**: Group A: Handles complaints and contracts, switches tasks every 5 minutes based on a Markov transition matrix.
  - **Group B**: Group B: Handles undergraduate applications and review requests, switches tasks every 7 minutes based on a Markov transition matrix.
  - **Group C**: Group C: Handles applications, review requests, and document confirmations, switches tasks every 10 minutes based on a Markov transition matrix.
- **Queue Management**: Implements FIFO, SPT, and SIRO queuing policies.
- **Performance Metrics**: Analyzes service time, waiting time, and customer counts.

## Project Structure
- **Customer**: Manages customer details and transitions.
- **Employee**: Handles task assignments and state changes based on a transition matrix.
- **Queue**: Manages customer queues based on policies.
- **Scheduler**: Manages multiple queues for different tasks.
- **System**: Integrates employees and queues, managing overall simulation.

## Getting Started

### Prerequisites
- Python 3.x
- Required libraries: Numpy, Matplotlib

### Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Ardalan-Sia/Employee_Service_Simulator.git
   ```
2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Simulation
1. **Run the Simulation**:
   ```sh
   python main.py
   ```

## Usage
- **Simulation Configuration**:
  - Enter the number of employees for each category.
  - Enter the total time interval for the simulation.
- **Analysis**:
  - Visualizes interarrival times, service times, total system times, queue times, and number of customers in the system and queue.

## Example
```python
from system import System
from customer import Customer
from utils import Task, Location

system = System(num_employees=5)
customer = Customer(arrival_time=0, service_type=Task.WRITING_A_CONTRACT, time_needs=300)
system.add_customer(customer)

for _ in range(1000):
    system.tick()

# Analyze and visualize results
analyse_result()
```

