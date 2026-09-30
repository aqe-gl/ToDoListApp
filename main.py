import customtkinter as ctk
from ctkdateentry import CTkDateEntry, CTkStringVar
import datetime

# APP SETUP
app = ctk.CTk()
app.geometry("700x500")
app.title("To-Do App")
ctk.set_appearance_mode("dark")
app.after(200, lambda: app.iconbitmap("to-do.ico"))  # Windows only
ctk.FontManager.load_font("Outfit-Black.ttf")

# LIST BACKEND
tasks = []

# FUNCTIONS
def add_task():
    task_input.pack(side='left', padx=15)
    enter.pack(side='left', padx=5)
    task_input.focus()

def refresh_tasks():
    # clear old rows
    for widget in task_container.winfo_children():
        widget.destroy()

    # one frame per task
    for i, item in enumerate(tasks, start=1):
        row = ctk.CTkFrame(task_container)
        row.pack(fill="x", pady=3, padx=10)
        ctk.CTkCheckBox(row, text='', width=10).pack(side='left')
        ctk.CTkLabel(row, text=f"{i}. {item}", anchor="w", font=("Outfit", 15, 'bold'), fg_color='#6F7173', padx=10
                     ).pack(side="left", padx=(0, 8), pady=6)
        ctk.CTkLabel(row, text="Priority: ").pack(side='left', padx=5)
        COLORS = {
            'Low ⚑': '#42AF2F',
            'Medium ⚑': '#F2C712',
            'High ⚑': '#F20004',
        }

        def update(choice=None):
            priority.configure(text_color=COLORS.get(priority.get(), '#FFFFFF'))
        priority = ctk.CTkComboBox(row,
                        values=list(COLORS.keys()), command=update)
        priority.pack(side='left', padx=10)
        update()

        var = CTkStringVar(row, value='Enter a Date')
        date_entry = CTkDateEntry(row, variable=var)
        date_entry.pack(side="left")

        """def update():
            if priority.get() == 'Low ⚑':
                priority.configure(text_color='#42AF2F')
            elif priority.get() == 'Medium ⚑':
                priority.configure(text_color='#F2C712')
            elif priority.get() == 'High ⚑':
                priority.configure(text_color='#F20004')
        while True:
            update()"""
        #apply = ctk.CTkButton(row, text="Apply", command=update, width=10)
        #apply.pack(side='left', padx=5)

        def get_date():
            return var.get()




def append_task():
    task = task_input.get().strip()
    if task:
        tasks.append(task)
        refresh_tasks()
    task_input.delete(0, 'end')
    task_input.pack_forget()
    enter.pack_forget()

# WIDGETS (created in the order you want them to appear)
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
task_input = ctk.CTkEntry(input_frame, placeholder_text="Enter your task")
enter = ctk.CTkButton(input_frame, text="Enter", font=("Outfit", 15), corner_radius=10,
                      width=30, command=append_task)

# Task list goes last so it appears below everything else
task_container = ctk.CTkScrollableFrame(app)
task_container.pack(fill="both", expand=True, padx=10, pady=10)
if not tasks:
    empty = ctk.CTkLabel(task_container, text="Your to-do list is empty", font=("Outfit", 15))
    empty.pack(pady=10)
if tasks:
    empty.pack_forget()

app.mainloop()