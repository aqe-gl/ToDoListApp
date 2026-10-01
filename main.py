import customtkinter as ctk
from ctkdateentry import CTkDateEntry, CTkStringVar
from tktimepicker import AnalogPicker, AnalogThemes

# APP SETUP
app = ctk.CTk()
app.geometry("900x600")
app.title("To-Do App")
ctk.set_appearance_mode("dark")
app.after(200, lambda: app.iconbitmap("to-do.ico"))  # Windows only
ctk.FontManager.load_font("Outfit-Black.ttf")

# LIST BACKEND
tasks = []

PRIORITY_COLORS = {
    'Low ⚑': '#42AF2F',
    'Medium ⚑': '#F2C712',
    'High ⚑': '#F20004',
}


# WIDGETS (created in the order you want them to appear)
title = ctk.CTkLabel(app, text="To-Do App", font=("Outfit", 30, "bold"))
title.pack(pady=10)

color = app.cget("fg_color")

button_frame = ctk.CTkFrame(app, fg_color=color, height=20)
button_frame.pack(fill="x", pady=8)

input_frame = ctk.CTkFrame(app, fg_color=color, height=20)
input_frame.pack(fill="x", pady=8)
task_input = ctk.CTkEntry(input_frame, placeholder_text="Enter your task")

# Task list goes last so it appears below everything else
task_container = ctk.CTkScrollableFrame(app)
task_container.pack(fill="both", expand=True, padx=10, pady=10)

empty = ctk.CTkLabel(task_container, text="Your to-do list is empty",
                     font=("Outfit", 15))


# FUNCTIONS
def update_empty_label():
    if tasks:
        empty.pack_forget()
    else:
        empty.pack(pady=10)


def add_task():
    task_input.pack(side='left', padx=15)
    enter.pack(side='left', padx=5)
    task_input.focus()


def create_row(number, text):
    """Builds one task row (everything it needs is defined in here)."""
    row = ctk.CTkFrame(task_container, border_width=1, border_color="blue")
    row.pack(fill="x", pady=3, padx=10)

    ctk.CTkCheckBox(row, text='', width=10).pack(side='left')
    ctk.CTkLabel(row, text=f"{number}. {text}", anchor="w",
                 font=("Outfit", 15, 'bold'), fg_color='#6F7173',
                 padx=10, corner_radius=5
                 ).pack(side="left", padx=(0, 8), pady=6)

    # Priority
    ctk.CTkLabel(row, text="Priority: ").pack(side='left', padx=5)

    def update(choice=None):
        priority.configure(text_color=PRIORITY_COLORS.get(priority.get(), '#FFFFFF'))

    priority = ctk.CTkComboBox(row, values=list(PRIORITY_COLORS.keys()),
                               command=update)
    priority.pack(side='left', padx=10)
    update()

    # Date
    var = CTkStringVar(row, value='Enter a deadline')
    date_entry = CTkDateEntry(row, variable=var)
    date_entry.pack(side="left")

    # Time
    def open_time_picker():
        popup = ctk.CTkToplevel(app)
        popup.title("Select Time")
        popup.geometry("300x350")
        popup.transient(app)   # keep popup above the main window
        popup.grab_set()

        time_picker = AnalogPicker(popup)
        time_picker.pack(expand=True, fill="both", padx=10, pady=10)
        theme = AnalogThemes(time_picker)
        theme.setDracula()

        def select_time():
            hours, minutes, period = time_picker.time()
            time_lab.configure(text=f"{hours}:{minutes:02d} {period}")
            time_button.configure(text="Time selected")
            popup.destroy()

        ctk.CTkButton(popup, text="Select", command=select_time).pack(pady=(0, 15))

    time_button = ctk.CTkButton(row, text="Select time", width=100,
                                command=open_time_picker)
    time_lab = ctk.CTkLabel(row, text="0:00", font=("Outfit", 15, 'bold'))
    time_lab.pack(side="left", padx=5)
    time_button.pack(side="left", padx=10)

    return row


def append_task():
    text = task_input.get().strip()
    if not text:
        return
    tasks.append(text)
    update_empty_label()
    create_row(len(tasks), text)

    task_input.delete(0, 'end')
    task_input.pack_forget()
    enter.pack_forget()


# Buttons that depend on the functions above
add = ctk.CTkButton(button_frame, text="Add task", font=("Outfit", 15),
                    corner_radius=10, border_color="#4080FF", border_width=1,
                    command=add_task)
add.pack(side="left", padx=15)

enter = ctk.CTkButton(input_frame, text="Enter", font=("Outfit", 15),
                      corner_radius=10, width=30, command=append_task)

update_empty_label()
app.mainloop()