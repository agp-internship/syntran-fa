import stanza

nlp = stanza.Pipeline('fa')
import pandas as pd

question_sign = (
    '؟', ' آیا ', ' چرا ', ' چگونه ', ' کی ', ' کجا ', ' چندمین ', ' چندم ', ' کدام ', ' چی ', ' چقدر ', ' چند ')
che_list = ('رنگی', 'موقعی', 'کسیایی', 'کسانی', 'کسی', 'نوعی', 'چیزی', 'کاره', 'موقع', 'سالی')


def timer(i):
    if i % 200 == 0:
        print(i)


def extract_words(sent_list):
    final_list = list()
    for i in range(len(sent_list)):
        if sent_list[i - 1]['text'] == 'چه' and sent_list[i]['text'] in che_list:
            i += 1
            continue
        elif i > 0 and sent_list[i - 1]['text'] == 'چه' and sent_list[i]['roll'] == 'NOUN' and sent_list[i]['text'][
            -1] == 'ی':
            final_list.append({'text': sent_list[i]['text'][:-1], 'roll': sent_list[i]['roll']})
        else:
            final_list.append(sent_list[i])
    sentence = ""
    for i in range(len(final_list)):
        sentence += final_list[i]['text']
        sentence += ' '

    return final_list, sentence


def wich_one_of(sentence):
    doc = nlp(sentence)
    sent = sentence
    if 'کدامیک از' in sent:
        words = sent.split()
        for i in range(2, len(sent.split())):
            if doc.sentences[0].words[i].feats == 'Number=Plur' and words[i - 1] == 'از' and words[i - 2] == 'کدامیک':
                sent = sent.replace(doc.sentences[0].words[i].text, doc.sentences[0].words[i].lemma)
        sent = sent.replace('کدامیک از', '')
    return sent


def che_remover(old_str):
    return old_str.replace(' چه ', ' ')


def first_phase(df):
    number_of_QA = 35620
    key_word = list()
    for i in range(number_of_QA):
        timer(i)
        doc = nlp(df.data[i]['question'])
        my_list = list()
        for sent in doc.sentences:
            for word in sent.words:
                if word.text == '؟':
                    continue
                elif word.text == 'ست':
                    my_list.append({'text': 'است', 'roll': 'AUX'})
                elif word.text in question_sign:
                    continue
                else:
                    my_list.append({'text': word.text, 'roll': word.upos})
        key_word.append(my_list)
    return key_word


def second_phase(key_word):
    lines = list()
    for i in range(len(key_word)):
        timer(i)
        ff, string = extract_words(key_word[i])
        string = " " + string + " "
        string = che_remover(string)
        string = wich_one_of(string)
        for q in question_sign:
            string = string.replace(q, ' ')
        lines.append(string)
    return lines


def do():
    df = pd.read_json('./sample1.json')
    lines = second_phase(first_phase(df))
    with open('final.txt', 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    do()
    print("_")
