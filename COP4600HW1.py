class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.end_time = None
        self.status = "pending"  # Status can be "pending", "running", or "completed"
        self.response_time = 0
        self.waiting_time = 0

def fifo_scheduler(processes):
    current_time = 0
    for process in processes:
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        process.status = "running"
        process.start_time = current_time
        current_time += process.burst_time
        process.end_time = current_time
        process.status = "completed"

def sjf_scheduler(processes):
    current_time = 0
    while processes:
        shortest_process = min(processes, key=lambda x: x.remaining_time)
        if shortest_process.arrival_time > current_time:
            current_time = shortest_process.arrival_time
        shortest_process.status = "running"
        shortest_process.start_time = current_time
        current_time += shortest_process.remaining_time
        shortest_process.end_time = current_time
        shortest_process.status = "completed"
        processes.remove(shortest_process)

def round_robin_scheduler(processes, quantum):
    current_time = 0
    while processes:
        # Track whether any process has been scheduled in this iteration
        scheduled = False
        for process in processes:
            if process.arrival_time <= current_time and process.status != "completed":
                process.status = "running"
                process.start_time = current_time
                # If the process has remaining time greater than quantum
                if process.remaining_time > quantum:
                    current_time += quantum
                    process.remaining_time -= quantum
                else:
                    # If the process finishes within this quantum
                    current_time += process.remaining_time
                    process.remaining_time = 0
                # Update the end time and status of the process
                process.end_time = current_time
                process.status = "completed"
                # Set scheduled flag to indicate a process was scheduled
                scheduled = True
        # If no process was scheduled in this iteration, move time forward
        if not scheduled:
            current_time += 1

def calculate_metrics(processes):
    for process in processes:
        process.waiting_time = process.end_time - process.arrival_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time

def print_output(processes, algorithm, quantum=None):
    print(len(processes), "processes")
    print("Using", algorithm)
    if algorithm == "rr":
        print("Quantum:", quantum)
    current_time = 0
    for process in processes:
        if process.start_time is None:
            print("Time", current_time, ":", process.name, "arrived")
            process.start_time = current_time
        else:
            print("Time", current_time, ":", process.name, "selected (burst", process.burst_time, ")")
        current_time = process.end_time
        print("Time", current_time, ":", process.name, "finished")
    print("Finished at time", current_time)
    for process in processes:
        print(process.name, "wait", process.waiting_time, "turnaround", process.end_time - process.arrival_time, "response", process.response_time)

def read_input(filename):
    processes = []
    algorithm = None
    quantum = None
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if parts[0] == "process":
                name = parts[2]
                arrival_time = int(parts[4])
                burst_time = int(parts[6])
                processes.append(Process(name, arrival_time, burst_time))
            elif parts[0] == "use":
                algorithm = parts[1]
            elif parts[0] == "quantum":
                quantum = int(parts[1])
    return processes, algorithm, quantum

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        return
    
    input_filename = sys.argv[1]
    output_filename = input_filename.replace(".in", ".out")

    try:
        processes, algorithm, quantum = read_input(input_filename)
    except Exception as e:
        print("Error:", str(e))
        return
    if algorithm == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        return

    # Call the appropriate scheduler function based on the selected algorithm
    if algorithm == 'fcfs':
        fifo_scheduler(processes)
    elif algorithm == 'sjf':
        sjf_scheduler(processes)
    elif algorithm == 'rr':
        round_robin_scheduler(processes, quantum)

    # Calculate metrics for the scheduled processes
    calculate_metrics(processes)

    # Print the scheduling results and metrics
    print_output(processes, algorithm, quantum)

    # Write the output to the output file
    with open(output_filename, 'w') as f:
        f.write(str(len(processes)) + " processes\n")
        f.write("Using " + algorithm + "\n")
        if algorithm == 'rr':
            f.write("Quantum: " + str(quantum) + "\n")
        current_time = 0
        for process in processes:
            if process.start_time is None:
                f.write("Time " + str(current_time) + " : " + process.name + " arrived\n")
                process.start_time = current_time
            else:
                f.write("Time " + str(current_time) + " : " + process.name + " selected (burst " + str(process.burst_time) + ")\n")
            current_time = process.end_time
            f.write("Time " + str(current_time) + " : " + process.name + " finished\n")
        f.write("Finished at time " + str(current_time) + "\n")
        for process in processes:
            f.write(process.name + " wait " + str(process.waiting_time) + " turnaround " + str(process.end_time - process.arrival_time) + " response " + str(process.response_time) + "\n")

main()