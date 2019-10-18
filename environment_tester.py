from music21 import note, pitch, corpus, stream, key, clef, meter
import numpy as np
s = stream.Score(id='main score')

key_and_time = [key.Key('F'), meter.TimeSignature('3/4')]
soprano = stream.Part(key_and_time)
bass = stream.Part(key_and_time)
bass.clef = clef.BassClef()

for pitch in ['C', 'D', 'E', 'F', 'G']:
    soprano_oct = 4
    bass_oct = 3
    soprano.append(
        note.Note('{}{}'.format(pitch, soprano_oct)).transpose('P5'))
    bass.append(note.Note('{}{}'.format(pitch, bass_oct)))

s.append([soprano, bass])
s.show()