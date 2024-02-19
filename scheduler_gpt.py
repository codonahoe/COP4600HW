# Group 19 - Sydney Baldwin, Devon Lister, Talia Martin, Casey O'Donahoe

import sys
from collections import deque

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.status = "Waiting"  # Initially set status to "Waiting"
        self.selection_time = None
        self.completion_time = None

    def __str__(self):
        return f"Process {self.name}: Arrival={self.arrival}, Burst={self.burst}, Status={self.status}"

class Parameters:
    def __init__(self, processcount, runfor, use, quantum, processes):
        self.processcount = processcount
        self.runfor = runfor
        self.use = use
        self.quantum = quantum
        self.processes = processes

def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: File not found")
        return

    if len(lines) < 3:
        print("Error: Insufficient parameters")
        return

    processcount_line = lines[0].strip().split()
    runfor_line = lines[1].strip().split()
    use_line = lines[2].strip().split()

    if len(processcount_line) < 2 or processcount_line[0] != "processcount":
        print("Error: Missing parameter <processcount>")
        return
    if len(runfor_line) < 2 or runfor_line[0] != "runfor":
        print("Error: Missing parameter <runfor>")
        return
    if len(use_line) < 2 or use_line[0] != "use":
        print("Error: Missing parameter <use>")
        return

    processcount = int(processcount_line[1])
    runfor = int(runfor_line[1])
    use = use_line[1]

    if use not in ["fcfs", "sjf", "rr"]:
        print("Error: Invalid parameter <use>")
        return

    if use == "rr":
        if len(lines) < 4:
            print("Error: Missing quantum parameter when use is 'rr'")
            return
        quantum_line = lines[3].strip().split()
        if len(quantum_line) < 2 or quantum_line[0] != "quantum":
            print("Error: Missing quantum parameter when use is 'rr'")
            return
        quantum = int(quantum_line[1])
        index = 4
    else:
        quantum = None
        index = 3

    processes = []
    while index < len(lines):
        line = lines[index].strip().split()
        if line[0] == "end":
            break
        if len(line) < 7:
            print("Error: Invalid parameter <process>")
            return
        if line[0] != "process":
            print("Error: Missing parameter <process>")
            return
        if line[1] != "name":
            print("Error: Missing parameter <name>")
            return
        if line[3] != "arrival":
            print("Error: Missing parameter <arrival>")
            return
        if line[5] != "burst":
            print("Error: Missing parameter <burst>")
            return
        
        name = line[2]
        arrival = int(line[4])
        burst = int(line[6])
        processes.append(Process(name, arrival, burst))
        index += 1

    return Parameters(processcount, runfor, use, quantum, processes)

def calculate_times(arrival_time, burst_time, selection_time, completion_time):
    wait_time = completion_time - arrival_time - burst_time
    turnaround_time = completion_time - arrival_time
    response_time = selection_time - arrival_time

    return wait_time, turnaround_time, response_time

def fifo_scheduler(runfor, processes, processcount): # human edit - added processcount as a parameter for heading purposes
    output_filename = sys.argv[1].replace('.in', '.out')

    with open(output_filename, 'w') as output_file:
        current_time = 0
        # human edit - removed wait and response time lists after switching to calculating wait/response/turnaround times in separate function
        arrived_processes = deque()  # Queue to store arrived processes
        selected_process = None
        # human edit - added original burst list and index to keep track of correct burst values for calculating times
        original_burst = []
        index = 0
        for process in processes:
            original_burst.append(process.burst)

        output_file.write(f"{processcount} processes\n")
        output_file.write("Using First-Come First-Served\n")
        while current_time < runfor: # human edit - got rid of extra conditions leading to running past runfor
            # Check for arrived processes
            for process in processes:
                if process.arrival == current_time and process not in arrived_processes and process != selected_process:
                    arrived_processes.append(process)
                    output_file.write(f"Time {current_time} : {process.name} arrived\n")

            # Execute current process
            if selected_process:
                if selected_process.burst == 1:
                    output_file.write(f"Time {current_time} : {selected_process.name} finished\n")
                    selected_process.status = "Finished"
                    # human edit - update completion time
                    selected_process.completion_time = current_time
                    selected_process = None
                else:
                    selected_process.burst -= 1

            # Select next process if no process is currently running or the current process has finished
            if selected_process is None or selected_process.burst == 0:
                if arrived_processes:
                    selected_process = arrived_processes.popleft()
                    output_file.write(f"Time {current_time} : {selected_process.name} selected (burst {selected_process.burst})\n")
                    selected_process.status = "Selected"
                    selected_process.selection_time = current_time  # human edit - update selection time
                elif selected_process is None:
                    output_file.write(f"Time {current_time} : Idle\n")

            current_time += 1

        output_file.write(f"Finished at time {runfor}\n\n") # human edit - added a second newline for formatting purposes
        
        for process in processes:
            if process.status == "Finished":
                wait_time, turnaround_time, response_time = calculate_times(process.arrival, original_burst[index], process.selection_time, process.completion_time)
                output_file.write(f"{process.name} wait {wait_time} turnaround {turnaround_time} response {response_time}\n")
            else:
                output_file.write(f"{process.name} did not finish\n")
            index += 1 # human edit - increment index to traverse array of burst times

def sjf_scheduler(processcount, runfor, processes):
    output_filename = sys.argv[1].replace('.in', '.out')

    with open(output_filename, 'w') as output_file:
        output_file.write(f"{processcount} processes\n")
        output_file.write("Using preemptive Shortest Job First\n")
        
        current_time = 0
        # human edit - got rid of selection times/completion times lists, added index to traverse original_burst
        original_burst = [process.burst for process in processes]
        index = 0
        # human edit - added selections list to keep track of selections
        selections = []
        
        while current_time < runfor:
            shortest_burst = float('inf')
            shortest_process = None

            for i, process in enumerate(processes):
                if process.arrival <= current_time and process.burst < shortest_burst and process.burst > 0:
                    shortest_burst = process.burst
                    shortest_process = i

            # Check for process arrivals
            for process in processes:
                if process.arrival == current_time:
                    output_file.write(f"Time {current_time} : {process.name} arrived\n")

            # human edit - check for process completions
            for process in processes:
                if process.completion_time == current_time:
                    output_file.write(f"Time {current_time} : {process.completion_time} finished\n")

            if shortest_process is None:
                output_file.write(f"Time {current_time} : Idle\n")
                current_time += 1
                continue

            # human edit - fixed issue with certain selections not being written to file
            if selections == [] or shortest_process != selections[len(selections)-1]:
                selections.append(shortest_process)
                output_file.write(f"Time {current_time} : {processes[shortest_process].name} selected (burst {processes[shortest_process].burst})\n")
                processes[shortest_process].status = "Running"

            # human edit - update selection time
            if processes[shortest_process].selection_time == None:
                processes[shortest_process].selection_time = current_time

            processes[shortest_process].burst -= 1

            # human edit - fixed issue with incorrect completion times
            if processes[shortest_process].burst == 0:
                processes[shortest_process].completion_time = current_time+1
                processes[shortest_process].status = "Finished"

            current_time += 1

        output_file.write(f"Finished at time {runfor}\n\n") # human edit - added extra newline for formatting purposes

        for process in processes:
            if process.status == "Finished":
                wait_time, turnaround_time, response_time = calculate_times(process.arrival, original_burst[index], process.selection_time, process.completion_time)
                output_file.write(f"{process.name} wait {wait_time} turnaround {turnaround_time} response {response_time}\n")
            else:
                output_file.write(f"{process.name} did not finish\n")
            index += 1 # human edit - increment index to traverse array of burst times

def rr_scheduler(processcount, runfor, quantum, processes):
    output_filename = sys.argv[1].replace('.in', '.out')

    # Initialize lists
    original_burst = [process.burst for process in processes]
    # human edit - got rid of selection time, completion time, and process name lists

    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda x: x.arrival)

    # Create a queue to hold processes
    process_queue = deque()

    # Initialize quantum counter
    quantum_counter = quantum

    # Initialize currently running process
    running_process = None

    # human edit - added index for traversing original_burst
    i = 0

    with open(output_filename, 'w') as output_file:
        output_file.write(f"{processcount} processes\n")
        output_file.write("Using Round-Robin\n")
        output_file.write(f"Quantum {quantum}\n\n") # human edit - added extra newline for formatting

        current_time = 0
        index = 0

        # Main loop
        while current_time < runfor:
            # Check for arrived processes
            while index < len(sorted_processes) and sorted_processes[index].arrival == current_time:
                process_queue.append(sorted_processes[index])
                output_file.write(f"Time {current_time} : {sorted_processes[index].name} arrived\n")
                index += 1

            if running_process:
                running_process.burst -= 1
                if running_process.burst == 0:
                    output_file.write(f"Time {current_time} : {running_process.name} finished\n")
                    running_process.status = "Finished"
                    # human edit - completion time update
                    running_process.completion_time = current_time
                    quantum_counter = 0
                    # Check if there is a process waiting in the queue
                    if process_queue:
                        next_process = process_queue.popleft()
                        output_file.write(f"Time {current_time} : {next_process.name} selected (burst {next_process.burst})\n")
                        next_process.status = "Running"
                        # human edit - selection time update
                        if next_process.selection_time == None:
                            next_process.selection_time = current_time
                        running_process = next_process
                    else:
                        running_process = None

            # Check if quantum is reached
            if quantum_counter == quantum:
                # Check for processes in queue
                if process_queue:
                    next_process = process_queue.popleft()
                    output_file.write(f"Time {current_time} : {next_process.name} selected (burst {next_process.burst})\n")
                    next_process.status = "Running"
                    # human edit - selection time update
                    if next_process.selection_time == None:
                            next_process.selection_time = current_time
                    # Check if there is a currently running process
                    if running_process:
                        # Append the currently running process to the end of the queue
                        process_queue.append(running_process)
                    # Set next_process as the currently running process
                    running_process = next_process
                    # Reset quantum counter
                # If there is no process in the queue, continue running the currently running process
                else:
                    if running_process:
                        output_file.write(f"Time {current_time} : {running_process.name} selected (burst {running_process.burst})\n")
                        running_process.status = "Running"
                        # human edit - selection time update
                        if next_process.selection_time == None:
                            next_process.selection_time = current_time
                quantum_counter = 0 # human edit - moved quantum_counter edit out of nested if

            if not running_process:
                output_file.write(f"Time {current_time} : Idle\n")

            # Increment quantum counter
            quantum_counter += 1

            # Increment current time
            current_time += 1

        output_file.write(f"Finished at time {runfor}\n\n") # human edit - added extra newline for formatting

        for process in processes:
            if process.status == "Finished":
                wait_time, turnaround_time, response_time = calculate_times(process.arrival, original_burst[i], process.selection_time, process.completion_time)
                output_file.write(f"{process.name} wait {wait_time} turnaround {turnaround_time} response {response_time}\n")
            else:
                output_file.write(f"{process.name} did not finish\n")
            i += 1 # human edit - increment index to traverse array of burst times

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
    else:
        params = read_input_file(sys.argv[1])
        if params:
            # human edit - fixed unwanted reordering of parameters
            if params.use == "fcfs":
                fifo_scheduler(params.runfor, params.processes, params.processcount)
            elif params.use == "sjf":
                sjf_scheduler(params.processcount, params.runfor, params.processes)
            elif params.use == "rr":
                rr_scheduler(params.processcount, params.runfor, params.quantum, params.processes)
            else:
                print("Error: Invalid parameter <use>")
