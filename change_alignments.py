import csv
import os
from pydub import AudioSegment
import json

path = 'alignments.json'
audio_path = 'questions_wav/'


idn = 0
with open('questions_subtitles_updated.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    i = 0
    for row in reader:
        if '@' not in row['transcript'] and '?' in row['transcript']:
            # print(row['transcript'])
            phrases = row['transcript'].split(' # ')
            for phrase in phrases:
                if '?' in phrase:
                    idn += 1
                    # print(phrase, i, row['quest_num'].strip('questions_wav/'))
                    with open(path, encoding='utf-8') as data_file:
                        for line in data_file:
                            newline = json.loads(line)
                            if row['quest_num'].strip('questions_wav/') in newline['path']:
                                data = {}
                                data['text'] = phrase
                                data['ID'] = idn
                                data['relpath'] = newline['path']
                                data['purpose'] = 'question'
                                #print(data)

                                word_stamps = {}
                                word_stamps['ID'] = idn
                                word_stamps['words'] = []
                                for wrd in phrase.split(' '):
                                    wrd.replace('?', '')
                                    wrd.replace('/', '')
                                    wrd.replace('*П', '')
                                    for w in newline['words']:
                                        if w['text'] == wrd:
                                            newdict = {}
                                            newdict['text'] = w['text']
                                            newdict['start'] = w['start']
                                            newdict['stop'] = w['stop']

                                            word_stamps['words'].append(newdict)

                                if word_stamps['words'] != []:
                                    dist = word_stamps['words'][0]['start']
                                    word_stamps['words'][0]['stop'] = word_stamps['words'][0]['stop'] - dist
                                    word_stamps['words'][0]['start'] = 0.0
                                    for v in word_stamps['words'][1:]:
                                        v['start'] = v['start'] - dist
                                        v['stop'] = v['stop'] - dist
                                    word_stamps['path'] = '%s.wav' % (newline['path'].strip('.wav'))
                                print(word_stamps)

                                with open('index.json', 'a', encoding='utf-8') as json_file:
                                    json.dump(data, json_file, ensure_ascii=False)
                                    json_file.write("\n")

                                """
                                with open('new_alignments.json', 'a', encoding='utf-8') as json_file:
                                    json.dump(word_stamps, json_file, ensure_ascii=False)
                                    json_file.write("\n")


                                for w in word_stamps['words']:
                                    time1 = w['start'] * 1000
                                    time2 = w['stop'] * 1000
                                    print(w['text'], time1, time2, newline["path"])
                                    audio = "cut_sent/" + word_stamps['path']
                                    readAudio = AudioSegment.from_wav(audio)
                                    newAudio = readAudio[time1:time2]
                                    newQuestion = newAudio.export('test/%s_%s.wav' %(word_stamps['path'], w['text']),
                                                                  format='wav')
                                """

with open('questions_subtitles_updated.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    i = 0
    for row in reader:
        if '@' not in row['transcript'] and '?' not in row['transcript']:
            phrases = row['transcript'].split(' # ')
            i = 1
            for phrase in phrases:
                idn += 1
                with open(path, encoding='utf-8') as data_file:
                    for line in data_file:
                        newline = json.loads(line)
                        if row['quest_num'].strip('questions_wav/') in newline['path']:
                            data = {}
                            data['text'] = phrase
                            data['ID'] = idn
                            data['relpath'] = newline['path']
                            data['purpose'] = 'declaration'
                            # print(data)

                            sent_num = '%s_%s.wav' % (newline['path'].strip('.wav'), i)

                            word_stamps = {}
                            word_stamps['ID'] = idn
                            word_stamps['words'] = []
                            for wrd in phrase.split(' '):
                                for w in newline['words']:
                                    if w['text'] == wrd:
                                        newdict = {}
                                        newdict['text'] = w['text']
                                        newdict['start'] = w['start']
                                        newdict['stop'] = w['stop']

                                        word_stamps['words'].append(newdict)

                            if word_stamps['words'] != []:
                                dist = word_stamps['words'][0]['start']
                                word_stamps['words'][0]['stop'] = word_stamps['words'][0]['stop'] - dist
                                word_stamps['words'][0]['start'] = 0.0
                                for v in word_stamps['words'][1:]:
                                    v['start'] = v['start'] - dist
                                    v['stop'] = v['stop'] - dist
                                word_stamps['path'] = sent_num
                                print(word_stamps)

                                with open('index.json', 'a', encoding='utf-8') as json_file:
                                    json.dump(data, json_file, ensure_ascii=False)
                                    json_file.write("\n")
                                """
                                with open('new_alignments.json', 'a', encoding='utf-8') as json_file:
                                    json.dump(word_stamps, json_file, ensure_ascii=False)
                                    json_file.write("\n")
                                """
                            i += 1
                            """
                            for w in word_stamps['words']:
                                if w['start'] > 0 and w['stop'] > 0:
                                    time1 = w['start'] * 1000
                                    time2 = w['stop'] * 1000
                                    print(w['text'], time1, time2, newline["path"])
                                    audio = "cut_sent/" + word_stamps['path']
                                    readAudio = AudioSegment.from_wav(audio)
                                    newAudio = readAudio[time1:time2]
                                    newQuestion = newAudio.export('test/%s_%s_%s.wav' % (newline['path'].strip('.wav'),
                                                                                         i, w['text']), format='wav')
                            """