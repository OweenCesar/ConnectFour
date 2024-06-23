
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
import random
from tkinter import filedialog, messagebox
import pygame

root = tk.Tk()
root.title("GUI Clock")
root.geometry("700x500")
root.configure(bg='white')

root.resizable(False, False)
root.attributes("-topmost", -1)

#Our main window will be divided in 3 frames

frame = tk.Frame(root, bg="black", width=600, height=150, relief="sunken")
frame.pack(pady=10, padx=10)
frame.pack_propagate(False)  

frame2 = tk.Frame(root, bg="black", width=700, height=300, relief="sunken")
frame2.pack( side="left", anchor="nw", pady=10, padx=50)
frame2.pack_propagate(False)

frame3 = tk.Frame(root, bg="black", width=400, height=300, relief="sunken")
frame3.pack(  anchor="ne", pady=10, padx=50)
frame3.place(x=390, y=180)
frame3.pack_propagate(False)






# Setting the labels for the first frame (showing the current time, date, etc)
showing_time = tk.Label(frame, bg="lightblue", fg="black", font=("Bold", 15), anchor='center')
showing_time.place(relx=0.5, rely=0.2, anchor='center')

showing_day = tk.Label(frame, bg="lightblue", fg="black", font=("Bold", 15), anchor='center')
showing_day.place(relx=0.5, rely=0.5, anchor = "center" )
tasks = ["go to the gym", "visit Mom's", "have a walk", "do the laundry", "study math", "clean your room", "study german"]
today_tasks = random.choice(tasks)

showing_date= tk.Label(frame, bg="lightblue", fg="black", font=("Bold", 15), anchor='center')
showing_date.place(relx=0.5, rely=0.8, anchor = "center" )
start_time = None
running_time = False
elapsed_time = 0

# Starting from the left side of our window, i implemented here the function which will be called after the timer is started
# Note that here, in this function, we are using time in order to know at what time (Uhr) it was started but the timer will start always from 00.00

def start_clicked():
    global start_time, running_time, elapsed_time, time_clicked
    if not running_time:
        start_time = time.time()
        elapsed_time = 0
        running_time = True
        update_timer()
        moving_circle()
        time_clicked = time.strftime("%H:%M:%S")
        
    start_button.config(text="Stop", bg="red", command= stop_timer)
    

# After starting, the timer will change its name and will call another different function too which is stop_timer, the last action in this method is saving the information 
# of the timer and its duration. To be more precise, the file will show at what time it started , its end time and of course duration.

def stop_timer():
    global running_time 
    running_time = False
    end_timer = tk.Label(frame2, text= f"End time: {minutes:02}:{seconds:02}" )
    end_timer.grid(row=5, column=0,padx=10, pady=10)
    start_button.config(command=start_clicked, text="Start", bg="lightblue") 
    #pygame.time.wait(100)
    save_timer()



def save_timer():
    global minutes, seconds
    file_saver = filedialog.asksaveasfile(filetypes = [('All Files', '*.*'),  ('Text Document', '*.txt')], defaultextension = ".txt")
    if file_saver:
        file_path = file_saver.name
        with open(file_path, "w") as file:
            file.write(f"Welcome to your timer data\n Start time: 00:00 at {time_clicked}\n Your timer finished at : {current_time }\n Duration: {minutes:02}:{seconds:02} \n ")
        messagebox.showinfo("Success", f"Your end time was save to {file_path}")
        minutes = 0
        seconds = 0 


def update_timer():
    global start_time, running_time, elapsed_time, minutes, seconds
    if running_time:
        elapsed_time = time.time()  - start_time 
        minutes= int(elapsed_time// 60)
        seconds = int(elapsed_time % 60)
        timing.config(text=f"Start time: {minutes:02}:{seconds:02}")
        root.after(1000, update_timer)

        
timing = tk.Label(frame2, text= "Start time: 00:00" )
timing.grid(row=1, column=0,padx=10, pady=10)

start_button = tk.Button(frame2, command = start_clicked, text="Start", bg="lightblue", fg="black", font=("Bold",13) )
start_button.grid(row=0, column=0, padx=10, pady=10)


def temp_text(e):
    entry_minutes.delete(0, "end")

entry_minutes = Entry(frame2, bg="white", borderwidth=1)
entry_minutes.insert(0,"write the minutes")
entry_minutes.grid(row=1, column=3, padx=10, pady=10)

entry_minutes.bind("<FocusIn>" , temp_text)



def temp_text2(e):
    entry_seconds.delete(0, "end")


entry_seconds = Entry(frame2,bg="white", borderwidth=1)
entry_seconds.insert(0, "write the seconds")
entry_seconds.grid(row=2, column=3, padx=10, pady=10)

entry_seconds.bind("<FocusIn>" , temp_text2)


def start_countdown():
    
    try:
        remaining_minutes = int(entry_minutes.get())
        remaining_seconds = int(entry_seconds.get())
        if remaining_minutes >= 0 and remaining_seconds >= 0 :
            update_countdown(remaining_minutes, remaining_seconds)
            
            
    except ValueError:
        messagebox.showerror("Invalid Input", "PLease enter a valid number of minutes")


bouncing_balls = False #this flag will help us to start the animation for the countdown!

def update_countdown(minutes_left, seconds_left):
    global bouncing_balls
    colorful_balls()
    #I decided to check every case that could show up in the countdown        
    if minutes_left >= 0 and seconds_left >= 0: 
        countdown_label.config(text=f"Time remaining: {minutes_left} minute(s)")
        countdown_seconds_label.config(text=f"Time remaining: {seconds_left} second(s)")
        
            
   
    if seconds_left == 0 and minutes_left > 0:
        minutes_left -=1
        seconds_left = 60
        root.after(1000, update_countdown, minutes_left, seconds_left)
        
    

    elif seconds_left > 0 and minutes_left >= 0:
        seconds_left -=1 
        root.after(1000, update_countdown, minutes_left, seconds_left)
    
    


    else:
        bouncing_balls = True
        messagebox.showinfo("Time's up", "the countdown has finished")
        
        
        
        
        

        
        

countdown_label = tk.Label(frame2, text="Time remaining: 0 minute(s)")
countdown_label.place(x=130, y=100)

countdown_seconds_label = tk.Label(frame2, text="Time remaining:0 second(s)")
countdown_seconds_label.place(x=130, y=180)





countdown_button = tk.Button(frame2, command = start_countdown, text="Start countdown", activebackground="blue", bg="lightblue", fg="black", font=("Bold",13) )
countdown_button.grid(row=0, column=3, padx=10, pady=10)



canvas = tk.Canvas(frame2, width=100,height=100, bg="white")
canvas.grid(row=2, column=0, padx=10, pady=10)


canvas2 = tk.Canvas(frame3, width=250,height=200, bg="white")
canvas2.grid(row=2, column=0, padx=10, pady=10)



def get_current_time():
    global current_time
    current_time = time.strftime("%H:%M:%S")
    today_is = time.strftime("%A")
    datum=time.strftime("%d/%b/%Y")

    showing_time.config(text=current_time)
    showing_day.config(text=f"Today is {today_is} - dont forget to {today_tasks}")
    showing_date.config(text=datum)

    root.after(1000, get_current_time)



#When started, the timer will have a canvas which show two balls moving in opposite directions

x= 0
x2=80
to_the_right = True

def moving_circle():
    global x,x2, to_the_right
    canvas.delete("all")
    canvas.create_oval(x,60,x+20,80, fill="red")
    canvas.create_oval(x2,30,x2+20,50, fill="yellow")
    if to_the_right:
        x +=2
        x2 -=2
        if x+20 >100 and x2<0:
            to_the_right = False
    else:
        x-=2
        x2 +=2
        if x<= 0:
            to_the_right = True
    if running_time:
        canvas.after(50, moving_circle)


# using an array, there will be colorful balls by the countdown's side. They will stop as soon as the countdown is 0. 
balls = []
for _ in range(10):
    ball = {
        "x" : random.randint(10,150),
        "y" : random.randint(10,200),
        "dx": random.choice([-2,2]),
        "dy": random.choice([-2,2])
        }
    balls.append(ball)


def colorful_balls():
    
    canvas2.delete("all")
    for ball in balls:
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]
        if ball["x"] <= 0 or ball["x"]>=250:
            ball["dx"] = -ball["dx"]
        if ball["y"] <= 0 or ball["y"]>= 250:
            ball["dy"] = -ball["dy"]
        colors = ["green", "blue", "red", "yellow"]
        selected_color = random.choice(colors)
        canvas2.create_oval(ball["x"],ball["y"],ball["x"]+20, ball["y"] +20, fill= selected_color)
    if bouncing_balls == False:
        canvas2.after(50, colorful_balls)


get_current_time()
root.mainloop()

