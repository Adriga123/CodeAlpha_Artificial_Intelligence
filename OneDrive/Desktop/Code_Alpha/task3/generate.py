import pickle
import numpy as np

from tensorflow.keras.models import load_model # pyright: ignore[reportMissingModuleSource]
from music21 import note, chord, stream

# Load notes
with open("notes.pkl", "rb") as f:
    notes = pickle.load(f)

pitchnames = sorted(set(notes))

note_to_int = {n: i for i, n in enumerate(pitchnames)}
int_to_note = {i: n for i, n in enumerate(pitchnames)}

# Create sequences
sequence_length = 100
network_input = []

for i in range(len(notes) - sequence_length):
    sequence = notes[i:i + sequence_length]
    network_input.append([note_to_int[n] for n in sequence])

# Load trained model
model = load_model("music_model.h5")

# Pick random seed
start = np.random.randint(0, len(network_input) - 1)
pattern = network_input[start]

generated_notes = []

print("Generating music...")

for _ in range(100):  # generate 100 notes

    prediction_input = np.reshape(
        pattern,
        (1, len(pattern), 1)
    )

    prediction_input = prediction_input / float(len(pitchnames))

    prediction = model.predict(
        prediction_input,
        verbose=0
    )

    index = np.argmax(prediction)

    result = int_to_note[index]

    generated_notes.append(result)

    pattern.append(index)
    pattern = pattern[1:]

print("Sample Generated Notes:")
print(generated_notes[:20])

# Convert to MIDI
offset = 0
output_notes = []

for pattern in generated_notes:

    try:
        # Chord
        if "." in pattern:
            notes_in_chord = pattern.split(".")
            chord_notes = []

            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.offset = offset
                chord_notes.append(new_note)

            new_chord = chord.Chord(chord_notes)
            output_notes.append(new_chord)

        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            output_notes.append(new_note)

        offset += 0.5

    except:
        pass

midi_stream = stream.Stream(output_notes)

midi_stream.write(
    "midi",
    fp="generated_music.mid"
)

print("generated_music.mid created successfully")
print("Playable Notes:", len(output_notes))