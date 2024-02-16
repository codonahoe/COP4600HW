import sys
from collections import deque

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst

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
        while current_time < runfor or selected_process is not None or arrived_processes:
            # Check for arrived processes
            for process in processes:
                if process.arrival == current_time and process not in arrived_processes and process != selected_process:
                    arrived_processes.append(process)
                    output_file.write(f"Time {current_time} : {process.name} arrived\n")

            # Execute current process
            if selected_process:
                if selected_process.burst == 1:
                    output_file.write(f"Time {current_time} : {selected_process.name} finished\n")
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
    else:
        params = read_input_file(sys.argv[1])
        if params:
            fifo_scheduler(params.runfor, params.processes, params.processcount) #human edit - added processcount as a parameter