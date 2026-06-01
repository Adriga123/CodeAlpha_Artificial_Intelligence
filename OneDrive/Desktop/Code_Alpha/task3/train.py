import pickle
import numpy as np

from tensorflow.keras.models import Sequential # pyright: ignore[reportMissingModuleSource]
from tensorflow.keras.layers import LSTM, Dense, Dropout # pyright: ignore[reportMissingModuleSource]
from tensorflow.keras.utils import to_categorical # pyright: ignore[reportMissingImports]

# Load notes from preprocess.py
with open("notes.pkl", "rb") as filepath:
    notes = pickle.load(filepath)

print("Total Notes:", len(notes))

# Create unique note list
pitchnames = sorted(set(notes))

print("Unique Notes:", len(pitchnames))

# Map notes to integers
note_to_int = dict(
    (note, number)
    for number, note in enumerate(pitchnames)
)

# Create training sequences
sequence_length = 100

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):

    sequence_in = notes[i:i + sequence_length]

    sequence_out = notes[i + sequence_length]

    network_input.append(
        [note_to_int[n]
         for n in sequence_in]
    )

    network_output.append(
        note_to_int[sequence_out]
    )

n_patterns = len(network_input)

print("Patterns:", n_patterns)

# Reshape input
network_input = np.reshape(
    network_input,
    (n_patterns,
     sequence_length,
     1)
)

# Normalize
network_input = network_input / float(len(pitchnames))

# One-hot encode output
network_output = to_categorical(
    network_output,
    num_classes=len(pitchnames)
)

# Build model
model = Sequential()

model.add(
    LSTM(
        128,
        input_shape=(100, 1)
    )
)

model.add(
    Dropout(0.2)
)

model.add(
    Dense(128)
)

model.add(
    Dense(
        len(pitchnames),
        activation="softmax"
    )
)

# Compile model
model.compile(
    loss="categorical_crossentropy",
    optimizer="adam"
)

# Show summary
model.summary()

# Train model
model.fit(
    network_input,
    network_output,
    epochs=5,
    batch_size=64
)

# Save model
model.save("music_model.h5")

print("Model Saved Successfully")