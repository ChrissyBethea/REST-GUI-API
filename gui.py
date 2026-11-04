
import tkinter as tk
from tkinter import messagebox
import requests
import re
import math

API_URL = "http://127.0.0.1:5001/purchase"

def submit_purchase():
    product_id = product_id_entry.get().strip()
    description = description_entry.get().strip()
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    price_text = price_entry.get().strip()

    if not all([product_id, description, name, email, price_text]):
        messagebox.showerror("Error", "Please complete all fields.")
        return

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    try:
        price = float(price_text)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid price.")
        return

    if not math.isfinite(price) or not 0 <= price <= 1000:
        messagebox.showerror("Error", "Price must be between $0 and $1,000.")
        return

    purchase = {
        "product_id": product_id,
        "description": description,
        "name": name,
        "email": email,
        "price": price,
        "online": online_var.get()
    }

    try:
        response = requests.post(API_URL, json=purchase, timeout=5)
        result = response.json()

        if response.ok:
            messagebox.showinfo("Success", result["message"])
        else:
            messagebox.showerror(
                "API Error", result.get("error", "Submission failed.")
            )

    except requests.RequestException:
        messagebox.showerror(
            "Connection Error", "Could not connect to the Flask API."
        )
    except ValueError:
        messagebox.showerror("Error", "Invalid response from the API.")


root = tk.Tk()
root.title("Purchase Information Form")
root.geometry("400x380")

fields = [
    ("Product ID", "product_id"),
    ("Description", "description"),
    ("Customer Name", "name"),
    ("Customer Email", "email"),
    ("Price ($)", "price")
]

entries = {}

for label_text, field_name in fields:
    tk.Label(root, text=label_text).pack(pady=(8, 0))
    entry = tk.Entry(root, width=40)
    entry.pack()
    entries[field_name] = entry

product_id_entry = entries["product_id"]
description_entry = entries["description"]
name_entry = entries["name"]
email_entry = entries["email"]
price_entry = entries["price"]

online_var = tk.BooleanVar(value=False)

tk.Checkbutton(
    root,
    text="Online Purchase (unchecked = In-Store)",
    variable=online_var
).pack(pady=12)

tk.Button(
    root,
    text="Submit Purchase",
    command=submit_purchase
).pack(pady=10)

root.mainloop()
