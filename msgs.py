import json

class Msg:
    def __init__(self, title, detail):
        self.title = title
        self.detail = detail

def write_msgs_to_json(msgs, filename):
    """Serialize a list of Msg objects to a JSON file."""
    data = {"msgs": [msg.to_dict() for msg in msgs]}  # Wrap in a top-level "msgs" key
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")

def read_msgs_from_json(filename):
    """Deserialize a JSON file to a list of Msg objects."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        msgs_data = data.get("msgs", [])  # Safely get the "msgs" list
        msgs = []
        for msg_data in msgs_data:
            msgs.append(Msg(msg_data["title"], msg_data["detail"]))
        return msgs
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []  # Return an empty list if the file doesn't exist
    except Exception as e:
        print(f"An error occurred while reading from {filename}: {e}")
        return []  # Return an empty list in case of other errors

def get_msg_txt(msgs, msg_title):
    if msgs:
        for msg in msgs:
            if msg.title == msg_title:
                return msg.detail
    return ""

# Example Usage:
# Create some Person and Group objects
msg1 = Msg("Titulo 1", "Texto de teste 1")
msg2 = Msg("Titulo 2", "Texto de teste 2")
msgs = [msg1, msg2]

# Serialize the list of groups to a JSON file
json_file = "msgs.json"
#write_groups_to_json(groups, json_file)

# Deserialize the list of groups from the JSON file
loaded_msgs = read_msgs_from_json(json_file)


# Print the loaded data to verify
#if loaded_groups:
#    for group in loaded_groups:
#        print(f"Group Name: {group.name}")
#        for person in group.persons:
#            print(f"  Person Name: {person.name}, Phone: {person.phone_number}")
#else:
#    print("No groups loaded or error occurred during loading.")
