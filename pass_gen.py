from tkinter import *
from tkinter import messagebox
from random import *
import string

#create the window
root = Tk()
root.title("PASSWORD GENERATOR")
root.geometry("500x400")
root.configure(background="#024950")


#function to generate the random strong password
def new_rand(event=None):
    # Get the password length from the entry widget
    pw_length = my_entry.get()
    
    # Check if the length is not provided
    if not pw_length:  
        messagebox.showerror(title="Error", message="Please enter the length of the password.")
        return

    try:
        pw_length = int(pw_length)  # Convert to integer
    except ValueError:
        messagebox.showerror(title="Error", message="Please enter a valid number for password length.")
        return

    if pw_length <= 0:
        messagebox.showerror(title="Error", message="Password length should be greater than 0.")
        return

    # Define the character pool for the password
    characters = string.ascii_letters + string.digits + '@-_'

    # Generate the password
    my_password = ''.join(choice(characters) for _ in range(pw_length))

    # Clear the entry box
    pw_entry.delete(0, END)

    # Output the password to the entry widget
    pw_entry.insert(0, my_password)

    # Enable the "Copy to clipboard" button
    clip_but['state'] = NORMAL


#copy to clipboard -----
def clipper():
    password = pw_entry.get()

    if password:
        #clear the clipboard
        root.clipboard_clear()
        #copy to clipboad 
        root.clipboard_append(password)
        messagebox.showinfo(title="Copy status", message="Copy successful!")
    else:
        messagebox.showerror(title="Error", message="Please generate a password first.")


def change_button_color_enter(event):
    my_but.config(bg="#7FFF00")  # Change button color to green when mouse enters

def change_button_color_leave(event):
    my_but.config(bg="#AFDDE5")  # Change button color back to original when mouse leaves



lf = LabelFrame(root,text="How many characters in password ?",fg= "black",font=("arieal",12,"bold"),bg="#AFDDE5")
lf.pack(pady=20)

lf1 = LabelFrame(root,text="Generated Password ..",fg= "black",font=("arieal",12,"bold"),bg="#AFDDE5")
lf1.pack(pady=20)

my_entry = Entry(lf,font=("serif",24),bd=2,bg="#0FA4AF")
my_entry.pack(pady=20,padx=20)


pw_entry = Entry(lf1, text='',font=("Sans-serif",24),bd=2,bg="#0FA4AF")
pw_entry.pack(padx=20,pady=20)

my_frame = Frame(root,bg="#024950")
my_frame.pack(pady=20)


#create buttons----
my_but = Button(my_frame,text= " Generate strong password ", bd=2,bg="#AFDDE5",command=new_rand)
my_but.pack(side=LEFT, padx=10)

clip_but = Button(my_frame,text =" Copy to clipboard",bd=2,bg="#AFDDE5",command=clipper)
clip_but.pack(side=RIGHT, padx=10)

# Bind events for hover effect
my_but.bind("<Enter>", change_button_color_enter)
my_but.bind("<Leave>", change_button_color_leave)

root.bind('<Return>', new_rand)

root.mainloop()