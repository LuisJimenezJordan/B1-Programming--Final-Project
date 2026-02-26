# schema.py
# Pydantic models used for request validation and response shaping throughout the API.
# FastAPI uses these models to automatically validate incoming data and serialise
# outgoing responses, rejecting any requests that don't match the defined structure.

from pydantic import BaseModel, Field


# --- Input Model: Create Sequence ---
# Defines the fields a user must provide when submitting a new sequence.
# Field(...) means the field is required — no default value is provided.
class NucSeqCreate(BaseModel):
    label: str = Field(..., description="A label for the DNA sequence")
    sequence: str = Field(..., description="The actual DNA sequence (A, T, C, G)")


# --- Full Sequence Model ---
# Represents a complete sequence record as stored in sequences.txt and returned
# by most endpoints. All analysis fields are optional (None by default) since
# they are only populated after the relevant analysis has been performed.
class NucSeq(BaseModel):
    message: str | None = None          # Optional response message from the API
    id: int                             # Auto-generated unique identifier
    label: str                          # User-provided sequence label
    sequence: str                       # The raw DNA sequence string
    nuc_analysed: bool = False          # True once nucleotide analysis has been run
    aa_analysed: bool = False           # True once amino acid analysis has been run
    gc_content: float | None = None     # Populated by nucleotide analysis
    seq_length: int | None = None       # Populated by nucleotide analysis
    amino_acid_sequence: str | None = None  # Populated by amino acid analysis
    residue_count: int | None = None    # Populated by amino acid analysis
    composition: dict | None = None     # Populated by amino acid analysis
    top_3_residues: list[dict] | None = None  # Populated by amino acid analysis


# --- Summary Sequence Model ---
# A lightweight version of NucSeq used by the list endpoint.
# Only returns the fields needed for an overview — omits analysis results
# to keep list responses concise.
class NucSeqSummary(BaseModel):
    id: int
    label: str
    sequence: str
    nuc_analysed: bool
    aa_analysed: bool


# --- Input Model: Update Sequence Label ---
# Defines the single field a user provides when updating a sequence label.
class NucSeqUpdate(BaseModel):
    label: str


# --- Response Model: Nucleotide Analysis ---
# Returned by the nucleotide analysis endpoint.
# Contains GC content and sequence length calculated from the stored DNA sequence.
class NucleotideResult(BaseModel):
    message: str | None = None
    sequence_id: int
    label: str
    length: int
    gc_content: float


# --- Response Model: Amino Acid Analysis ---
# Returned by the amino acid analysis endpoint.
# Contains the translated amino acid sequence, residue count, chemical property
# composition, and the top 3 most frequent residues.
class AminoAcidResult(BaseModel):
    message: str | None = None
    sequence_id: int
    label: str
    amino_acid_sequence: str
    residue_count: int
    composition: dict
    top_3_residues: list[dict]


# --- Response Model: Summary Statistics ---
# Returned by the summary statistics endpoint.
# Aggregates data across all stored sequences. Fields that depend on analysis
# (gc content, lengths, longest/shortest) are optional in case no analysis
# has been performed yet.
class SummaryStats(BaseModel):
    message: str | None = None
    total_sequences: int
    nuc_analysed_sequences: int         # Count of sequences with nucleotide analysis done
    aa_analysed_sequences: int          # Count of sequences with amino acid analysis done
    average_gc_content: float | None = None
    average_nucleotide_length: float | None = None
    average_amino_acid_length: float | None = None
    longest_nucleotide_sequence: str | None = None
    shortest_nucleotide_sequence: str | None = None