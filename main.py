import customtkinter as ctk
from ctkdateentry import CTkDateEntry, CTkStringVar
from tktimepicker import AnalogPicker, AnalogThemes
import json
import atexit


# APP SETUP
app = ctk.CTk()
app.geometry("900x600")
app.title("To-Do App")
ctk.set_appearance_mode("dark")
app.after(200, lambda: app.iconbitmap("to-do.ico"))  # Windows only
ctk.FontManager.load_font("Outfit-Black.ttf")
# LIST BACKEND
tasks = []
for i in tasks:
    print(i)

try:
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    tasks = []


def save_tasks():
    data = json.dumps(tasks)  # serialize first; if this fails, the file is untouched
    with open('tasks.json', 'w') as f:
        f.write(data)
# saving tasks
atexit.register(save_tasks)


PRIORITY_COLORS = {
    'Low ⚑': '#42AF2F',
    'Medium ⚑': '#F2C712',
    'High ⚑': '#F20004',
}


# WIDGETS (created in the order you want them to appear)
title = ctk.CTkLabel(app, text="To-Do App", font=("Outfit", 30, "bold")) # 1
title.pack(pady=10)

color = app.cget("fg_color")

button_frame = ctk.CTkFrame(app, fg_color=color, height=20) # 2
button_frame.pack(fill="x", pady=8)

input_frame = ctk.CTkFrame(app, fg_color=color, height=20) # 3
input_frame.pack(fill="x", pady=8)
task_input = ctk.CTkEntry(input_frame, placeholder_text="Enter your task") # 4

# Task list goes last so it appears below everything else
task_container = ctk.CTkScrollableFrame(app)
task_container.pack(fill="both", expand=True, padx=10, pady=10)

empty = ctk.CTkLabel(task_container, text="Your to-do list is empty",
                     font=("Outfit", 15))


# FUNCTIONS
# 1 Deletes label if list is empty
def update_empty_label():
    if tasks:
        empty.pack_forget()
    else:
        empty.pack(pady=10)

update_empty_label()
#2 Packs entry and button and focuses on entry
def add_task():
    task_input.pack(side='left', padx=15)
    enter.pack(side='left', padx=5)
    task_input.focus()

# creates row with needed widgets and functions
def create_row(number, task_data):
    print(f"Create row with data {task_data}")
    text = task_data[0]
    priority = task_data[1]
    hour = task_data[2]
    deadline = task_data[3]

    row = ctk.CTkFrame(task_container, border_width=1, border_color="blue")
    row.pack(fill="x", pady=3, padx=10)

    def on_check():
        if check.get():
            delete_button.pack(side='right', padx=5)
        else:
            delete_button.pack_forget()

    def delete_row():
        row.pack_forget()
        for i, item in enumerate(tasks, start=1):
            print(i, item)
            global number
            number = i
        label_num = number
        print(task_data)
        del tasks[label_num-1]

    check = ctk.BooleanVar(value=False)
    delete_button = ctk.CTkButton(row, width=6, text="🗑", text_color="red", fg_color='transparent',
                                  font=("Helvetica", 12, 'bold'), command=delete_row)
    ctk.CTkCheckBox(row, text='', width=10, variable=check, command=on_check).pack(side='left')
    ctk.CTkLabel(row, text=f"{number}- {text}", anchor="w",
                 font=("Outfit", 15, 'bold'), fg_color='#6F7173',
                 padx=10, corner_radius=5
                 ).pack(side="left", padx=(0, 8), pady=6)

    # Priority
    ctk.CTkLabel(row, text="Priority: ").pack(side='left', padx=5)

    def update(choice=None):
        priority_combo.configure(text_color=PRIORITY_COLORS.get(priority_combo.get(), '#FFFFFF'))
        # configure priority text color depending on the selected value
        task_data[1] = priority_combo.get()

    priority_combo = ctk.CTkComboBox(row, values=list(PRIORITY_COLORS.keys()),
                               command=update)
    priority_combo.set(priority)
    priority_combo.pack(side='left', padx=10)
    update()
    # priority gets created with the update function before it and once the combo is packed

    # Date
    var = CTkStringVar(row, value='Enter a deadline')
    date_entry = CTkDateEntry(row, variable=var)
    date_entry.pack(side="left")
    def save_deadline():
        global got
        got = var.get()
        task_data[3] = got
    atexit.register(save_deadline)
    try:
        var.set(task_data[3])
    except NameError:
        var.set('Enter a deadline')


    # Time
    def open_time_picker():
        popup = ctk.CTkToplevel(app)
        popup.title("Select Time")
        popup.geometry("300x350")
        popup.transient(app)   # keep popup above the main window
        popup.grab_set() # important?

        time_picker = AnalogPicker(popup)
        time_picker.pack(expand=True, fill="both", padx=10, pady=10)
        theme = AnalogThemes(time_picker)
        theme.setDracula()

        def select_time():
            hours, minutes, period = time_picker.time()
            time = f"{hours}:{minutes:02d} {period}"
            time_lab.configure(text=time)
            print(time)
            time_button.configure(text="Time selected")
            popup.destroy()
            task_data[2] = time

        ctk.CTkButton(popup, text="Select", command=select_time).pack(pady=(0, 15))
    time_button = ctk.CTkButton(row, text="Select time", width=100,
                                command=open_time_picker)

    time_lab = ctk.CTkLabel(row, text="0:00", font=("Outfit", 15, 'bold'))
    time_lab.pack(side="left", padx=5)
    time_lab.configure(text=task_data[2])
    time_button.pack(side="left", padx=10)


    return row


def append_task():
    text = task_input.get().strip()
    if not text:
        return
    task_data = [text, next(iter(PRIORITY_COLORS)), '0:00', 'Enter a deadline']
    tasks.append(task_data)
    update_empty_label()
    create_row(len(tasks), task_data)

    task_input.delete(0, 'end')
    task_input.pack_forget()
    enter.pack_forget()

if tasks:
    for i, item in enumerate(tasks):
        create_row(i, tasks[i-1])

# Buttons that depend on the functions above
add = ctk.CTkButton(button_frame, text="Add task", font=("Outfit", 15),
                    corner_radius=10, border_color="#4080FF", border_width=1,
                    command=add_task)
add.pack(side="left", padx=15)

enter = ctk.CTkButton(input_frame, text="Enter", font=("Outfit", 15),
                      corner_radius=10, width=30, command=append_task)

update_empty_label()
app.mainloop()