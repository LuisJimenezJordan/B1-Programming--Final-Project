# DNA Sequence Toolkit API

A FastAPI-based REST API for storing, managing, and analysing DNA nucleotide sequences. Built as a final project for B1 Programming, this toolkit allows users to submit DNA sequences, perform nucleotide and amino acid analyses, filter sequences by analysis status, and retrieve summary statistics across all stored sequences.

---

## Background: DNA, Amino Acids, and Why We Analyse Sequences

### What is DNA?

DNA (Deoxyribonucleic Acid) is the molecule that carries the genetic instructions for the development, functioning, and reproduction of all known living organisms. It is made up of four chemical bases:

- A — Adenine
- T — Thymine
- G — Guanine
- C — Cytosine

The order of these bases forms a sequence, and it is this sequence that encodes biological information. For example, a DNA sequence might look like: `ATGGAGGCGAT`.

### What is GC Content?

GC content refers to the proportion of bases in a DNA sequence that are either Guanine (G) or Cytosine (C). This is a biologically important metric because G-C base pairs form three hydrogen bonds, making them stronger and more thermally stable than A-T pairs, which form only two.

Knowing the GC content of a sequence is essential for:

- Designing PCR primers — the melting temperature of a primer is directly influenced by its GC content
- Predicting sequence stability under different temperatures
- Identifying gene-rich regions in a genome, which tend to be GC-rich

### What are Amino Acids?

DNA sequences are read by the cell in groups of three bases called codons. Each codon corresponds to a specific amino acid — the building blocks of proteins. For example:

- `ATG` encodes Methionine, and also serves as the universal start codon
- `TAA`, `TAG`, and `TGA` are stop codons, signalling the end of translation

A sequence of amino acids folds into a protein, which performs virtually every function in the body — from catalysing chemical reactions to providing structural support. Understanding the amino acid composition of a sequence helps researchers predict the chemical properties of the resulting protein, such as whether it is hydrophobic, polar, or charged, as well as evolutionary relationships between organisms.

### Why Build a Toolkit Like This?

In real bioinformatics workflows, researchers routinely need to store, retrieve, and analyse large numbers of sequences. This toolkit demonstrates the fundamental concepts behind such systems — sequence storage, GC content calculation, codon translation, and compositional analysis — implemented as a clean RESTful API.

---

## Project Structure

```
B1-Programming--Final-Project/
├── main.py           # App entry point, router registration
├── schema.py         # Pydantic models for request validation and response shaping
├── storage.py        # File I/O helper functions (load and save)
├── AA_lookup.py      # Codon table and amino acid property mappings
├── sequences.txt     # JSON Lines storage file (one sequence per line)
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

# Create an empty sequences file before running
touch sequences.txt

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`

---

## Data Storage

Sequences are stored using the JSON Lines format in `sequences.txt` — one sequence per line, each as a complete JSON object. This provides simple persistence across server restarts without requiring a database.

Example `sequences.txt` content:

```
{"id": 1, "label": "Test Sequence 1", "sequence": "ATGGAGGCGAT", "nuc_analysed": true, "aa_analysed": false, "gc_content": 0.5, "seq_length": 11}
{"id": 2, "label": "Test Sequence 2", "sequence": "ATGCAGCTAGCTG", "nuc_analysed": false, "aa_analysed": false}
```

Analysis fields such as `gc_content`, `seq_length`, `amino_acid_sequence`, and `residue_count` are only added to a record once the relevant analysis has been performed.

---

## Sequence Validation Rules

The following rules are enforced when creating a new sequence entry:

- The sequence must only contain the characters `A`, `T`, `C`, and `G`
- The sequence must be at least 3 nucleotides long (the minimum length for a single codon)
- A non-empty label must be provided

---

## API Endpoints

### Root

#### GET /

Confirms the API is running and provides a brief description of the toolkit.

Response (200):
```json
{
  "message": "Welcome to the DNA Sequence Toolkit API",
  "status": "System Online — Ready for DNA Analysis",
  "description": "Submit DNA nucleotide sequences for storage, perform GC content and amino acid analyses, and retrieve summary statistics across your sequence library.",
  "docs": "Visit /docs for the full interactive API documentation."
}
```

---

### Sequence Management

All sequence management endpoints are accessible under the `/sequences` prefix.

---

#### POST /sequences/

Creates a new sequence entry and saves it to storage. The ID is auto-generated based on the current highest ID in the file.

Request body:
```json
{
  "label": "Test Sequence 1",
  "sequence": "ATGGAGGCGAT"
}
```

Response (200):
```json
{
  "message": "A new DNA Nucleotide sequence has been successfully created and added to the DNA Toolkit. You can search for this entry via its unique ID, displayed below, or perform sequence analyses or an amino acid conversion.",
  "id": 1,
  "label": "Test Sequence 1",
  "sequence": "ATGGAGGCGAT",
  "nuc_analysed": false,
  "aa_analysed": false
}
```

Errors:

| Status | Detail |
|--------|--------|
| 400 | No nucleotide sequence was entered |
| 400 | Sequence too short — minimum 3 nucleotides required |
| 400 | Sequence contains invalid characters — must only contain A, T, C, G |
| 400 | No sequence label was entered |

---

#### GET /sequences/

Returns all stored sequences. Supports optional query parameters to filter by analysis status. Both filters can be applied simultaneously.

Query parameters (all optional):

| Parameter | Type | Description |
|-----------|------|-------------|
| nuc_analysed | bool | Filter by nucleotide analysis status |
| aa_analysed | bool | Filter by amino acid analysis status |

Examples:
```
GET /sequences/
GET /sequences/?nuc_analysed=true
GET /sequences/?aa_analysed=false
GET /sequences/?nuc_analysed=true&aa_analysed=false
```

Response (200):
```json
[
  {
    "id": 1,
    "label": "Test Sequence 1",
    "sequence": "ATGGAGGCGAT",
    "nuc_analysed": true,
    "aa_analysed": false
  }
]
```

Errors:

| Status | Detail |
|--------|--------|
| 404 | No nucleotide sequences have been submitted to DNA Toolkit |
| 404 | No sequences match the applied filter criteria |

---

#### GET /sequences/{id}

Retrieves the full record for a single sequence by its ID, including any analysis results that have been stored.

Response (200):
```json
{
  "message": "DNA Nucleotide Sequence with ID:1 successfully retrieved.",
  "id": 1,
  "label": "Test Sequence 1",
  "sequence": "ATGGAGGCGAT",
  "nuc_analysed": true,
  "aa_analysed": false,
  "gc_content": 0.5,
  "seq_length": 11,
  "amino_acid_sequence": null,
  "residue_count": null,
  "composition": null,
  "top_3_residues": null
}
```

Errors:

| Status | Detail |
|--------|--------|
| 404 | Could not find sequence entry with the given ID |

---

#### PUT /sequences/{id}

Updates the label of an existing sequence. Only the label can be updated — the sequence itself cannot be changed.

Request body:
```json
{
  "label": "Updated Label"
}
```

Response (200):
```json
{
  "message": "DNA Nucleotide Sequence label successfully updated, for sequence entry with ID:1.",
  "id": 1,
  "label": "Updated Label",
  "sequence": "ATGGAGGCGAT",
  "nuc_analysed": true,
  "aa_analysed": false
}
```

Errors:

| Status | Detail |
|--------|--------|
| 400 | No sequence label was entered |
| 404 | Could not update label — ID not found |

---

#### DELETE /sequences/{id}

Deletes a single sequence by ID and returns the deleted record for confirmation.

Response (200):
```json
{
  "message": "DNA Nucleotide Sequence with ID:1 successfully deleted. See details of deleted entry below",
  "id": 1,
  "label": "Test Sequence 1",
  "sequence": "ATGGAGGCGAT",
  "nuc_analysed": false,
  "aa_analysed": false
}
```

Errors:

| Status | Detail |
|--------|--------|
| 404 | Could not delete sequence — ID not found |

---

#### DELETE /sequences/

Deletes all sequences from storage. This action is permanent and cannot be undone.

Response (200):
```json
{
  "message": "All entries successfully deleted."
}
```

---

### DNA Analysis

All analysis endpoints are accessible under the `/analysis` prefix.

---

#### GET /analysis/{id}/nucleotide

Performs nucleotide analysis on the sequence with the given ID. Calculates the GC content (proportion of G and C bases) and total sequence length. Updates the record in storage and sets `nuc_analysed` to `true`.

Response (200):
```json
{
  "message": "DNA Nucleotide sequence with ID:1 successfully analysed. See below the length of the sequence and its total GC content, which can be used to design primer melting and annealing temperatures",
  "sequence_id": 1,
  "label": "Test Sequence 1",
  "length": 11,
  "gc_content": 0.5
}
```

Errors:

| Status | Detail |
|--------|--------|
| 404 | Analysis could not be performed — ID not found |

---

#### GET /analysis/{id}/aminoacid

Translates the DNA sequence with the given ID into its amino acid sequence using the standard genetic codon table. Codons are read in triplets; translation stops at a stop codon or an incomplete codon at the end of the sequence.

Also calculates:
- The chemical property composition of the resulting protein (nonpolar, polar, positively charged, negatively charged)
- The top 3 most frequently occurring amino acid residues by percentage

Updates the record in storage and sets `aa_analysed` to `true`.

Response (200):
```json
{
  "message": "DNA Nucleotide conversion to Amino Acid sequence with ID:1 successfully completed. See below the converted sequence, the Amino Acid sequence length, the proportion of the different types of Amino Acid properties present in the sequence, and the top 3 most common Amino Acid Residues.",
  "sequence_id": 1,
  "label": "Test Sequence 1",
  "amino_acid_sequence": "Met-Glu-Ala",
  "residue_count": 3,
  "composition": {
    "nonpolar": 2,
    "negatively charged": 1
  },
  "top_3_residues": [
    {"residue": "Met", "percentage": 33.33},
    {"residue": "Glu", "percentage": 33.33},
    {"residue": "Ala", "percentage": 33.33}
  ]
}
```

Errors:

| Status | Detail |
|--------|--------|
| 400 | Sequence consists only of a stop codon — no viable amino acid sequence produced |
| 404 | Conversion could not be performed — ID not found |

---

#### GET /analysis/summary_statistics

Returns aggregated statistics across all sequences currently stored in the toolkit.

Nucleotide statistics (GC content, length, longest/shortest sequence) are calculated only from sequences that have had nucleotide analysis performed. Amino acid statistics are calculated only from sequences that have had amino acid analysis performed. If no amino acid analysis has been performed, `average_amino_acid_length` is returned as `null` rather than raising an error.

Response (200):
```json
{
  "message": "Summary of key statistics of all sequences currently stored in DNA Toolkit. If a statistic is missing, it is likely due to GC content analysis or Amino Acid conversion not having been performed yet.",
  "total_sequences": 3,
  "nuc_analysed_sequences": 2,
  "aa_analysed_sequences": 1,
  "average_gc_content": 0.5644,
  "average_nucleotide_length": 11.5,
  "average_amino_acid_length": 4.5,
  "longest_nucleotide_sequence": "Test Sequence 2",
  "shortest_nucleotide_sequence": "Test Sequence 1"
}
```

Errors:

| Status | Detail |
|--------|--------|
| 404 | No sequences have been submitted to the toolkit |
| 404 | No sequences have undergone nucleotide analysis yet |

---

## Error Reference

A summary of all possible error responses across the API:

| Status Code | Meaning | When it occurs |
|-------------|---------|----------------|
| 400 | Bad Request | Invalid input — empty sequence, invalid bases, sequence too short, empty label, stop-codon-only sequence |
| 404 | Not Found | No sequences in storage, ID not found, no sequences match filter criteria, no sequences analysed yet |

---

*Built with FastAPI, Pydantic, and Python 3.10+*
