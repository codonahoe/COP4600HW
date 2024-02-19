class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining_time = burst
        self.status = 'READY'
        self.start_time = None
        self.finish_time = None
        self.response_time = None

def scheduler_RR(processes, runfor, quantum):
    current_time = 0
    events = []
    CPU = 'Idle'
    tasks = []
    current_repeat = 0
    while current_time < runfor:
        # Label if the process has arrived
        
        for process in processes:
            if process.arrival == current_time:
                tasks.append(process)
                events.append((current_time, process.name, 'arrived'))
        if CPU == 'Idle':
            if len(tasks) == 0:#If nothing is happening and nothing to do, Idle
                events.append((current_time, 'Idle'))
            elif len(tasks) >= 1:#If nothing is happening and a task appears
                CPU = 'Running'
                tasks[0].start_time = current_time
                events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
                current_repeat = 0
        elif CPU == 'Running':
            tasks[0].remaining_time -= 1
            current_repeat += 1
            #print(current_repeat)
            if tasks[0].remaining_time == 0:
                tasks[0].finish_time = current_time
                tasks[0].status = 'FINISHED'
                events.append((current_time, tasks[0].name, 'finished'))
                tasks.pop(0)
                CPU = 'Idle'
                current_repeat = 0
                if len(tasks) >= 1:
                    CPU = 'Running'
                    tasks[0].start_time = current_time
                    events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
                else:
                    events.append((current_time, 'Idle'))
            if current_repeat == quantum:
                tempObj = tasks[0]
                tasks.pop(0)
                tasks.append(tempObj)
                events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
                current_repeat = 0

        current_time += 1

    # Label processes that did not finish
    for process in processes:
        if process.status != 'FINISHED':
            events.append((runfor, process.name, 'did not finish'))

    return events


def scheduler_SJF(processes, runfor):
    current_time = 0
    events = []
    CPU = 'Idle'
    tasks = []
    while current_time < runfor:
        isNewSelected = 0
        #Label if the process has arrived
        for process in processes:
            if process.arrival == current_time:
                tasks.append((process))
                events.append((current_time, process.name, 'arrived'))

        if CPU == 'Idle':
            if len(tasks) == 0:#If nothing is happening and nothing to do, Idle
                events.append((current_time, 'Idle'))
            elif len(tasks) >= 1:#If nothing is happening and a task appears
                CPU = 'Running'
                tasks[0].start_time = current_time
                events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
        elif CPU == 'Running':
            tasks[0].remaining_time -= 1
            if tasks[0].remaining_time == 0:
                tasks[0].finish_time = current_time
                tasks[0].status = 'FINISHED'
                events.append((current_time, tasks[0].name, 'finished'))
                tasks.pop(0)
                CPU = 'Idle'
                if len(tasks) == 0:
                    events.append((current_time, 'Idle'))
                isNewSelected = 1
        if len(tasks) > 0:
            # Find the index of the task with the lowest remaining time
            min_index = 0
            min_remaining_time = tasks[0].remaining_time

            for i, task in enumerate(tasks[1:], start=1):
                if task.remaining_time < min_remaining_time:
                    min_remaining_time = task.remaining_time
                    min_index = i

            # If the task with the lowest remaining time is not already at the beginning of the list, swap it
            if min_index != 0:
                tasks[0], tasks[min_index] = tasks[min_index], tasks[0]    
                events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
                CPU = "Running"
            elif isNewSelected == 1:  
                CPU = "Running"
                events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
                isNewSelected = 0
                
        
        current_time += 1
    for process in processes:
        if process.status != 'FINISHED':
            events.append((runfor, process.name, 'did not finish'))
    
    return events

def scheduler_FCFS(processes, runfor):
    current_time = 0
    events = []
    CPU = 'Idle'
    tasks = []
    while current_time < runfor:
        #Label if the process has arrived
        for process in processes:
            if process.arrival == current_time:
                tasks.append((process))
                events.append((current_time, process.name, 'arrived'))
        if CPU == 'Idle':
            if len(tasks) == 0:#If nothing is happening and nothing to do, Idle
                events.append((current_time, 'Idle'))
            elif len(tasks) >= 1:#If nothing is happening and a task appears
                CPU = 'Running'
                tasks[0].start_time = current_time
                events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
        elif CPU == 'Running':
            tasks[0].remaining_time -= 1
            if tasks[0].remaining_time == 0:
                tasks[0].finish_time = current_time
                tasks[0].status = 'FINISHED'
                events.append((current_time, tasks[0].name, 'finished'))
                tasks.pop(0)
                CPU = 'Idle'
                if len(tasks) >= 1:
                    CPU = 'Running'
                    tasks[0].start_time = current_time
                    events.append((current_time, tasks[0].name, 'selected', tasks[0].remaining_time))
                else:
                    events.append((current_time, 'Idle'))
        current_time += 1
    for process in processes:
        if process.status != 'FINISHED':
            events.append((runfor, process.name, 'did not finish'))
    return events

def calculate_metrics(processes):
    for process in processes:
        #print(f"{process.name} {process.arrival}  {process.finish_time}")
        process.turnaround_time = process.finish_time - process.arrival
        process.wait_time = process.turnaround_time - process.burst
        process.response_time = process.start_time - process.arrival if process.start_time else 0

def read_input(filename):
    processes = []
    with open(filename, 'r', encoding='utf-8') as f:
        quantum = None
        for line in f:
            parts = line.strip().split()
            if parts[0] == 'quantum':
                quantum = int(parts[1])
            elif parts[0] == 'processcount':
                processcount = int(parts[1])
            elif parts[0] == 'runfor':
                runfor = int(parts[1])
            elif parts[0] == 'use':
                scheduler_type = parts[1]
            elif parts[0] == 'process':
                name = parts[2]
                arrival = int(parts[4])
                burst = int(parts[6])
                processes.append(Process(name, arrival, burst))
            elif parts[0] == 'end':
                break
    return processcount, runfor, scheduler_type, quantum, processes

def write_output(filename, processcount, events, processes):
    with open(filename, 'w') as f:
        #Start Write to file
        f.write(f"\t{processcount} processes\n") #Add amount of processes
        f.write(f"Using {scheduler_type}\n") #Describe Job type

        if scheduler_type == 'rr':
            f.write(f"Quantum {quantum}\n") #If using Round robin label our quantum 
        
        #Write to file the recorded events from each function
        for event in events:
            if len(event) >= 3:
                time, name, action = event[:3] #Record the event as the Time, Process name and action that was being taken
                if action == 'selected':
                    burst = event[3]
                    f.write(f"Time {time:4} : {name} selected (burst {burst:4})\n") #If the action was selected, label the burst
                else:
                    f.write(f"Time {time:4} : {name} {action}\n") #Otherwise write the event
            elif len(event) == 2: #Writing this just for Idle 
                time, action = event[:2]
                f.write(f"Time {time:4} : {action}\n")

        
        f.write(f"Finished at time {runfor}\n\n")
        
        #Using Metrics data calculate the Wait, Turnaround and response time
        for process in processes:
            f.write(f"{process.name} wait {(process.wait_time):4} turnaround {(process.turnaround_time):4} response {process.response_time}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = input_filename+ '.out'

    processcount, runfor, scheduler_type, quantum, processes = read_input(input_filename)

    if scheduler_type == 'fcfs':
        events = scheduler_FCFS(processes, runfor)
    elif scheduler_type == 'sjf':
        events =  scheduler_SJF(processes, runfor)
    elif scheduler_type == 'rr':
        events =  scheduler_RR(processes, runfor,quantum)
    else:
        print("Error: Invalid scheduler type")
        sys.exit(1)

    calculate_metrics(processes)

    write_output(output_filename, processcount, events, processes)
