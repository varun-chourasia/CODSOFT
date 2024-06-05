import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as mysql

# Connect to MySQL Database
db_connection = mysql.connect(
    host="localhost",
    user="root",
    passwd="1207",
    database="work"
)
db_cursor = db_connection.cursor()

# Create the 'tasks' table if it doesn't exist
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL
    )
""")
db_connection.commit()

# Function to add task to the MySQL database and text file
def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        # Update MySQL database
        query = "INSERT INTO tasks (title) VALUES (%s)"
        db_cursor.execute(query, (task_string,))
        db_connection.commit()

        ''' if you want to store the data into the text file '''
        # Update text file
        with open("tasks.txt", "a") as file:
            file.write(task_string + "\n")
        list_update()
        task_field.delete(0, 'end')

# Function to delete task from MySQL database and text file
def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            # Delete from MySQL database
            query = "DELETE FROM tasks WHERE title = %s"
            db_cursor.execute(query, (the_value,))
            db_connection.commit()
            # Delete from text file
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
            with open("tasks.txt", "w") as file:
                for line in lines:
                    if line.strip() != the_value:
                        file.write(line)
            list_update()
    except Exception as e:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

# Function to delete all tasks from MySQL database and text file
def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box == True:
        tasks.clear()
        # Delete all from MySQL database
        query = "DELETE FROM tasks"
        db_cursor.execute(query)
        db_connection.commit()
        # Clear text file
        open("tasks.txt", "w").close()
        list_update()

# Function to retrieve tasks from MySQL database and text file
def retrieve_database():
    tasks.clear()
    # Retrieve from MySQL database
    query = "SELECT title FROM tasks"
    db_cursor.execute(query)
    for row in db_cursor.fetchall():
        tasks.append(row[0])
    # Retrieve from text file
    with open("tasks.txt", "r") as file:
        for line in file:
            tasks.append(line.strip())

# Function to update the list box with tasks
def list_update():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Main function ---

if __name__ == "__main__":
    #create the window ---
    guiWindow = tk.Tk()
    guiWindow.title("To-Do List Manager")
    guiWindow.geometry("500x450+750+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#EDC7B7")

    tasks = []

    header_frame = tk.Frame(guiWindow, bg="#EDC7B7")
    functions_frame = tk.Frame(guiWindow, bg="#EDC7B7")
    listbox_frame = tk.Frame(guiWindow, bg="#EDC7B7")

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(
        header_frame,
        text="The To-Do List",
        font=("Brush Script MT", "30"),
        background="#EDC7B7",
        foreground="#AC3B61"
    )
    header_label.pack(padx=20, pady=20)

    task_label = ttk.Label(
        functions_frame,
        text="Enter the Task:",
        font=("Consolas", "11", "bold"),
        background="#EDC7B7",
        foreground="#000000"
    )
    task_label.place(x=30, y=40)

    task_field = ttk.Entry(
        functions_frame,
        font=("Consolas", "12"),
        width=18,
        background="#FFF8DC",
        foreground="#A52A2A"
    )
    task_field.place(x=30, y=80)

    #buttons ---
    style = ttk.Style()
    style.configure("Custom.TButton", background="#BAB2B5", foreground="#5085A5")

    add_button = ttk.Button(
        functions_frame,
        text="Add Task",
        width=24,
        command=add_task,
        style="Custom.TButton"
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete Task",
        width=24,
        command=delete_task,
        style="Custom.TButton"
    )
    del_all_button = ttk.Button(
        functions_frame,
        text="Delete All Tasks",
        width=24,
        command=delete_all_tasks,
        style="Custom.TButton"
    )
    exit_button = ttk.Button(
        functions_frame,
        text="Exit",
        width=24,
        command=guiWindow.quit,
        style="Custom.TButton"
    )
    add_button.place(x=30, y=120)
    del_button.place(x=30, y=160)
    del_all_button.place(x=30, y=200)
    exit_button.place(x=30, y=240)

    task_listbox = tk.Listbox(
        listbox_frame,
        width=26,
        height=13,
        selectmode='SINGLE',
        background="#FFFFFF",
        foreground="#000000",
        selectbackground="#CD853F",
        selectforeground="#FFFFFF"
    )
    task_listbox.place(x=10, y=20)

    retrieve_database()
    list_update()
    guiWindow.mainloop()

    db_cursor.close()
    db_connection.close()
