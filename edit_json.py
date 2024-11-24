import json
import os

# Path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'lattice.json')

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# List of file types
file_types = ["MoNb", "MoTa", "MoV", "MoW", "NbTa", "NbV", "NbW", "TaV", "TaW", "VW"]

for file_type in file_types:
    # Path to the text file
    text_file_path = os.path.join(os.path.dirname(__file__), f'{file_type}.txt')

    # check if the file exists
    if not os.path.exists(text_file_path):
        print(f'{text_file_path} does not exist')
    else:
        print(text_file_path)

        # Read the text file
        with open(text_file_path, 'r') as file:
            data_text = file.read()
            data_text_list = data_text.replace('\n', ',').split(',')  # Replace newlines with commas and split into a list

        # Replace the entire first element of the key with the new list
        if file_type in data:
            data[file_type][0] = data_text_list

# Write the modified JSON data back to the file
with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=4)
