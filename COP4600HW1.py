
# HW1 OS

class Process: 
    def __init__(self, arrival_time, execution_time, pid):
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.pid = pid
        self.status = "Ready"
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.wait_time = None

def FIFO_Scheduler(processes): #first in first out
    cur_time = 0
    for process in processes: #for each process in our queue
        if process.arrival_time > cur_time: #then the current time is updated
            cur_time = process.arrival_time
        process.start_time = current_time
        process.response_time = current_time - process.arrival_time
        process.finish_time = current_time + process.execution_time
        process.wait_time = process.start_time - process.arrival_time
        current_time = process.finish_time

def SJF_Scheduler(processes): #shortest job first
    cur_time = 0;
    #for process in processes:

def RR_Scheduler(processes, q_value): #round robin
    cur_time = 0

def calculate_performance(processes): #find out how turnaround, wait time,and response time performs
    turnaround_time = 0
    response_time = 0
    wait_time = 0
    for process in processes: #find total times in order to get an average
        turnaround_time += process.finish_time - process.arrival_time
        wait_time += process.wait_time
        response_time += process.response_time
    num_processes = len(processes)
    avg_turnaround_time = turnaround_time / num_processes
    avg_wait_time = wait_time / num_processes
    avg_response_time = response_time / num_processes
    return avg_turnaround_time, avg_wait_time, avg_response_time
