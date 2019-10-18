from music21 import note, pitch, corpus, stream, key, clef, meter, interval
import numpy as np


def generate_cf(key='C', time_siganture='2/4', cf_type='bass', measures=8):
    """
    Automatically generate a canctus firmus.

    Parameters
    ----------
    key: str
        the key of cf
    time_signature: str
        the time signature, also decides the duration of cf.
    cf_type: str
        'bass' or 'soprano'.
    mesures: int
        the number of measure to generate.
    """
    pass

def write_two_part(cf, cf_type='bass', species=1, show=False):
    """
    write two part counterpoints.

    Parameters
    ----------
    cf: stream
        canctus firmus in stream.
    cf_type: str
        'soprano' or 'bass'.
    species: int
        how many species to be generated, between 1 and 4.
    show: bool
        show the sheet output.

    Returns
    -------
    s: stream
        the generated two part counter point.
    """


    s = stream.Stream([cf.keySignature, cf.timeSignature])
    if cf_type == 'bass':
        soprano = stream.Part([cf.keySignature, cf.timeSignature])
        bass = stream.Part(cf.flat.elements)
    elif cf_type == 'soprano':
        bass = stream.Part([cf.keySignature, cf.timeSignature])
        soprano = stream.Part(cf.flat.elements)

    # decide the duration by species
    species_length = bass.notes[0].quarterLength / species
    # according to key, decide the possible notes
    key_notes = s.keySignature.getPitches()


    # iterate for each cf note
    if cf_type == 'bass':
        for current_bass in bass.flat.notes:
            if not type(current_bass.previous()) == note.Note:
                # The first note
                soprano.append(current_bass.transpose('P15'))
            elif not current_bass.next():
                # The last note
                soprano.append(current_bass.transpose('P8'))
            else:
                soprano.append(note.Note(pitch=np.random.choice(key_notes),
                            quarterLength=species_length))
                soprano.append(note.Note(pitch=np.random.choice(key_notes),
                            quarterLength=species_length))

    s.insert(0, soprano)
    s.insert(0, bass)

    if show:
        s.show()
    return s



if __name__ == "__main__":
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

    result = write_two_part(cf=cf, cf_type='bass', species=2, show=True)