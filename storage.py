# storage.py
import json
import os

FILE_PATH = "sequences.txt"

def load_sequences():
    if not os.path.exists(FILE_PATH):
        return []
    sequences = []
    with open(FILE_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                sequences.append(json.loads(line))
    return sequences

def save_sequences(sequences):
    with open(FILE_PATH, "w") as f:
        for sequence in sequences:
            f.write(json.dumps(sequence) + "\n")