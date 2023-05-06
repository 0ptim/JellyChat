import json
import csv

# open the JSON file with the correct encoding
with open('qa.json', encoding='utf-8') as f:
    data = json.load(f)

# remove newlines from the "answer" strings
for entry in data:
    entry['answer'] = entry['answer'].replace('\n', ' ')

# write the filtered data to a CSV file
with open('qa.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    # write header row
    writer.writerow(['id', 'question', 'answer', 'rating', 'date'])
    for entry in data:
        writer.writerow([entry['id'], entry['question'],
                        entry['answer'], entry['rating'], entry['date']])
