from pandas import read_csv, DataFrame, Series
import pandas as pd
import json
from collections import Counter
import wave
from pydub import AudioSegment

path = 'alignments.json'

record = [json.loads(line) for line in open(path, encoding='utf-8')]

sent = record[24]['words']
path = record[24]['path']

def write_words():
    audio = "questions_wav/" + path
    for s in sent:
        # print(s['text'], s['start'], s['stop'])
        time1 = s['start']*1000
        time2 = s['stop']*1000
        readAudio = AudioSegment.from_wav(audio)
        newAudio = readAudio[time1:time2]
        newQuestion = newAudio.export('words_wav/%s_%s.wav' % (path, s['text']), format='wav')


def main():
    write_words()

if __name__ == '__main__':
    main()