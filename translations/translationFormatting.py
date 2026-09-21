import json
import os
import re

#---- Read and process translation files

data = []
folder = 'translations/data/'

# Iterate through each file in the folder

def load_translations(folder='translations/data/'):
    translations = []
    for file in os.listdir(folder):
        if file.endswith('.txt'):
            parts = file.split('.')

            # Expecting filename format: language.author.txt
            if len(parts) == 3:
                lang = parts[0]
                author = parts[1]

                # Read and process the file
                with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
                    content = []

                    # Read each line until an empty line is encountered
                    for line in f:
                        if line.strip() == '':
                            break
                        parts = line.strip().split('|') 
                        plain_text = re.sub(r'<[^>]+>', '', parts[2]).strip()
                        parts[2] = plain_text
                        content.append(parts)

                    # Append processed data to the main list
                    translations.append({
                        'language': lang,
                        'author': author,
                        'verses': content
                    })
    return translations

#---- Export processed data to JSON file

data = load_translations()
                
with open(f'{folder}/output.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data exported to output.json")

