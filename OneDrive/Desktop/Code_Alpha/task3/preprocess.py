from music21 import converter, note, chord
import glob
import pickle

notes = []

for file in glob.glob("dataset/*.mid"):

    print("Processing:", file)

    midi = converter.parse(file)

    for element in midi.recurse().notes:

        if isinstance(element, note.Note):
            notes.append(str(element.pitch))

        elif isinstance(element, chord.Chord):
            notes.append(
                ".".join(
                    str(n)
                    for n in element.normalOrder
                )
            )

print("Total Notes:", len(notes))

with open("notes.pkl", "wb") as filepath:
    pickle.dump(notes, filepath)