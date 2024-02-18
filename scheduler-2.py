"""
import sys
from collections import deque

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_burst = burst
        self.status = 'ready'
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def fcfs(processes, runfor):
    current_time = 0
    events = []
    ready_queue = deque(processes)
    while ready_queue:
        current_process = ready_queue.popleft()
        while current_time < current_process.arrival:
            events.append((current_time, 'idle', '', ' '))
            current_time += 1
        events.append((current_time, current_process.name, 'selected', f'(burst {current_process.remaining_burst})'))
        current_process.response_time = current_time - current_process.arrival if current_process.response_time == -1 else current_process.response_time
        current_time += current_process.remaining_burst
        current_process.turnaround_time = current_time - current_process.arrival
        current_process.status = 'finished'
        events.append((current_time, current_process.name, current_process.status, " <3"))
        for process in ready_queue:
            process.wait_time += current_process.remaining_burst
        while ready_queue and ready_queue[0].arrival <= current_time:
            ready_queue[0].wait_time = current_time - ready_queue[0].arrival
            ready_queue.rotate(-1)
    while current_time < runfor:
        events.append((current_time, 'idle', '', ' '))
        current_time += 1
    return events

def sjf(og_processes, runfor):
    current_time = 0
    events = []
    processes = og_processes.copy()
    ready_queue = []

    finished_processes = []
    while processes or ready_queue:
        if not ready_queue:
            next_arrival = processes[0].arrival
            if next_arrival > current_time:
                while current_time < next_arrival:
                    current_time +=1
                    events.append((current_time, 'idle', ' ', ' '))
        for process in processes[:]:
            if process.arrival <= current_time:
                ready_queue.append(process)
                processes.remove(process)
        if ready_queue:
            ready_queue.sort(key=lambda x: x.remaining_burst)
            current_process = ready_queue.pop(0)
            events.append((current_time, current_process.name, 'selected', f'(burst {current_process.remaining_burst})'))
            current_process.response_time = current_time - current_process.arrival if current_process.response_time == -1 else current_process.response_time
            if current_process.remaining_burst > 1:
                current_process.remaining_burst -= 1
                current_time += 1
                ready_queue.append(current_process)
            else:
                current_process.turnaround_time = current_time + 1 - current_process.arrival
                current_process.status = 'finished'
                events.append((current_time, current_process.name , 'finished', '<3'))
                finished_processes.append(current_process)
                for process in ready_queue:
                    process.wait_time += current_process.remaining_burst
                current_time += 1
        else:
            current_time += 1
    while current_time < runfor:
            events.append((current_time, 'idle', '', ' '))
            current_time += 1
    return events

def round_robin(processes, quantum):
    current_time = 0
    events = []
    ready_queue = deque(processes)
    while ready_queue:
        current_process = ready_queue.popleft()
        if current_time < current_process.arrival:
            events.append((current_time, 'idle', ' ', ' '))
            current_time = current_process.arrival
        events.append((current_time, current_process.name, 'selected', f'(burst {min(quantum, current_process.remaining_burst)})'))
        current_process.response_time = current_time - current_process.arrival if current_process.response_time == -1 else current_process.response_time
        if current_process.remaining_burst > quantum:
            current_time += quantum
            current_process.remaining_burst -= quantum
            while ready_queue and ready_queue[0].arrival <= current_time:
                ready_queue[0].wait_time += current_time - ready_queue[0].arrival
                ready_queue.rotate(-1)
            ready_queue.append(current_process)
        else:
            current_time += current_process.remaining_burst
            current_process.turnaround_time = current_time - current_process.arrival
            current_process.status = 'finished'
            for process in ready_queue:
                process.wait_time += current_process.remaining_burst
            while ready_queue and ready_queue[0].arrival <= current_time:
                ready_queue[0].wait_time += current_time - ready_queue[0].arrival
                ready_queue.rotate(-1)
    return events

"""
####
"""
def fcfs(processes):
    current_time = 0
    events = []
    ready_queue = deque(processes)
    while ready_queue:
        current_process = ready_queue.popleft()
        if current_time < current_process.arrival:
            current_time = current_process.arrival
        events.append((current_time, current_process.name, 'selected', f'(burst {current_process.remaining_burst})'))
        current_process.response_time = current_time - current_process.arrival if current_process.response_time == -1 else current_process.response_time
        current_time += current_process.remaining_burst
        current_process.turnaround_time = current_time - current_process.arrival
        current_process.status = 'finished'
        events.append((current_time, current_process.name, 'finished', " <3"))
        for process in ready_queue:
            process.wait_time += current_process.remaining_burst
        while ready_queue and ready_queue[0].arrival <= current_time:
            ready_queue[0].wait_time = current_time - ready_queue[0].arrival
            ready_queue.rotate(-1)
    return events

def sjf(processes):
    current_time = 0
    events = []
    ready_queue = []
    finished_processes = []
    while processes or ready_queue:
        for process in processes[:]:
            if process.arrival <= current_time:
                ready_queue.append(process)
                processes.remove(process)
        if ready_queue:
            ready_queue.sort(key=lambda x: x.remaining_burst)
            current_process = ready_queue.pop(0)
            events.append((current_time, current_process.name, 'selected', f'(burst {current_process.remaining_burst})'))
            current_process.response_time = current_time - current_process.arrival if current_process.response_time == -1 else current_process.response_time
            if current_process.remaining_burst > 1:
                events.append((current_time + 1, current_process.name, 'preempted', f'(burst {current_process.remaining_burst - 1})'))
                current_process.remaining_burst -= 1
                current_time += 1
                ready_queue.append(current_process)
            else:
                current_process.turnaround_time = current_time + 1 - current_process.arrival
                current_process.status = 'finished'
                finished_processes.append(current_process)
                for process in ready_queue:
                    process.wait_time += current_process.remaining_burst
                current_time += 1
        else:
            current_time += 1
    return events

def round_robin(processes, quantum):
    current_time = 0
    events = []
    ready_queue = deque(processes)
    while ready_queue:
        current_process = ready_queue.popleft()
        if current_time < current_process.arrival:
            current_time = current_process.arrival
        events.append((current_time, current_process.name, 'selected', f'(burst {min(quantum, current_process.remaining_burst)})'))
        current_process.response_time = current_time - current_process.arrival if current_process.response_time == -1 else current_process.response_time
        if current_process.remaining_burst > quantum:
            current_time += quantum
            current_process.remaining_burst -= quantum
            while ready_queue and ready_queue[0].arrival <= current_time:
                ready_queue[0].wait_time += current_time - ready_queue[0].arrival
                ready_queue.rotate(-1)
            ready_queue.append(current_process)
        else:
            current_time += current_process.remaining_burst
            current_process.turnaround_time = current_time - current_process.arrival
            current_process.status = 'finished'
            for process in ready_queue:
                process.wait_time += current_process.remaining_burst
            while ready_queue and ready_queue[0].arrival <= current_time:
                ready_queue[0].wait_time += current_time - ready_queue[0].arrival
                ready_queue.rotate(-1)
    return events

def calculate_metrics(processes):
    for process in processes:
        process.response_time = process.response_time if process.response_time != -1 else 0
        process.wait_time = process.turnaround_time - process.burst

def write_output(runfor, processes, algorithm, quantum, events=None):
    output_filename = sys.argv[1].replace('.in', '.out')
    with open(output_filename, 'w') as f:
        f.write(f'{len(processes)} processes\n')
        f.write(f'Using {algorithm}\n')
        if algorithm == 'rr':
            f.write('Quantum: {}\n'.format(quantum))
        if events:
            for event in events:
                f.write(f'Time {event[0]:>4} : {event[1]} {event[2]} {event[3]}\n')
        if runfor is not None:
            f.write('Finished at {} \n'.format(runfor))
        for process in processes:
            f.write(f'{process.name} wait {process.wait_time:>4} turnaround {process.turnaround_time:>4} response {process.response_time:>4}\n')

def parse_input(filename):
    processes = []
    quantum = None
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('processcount'):
                process_count = int(line.split()[1])
            elif line.startswith('runfor'):
                run_for = int(line.split()[1])
            elif line.startswith('use'):
                algorithm = line.split()[1]
            elif line.startswith('quantum'):
                quantum = int(line.split()[1])
            elif line.startswith('process'):
                name = line.split()[2]
                arrival = int(line.split()[4])
                burst = int(line.split()[6])
                processes.append(Process(name, arrival, burst))
    return process_count, run_for, algorithm, quantum, processes

def main():
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)

    filename = sys.argv[1]
    process_count, run_for, algorithm, quantum, processes = parse_input(filename)
    
    if algorithm == 'rr' and quantum is None:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)

    if algorithm == 'fcfs':
        events = fcfs(processes, run_for)
    elif algorithm == 'sjf':
        processes.sort(key=lambda x: x.arrival)
        events = sjf(processes, run_for)
    elif algorithm == 'rr':
        events = round_robin(processes, quantum)
    
    calculate_metrics(processes)
    write_output(run_for,processes, algorithm, quantum, events)

if __name__ == "__main__":
    main()

#############
import sys

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_time = burst
        self.start_time = None
        self.finish_time = None
        self.wait_time = 0
        self.turnaround_time = 0
        self.response_time = -1

def scheduler(processes, algorithm, quantum=None):
    current_time = 0
    ready_queue = []
    finished_processes = []
    total_processes = len(processes)

    if algorithm == 'sjf':
        processes.sort(key=lambda x: (x.arrival, x.burst))

    while True:
        if not processes and not ready_queue:
            break

        if processes:
            for process in processes:
                if process.arrival == current_time:
                    ready_queue.append(process)
                    processes.remove(process)

        if algorithm == 'rr' and ready_queue:
            process = ready_queue.pop(0)
            if process.response_time == -1:
                process.response_time = current_time - process.arrival
            if process.remaining_time <= quantum:
                current_time += process.remaining_time
                process.remaining_time = 0
                process.finish_time = current_time
                finished_processes.append(process)
            else:
                current_time += quantum
                process.remaining_time -= quantum
                ready_queue.append(process)
        
        elif ready_queue:
            if ready_queue[0].response_time == -1:
                ready_queue[0].response_time = current_time - ready_queue[0].arrival
            process = ready_queue.pop(0)
            process.start_time = current_time
            current_time += process.remaining_time
            process.finish_time = current_time
            process.remaining_time = 0
            finished_processes.append(process)
        else:
            current_time += 1

    return finished_processes

def calculate_metrics(processes):
    total_turnaround_time = 0
    total_wait_time = 0
    total_response_time = 0

    for process in processes:
        process.turnaround_time = process.finish_time - process.arrival
        process.wait_time = process.turnaround_time - process.burst
        total_turnaround_time += process.turnaround_time
        total_wait_time += process.wait_time
        total_response_time += process.response_time

    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_wait_time = total_wait_time / len(processes)
    avg_response_time = total_response_time / len(processes)

    return avg_turnaround_time, avg_wait_time, avg_response_time

def main(input_file):
    processes = []
    algorithm = None
    quantum = None

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        tokens = line.split()
        if tokens[0] == 'processcount':
            process_count = int(tokens[1])
        elif tokens[0] == 'runfor':
            run_for = int(tokens[1])
        elif tokens[0] == 'use':
            algorithm = tokens[1]
        elif tokens[0] == 'quantum':
            quantum = int(tokens[1])
        elif tokens[0] == 'process':
            name = tokens[2]
            arrival = int(tokens[4])
            burst = int(tokens[6])
            processes.append(Process(name, arrival, burst))
        elif tokens[0] == 'end':
            break

    if not algorithm or not processes:
        print("Error: Missing parameter.")
        sys.exit(1)

    finished_processes = scheduler(processes, algorithm, quantum)
    avg_turnaround_time, avg_wait_time, avg_response_time = calculate_metrics(finished_processes)
    finished_processes.sort(key = lambda x: (x.start_time))

    with open(input_file[:-2] + 'out', 'w') as outfile:
        outfile.write(f"{len(finished_processes)} processes\n")
        outfile.write(f"Using {'preemptive ' if algorithm == 'sjf' else ''}{algorithm.upper()}\n")
        if algorithm == 'rr':
            outfile.write(f"Quantum {quantum}\n")
        for process in finished_processes:
            outfile.write(f"Time {process.start_time:3d} : {process.name} arrived\n")
            outfile.write(f"Time {process.start_time:3d} : {process.name} selected (burst {process.burst:3d})\n")
            outfile.write(f"Time {process.finish_time:3d} : {process.name} finished\n")
        for t in range(run_for):
            if not any(p.arrival <= t < p.finish_time for p in finished_processes):
                outfile.write(f"Time {t:3d} : Idle\n")
        outfile.write(f"Finished at time {run_for}\n")
        outfile.write(f"Average turnaround time: {avg_turnaround_time:.2f}\n")
        outfile.write(f"Average wait time: {avg_wait_time:.2f}\n")
        outfile.write(f"Average response time: {avg_response_time:.2f}\n")
        unfinished_processes = [p.name for p in processes]
        if unfinished_processes:
            outfile.write("Unfinished processes:\n")
            for process_name in unfinished_processes:
                outfile.write(f"{process_name} did not finish\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scheduler-gpt.py <input file>")
        sys.exit(1)
    input_file = sys.argv[1]
    if not input_file.endswith('.in'):
        print("Input file must have the extension '.in'")
        sys.exit(1)
    main(input_file)
"""