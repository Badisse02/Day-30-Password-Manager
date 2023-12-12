from tkinter import *
from random import *
from tkinter import messagebox
import pyperclip
from json import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generator():
    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letters_list + symbols_list + numbers_list
    shuffle(password_list)

    generated_password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)

# ---------------------------- SEARCH FUNCTION ------------------------------- #


def search_website():
    website_name = website_entry.get()
    if len(website_name) > 0:
        try:
            with open("data.json", "r") as data_file:
                # Reading
                data = load(data_file)
            if website_name in data:
                messagebox.showinfo(f"{website_name}", f"\t\nEmail: {data[website_name]['Email']} \t"
                                                       f"\nPassword: {data[website_name]['Password']}\t\n\n")
            else:
                messagebox.showinfo("Oops", "Sorry\nThis website doesn't exist")
        except FileNotFoundError:
            messagebox.showinfo("Oops", "   File doesn't exist.\n   "
                                        "Enter your data and it will be created automatically 😊")
        except JSONDecodeError:
            messagebox.showerror("Oops", "      Empty File      ")
    else:
        messagebox.showinfo("Oops", "Please enter a website name.")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_info():
    mail = email_entry.get()
    website_name = website_entry.get()
    the_password = password_entry.get()
    new_data = {website_name: {
        "Email": mail,
        "Password": the_password,
    }}

    if len(website_name) == 0:
        messagebox.showerror(title="Something missing", message="WebSite is missing")
        website_entry.focus()
    elif len(mail) == 0 or mail == "@gmail.com" or mail[0] == "@":
        messagebox.showerror(title="Something missing", message="Email is missing or wrong")
        email_entry.focus()
    elif len(the_password) == 0:
        messagebox.showerror(title="Something missing", message="Password is missing")
        password_entry.focus()
    else:

        try:
            with open("data.json", "r") as data_file:
                # Reading
                data = load(data_file)
                # Updating
                data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving
                dump(data, data_file, indent=4)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving
                dump(new_data, data_file, indent=4)

        except JSONDecodeError:
            with open("data.json", "w") as data_file:
                # Saving
                dump(new_data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.insert(0, "@gmail.com")
            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.minsize(600, 500)
window.config(padx=50, pady=50)
window.title("Password Manager")

canvas = Canvas(highlightthickness=0, width=200, height=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(row=1, column=2, pady=20)

website = Label(text="Website:", font=("arial", 10, "normal"))
website.grid(row=2, column=1, padx=20)

email = Label(text="Email/Username:", font=("arial", 10, "normal"))
email.grid(row=3, column=1, padx=20)

password = Label(text="Password:", font=("arial", 10, "normal"))
password.grid(row=4, column=1, padx=20)

website_entry = Entry(window, width=30)
website_entry.grid(row=2, column=2, columnspan=2, sticky=W, padx=20)
website_entry.focus()

search_button = Button(text="Search", width=8, command=search_website)
search_button.grid(row=2, column=2, columnspan=2, sticky=E, padx=20)

email_entry = Entry(window, width=43)
email_entry.grid(row=3, column=2, columnspan=2, sticky=W, padx=20)
email_entry.insert(0, "@gmail.com")

password_entry = Entry(window, width=21)
password_entry.grid(row=4, column=2, sticky=W, padx=20)

generate_button = Button(text="Generate Password", command=password_generator)
generate_button.grid(row=4, column=2, columnspan=2, sticky=E, padx=20)

notice = Label(text="* Generated Password will be copied automatically! *",
               font=("arial", 8, "normal"), fg="red")
notice.grid(row=5, column=2, columnspan=2,  padx=20)

add = Button(text="Add", width=36, command=add_info)
add.grid(row=6, column=2, columnspan=2, sticky=W, padx=20)

window.mainloop()
