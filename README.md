# 🧬 DNA Sequence Toolkit API

A FastAPI-based REST API for storing, managing, and analysing DNA nucleotide sequences. Built as a final project for B1 Programming, this toolkit allows users to submit DNA sequences, perform nucleotide and amino acid analyses, filter sequences by analysis status, and retrieve summary statistics across all stored sequences.

---

## 🔬 Background: DNA, Amino Acids, and Why We Analyse Sequences

### What is DNA?
DNA (Deoxyribonucleic Acid) is the molecule that carries the genetic instructions for the development, functioning, and reproduction of all known living organisms. It is made up of four chemical **bases**:

- **A** — Adenine
- **T** — Thymine
- **G** — Guanine
- **C** — Cytosine

The order of these bases forms a **sequence**, and it is this sequence that encodes biological information. For example, a DNA sequence might look like: `ATGGAGGCGAT`.

### What is GC Content?
**GC content** refers to the proportion of bases in a DNA sequence that are either Guanine (G) or Cytosine (C). This is a biologically important metric because G-C base pairs form **three hydrogen bonds**, making them stronger and more thermally stable than A-T pairs (which form only two). 

Knowing the GC content of a sequence is essential for:
- Designing **PCR primers** — the melting temperature (Tm) of a primer is directly influenced by its GC content
- Predicting **sequence stability** under different temperatures
- Identifying **gene-rich regions** in a genome, which tend to be GC-rich

### What are Amino Acids?
DNA sequences are read by the cell in groups of three bases called **codons**. Each codon corresponds to a specific **amino acid** — the building blocks of proteins. For example:
- `ATG` → Methionine (the start codon)
- `TAA` → Stop (signals the end of the protein)

A sequence of amino acids folds into a **protein**, which performs virtually every function in the body — from catalysing chemical reactions to providing structural support. Understanding the amino acid composition of a sequence helps researchers predict:
- **Protein structure and function**
- **Chemical properties** of the resulting protein (e.g. whether it is hydrophobic, polar, or charged)
- **Evolutionary relationships** between organisms

### Why Build a Toolkit Like This?
In real bioinformatics workflows, researchers routinely need to store, retrieve, and analyse large numbers of sequences. This toolkit demonstrates the fundamental concepts behind such systems — sequence storage, GC content calculation, codon translation, and compositional analysis — implemented as a clean RESTful API.

---

## Project Structure

```
fastapi-tasks/
├── main.py           # App entry point, router registration
├── schema.py         # Pydantic models for validation
├── storage.py        # File I/O helper functions
├── AA_lookup.py      # Codon table and amino acid properties
├── sequences.txt     # JSON Lines storage file
└── routes/
    ├── sequences.py  # Sequence management endpoints
    └── analysis.py   # Analysis and statistics endpoints
```

---

## Setup and Installation

### Requirements
- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

### Installation

```bash
# Clone the repository
git clone https://github.com/LuisJimenezJordan/B1-Programming--Final-Project.git
cd B1-Programming--Final-Project

# Install dependencies
pip install fastapi uvicorn

# Create an empty sequences file
touch sequences.txt

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`  
Interactive Swagger docs available at `http://127.0.0.1:8000/docs`

---

## Data Storage

Sequences are stored using the JSON Lines format in `sequences.txt` — one sequence per line, each as a complete JSON object. This provides simple persistence across server restarts without requiring a database.

Example `sequences.txt` content:
```json
{"id": 1, "label": "Test Sequence 1", "sequence": "ATGGAGGCGAT", "nuc_analysed": true, "aa_analysed": false, "gc_content": 0.5, "seq_length": 11}
{"id": 2, "label": "Test Sequence 2", "sequence": "ATGCAGCTAGCTG", "nuc_analysed": false, "aa_analysed": false}
```

---

## 🔁 API Endpoints

### Sequence Management (`/sequences`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/sequences/` | Create a new sequence entry |
| `GET` | `/sequences/` | List all sequences (with optional filters) |
| `GET` | `/sequences/{id}` | Fetch a single sequence by ID |
| `PUT` | `/sequences/{id}` | Update the label of a sequence |
| `DELETE` | `/sequences/{id}` | Delete a sequence by ID |
| `DELETE` | `/sequences/` | Delete all sequences |

#### Filtering
The list endpoint supports optional query parameters to filter by analysis status:

```
GET /sequences?nuc_analysed=true
GET /sequences?aa_analysed=false
GET /sequences?nuc_analysed=true&aa_analysed=false
```

---

### Analysis (`/analysis`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/analysis/{id}/nucleotide` | Perform GC content and length analysis |
| `GET` | `/analysis/{id}/aminoacid` | Translate sequence to amino acids and analyse composition |
| `GET` | `/analysis/summary_statistics` | Get summary statistics across all analysed sequences |

---

## Example Responses

### Create Sequence (`POST /sequences/`)
```json
{
  "message": "A new DNA Nucleotide sequence has been successfully created and added to the DNA Toolkit.",
  "id": 1,
  "label": "Test Sequence 1",
  "sequence": "ATGGAGGCGAT",
  "nuc_analysed": false,
  "aa_analysed": false
}
```

### Nucleotide Analysis (`GET /analysis/1/nucleotide`)
```json
{
  "message": "DNA Nucleotide sequence with ID:1 successfully analysed.",
  "sequence_id": 1,
  "label": "Test Sequence 1",
  "length": 11,
  "gc_content": 0.5
}
```

### Amino Acid Analysis (`GET /analysis/1/aminoacid`)
```json
{
  "sequence_id": 1,
  "label": "Test Sequence 1",
  "amino_acid_sequence": "Met-Glu-Ala",
  "residue_count": 3,
  "composition": {"Nonpolar": 2, "Charged": 1},
  "top_3_residues": [
    {"residue": "Met", "percentage": 33.33},
    {"residue": "Glu", "percentage": 33.33},
    {"residue": "Ala", "percentage": 33.33}
  ]
}
```

### Summary Statistics (`GET /analysis/summary_statistics`)
```json
{
  "message": "Summary of key statistics of all sequences currently stored in DNA Toolkit.",
  "total_sequences": 3,
  "nuc_analysed_sequences": 2,
  "aa_analysed_sequences": 2,
  "average_gc_content": 0.5644,
  "average_nucleotide_length": 11.5,
  "average_amino_acid_length": 4.5,
  "longest_nuc_sequence": "Test 2",
  "shortest_nuc_sequence": "Test 1"
}
```

---

## Error Handling

The API returns appropriate HTTP status codes and descriptive messages for all error cases:

| Status Code | Scenario |
|-------------|----------|
| `400` | Invalid sequence (non-ATCG characters, too short, empty label) |
| `404` | Sequence ID not found, or no sequences available for the requested operation |

---

## Sequence Validation Rules

When creating a sequence, the following rules are enforced:
- The sequence must only contain the characters `A`, `T`, `C`, and `G`
- The sequence must be at least 3 nucleotides long
- A non-empty label must be provided

---

*Built with FastAPI · Pydantic · Python*
