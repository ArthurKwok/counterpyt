from music21 import note, pitch, corpus, stream, key, clef, meter, interval, duration, scale
import numpy as np

cf = stream.Stream([key.Key('Eb'), meter.TimeSignature('2/4')])
cf.append([
    note.Note("Eb3", type='half'),
    note.Note("D3", type='half'),
    note.Note("Eb3", type='half'),
    note.Note("F3", type='half'),
    note.Note("Ab3", type='half'),
    note.Note("G3", type='half'),
    note.Note("F3", type='half'),
    note.Note("Eb4", type='half')
])

n1 = note.Note('C3')
n2 = note.Note('G6')
print(interval.Interval(n1, n2).semiSimpleName)