import numpy as np
import os
from miditime.miditime import MIDITime

#====================================================================================================
def midi_note(Nmidi):
    '''
    Input: MIDI note number (0-127)
    Output: Note name (string)
    
    Middle C is C5 and MIDI note number 48.
    http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm
    '''
    # Use flats instead of sharps because the '#' symbol can cause problems in filenames
    names  = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    note   = names[Nmidi%12]
    octave = str(int(np.floor(Nmidi/12)))
    return note+octave


#====================================================================================================
def make_note(Nmidi, outdir=None):
    '''
    Input: MIDI note number (0-127)
    Output: Sound file in formats .mid, .mp3, .ogg.
    '''
    # Output file names
    if (outdir is None):
        name = midi_note(Nmidi)
    else:
        name = outdir + midi_note(Nmidi)
    fmidi = name + '.mid'
    fmp3  = name + '.mp3'
    fogg  = name + '.ogg'
    
    # Instantiate the MIDITime class
    tempo  = 120  # [beats min^-1] <-- 1 beat = 0.5 sec
    mymidi = MIDITime(tempo=tempo, outfile=fmidi)

    # At 0 beats (the start), play some pitch, with velocity/attack 127, for 1 beat duration
    note_list = []
    time      = 0      # [beats]
    pitch     = Nmidi  # [MIDI # 0-127]
    velocity  = 127    # Max volume
    duration  = 1      # [beats] <-- the note will last 0.5 seconds
    note      = [time, pitch, velocity, duration]
    note_list.append(note)

    # Add a track with this note
    mymidi.add_track(note_list=note_list)

    # Output the .mid file
    mymidi.save_midi()

    # Convert the .mid file to a .mp3 file
    command_mp3 = 'timidity -A100 -Ow -o - ' + fmidi + ' | lame - ' + fmp3
    os.system(command_mp3)

    # Convert the .mid file to a .ogg file
    command_ogg = 'timidity -A100 -Ow -o - ' + fmidi + ' | lame - ' + fogg
    os.system(command_ogg)

#====================================================================================================
