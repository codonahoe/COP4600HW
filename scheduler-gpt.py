class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.wait_time = None

def FIFO_scheduler(processes, runfor):
    current_time = 0
    events = []
    while current_time <= runfor:
        event = None
        for process in processes:
            if process.arrival == current_time:
                event = "Arrived: " + process.name
                process.start_time = current_time
                process.response_time = current_time - process.arrival
                processes.remove(process)
                break
        if not event:
            event = "Idle"
        events.append((current_time, event))
        current_time += 1
    return events

def preemptive_SJF_scheduler(processes, runfor):
    current_time = 0
    events = []
    while current_time <= runfor:
        event = None
        for process in processes:
            if process.arrival == current_time:
                event = "Arrived: " + process.name
                process.start_time = current_time
                process.response_time = current_time - process.arrival
                processes.remove(process)
                break
        if not event:
            event = "Idle"
        events.append((current_time, event))
        current_time += 1
    return events

def round_robin_scheduler(processes, quantum, runfor):
    current_time = 0
    events = []
    while current_time <= runfor:
        event = None
        for process in processes:
            if process.arrival == current_time:
                event = "Arrived: " + process.name
                process.start_time = current_time
                process.response_time = current_time - process.arrival
                processes.remove(process)
                break
        if not event:
            event = "Idle"
        events.append((current_time, event))
        current_time += 1
    return events

def write_results_to_file(filename,processcount, use, quantum, events, unfinished_processes):
    with open(filename, "w") as file:
        file.write("Number of processes: {}\n".format(processcount))
        file.write("Algorithm used: {}\n".format(use))
        if use == 'rr':
            file.write("Quantum: {}\n".format(quantum))
        file.write("Time Events:\n")
        for event in events:
            file.write("Time: {}, Event: {}\n".format(event[0], event[1]))
        file.write("Finished at: {}\n".format(events[-1][0]))
        if unfinished_processes:
            file.write("Unfinished processes: {}\n".format(", ".join(unfinished_processes)))
        else:
            file.write("All processes completed within runtime.\n")

def read_processes_from_file(filename):
    processes = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        processcount = None
        runfor = None
        use = None
        quantum = None
        for line in lines:
            parts = line.strip().split()
            if parts[0] == 'processcount':
                processcount = int(parts[1])
            elif parts[0] == 'runfor':
                runfor = int(parts[1])
            elif parts[0] == 'use':
                use = parts[1]
            elif parts[0] == 'quantum':
                quantum = int(parts[1])
            elif parts[0] == 'process':
                name, arrival, burst = parts[2], int(parts[4]), int(parts[6])
                processes.append(Process(name, arrival, burst))
            elif parts[0] == 'end':
                break
    return processcount, runfor, use, quantum, processes

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file[:-2] + "out"
    processcount, runfor, use, quantum, processes = read_processes_from_file(input_file)

    if use == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)

    if any(param is None for param in [processcount, runfor, use]):
        print("Error: Missing parameter(s).")
        sys.exit(1)

    events = []
    if use == 'fcfs':
        print("\nFIFO scheduling:")
        events = FIFO_scheduler(processes, runfor)
    elif use == 'sjf':
        print("\nPreemptive SJF scheduling:")
        events = preemptive_SJF_scheduler(processes, runfor)
    elif use == 'rr':
        print("\nRound Robin scheduling:")
        events = round_robin_scheduler(processes, quantum, runfor)
    else:
        print("Invalid algorithm specified.")
        sys.exit(1)

    unfinished_processes = [process.name for process in processes if process.burst > 0]

    write_results_to_file(output_file, processcount, use, quantum, events, unfinished_processes)

    print("Results written to input.out file.")
