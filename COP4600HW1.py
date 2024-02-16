
# HW1 OS
#TODO: read in file and choose algo based on inputs....display results
#TODO: test & debug

class Process: #structure to represent a processes
    def __init__(self, name, arrival_time, execution_time):
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.name = name
        self.status = "Ready"
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.wait_time = None

def FIFO_Scheduler(processes): #first in first out
    cur_time = 0
    #for each process in our queue
    for process in processes:
        if process.arrival_time > cur_time: #then the current time is updated since it is now first
            cur_time = process.arrival_time
        process.start_time = current_time
        process.response_time = current_time - process.arrival_time
        process.finish_time = current_time + process.execution_time
        process.wait_time = process.start_time - process.arrival_time
        current_time = process.finish_time

def SJF_Scheduler(processes): #shortest job first
    processes.sort(key=lambda x: (x.arrival_time, x.execution_time))
    cur_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        next_process = min(remaining_processes, key=lambda x: x.execution_time)
        if next_process.arrival_time > cur_time:
            cur_time = next_process.arrival_time
        next_process.start_time = cur_time
        next_process.response_time = cur_time - next_process.arrival_time
        cur_time += 1
        next_process.execution_time -= 1
        if next_process.execution_time == 0:
            next_process.finish_time = cur_time
            next_process.wait_time = next_process.start_time - next_process.arrival_time
            remaining_processes.remove(next_process)

def RR_Scheduler(processes, q_value): #round robin
    cur_time = 0
    remaining_processes = processes.copy()
    while remaining_processes:
        for process in remaining_processes:
            if process.arrival_time <= cur_time:
                process.start_time = cur_time
                process.response_time = cur_time - process.arrival_time
                if process.execution_time <= q_value:
                    cur_time += process.execution_time
                    process.finish_time = cur_time
                    process.wait_time = process.start_time - process.arrival_time
                    remaining_processes.remove(process)
                else:
                    cur_time += q_value
                    process.execution_time -= q_value
            else:
                cur_time += 1


def calculate_performance(processes): #find out how turnaround, wait time,and response time performs
    turnaround_time = 0
    response_time = 0
    wait_time = 0
    #find total times of each process in order to get an average
    for process in processes:
        turnaround_time += process.finish_time - process.arrival_time
        wait_time += process.wait_time
        response_time += process.response_time
    #calculate the averages
    num_processes = len(processes) 
    avg_turnaround_time = turnaround_time / num_processes
    avg_wait_time = wait_time / num_processes
    avg_response_time = response_time / num_processes
    return avg_turnaround_time, avg_wait_time, avg_response_time

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
                name, arrival_time, execution_time = parts[1], int(parts[2]), int(parts[3])
                processes.append(Process(name, arrival_time, execution_time))
            elif parts[0] == 'end':
                break
    return processcount, runfor, use, quantum, processes

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)