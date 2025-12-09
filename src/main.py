import os
import tkinter as tk
from datetime import datetime
#try:
    #import openpyxl
 #   import sendgrid



#THING HERE
file = open("fifi.csv", "w")
if not os.path.exist("fifi.csv"):
    file = open("fifi.csv", "w")
    file.write("Event Name, Date, Time, Description")
else:
    file = open("fifi.csv", "r")
    
def add_event(event_name, date, time, description):
    with open("fifi.csv", "a") as file:
        file.write(f"\n{event_name}, {date}, {time}, {description}")
    
def view_event():
    with open("fifi.csv", "r") as file:
        for cline, line in enumerate(file):
            arr = line.split(", ")
            if arr[1] == datetime.today() and arr[2] == datetime.now().strftime("%H:%M"):
                dosomething()
def dosomething():
    print("KING FIFI")    


window = tk.Tk()
window.title("Eventual")
window.geometry("900x600")
window.configure(bg="#1E1E1E")
window.mainloop()