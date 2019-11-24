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
species = 1
current_cf = note.Note('C3', quarterLength=2.0)
current_note = note.Note(pitch='G3')
current_note.quarterLength = (current_cf.quarterLength/species)
print(current_note.quarterLength)