import json
import re
import os
from collections import defaultdict

def cleaning_text(text):
    x = re.sub(r'#*@+[가-힣]{1,}#', '', text)
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

def read_json_file(root_directory, save_dict):
    f_list = os.listdir(root_directory)
    for f in f_list:
        dialog = {}
        file_path = os.path.join(root_directory, f)
        target_file = open(file_path, encoding="UTF-8")
        json_file = json.loads(target_file.read())

        text = json_file['info'][0]['annotations']['text']
        text = cleaning_text(text)
        category = json_file['info'][0]['annotations']['subject']
        lines = json_file['info'][0]['annotations']['lines']
        line_list = []
        morpheme = []
        for line in lines:
            morpheme.append(line['morpheme'])
            line_list.append(cleaning_text(line['text']))
        dialog['text'] = text
        dialog['lines'] = line_list
        dialog['morpheme'] = get_morpheme(morpheme)
        save_dict[f'{category}'].append(dialog)


def read_json_file_ver2(json_list):
    word_list = []
    txt = str()
    unique_key_pre = json_list[0]['대화셋일련번호']
    sent_num_pre = int(json_list[0]['문장번호'])
    dict_list = []

    for dialog in json_list:
        extract_key = ['고객질문(요청)', '상담사질문(요청)', '고객답변', '상담사답변']
        unique_key = dialog['대화셋일련번호']
        sent_num = int(dialog['문장번호'])

        if (unique_key_pre == unique_key) & (sent_num_pre <= sent_num):
            words = dialog['지식베이스'].split(',')
            if len(words) >= 1:
                for w in words:
                    if w:
                        word_list.append(w)
            else:
                pass

            for key in extract_key:
                if dialog.get(key):
                    txt += dialog[f'{key}'] + ' '
        else:
            category = dialog['카테고리']

            d_dict = {
                'category': category,
                'text': txt,
                'keyword': word_list,
            }
            dict_list.append(d_dict)

            word_list = []
            text_list = []
            txt = str()
            words = dialog['지식베이스'].split(',')
            if len(words) <= 2:
                for w in words:
                    if w:
                        word_list.append(w)
            for key in extract_key:
                if dialog.get(key):
                    dialog[f'{key}'].strip()
                    txt += dialog[f'{key}'] + ' '
                    text_list.append(txt)

        unique_key_pre = unique_key
        sent_num_pre = sent_num
    return dict_list


### json 파일 열어서 하나로 통합 + 대화를 하나의 텍스트로 통합
folder = './json_file/'
dialog_dict = defaultdict(list)
for category in os.listdir(folder):
    read_json_file(folder + category, dialog_dict)

with open("./상품 가입 및 해지_Training.json", "r", encoding='utf-8') as f:
    train_json = json.load(f)
with open("./금융보험_사고 및 보상 문의_Training.json", "r", encoding='utf-8') as f:
    train_json2 = json.load(f)
dialog_dict_ver2 = read_json_file_ver2(train_json) + read_json_file_ver2(train_json2)


### json file로 저장하기
with open("tokenized_morphs.json", "w", encoding="utf-8") as f:
    json.dump(dialog_dict, f, indent=4)


with open("not_tokenized_dialogs.json", "w", encoding="utf-8") as f2:
    json.dump(dialog_dict_ver2, f2, indent=4)


