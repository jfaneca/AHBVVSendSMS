import tkinter as tk
from tkinter import ttk
import threading
from configparser import ConfigParser

import msgs
from msgs import loaded_msgs
from persons import *
from android_sms_gateway import client, domain, MessageState
import time

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
        while state.state == 'Pending':
            time.sleep(0.5)
            state = c.get_state(state.id)

        if state.state == 'Failed':
           output_label.config(text=f"Envio falhado")
        else:
            output_label.config(text=f"Envio efetuado com sucesso!")

def on_button_click():
    """Handles the button click event."""
    text_content = text_field.get("1.0", tk.END).strip()
    selected_option = dropdownGrps.get()
    output_label.config(text="A enviar ...")
    # Use a separate thread to avoid blocking the GUI
    threading.Thread(target=call_api, args=(text_content, selected_option, output_label)).start()

def on_combobox_grp_selection(event):
    # let us celar all values
    for var in checkbox_vars:
        var.set(False)

def on_combobox_msg_selection(event):
    """
    This function is called when the combobox selection changes.
    """
    text_field.delete("1.0", tk.END)

    selected_item = dropdownMsg.get()
    new_msg = msgs.get_msg_txt(loaded_msgs, selected_item)
    text_field.insert("1.0",new_msg)

def populate_checkbox_names(main_window, scrollable_frame, checkbox_vars):
    all_names = get_all_names_in_order(loaded_groups)
    """Generates checkboxes for each person in the list."""
    for i, person_name in enumerate(all_names):
        var = tk.BooleanVar()
        checkbox_vars.append(var)
        checkbox = ttk.Checkbutton(scrollable_frame, text=person_name, variable=var)
        checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=2)

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
root.title("Envio de SMS")

# Create the main container frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left frame with scrollable checkboxes
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

canvas = tk.Canvas(left_frame, width=200)
scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
    scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Right frame for all other UI elements
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

# Multiline Text Field
text_label = tk.Label(right_frame, text="Texto do SMS:")
text_label.pack(pady=5)
text_field = tk.Text(right_frame, height=5, width=40)
text_field.pack(padx=10, pady=5)

# Dropdown
dropdown_label = tk.Label(right_frame, text="Escolha o grupo:")
dropdown_label.pack(pady=5)

checkbox_vars = []  # To store BooleanVar for each checkbox

options = []

if loaded_groups:
    for group in loaded_groups:
        options.append(group.name)

dropdownGrps = ttk.Combobox(right_frame, values=options)
dropdownGrps.set(options[0])  # Set a default value
dropdownGrps.pack(padx=10, pady=5)
# Bind the <<ComboboxSelected>> event to the on_combobox_selection function
dropdownGrps.bind("<<ComboboxSelected>>", on_combobox_grp_selection)

# Dropdown
dropdownMsg_label = tk.Label(right_frame, text="Escolha o texto da mensagem:")
dropdownMsg_label.pack(pady=5)

msgOptions = []

if loaded_msgs:
    for msg in loaded_msgs:
        msgOptions.append(msg.title)

dropdownMsg = ttk.Combobox(right_frame, values=msgOptions)
dropdownMsg.set(msgOptions[0])  # Set a default value
dropdownMsg.pack(padx=10, pady=5)
# Bind the <<ComboboxSelected>> event to the on_combobox_selection function
dropdownMsg.bind("<<ComboboxSelected>>", on_combobox_msg_selection)

# Button
call_button = tk.Button(right_frame, text="Enviar", command=on_button_click)
call_button.pack(pady=10)

# Output Label
output_label = tk.Label(right_frame, text="")
output_label.pack(pady=10)

populate_checkbox_names(left_frame, scrollable_frame, checkbox_vars)

# Start the Tkinter event loop
root.mainloop()
