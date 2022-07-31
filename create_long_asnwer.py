from transformers import AutoModelForMaskedLM, AutoTokenizer
import torch
import numpy as np
import pandas as pd
import csv
import sys

model_name = "HooshvareLab/bert-fa-zwnj-base"
model = AutoModelForMaskedLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def all_possible_answers(sent, sh_answer):
    com_answer = list()
    com_answer.append(sent + ' ' + sh_answer)
    for i in range(len(sent.split())):
        words_list = sent.split()
        words_list[i] = sh_answer + ' ' + words_list[i]
        our_answer = ' '.join(words_list)
        com_answer.append(our_answer)
    return com_answer


def loss_function(model, tokenizer, sentence):
    tensor_input = tokenizer.encode(sentence, return_tensors='pt')
    repeat_input = tensor_input.repeat(tensor_input.size(-1) - 2, 1)
    mask = torch.ones(tensor_input.size(-1) - 1).diag(1)[:-2]
    masked_input = repeat_input.masked_fill(mask == 1, tokenizer.mask_token_id)
    labels = repeat_input.masked_fill(masked_input != tokenizer.mask_token_id, -100)
    with torch.inference_mode():
        loss = model(masked_input, labels=labels).loss
    return np.exp(loss.item())


def create_csv(QA):
    rows = list()

    for i in range(len(QA)):
        row = [i, QA[i]['question'], QA[i]['answer'], QA[i]['complete'], QA[i]['loss']]
        rows.append(row)

    header = ['NO', 'Question', 'sh_answer', 'complete_answer', 'loss']

    with open('SynTranFa.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def read_files():
    df = pd.read_json('sample1.json')
    file1 = open('final.txt', 'r')
    Lines = file1.readlines()
    return Lines, df


def choose_best_answers(Lines, df):
    complete_answer = list()
    loss_list = list()
    for i, line in enumerate(Lines):
        print(i)
        line_arr = line.split()
        sh_answer = df['data'][i]['answer']
        min = sys.maxsize
        all = all_possible_answers(' '.join(line_arr), sh_answer)
        sent = ''
        for sit in all:
            loss = loss_function(sentence=sit, model=model, tokenizer=tokenizer)
            if loss < min:
                sent = sit
                min = loss
        loss_list.append(min)
        complete_answer.append(sent)
    return loss_list, complete_answer


def create_rows(loss_list, df, complete_answer):
    qa = list()
    for i in range(len(loss_list)):
        qa.append({'question': df['data'][i]['question'], 'answer': df['data'][i]['answer'], 'loss': loss_list[i],
                   'complete': complete_answer[i]})
    return qa


def do():
    Lines, df = read_files()
    loss_list, complete_answer = choose_best_answers(Lines, df)
    qa = create_rows(loss_list, df, complete_answer)
    QA = sorted(qa, key=lambda d: d['loss'], reverse=False)
    create_csv(QA)


if __name__ == '__main__':
    do()
