from music21 import note, pitch, corpus, stream, key, clef, meter, interval
import numpy as np


def scale_degree_to_pitch(scale_in, degree, range):
    """
    Calculates all the possible pitches for a scale degree in the range.

    Parameters
    ----------
    scale_in: scale.Scale
        the desired scale.
    degree: int
        the desired degree.
    range: tuple (low, high)
        two strings containing the range of the pitch.
        e.g.: ('C4', 'G4')
    
    Returns
    -------
    pitch_list: list of pitch.Pitch
        the list with all the possible pitches.
    """
    pass


def random_nextnote(pitch_list, last_note, current_cf, down_beat,
                     species, prob_factor=2, debug=False):
    """
    Randomly generate the next note according to the previous notes.

    Parameters
    ----------
    pitch_list: list of pitch.Pitch
        possible pitches
    last_note: note.Note
        the previous note
    current_cf: note.Note
        the current canctus firmus note
    down_beat: bool
        whether the current note is down beat. affects 
        the choise of interval.
    species: int
        the species of counterpoint
    prob_factor: int
        affects the probability factor of choosing pitches
    debug: bool
        if debug=True, print some process.
    Returns
    -------
    current_note: note.Note
        one current note that follows all the rules.
        * if there is no possible note, return None.
    """

    # list of pitch names in string
    pitch_name_list = [p.nameWithOctave for p in pitch_list]    

    # pitches to avoid:
    pitch_name_avoid = []
    # avoid same note
    pitch_name_avoid.append(last_note.pitch.nameWithOctave)
    # Avoid dissonants
    dissonant_intervals = ['m2', 'M2', 'P4', 'A4', 'D5', 'm7', 'M7']
    dissonant_pitches = [current_cf.transpose(interval).pitch.name for interval in dissonant_intervals]
    for p in pitch_list:
        if p.name in dissonant_pitches:
            pitch_name_avoid.append(p.nameWithOctave)

    # rules for down beats
    if down_beat:
        last_cf = current_cf.previous()
        # PPI from upbeat to downbeat
        inte = interval.Interval(last_cf, last_note) 
        if inte.semiSimpleName == 'P5':
            pitch_name_avoid.append(current_cf.transpose(inte).nameWithOctave)
        elif inte.semiSimpleName == 'P8':
            pitch_name_avoid.append(current_cf.transpose(inte).nameWithOctave)

        # PPI from last downbeat to downbeat
        # get the last downbeat
        last_db = last_note
        for _ in range(species-1):
            if type(last_db.previous()) == note.Note:
                last_db = last_db.previous()
        
        inte = interval.Interval(last_db, last_note)
        if inte.name == 'P5':
            pitch_name_avoid.append(current_cf.transpose('P5').nameWithOctave)
        elif inte.name == 'P8':
            pitch_name_avoid.append(current_cf.transpose('P8').nameWithOctave)
    # rules for up beats
    else:
        # upbeat's last cf is the current cf
        last_cf = current_cf
        # PPI from upbeat to downbeat
        if interval.Interval(last_cf, last_note).name == 'P5':
            pitch_name_avoid.append(current_cf.transpose('P5').nameWithOctave)
        elif interval.Interval(last_cf, last_note).name == 'P8':
            pitch_name_avoid.append(current_cf.transpose('P8').nameWithOctave)

    # Find every element in pitch_name_list and not in pitch_name_avoid
    pitch_name_valid = [pitch for pitch in pitch_name_list if not pitch in pitch_name_avoid]
    if not pitch_name_valid:
        # if no valid pitch, return None
        print('No valid pitch! Stucked!')
        return None
    # calculate the distance of interval to the last note
    interval_to_rf = np.array([np.abs(interval.Interval(last_note.pitch, pitch.Pitch(p)).semitones) for p in pitch_name_valid])
    if debug:
        print('intervals: {}'.format(np.around(interval_to_rf, decimals=3)))
    # generate a probability function according to the intervals. smaller interval has bigger probability.
    interval_p = 1 / interval_to_rf
    interval_p = interval_p ** prob_factor
    interval_p = interval_p / np.sum(interval_p)
    if debug:
        print('probabilities: {}'.format(np.around(interval_p, decimals=3)))
    current_note = note.Note(pitch=np.random.choice(pitch_name_valid, p=interval_p))
    current_note.quarterLength = (current_cf.quarterLength / species)
    # current_note = note.Note(pitch=np.random.choice(pitch_name_valid), quaterLength= current_cf.quarterLength / species)
    return current_note


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
    BASS_RANGE = ('D1', 'C3') # voice range of bass
    SOPRANO_RANGE = ('C4', 'G5') # voice range of soprano

    s = stream.Stream([cf.keySignature, cf.timeSignature])
    if cf_type == 'bass':
        soprano = stream.Part([cf.keySignature, cf.timeSignature], id='soprano')
        bass = stream.Part(cf.flat.elements, id='bass')
    elif cf_type == 'soprano':
        bass = stream.Part([cf.keySignature, cf.timeSignature], id='bass')
        soprano = stream.Part(cf.flat.elements, id='soprano')

    # decide the duration by species
    species_length = bass.notes[0].quarterLength / species
    # according to key, decide the possible notes
    s.scale = s.keySignature.getScale()
    bass_pitches = s.scale.getPitches(BASS_RANGE[0], BASS_RANGE[1])    
    soprano_pitches = s.scale.getPitches(SOPRANO_RANGE[0], SOPRANO_RANGE[1])
    soprano_tonic_pitches = s.scale.pitchesFromScaleDegrees([1], SOPRANO_RANGE[0], SOPRANO_RANGE[1])
    bass_tonic_pitches = s.scale.pitchesFromScaleDegrees([1], BASS_RANGE[0], BASS_RANGE[1])

    # iterate for each cf note
    if cf_type == 'bass':
        for current_bass in bass.flat.notes:
            if not type(current_bass.previous()) == note.Note:
                # The first note must be tonic
                soprano.append(note.Rest(quarterLength=species_length))
                soprano.append(note.Note(pitch=np.random.choice(soprano_tonic_pitches), quarterLength=species_length))
            elif not current_bass.next():
                # The last note must be tonic
                soprano.append(note.Note(pitch=np.random.choice(soprano_tonic_pitches), quarterLength=species_length*species))
            else:
                # for every middle note, generate multiple notes as the number of species, using random_nextnote()
                for i in range(species):
                    # soprano.append(note.Note(pitch=np.random.choice(soprano_pitches), quarterLength=species_length))
                    down_beat = (True if i == 0 else False)
                    soprano.append(random_nextnote(soprano_pitches, soprano.flat.notes[-1],
                     current_bass, down_beat, species, prob_factor=2, debug=True))
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

    result = write_two_part(cf=cf, cf_type='bass', species=2, show=False)
    result.write('musicxml', './output/result.xml')
    result.write('midi', './output/result.midi')