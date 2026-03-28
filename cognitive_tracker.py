import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Data storage
focus_levels = []
time_points = []
time = 0

# --- Functions ---

def add_entry():
    global time
    try:
        focus = int(entry.get())
        
        if focus < 1 or focus > 5:
            messagebox.showerror("Error", "Enter value between 1 and 5")
            return
        
        focus_levels.append(focus)
        time_points.append(time)
        time += 10
        
        entry.delete(0, tk.END)
        status_label.config(text=f"Added! Time: {time} mins")
        
    except:
        messagebox.showerror("Error", "Invalid input")

def end_session():
    if not focus_levels:
        messagebox.showwarning("Warning", "No data entered")
        return

    # --- Calculations ---
    avg_focus = sum(focus_levels) / len(focus_levels)

    fatigue_point = None
    for i in range(1, len(focus_levels)):
        if focus_levels[i] < focus_levels[i-1]:
            fatigue_point = time_points[i]
            break

    max_focus = max(focus_levels)
    peak_time = time_points[focus_levels.index(max_focus)]

    # --- Recommendations ---
    if avg_focus < 2:
        suggestion = "Very low focus detected. Improve environment, reduce distractions, and get proper rest."

    elif avg_focus < 3:
        suggestion = "Focus is below average. Try shorter sessions and take regular breaks."

    elif fatigue_point is not None:
        suggestion = f"Your focus drops around {fatigue_point} minutes. Take a break before this time."

    elif avg_focus >= 4:
        suggestion = "Excellent focus! Maintain your current study pattern."

    else:
        suggestion = "Good consistency. Minor improvements can further boost performance."

    # --- Result Display ---
    result = f"""
Average Focus: {avg_focus:.2f}
Peak Focus Time: {peak_time} mins
Fatigue Point: {fatigue_point if fatigue_point is not None else 'Not Detected'}

Recommendation:
{suggestion}
"""

    messagebox.showinfo("Session Analysis", result)

    # --- Graph ---
    plt.figure()
    plt.plot(time_points, focus_levels, marker='o')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Focus Level")
    plt.title("Cognitive Load Tracker")
    plt.grid()
    plt.show()
def reset_session():
    global focus_levels, time_points, time
    focus_levels = []
    time_points = []
    time = 0
    status_label.config(text="Session Reset")


# --- GUI Design ---

root = tk.Tk()
root.title("Cognitive Load Tracker")
root.geometry("400x350")

title = tk.Label(root, text="🧠 Cognitive Load Tracker", font=("Arial", 16))
title.pack(pady=10)

label = tk.Label(root, text="Enter Focus Level (1-5):")
label.pack()

entry = tk.Entry(root)
entry.pack(pady=5)

add_btn = tk.Button(root, text="Add Entry", command=add_entry)
add_btn.pack(pady=5)

end_btn = tk.Button(root, text="End Session", command=end_session)
end_btn.pack(pady=5)

reset_btn = tk.Button(root, text="Reset", command=reset_session)
reset_btn.pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()