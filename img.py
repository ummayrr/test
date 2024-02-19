import requests
import json
import os
import glob

cse_id = "e04372cb154a54723"
api_key = "AIzaSyAR5B6jKe0YECY0jcJc7PlWaFewTXoTTxc"

#delete 20 images
for i in range(1, 21):
    for file in glob.glob(f'image{i}.*'):
        if os.path.isfile(file):
            os.remove(file)
            print(f'Deleted: {file}')

num_files = len([name for name in os.listdir('.') if os.path.isfile(name) and name.startswith('text') and not name.endswith('original.txt')])

for i in range(1, num_files+1):
    with open(f'text{i}original.txt', 'r') as f:
        search_term = f.read().strip()

    url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&num=1&start=1&searchType=image&key={api_key}&cx={cse_id}"

    response = requests.get(url)
    response.raise_for_status()

    search_results = response.json()
    image_url = search_results['items'][0]['link']

    # determining extension
    file_extension = os.path.splitext(image_url)[1]
    if file_extension == '':
        file_extension = '.jpg'
    filename = f'image{i}{file_extension}'

    # downloading image
    response = requests.get(image_url)
    with open(filename, 'wb') as out_file:
        out_file.write(response.content)

    print('Image downloaded:', filename)