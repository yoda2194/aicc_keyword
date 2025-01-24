import json
import re
import os
from collections import defaultdict

def cleaning_text(text):
    x = re.sub(r'#@[가-힣]{1,}#', '', text)
    x = re.sub(r'[A-Z]{1}.', '', x)
    x = re.sub("\n", '. ', x)
    x = x.strip()
    return x

def get_morpheme(lines):
    morpheme = []
    for line in lines:
        morpheme_list = re.findall('[가-힣]{1,}', line)
        morpheme.append(morpheme_list)
    return morpheme


def read_json_file(root_directory, save_list):
    f_list = os.listdir(root_directory)
    text_list = []
    for f in f_list:
        dialog = {}
        file_path = os.path.join(root_directory, f)
        target_file = open(file_path, encoding="UTF-8")
        json_file = json.loads(target_file.read())

        text = json_file['info'][0]['annotations']['text']
        text = cleaning_text(text)
        category = json_file['info'][0]['annotations']['subject']
        # lines = json_file['info'][0]['annotations']['lines']
        # morpheme = []
        # for line in lines:
        #     morpheme.append(line['morpheme'])
        text_list.append(text)
        dialog['text'] = text_list
        dialog['category'] = category
        # dialog['morpheme'] = get_morpheme(morpheme)
        save_list.append(dialog)

folder = './json_file/'
dialog_list = []
for category in os.listdir(folder):
    read_json_file(folder + category, dialog_list)

with open("tokenized.json", "w", encoding="utf-8") as json_file:
    json.dump(dialog_list, json_file, indent=4)
