# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z6ers4Z6nSXSWck8gjXFOTPaT-WCHM69
"""

import matplotlib.pyplot as plt

# Function to calculate waiting time for FCFS
def calculate_fcfs(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    current_time = 0
    gantt_chart = []
    for process in processes:
        if current_time < process[1]:  # If CPU is idle
            gantt_chart.append(("Idle", current_time, process[1]))
            current_time = process[1]
        gantt_chart.append((process[0], current_time, current_time + process[2]))
        process[4] = current_time - process[1]  # Waiting time
        process[5] = process[4] + process[2]  # Turnaround time
        current_time += process[2]
    return gantt_chart

# Function to calculate SRT (Shortest Remaining Time)
def calculate_srt(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    completed, current_time = 0, 0
    gantt_chart, ready_queue = [], []
    while completed < len(processes):
        ready_queue += [p for p in processes if p[1] <= current_time and p not in ready_queue and p[3] > 0]
        ready_queue.sort(key=lambda x: x[3])  # Sort by remaining time
        if not ready_queue:
            gantt_chart.append(("Idle", current_time, current_time + 1))
            current_time += 1
            continue
        current_process = ready_queue.pop(0)
        gantt_chart.append((current_process[0], current_time, current_time + 1))
        current_process[3] -= 1
        if current_process[3] == 0:
            current_process[5] = current_time + 1 - current_process[1]  # Turnaround time
            current_process[4] = current_process[5] - current_process[2]  # Waiting time
            completed += 1
        current_time += 1
    return gantt_chart

# Function to calculate Round-Robin
def calculate_rr(processes, quantum):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    current_time, queue = 0, []
    gantt_chart = []
    while any(p[3] > 0 for p in processes):
        queue += [p for p in processes if p[1] <= current_time and p not in queue and p[3] > 0]
        if not queue:
            gantt_chart.append(("Idle", current_time, current_time + 1))
            current_time += 1
            continue
        current_process = queue.pop(0)
        execution_time = min(quantum, current_process[3])
        gantt_chart.append((current_process[0], current_time, current_time + execution_time))
        current_process[3] -= execution_time
        current_time += execution_time
        if current_process[3] > 0:
            queue.append(current_process)
        else:
            current_process[5] = current_time - current_process[1]  # Turnaround time
            current_process[4] = current_process[5] - current_process[2]  # Waiting time
    return gantt_chart

# Function to display results
def display_results(processes, gantt_chart, algorithm):
    print(f"\n{algorithm} Scheduling Results:")
    print("Process\tFinish Time\tWaiting Time\tTurnaround Time")
    for p in processes:
        print(f"{p[0]}\t{p[1] + p[2] + p[4]}\t\t{p[4]}\t\t{p[5]}")
    print("\nGantt Chart:")
    for g in gantt_chart:
        print(f"{g[0]} [{g[1]}-{g[2]}]", end=" ")
    print()
    cpu_utilization = sum(p[2] for p in processes) / gantt_chart[-1][2] * 100
    print(f"CPU Utilization: {cpu_utilization:.2f}%")

# Main function
def main():
    filename = input("Enter the input file name: ")
    quantum = int(input("Enter the time quantum for Round-Robin: "))
    with open(filename, "r") as file:
        lines = file.readlines()
    processes = [[line.split()[0], int(line.split()[1]), int(line.split()[2]), int(line.split()[2]), 0, 0] for line in lines]

    for algo, func in zip(["FCFS", "SRT", "RR"], [calculate_fcfs, calculate_srt, lambda p: calculate_rr(p, quantum)]):
        proc_copy = [p[:] for p in processes]
        gantt_chart = func(proc_copy)
        display_results(proc_copy, gantt_chart, algo)

if __name__ == "__main__":
    main()