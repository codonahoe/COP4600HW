
# HW1 OS
#TODO: read in file and choose algo based on inputs....display results
#TODO: test & debug

class Process: #structure to represent a processes
    def __init__(self, name, arrival, burst):
        self.arrival = arrival
        self.burst = burst
        self.name = name
        self.status = "Ready"
        self.start = None
        self.finish = None
        self.response = None
        self.wait = None

def FIFO_Scheduler(processes): #first in first out
    cur_time = 0
    #for each process in our queue
    for process in processes:
        if process.arrival > cur_time: #then the current time is updated since it is now first
            cur_time = process.arrival
        process.start = current_time
        process.response = current_time - process.arrival
        process.finish = current_time + process.burst
        process.wait = process.start - process.arrival
        current_time = process.finish

def SJF_Scheduler(processes): #shortest job first
    processes.sort(key=lambda x: (x.arrival_time, x.burst))
    cur_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        next_process = min(remaining_processes, key=lambda x: x.burst)
        if next_process.arrival > cur_time:
            cur_time = next_process.arrival
        next_process.start = cur_time
        next_process.response = cur_time - next_process.arrival
        cur_time += 1
        next_process.burst -= 1
        if next_process.burst == 0:
            next_process.finish = cur_time
            next_process.wait = next_process.start - next_process.arrival
            remaining_processes.remove(next_process)

def RR_Scheduler(processes, q_value): #round robin
    cur_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        for process in remaining_processes:
            if process.arrival <= cur_time:
                process.start = cur_time
                process.response = cur_time - process.arrival
                if process.burst <= q_value:
                    cur_time += process.burst
                    process.finish = cur_time
                    process.wait = process.start - process.arrival
                    remaining_processes.remove(process)
                else:
                    cur_time += q_value
                    process.burst -= q_value
            else:
                cur_time += 1


def calculate_performance(processes): #find out how turnaround, wait time,and response time performs
    turnaround = 0
    response = 0
    wait = 0
    #find total times of each process in order to get an average
    for process in processes:
        turnaround += process.finish - process.arrival
        wait += process.wait
        response += process.response
    #calculate the averages
    num_processes = len(processes) 
    avg_turnaround = turnaround / num_processes
    avg_wait = wait / num_processes
    avg_response = response / num_processes
    return avg_turnaround, avg_wait, avg_response

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
                name, arrival_time, burst = parts[1], int(parts[2]), int(parts[3])
                processes.append(Process(name, arrival_time, burst))
            elif parts[0] == 'end':
                break
    return processcount, runfor, use, quantum, processes

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_file = sys.argv[1]
    processcount, runfor, use, quantum, processes = read_processes_from_file(input_file)

    if use == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)

    if any(param is None for param in [processcount, runfor, use]):
        print("Error: Missing parameter(s).")
        sys.exit(1)