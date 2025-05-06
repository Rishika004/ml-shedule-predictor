import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import joblib

model = joblib.load(r'C:\Users\DELL\OneDrive\Desktop\os\rf_scheduler_model.pkl')
encoder = joblib.load(r'C:\Users\DELL\OneDrive\Desktop\os\label_encoder.pkl')

def draw_gantt_chart(processes):
    fig, gnt = plt.subplots()
    gnt.set_title("Gantt Chart")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Processes")

    gnt.set_yticks([15 * (i + 1) for i in range(len(processes))])
    gnt.set_yticklabels([f"P{i+1}" for i in range(len(processes))])
    gnt.grid(True)

    time = 0
    for i, burst_time in enumerate(processes):
        gnt.broken_barh([(time, burst_time)], (15 * (i + 1) - 5, 10), facecolors='tab:blue')
        time += burst_time

    plt.show()


def predict_scheduler():
    try:
        avg_burst = float(entry_burst.get())
        variance = float(entry_variance.get())
        avg_priority = float(entry_priority.get())
        spread = float(entry_spread.get())
        process_list = list(map(int, entry_bursts.get().split()))

        input_data = np.array([[avg_burst, variance, avg_priority, spread]])
        prediction = model.predict(input_data)
        label = encoder.inverse_transform(prediction)[0]

        result_var.set(f"📌 Predicted Scheduler: {label}")
        draw_gantt_chart(process_list)

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("ML Scheduler Predictor")
root.geometry("400x400")

tk.Label(root, text="Avg Burst Time:").pack()
entry_burst = tk.Entry(root)
entry_burst.pack()

tk.Label(root, text="Burst Time Variance:").pack()
entry_variance = tk.Entry(root)
entry_variance.pack()

tk.Label(root, text="Avg Priority:").pack()
entry_priority = tk.Entry(root)
entry_priority.pack()

tk.Label(root, text="Arrival Spread:").pack()
entry_spread = tk.Entry(root)
entry_spread.pack()

tk.Label(root, text="Process Burst Times (space-separated):").pack()
entry_bursts = tk.Entry(root)
entry_bursts.pack()

tk.Button(root, text="Predict & Show Gantt", command=predict_scheduler).pack(pady=10)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, font=("Arial", 12, "bold")).pack(pady=10)

root.mainloop()
