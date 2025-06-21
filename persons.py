import json

class Person:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def to_dict(self):
        """Convert Person object to a dictionary."""
        return {
            "name": self.name,
            "phone_number": self.phone_number
        }

class Group:
    def __init__(self, name, persons):
        self.name = name
        self.persons = persons

    def to_dict(self):
        """Convert Group object to a dictionary."""
        return {
            "name": self.name,
            "persons": [person.to_dict() for person in self.persons]
        }

def write_groups_to_json(groups, filename):
    """Serialize a list of Group objects to a JSON file."""
    data = {"groups": [group.to_dict() for group in groups]}  # Wrap in a top-level "groups" key
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")

def read_groups_from_json(filename):
    """Deserialize a JSON file to a list of Group objects."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        groups_data = data.get("groups", [])  # Safely get the "groups" list
        groups = []
        for group_data in groups_data:
            persons = [Person(p["name"], p["phone_number"]) for p in group_data.get("persons", [])] #Handles empty persons list
            groups.append(Group(group_data["name"], persons))
        return groups
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []  # Return an empty list if the file doesn't exist
    except Exception as e:
        print(f"An error occurred while reading from {filename}: {e}")
        return []  # Return an empty list in case of other errors

def get_phone_by_person_name(groups, person_name):
    if groups:
        for group in groups:
            for person in group.persons:
                if person.name == person_name:
                    return person.phone_number
    return None

def get_names_by_group(groups, group_name):
    names = {}
    if groups:
        for group in groups:
            if group.name == group_name:
                for person in group.persons:
                    names[person.name] = True
    return names

def get_all_names_in_order(groups):
    all_names = set()  # Use a set to store unique names
    for group in groups:
        for person in group.persons:
            all_names.add(person.name)  # Add names to the set; duplicates are ignored

    # Convert the set to a list and sort it
    ordered_unique_names = sorted(list(all_names))
    return ordered_unique_names

# Example Usage:
# Create some Person and Group objects
person1 = Person("Alice", "123-456-7890")
person2 = Person("Bob", "987-654-3210")
person3 = Person("Charlie", "555-123-4567")

group1 = Group("Group A", [person1, person2])
group2 = Group("Group B", [person2, person3])
group3 = Group("Empty Group", []) # test case with empty group
groups = [group1, group2, group3]

# Serialize the list of groups to a JSON file
json_file = "groups.json"
#write_groups_to_json(groups, json_file)

# Deserialize the list of groups from the JSON file
loaded_groups = read_groups_from_json(json_file)


# Print the loaded data to verify
#if loaded_groups:
#    for group in loaded_groups:
#        print(f"Group Name: {group.name}")
#        for person in group.persons:
#            print(f"  Person Name: {person.name}, Phone: {person.phone_number}")
#else:
#    print("No groups loaded or error occurred during loading.")
