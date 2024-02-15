
# PROMPT 1
# You are tasked with implementing three process scheduling algorithms: FIFO (First In, First Out), Pre-emptive SJF (Shortest Job First), and Round Robin in Python, but using ChatGPT. ChatGPT's implementation should be able to simulate the scheduling of multiple processes under each algorithm and calculate their turnaround time, response time, and wait time.

# ChatGPT's implementation should include the following components:

# A data structure to represent a process, including its arrival time, execution time, and status.
# A scheduler function for each algorithm that takes in a list of processes and implements the chosen scheduling algorithm.
# A time slice parameter (Q-value) for Round Robin, which determines how long each process should be allowed to run before being preempted.
# A function to calculate our standard metrics: turnaround time, waiting time, and response time for each process.
# You will be provided with test inputs and outputs to use as a benchmark for your results.

# Each member of your team will be responsible for providing at least one prompt. You are allowed multiple iterations. You may continue to refine your prompt as much as necessary in order to get desirable results. You are encouraged to compare prompts as a team to arrive at a "best solution" for final submission. However, you will be required to keep and track your prompt history (see below).

# At some point, it may seem like continuing prompt iteration yields diminishing returns. At your discretion, you may choose to stop prompting and complete the project on your own. Ideally, human-written code would be limited to output formatting and other superficial, minor tweaks. However, there may be some features or aspects of the project which perhaps ChatGPT refuses to generate. These should be clearly documented. All cases of human-generated code should be commented as such.

# Finally, as a caution -- ChatGPT, at least as implemented at OpenAI.com, will occasionally refuse to generate code literally telling you that it can't. You can rephrase your prompt or even just ask it to carry it out regardless ("You've done this before. Please do it now").




class Process:
    def __init__(self, arrival_time, execution_time):
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.status = "pending"  # Status can be "pending", "running", or "completed"
        self.start_time = None   # Time when the process started execution
        self.end_time = None     # Time when the process completed execution

    def fifo_scheduler(processes):
        current_time = 0
        for process in processes:
            if process.arrival_time > current_time:
                current_time = process.arrival_time
                process.status = "running"
                process.start_time = current_time
                current_time += process.execution_time
                process.end_time = current_time
                process.status = "completed"

    def calculate_metrics(processes):
        total_turnaround_time = 0
        total_waiting_time = 0
        total_response_time = 0
        for process in processes:
            turnaround_time = process.end_time - process.arrival_time
            waiting_time = turnaround_time - process.execution_time
            response_time = process.start_time - process.arrival_time
            total_turnaround_time += turnaround_time
            total_waiting_time += waiting_time
            total_response_time += response_time
        num_processes = len(processes)
        avg_turnaround_time = total_turnaround_time / num_processes
        avg_waiting_time = total_waiting_time / num_processes
        avg_response_time = total_response_time / num_processes
        return avg_turnaround_time, avg_waiting_time, avg_response_time



    def sjf_scheduler(processes):
        current_time = 0
        while processes:
            shortest_process = min(processes, key=lambda x: x.execution_time)
            if shortest_process.arrival_time > current_time:
                current_time = shortest_process.arrival_time
            shortest_process.status = "running"
            shortest_process.start_time = current_time
            current_time += shortest_process.execution_time
            shortest_process.end_time = current_time
            shortest_process.status = "completed"
            processes.remove(shortest_process)

    def round_robin_scheduler(processes, time_slice):
        current_time = 0
        while processes:
            for process in processes:
                if process.arrival_time <= current_time and process.status != "completed":
                    process.status = "running"
                    process.start_time = current_time
                    if process.execution_time <= time_slice:
                        current_time += process.execution_time
                        process.end_time = current_time
                        process.status = "completed"
                    else:
                        current_time += time_slice
                        process.execution_time -= time_slice
                        process.status = "pending"