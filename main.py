import customtkinter as ctk

# APP SETUP
app = ctk.CTk()
app.geometry("700x500")
app.title("To-Do App")
ctk.set_appearance_mode("dark")
app.iconbitmap("to-do.ico")
ctk.FontManager.load_font("Outfit-Black.ttf")

# LIST BACKEND
tasks = []

# WIDGET FUNCTIONS
def add_task():
    task_input.pack(side='left', padx=15)
    enter.pack(side='left', padx=5)

def append_task():
    task = task_input.get()
    tasks.append(task)
    print(tasks)
    task_input.delete(0, 'end')
    print(tasks)

    for widget in task_frame.winfo_children():
        widget.destroy()

    for i, item in enumerate(tasks, start=1):
        print(f"{i}. {item}")
        task_frame.pack(fill="x") #padx=15, pady=10)
        text = ctk.CTkLabel(task_frame, text=tasks[i-1], bg_color="blue", width=100)
        text.pack()
    task_input.pack_forget()
    enter.pack_forget()

# WIDGETS
title = ctk.CTkLabel(app, text="To-Do App", font=("Outfit", 30, "bold"))
title.pack(pady=10)

color = app.cget("fg_color")
button_frame = ctk.CTkFrame(app, fg_color=color, height=20)
button_frame.pack(fill="x", pady=8)
add = ctk.CTkButton(button_frame, text="Add task", font=("Outfit", 15), corner_radius=10,
                    border_color="#4080FF", border_width=1, command=add_task)
add.pack(side="left", padx=15)

input_frame = ctk.CTkFrame(app, fg_color=color, height=20)
input_frame.pack(fill="x", pady=8)
task_input = ctk.CTkEntry(input_frame, placeholder_text="Enter yor task")
enter = ctk.CTkButton(input_frame, text="Enter", font=("Outfit", 15), corner_radius=10
                      , width=30, command=append_task)

# Creating frame, with textbox, combo, and dateEntry
task_frame = ctk.CTkFrame(app, height=50, fg_color='red')


app.mainloop()