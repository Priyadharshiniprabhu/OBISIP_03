
import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

def setup_database():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_data(username, weight, height, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bmi_records (username, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)', 
                   (username, weight, height, bmi, category))
    conn.commit()
    conn.close()

def calculate_bmi():
    try:
        username = username_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # convert cm to m
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive.")

        bmi = weight / (height ** 2)
        category = classify_bmi(bmi)

        result_label.config(text=f"BMI: {bmi:.2f}, Category: {category}")
        save_data(username, weight, height, bmi, category)
        visualize_bmi_trend(username)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def visualize_bmi_trend(username):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT bmi FROM bmi_records WHERE username=?', (username,))
    bmis = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not bmis:
        messagebox.showinfo("Trend Analysis", "No data available for this user.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(bmis)), bmis, marker='o', label='BMI', color='blue')
    plt.title(f'BMI Trend Analysis for {username}')
    plt.xlabel('User Entries')
    plt.ylabel('BMI')
    plt.axhline(y=18.5, color='r', linestyle='--', label='Underweight Threshold')
    plt.axhline(y=24.9, color='orange', linestyle='--', label='Normal Weight Threshold')
    plt.axhline(y=29.9, color='purple', linestyle='--', label='Overweight Threshold')
    plt.legend()
    plt.grid()
    plt.show()

root = tk.Tk()
root.title("BMI Calculator")

setup_database()

tk.Label(root, text="Enter Username:").grid(row=0, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

tk.Label(root, text="Enter Weight (kg):").grid(row=1, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1)

tk.Label(root, text="Enter Height (cm):").grid(row=2, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=3, column=0, columnspan=2)

result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()
