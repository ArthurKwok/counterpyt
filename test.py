from music21 import note, pitch, corpus, stream, key, clef, meter, interval, duration

cf = stream.Stream([key.Key('Eb'), meter.TimeSignature('2/4')])
cf.append([
    note.Note("Eb3", type='half'),
    note.Note("D3", type='half'),
    note.Note("Eb3", type='half'),
    note.Note("F3", type='half'),
    note.Note("Ab3", type='half'),
    note.Note("G3", type='half'),
    note.Note("F3", type='half'),
    note.Note("Eb3", type='half')
])

# for note in cf.flat.notes:
#     print("previous note: {}, current note: {}, next note: {}".format(
#         note.previous(), note, note.next()))

if not cf.flat.notes[-1].next():
    print('haha')