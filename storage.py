# storage.py
# Handles all file I/O for the DNA Toolkit. Sequences are stored using the JSON Lines
# format in sequences.txt — one complete JSON object per line. This provides simple
# persistence across server restarts without requiring a database.

import json
import os

# Path to the storage file, relative to the project root
FILE_PATH = "sequences.txt"


# --- Load Sequences ---
# Reads sequences.txt and returns all stored sequences as a list of dictionaries.
# If the file doesn't exist yet (e.g. on first run), returns an empty list
# rather than raising an error.
def load_sequences():
    if not os.path.exists(FILE_PATH):
        return []
    sequences = []
    with open(FILE_PATH, "r") as f:
        for line in f:
            line = line.strip()
            # Skip any blank lines to avoid JSON parse errors
            if line:
                sequences.append(json.loads(line))
    return sequences


# --- Save Sequences ---
# Writes the entire sequence list back to sequences.txt, overwriting the file.
# Each sequence is serialised as a single JSON object on its own line,
# maintaining the JSON Lines format. This full rewrite approach ensures
# data integrity after any create, update, or delete operation.
def save_sequences(sequences):
    with open(FILE_PATH, "w") as f:
        for sequence in sequences:
            f.write(json.dumps(sequence) + "\n")