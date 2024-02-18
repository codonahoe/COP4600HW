class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_time = burst
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.wait_time = None

def FIFO_scheduler(processes, runfor):
    current_time = 0
    events = []
    processesCopy = processes.copy()
    while current_time < runfor:
        event = None
        for process in processesCopy:
            if process.arrival == current_time:
                event = process.name + " arrived"
                events.append((current_time, event))
                event = process.name + " selected"
                events.append((current_time, event))
                process.start_time = current_time
                process.response_time = current_time - process.arrival
                process.wait_time = process.start_time - process.arrival
                event = process.name + " finished" 
                finish = current_time+process.burst
                process.finish_time = finish
                process.remaining_time = 0
                events.append((current_time+process.burst, event))
                processesCopy.remove(process)
                break
        if not event and (current_time >= finish):
            event = "idle"
            events.append((current_time, event))
        current_time += 1
    return events

def preemptive_SJF_scheduler(processes, runfor):
    current_time = 0
    events = []
    processes.sort(key=lambda x: (x.arrival, x.burst))
    remaining_processes = processes.copy()
    while remaining_processes:
        event = None
        next_process = min(remaining_processes, key=lambda x: x.remaining_time)
        if next_process.arrival > current_time:
            current_time = next_process.arrival
            event = next_process.name + " arrived"
            events.append((current_time,event))
        next_process.start_time = current_time
        next_process.response_time = current_time - next_process.arrival
        event = next_process.name + " selected"
        events.append((current_time,event))
        current_time += 1
        next_process.remaining_time -= 1
        if next_process.remaining_time == 0:
            next_process.finish_time = current_time
            event = next_process.name + " finished"
            next_process.remaining_time = 0
            events.append((current_time,event))
            next_process.wait_time = next_process.start_time - next_process.arrival
            remaining_processes.remove(next_process)
    while current_time < runfor:
        events.append((current_time,"idle"))
        current_time +=1
    return events


def round_robin_scheduler(processes, quantum, runfor):
    current_time = -1
    events = []
    remaining_processes = processes.copy()
    while remaining_processes:
        event = None
        for process in remaining_processes:
            if process.arrival == current_time:
                event = process.name + " arrived"
                events.append((current_time,event))
            if process.arrival <= current_time:
                process.start_time = current_time
                event = process.name + " selected (burst {})".format(process.burst)
                events.append((current_time,event))
                process.response_time = current_time - process.arrival
                if process.burst <= quantum:
                    current_time += process.burst
                    process.finish_time = current_time
                    event = process.name + " finished"
                    events.append((current_time,event))
                    process.wait_time = process.start_time - process.arrival
                    process.remaining_time = 0
                    remaining_processes.remove(process)
                else:
                    current_time += quantum
                    process.burst -= quantum
            else:
                current_time += 1
    while current_time < runfor:
        events.append((current_time,"idle"))
        current_time +=1
    return events

def write_results_to_file(processes,filename,processcount, use, quantum, events, unfinished_processes, runfor):
    events.sort(key=lambda x: x[0])
    with open(filename, "w") as file:
        file.write("Number of processes: {}\n".format(processcount))
        file.write("Algorithm used: {}\n".format(use))
        if use == 'rr':
            file.write("Quantum: {}\n".format(quantum))
        file.write("Time Events:\n")
        for event in events:
            file.write("Time {} {}\n".format(event[0], event[1]))
        file.write("Finished at: {}\n".format(runfor))
        for process in processes:
            turnaround = process.finish_time - process.start_time
            file.write("{} wait {} turnaround {} response {}\n".format(process.name, process.wait_time, turnaround, process.response_time))
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
        print("Usage: scheduler-gpt.py <input file>")
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

    unfinished_processes = [process.name for process in processes if process.remaining_time > 0]

    write_results_to_file(processes,output_file, processcount, use, quantum, events, unfinished_processes, runfor)

    print("Results written to output.out file.")
