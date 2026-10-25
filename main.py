
import customtkinter as ctk
import json

# تنظیم ظاهر برنامه
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ساخت پنجره اصلی
app = ctk.CTk()
app.title("My Task Manager")
window_width = 500
window_height = 500

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{x}+{y}")
app.configure(fg_color="#18212F")

# عنوان برنامه
title_label = ctk.CTkLabel(
    app,
    text="My Tasks",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=20)

# کادر ورود کار جدید
task_entry = ctk.CTkEntry(
    app,
    placeholder_text="Enter a new task...",
    width=300
)
task_entry.pack(pady=10)

# محل نمایش کارها
task_list = ctk.CTkFrame(app)
task_list.pack(padx=20, pady=10, fill="both", expand=True)

def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)
def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
tasks = load_tasks()
def display_task(new_task):
    task = new_task["text"]

    def toggle_task():
        new_task["completed"] = bool(checkbox.get())
        save_tasks()

        if new_task["completed"]:
            checkbox.configure(
                font=("Arial", 14, "overstrike"),
                text_color="gray"
            )
        else:
            checkbox.configure(
                font=("Arial", 14),
                text_color=("black", "white")
            )

    task_frame = ctk.CTkFrame(
        task_list,
        corner_radius=10,
        fg_color=("gray90", "gray20")
    )
    task_frame.pack(fill="x", padx=10, pady=8)

    checkbox = ctk.CTkCheckBox(
        task_frame,
        text=task,
        command=toggle_task
    )
    checkbox.pack(side="left", padx=10, pady=0, anchor="center")

    def edit_task():
        edit_window = ctk.CTkToplevel(app)
        edit_window.title("Edit Task")
        edit_window.geometry("350x180")

        edit_window.update_idletasks()

        x = (edit_window.winfo_screenwidth() - 350) // 2
        y = (edit_window.winfo_screenheight() - 180) // 2

        edit_window.geometry(f"350x180+{x}+{y}")
        edit_window.configure(fg_color="#18212F")
        edit_window.transient(app)
        edit_window.grab_set()

        edit_entry = ctk.CTkEntry(
            edit_window,
            width=280,
            placeholder_text="Enter the new task name..."
        )
        edit_entry.pack(pady=(25, 15))
        edit_entry.insert(0, new_task["text"])
        edit_entry.focus()

        def save_edit():
            new_text = edit_entry.get().strip()

            if new_text:
                new_task["text"] = new_text
                checkbox.configure(text=new_text)
                save_tasks()
                edit_window.destroy()

        save_button = ctk.CTkButton(
            edit_window,
            text="Save Changes",
            command=save_edit
        )
        save_button.pack(pady=5)

        edit_entry.bind("<Return>", lambda event: save_edit())

    def delete_task():
        tasks.remove(new_task)
        save_tasks()
        task_frame.destroy()

    edit_button = ctk.CTkButton(
        task_frame,
        text="✎",
        width=30,
        height=30,
        fg_color="transparent",
        hover_color="#243B55",
        border_width=1,
        border_color="#355777",
        text_color="#6BA8E5",
        corner_radius=8,
        font=("Arial", 18, "bold"),
        command=edit_task
    )

    edit_button.pack(side="right", padx=5, pady=5, anchor="center")

    delete_button = ctk.CTkButton(
        task_frame,
        text="×",
        width=30,
        height=30,
        fg_color="transparent",
        hover_color="#3A202B",
        border_width=1,
        border_color="#6B263D",
        text_color="#A83250",
        corner_radius=8,
        font=("Arial", 20, "bold"),
        command=delete_task
    )
    delete_button.pack(side="right", padx=10, pady=5, anchor="center")

    if new_task["completed"]:
        checkbox.select()
        checkbox.configure(
            font=("Arial", 14, "overstrike"),
            text_color="gray"
        )
# تابع افزودن کار
def add_task():
    task = task_entry.get().strip()

    if task:
        new_task = {
            "text": task,
            "completed": False
        }

        tasks.append(new_task)
        save_tasks()

        display_task(new_task)

        task_entry.delete(0, "end")

# دکمه افزودن
add_button = ctk.CTkButton(
    app,
    text="Add New Task",
    command=add_task
)
add_button.pack(pady=15)

for task in tasks:
    display_task(task)

task_entry.bind("<Return>", lambda event: add_task())

# اجرای برنامه
app.mainloop()
