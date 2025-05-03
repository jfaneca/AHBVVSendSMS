import tkinter as tk
from tkinter import ttk
import requests
from requests.auth import HTTPBasicAuth
import threading
from configparser import ConfigParser
from persons import *
from android_sms_gateway import client, domain

def call_api(text_content, selected_option, output_label):
    """Calls a dummy HTTP endpoint and updates the output label."""
    api_url = "http://" + ipaddr + ":" + port + "/message"
    api_url = "http://" + ipaddr + ":" + port + "/"

    phoneNumbers = get_phone_numbers(loaded_groups,selected_option)

    message = domain.Message(
        text_content,
        phoneNumbers
    )

    with client.APIClient(
        username,
        password,
        base_url=api_url
    ) as c:
        state = c.send(message)
        #print(state)

        state = c.get_state(state.id)
        #print(state)

    payload = {
        "message": text_content,
        "phoneNumbers": phoneNumbers
    }

    try:
        response = requests.post(api_url, json=payload, auth = HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        output_label.config(text=f"API Response:\n{data}")
    except requests.exceptions.RequestException as e:
        output_label.config(text=f"Error calling API: {e}")

def on_button_click():
    """Handles the button click event."""
    text_content = text_field.get("1.0", tk.END).strip()
    selected_option = dropdown.get()
    output_label.config(text="Calling API...")
    # Use a separate thread to avoid blocking the GUI
    threading.Thread(target=call_api, args=(text_content, selected_option, output_label)).start()

config_object = ConfigParser()
config_object.read("config.ini")
credentials = config_object["CREDENTIALS"]
username = credentials["username"]
password = credentials["password"]
connections = config_object["CONNECTIONS"]
ipaddr = connections["ipaddr"]
port = connections["port"]

# Create the main window
root = tk.Tk()
root.title("Text Input and API Call")

# Multiline Text Field
text_label = tk.Label(root, text="Enter Text:")
text_label.pack(pady=5)
text_field = tk.Text(root, height=5, width=40)
text_field.pack(padx=10, pady=5)

# Dropdown
dropdown_label = tk.Label(root, text="Select Option:")
dropdown_label.pack(pady=5)

options = []

if loaded_groups:
    for group in loaded_groups:
        options.append(group.name)

dropdown = ttk.Combobox(root, values=options)
dropdown.set(options[0])  # Set a default value
dropdown.pack(padx=10, pady=5)

# Button
call_button = tk.Button(root, text="Call API", command=on_button_click)
call_button.pack(pady=10)

# Output Label
output_label = tk.Label(root, text="")
output_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()