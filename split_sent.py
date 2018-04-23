import json
import csv
from pydub import AudioSegment
import os

path = 'alignments.json'
audio_path = 'questions_wav/'

with open(path, encoding='utf-8') as data_file:
    for line in data_file:
        newline = json.loads(line)
        if 'question' in newline['path']:
            os.makedirs('quest_split/'+newline['path'])
            words = newline['words']
            for word in words:
                print(word['text'], type(word['start']), word['stop'], newline['path'])
                audio = "questions_wav/" + newline['path']
                time1 = word['start'] * 1000
                time2 = word['stop'] * 1000
                readAudio = AudioSegment.from_wav(audio)
                newAudio = readAudio[time1:time2]
                newWord = newAudio.export('quest_split/%s/%s_%s.wav' % (newline['path'], newline['path'],
                                                                        word['text']), format='wav')