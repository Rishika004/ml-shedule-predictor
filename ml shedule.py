import random
import pandas as pd
from collections import deque



def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x['arrival_time'])
    time = 0
    waiting_times = []
    for p in processes:
        if time < p['arrival_time']:
            time = p['arrival_time']
        waiting_times.append(time - p['arrival_time'])
        time += p['burst_time']
    return sum(waiting_times) / len(waiting_times)

def sjf_scheduling(processes):
    processes = sorted(processes, key=lambda x: (x['arrival_time'], x['burst_time']))
    time = 0
    completed = 0
    n = len(processes)
    waiting_times = [0] * n
    ready_queue = []
    i = 0
    while completed != n:
        while i < n and processes[i]['arrival_time'] <= time:
            ready_queue.append(processes[i])
            i += 1
        if ready_queue:
            ready_queue.sort(key=lambda x: x['burst_time'])
            p = ready_queue.pop(0)
            waiting_times[completed] = time - p['arrival_time']
            time += p['burst_time']
            completed += 1
        else:
            time = processes[i]['arrival_time']
    return sum(waiting_times) / len(waiting_times)

def priority_scheduling(processes):
    processes = sorted(processes, key=lambda x: (x['arrival_time'], x['priority']))
    time = 0
    completed = 0
    n = len(processes)
    waiting_times = [0] * n
    ready_queue = []
    i = 0
    while completed != n:
        while i < n and processes[i]['arrival_time'] <= time:
            ready_queue.append(processes[i])
            i += 1
        if ready_queue:
            ready_queue.sort(key=lambda x: x['priority'])
            p = ready_queue.pop(0)
            waiting_times[completed] = time - p['arrival_time']
            time += p['burst_time']
            completed += 1
        else:
            time = processes[i]['arrival_time']
    return sum(waiting_times) / len(waiting_times)

def round_robin_scheduling(processes, quantum=10):
    processes = sorted(processes, key=lambda x: x['arrival_time'])
    n = len(processes)
    remaining_bt = [p['burst_time'] for p in processes]
    waiting_time = [0] * n
    arrival_time = [p['arrival_time'] for p in processes]
    time = 0
    queue = deque()
    i = 0
    while i < n or queue:
        if not queue:
            queue.append(i)
            time = max(time, arrival_time[i])
            i += 1
        idx = queue.popleft()
        exec_time = min(quantum, remaining_bt[idx])
        time += exec_time
        remaining_bt[idx] -= exec_time
        for j in range(i, n):
            if arrival_time[j] <= time:
                queue.append(j)
                i += 1
        if remaining_bt[idx] > 0:
            queue.append(idx)
        else:
            waiting_time[idx] = time - processes[idx]['arrival_time'] - processes[idx]['burst_time']
    return sum(waiting_time) / n



def generate_process_set(num_processes):
    return [{
        'burst_time': random.randint(1, 100),
        'priority': random.randint(1, 10),
        'arrival_time': random.randint(0, 50)
    } for _ in range(num_processes)]



def create_dataset(samples=1000):
    dataset = []
    for _ in range(samples):
        num_processes = random.randint(5, 50)
        processes = generate_process_set(num_processes)

        avg_burst = sum(p['burst_time'] for p in processes) / num_processes
        var_burst = (sum((p['burst_time'] - avg_burst)**2 for p in processes) / num_processes)**0.5
        avg_priority = sum(p['priority'] for p in processes) / num_processes
        arrival_rate = num_processes / (max(p['arrival_time'] for p in processes) + 1)  # avoid division by zero

      
        fcfs_wt = fcfs_scheduling(processes.copy())
        sjf_wt = sjf_scheduling(processes.copy())
        priority_wt = priority_scheduling(processes.copy())
        rr_wt = round_robin_scheduling(processes.copy(), quantum=10)

        scores = {
            "FCFS": fcfs_wt,
            "SJF": sjf_wt,
            "Priority": priority_wt,
            "RR": rr_wt
        }
        best_policy = min(scores, key=scores.get)

        dataset.append({
            "avg_burst_time": avg_burst,
            "burst_time_variance": var_burst,
            "avg_priority": avg_priority,
            "arrival_rate": arrival_rate,
            "best_scheduler": best_policy
        })

    df = pd.DataFrame(dataset)
    df.to_csv('process_scheduling_dataset.csv', index=False)
    print(f"Dataset created successfully with {samples} samples!")



if __name__ == "__main__":
    create_dataset(samples=1000)  
