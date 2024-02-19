# Group 19 - Sydney Baldwin, Devon Lister, Talia Martin, Casey O'Donahoe

import sys
from collections import deque

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.status = "Waiting"  # Initially set status to "Waiting"

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

def fifo_scheduler(runfor, processes, processcount): #human edit - added processcount as a parameter for heading purposes
    output_filename = sys.argv[1].replace('.in', '.out')

    with open(output_filename, 'w') as output_file:
        current_time = 0
        # human edit - removed wait and response time lists after switching to calculating wait/response/turnaround times in separate function
        arrived_processes = deque()  # Queue to store arrived processes
        selected_process = None
        finished_processes = []
        # human edit - added selection, completion time, sorted order, original burst value lists, and index tracker for future calculations
        selection_times = []
        completion_times = []
        sorted_order = []
        original_burst = []
        index = 0
        for process in processes:
            sorted_order.append(process.name)
            original_burst.append(process.burst)

        output_file.write(f"{processcount} processes\n")
        output_file.write("Using First-Come First-Served\n")
        while current_time < runfor: # human edit - got rid of extra conditions leading to error
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
                    finished_processes.append(selected_process)
                    # human edit - add to completion times list
                    completion_times.append((selected_process.name, current_time))
                    selected_process = None
                else:
                    selected_process.burst -= 1

            # Select next process if no process is currently running or the current process has finished
            if selected_process is None or selected_process.burst == 0:
                if arrived_processes:
                    selected_process = arrived_processes.popleft()
                    output_file.write(f"Time {current_time} : {selected_process.name} selected (burst {selected_process.burst})\n")
                    selected_process.status = "Running"
                    # human edit - add to selection times list
                    selection_times.append((selected_process.name, current_time))
                elif selected_process is None:
                    output_file.write(f"Time {current_time} : Idle\n")

            current_time += 1

        output_file.write(f"Finished at time {runfor}\n\n") # human edit - added a second newline for formatting purposes

        # human edit - re-sort selection and completion times into order that will match corresponding arrival and burst times
        selection_times = [tuple for x in sorted_order for tuple in selection_times if tuple[0] == x]
        completion_times = [tuple for x in sorted_order for tuple in completion_times if tuple[0] == x]
        
        for process in processes:
            if process not in finished_processes:
                output_file.write(f"{process.name} did not finish\n")
                index += 1
            # human edit - used a separate, reusable function to calculate wait, turnaround and response times
            else:
                wait_time, turnaround_time, response_time = calculate_times(process.arrival, original_burst[index], selection_times[index][1], completion_times[index][1])
                output_file.write(f"{process.name} wait {wait_time} turnaround {turnaround_time} response {response_time} \n")
                index += 1

def sjf_scheduler(processcount, runfor, processes):
    output_filename = sys.argv[1].replace('.in', '.out')

    # Initialize sorted_order list to keep track of original order of processes
    sorted_order = [process.name for process in processes]

    with open(output_filename, 'w') as output_file:
        output_file.write(f"{processcount} processes\n")
        output_file.write("Using preemptive Shortest Job First\n")
        
        current_time = 0
        selection_times = []
        completion_times = []
        original_burst = [process.burst for process in processes]
        # human edit - added selections list to keep track of all selections
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
            for x in range (len(completion_times)):
                if completion_times[x][1] == current_time:
                    output_file.write(f"Time {current_time} : {processes[completion_times[x][0]].name} finished\n")
                    processes[shortest_process].status = "Finished" # human edit - added status update

            if shortest_process is None:
                output_file.write(f"Time {current_time} : Idle\n")
                current_time += 1
                continue

            # human edit - fixed issue with certain selections not being written to file
            if selections == [] or shortest_process != selections[len(selections)-1]:
                selections.append(shortest_process)
                output_file.write(f"Time {current_time} : {processes[shortest_process].name} selected (burst {processes[shortest_process].burst})\n")
                processes[shortest_process].status = "Running" # human edit - added status update
            
            if shortest_process not in [x[0] for x in selection_times]:
                selection_times.append((shortest_process, current_time))

            processes[shortest_process].burst -= 1

            # human edit - fixed issue with incorrect completion times
            if processes[shortest_process].burst == 0 and shortest_process not in [x[0] for x in completion_times]:
                completion_times.append((shortest_process, current_time+1))

            current_time += 1

        output_file.write(f"Finished at time {runfor}\n\n") # human edit - added extra newline for formatting purposes

        # Sort selection_times and completion_times according to sorted_order
        selection_times.sort(key=lambda x: sorted_order.index(processes[x[0]].name))
        completion_times.sort(key=lambda x: sorted_order.index(processes[x[0]].name))

        for i, process in enumerate(processes):
            if i not in [x[0] for x in completion_times]:
                output_file.write(f"{process.name} did not finish\n")
            else:
                # human edit - fixed selection_times index
                wait_time, turnaround_time, response_time = calculate_times(process.arrival, original_burst[i], selection_times[i][1], completion_times[i][1])
                output_file.write(f"{process.name} wait {wait_time} turnaround {turnaround_time} response {response_time}\n")

def rr_scheduler(processcount, runfor, quantum, processes):
    output_filename = sys.argv[1].replace('.in', '.out')

    # Initialize lists
    original_burst = [process.burst for process in processes]
    selection_times = []
    completion_times = []
    process_names = [process.name for process in processes]

    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda x: x.arrival)

    # Create a queue to hold processes
    process_queue = deque()

    # Initialize quantum counter
    quantum_counter = quantum

    # Initialize currently running process
    running_process = None

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
                    running_process.status = "Finished" # human edit - added status update
                    completion_times.append((running_process.name, current_time))
                    quantum_counter = 0
                    # Check if there is a process waiting in the queue
                    if process_queue:
                        next_process = process_queue.popleft()
                        output_file.write(f"Time {current_time} : {next_process.name} selected (burst {next_process.burst})\n")
                        next_process.status = "Running"
                        # Add to selection times if not already selected
                        if next_process.name not in [x[0] for x in selection_times]:
                            selection_times.append((next_process.name, current_time))
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
                    # Add to selection times if not already selected
                    if next_process.name not in [x[0] for x in selection_times]:
                        selection_times.append((next_process.name, current_time))
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
                        # human edit - add this selection to selection_times if applicable
                        if running_process.name not in [x[0] for x in selection_times]:
                            selection_times.append((running_process.name, current_time))
                quantum_counter = 0 # human edit - moved quantum_counter edit out of nested if

            if not running_process:
                output_file.write(f"Time {current_time} : Idle\n")

            # Increment quantum counter
            quantum_counter += 1

            # Increment current time
            current_time += 1

        output_file.write(f"Finished at time {runfor}\n\n") # human edit - added extra newline for formatting

        # Sort selection_times and completion_times according to process_names order
        selection_times.sort(key=lambda x: process_names.index(x[0]))
        completion_times.sort(key=lambda x: process_names.index(x[0]))

        # Check if any process did not finish
        for process in process_names:
            if process not in [x[0] for x in completion_times]:
                output_file.write(f"{process} did not finish\n")

        # Calculate wait, turnaround, and response times
        for i, process in enumerate(processes):
            if process.name in [x[0] for x in completion_times]:
                wait_time, turnaround_time, response_time = calculate_times(process.arrival, original_burst[i], selection_times[i][1], completion_times[i][1])
                output_file.write(f"{process.name} wait {wait_time} turnaround {turnaround_time} response {response_time}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
    else:
        params = read_input_file(sys.argv[1])
        if params:
            # human edit - fixed ChatGPT's reordering of parameters
            if params.use == "fcfs":
                fifo_scheduler(params.runfor, params.processes, params.processcount)
            elif params.use == "sjf":
                sjf_scheduler(params.processcount, params.runfor, params.processes)
            elif params.use == "rr":
                rr_scheduler(params.processcount, params.runfor, params.quantum, params.processes)
            else:
                print("Error: Invalid parameter <use>")
