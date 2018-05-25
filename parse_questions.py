import csv
import os
from pydub import AudioSegment
import json

path = 'alignments.json'
audio_path = 'questions_wav/'
def pase_questions():
    with open('questions_subtitles_updated.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        i = 0
        for row in reader:
            if '@' not in row['transcript'] and '?' in row['transcript']:
                # print(row['transcript'])
                phrases = row['transcript'].split(' # ')
                for phrase in phrases:
                    if '?' in phrase:
                        # print(phrase, i, row['quest_num'].strip('questions_wav/'))
                        with open(path, encoding='utf-8') as data_file:
                            for line in data_file:
                                newline = json.loads(line)
                                if row['quest_num'].strip('questions_wav/') in newline['path']:
                                    data = {}
                                    data['text'] = phrase
                                    data['ID'] = str(newline['ID'])
                                    data['relpath'] = newline['path']
                                    data['purpose'] = 'question'
                                    # print(data)

                                    """
                                    with open('index_new.json', 'a', encoding='utf-8') as json_file:
                                        json.dump(data, json_file, ensure_ascii=False)
                                        json_file.write("\n")
                                    """

                                    for w in newline['words']:
                                        if w['text'] == phrase.split(' ')[0]:
                                            tstamp1 = w['start']
                                    for wrd in phrase.split(' '):
                                        for item in newline['words']:
                                            if item['text'] == wrd:
                                                tstamp2 = item['stop']
                                        else:
                                            tstamp2 = item['stop']
                                    print(phrase.split(' '), tstamp1, tstamp2, newline)
                                    print(phrase, tstamp1, tstamp2, newline)

                                    audio = "questions_wav/" + newline['path']
                                    # print('cut_sent/%s.wav' % (newline['path'].strip('.wav')))
                                    time1 = tstamp1 * 1000
                                    time2 = tstamp2 * 1000
                                    readAudio = AudioSegment.from_wav(audio)
                                    newAudio = readAudio[time1:time2]
                                    newQuestion = newAudio.export(
                                        'cut_sent_new/%s.wav' % (newline['path'].strip('.wav')),
                                        format='wav')


def parse_sentences():
    with open('questions_subtitles_updated.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        i = 0
        for row in reader:
            if '@' not in row['transcript'] and '?' not in row['transcript']:
                if '#' in row['transcript']:
                    phrases = row['transcript'].split(' # ')
                else:
                    phrases = []
                    phrases.append(row['transcript'])
                i = 1
                for phrase in phrases:
                    phrase = phrase.replace(r'*Н ', '')
                    phrase = phrase.replace(r'*П ', '')
                    phrase = phrase.replace(r'*C ', '')
                    phrase = phrase.replace(r'*С ', '')
                    phrase = phrase.replace(r'*В ', '')
                    phrase = phrase.replace(r'...', '')
                    phrase = phrase.replace(r' //', '')
                    phrase = phrase.replace(r' /', '')
                    phrase = phrase.replace(r'%', '')
                    phrase = phrase.replace(r'-', '')
                    phrase = phrase.replace(r'(', '')
                    phrase = phrase.replace(r')', '')
                    print(phrase)
                    with open(path, encoding='utf-8') as data_file:
                        for line in data_file:
                            newline = json.loads(line)
                            if row['quest_num'].strip('questions_wav/') in newline['path']:
                                data = {}
                                data['text'] = phrase
                                data['ID'] = str(newline['ID'])
                                data['relpath'] = newline['path']
                                data['purpose'] = 'declaration'
                                print(data)

                                for w in newline['words']:
                                    if w['text'] == phrase.split(' ')[0]:
                                        tstamp1 = w['start']
                                    for wrd in phrase.split(' '):
                                        for item in newline['words']:
                                            if item['text'] == wrd:
                                                tstamp2 = item['stop']

                                print(phrase.split(' '), tstamp1, tstamp2, newline)

                                audio = "questions_wav/" + newline['path']
                                time1 = tstamp1 * 1000
                                time2 = tstamp2 * 1000
                                readAudio = AudioSegment.from_wav(audio)
                                newAudio = readAudio[time1:time2]
                                newQuestion = newAudio.export(
                                    'cut_sent_new/%s_%s.wav' % (newline['path'].strip('.wav'), i),
                                    format='wav')
                                i += 1

def main():
    pase_questions()
    parse_sentences()

if __name__ == '__main__':
    main()
