from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password_entry.get())

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_name = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website_name:{
            "email": email,
            "password": password
        }
    }
    if len(website_name) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo("Oops", "Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel("Confirmation", f"website: {website_name}\nemail: {email}\npassword: {password}\n"
                                               f"Are you sure you want to add the following information?")
        if is_ok:
            info = f"{website_name} | {email} | {password}"
            try:
                with open("info.json", 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("info.json", 'w') as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("info.json", 'w') as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def search():
    website = website_entry.get()
    try:
        with open("info.json", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No Data File Found.")
    else:
        try:
            email = data[website]['email']
            password = data[website]['password']
        except KeyError:
            messagebox.showerror("Error!", f"No details for {website} exists.")
        else:
            print(f"Email: {email}\nPassword: {password}")
            messagebox.showinfo(website, f"Email: {email}\nPassword: {password}")
            pyperclip.copy(password)
    website_entry.delete(0, END)
    password_entry.delete(0, END)
# ---------------------------- UI SETUP ------------------------------- #
YELLOW = "#FFFF00"
window = Tk()
window.title("Password Manage App")
window.config(padx=50, pady=50)


image_path = "logo.png"
img = PhotoImage(file=image_path)


canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

email_username_entry = Entry(width=35)
email_username_entry.insert(0,"msanoko5@gmail.com")
email_username_entry.grid(column=1, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=2, row=1)


window.mainloop()
