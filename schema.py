#PYDANTIC MODELS
from pydantic import BaseModel, Field

# 1. This is what the user sends in the request body
class NucSeqCreate(BaseModel):
    label: str = Field(..., description="A label for the DNA sequence")
    sequence: str = Field(..., description="The actual DNA sequence (A, T, C, G)")

# 2. This is what is saved to sequences.txt and returned to the user
class NucSeq(BaseModel):
    message: str | None = None
    id: int
    label: str
    sequence: str
    nuc_analysed: bool = False
    aa_analysed: bool = False
    gc_content: float | None = None
    seq_length: int | None = None
    amino_acid_sequence: str | None = None
    residue_count: int | None = None
    composition: dict | None = None
    top_3_residues: list [dict] | None = None

class NucSeqSummary(BaseModel):
    id: int
    label: str
    sequence: str
    nuc_analysed: bool
    aa_analysed: bool

class NucSeqUpdate(BaseModel):
    label: str 

class NucleotideResult(BaseModel):
    message: str | None = None
    sequence_id: int
    label: str
    length: int
    gc_content: float

class AminoAcidResult(BaseModel):
    message: str | None = None
    sequence_id: int
    label: str
    amino_acid_sequence: str
    residue_count: int
    composition: dict
    top_3_residues: list [dict]

class SummaryStats(BaseModel):
    message: str | None = None
    total_sequences: int
    nuc_analysed_sequences: int
    aa_analysed_sequences: int
    average_gc_content: float | None = None
    average_nucleotide_length: float | None = None
    average_amino_acid_length: float | None = None
    longest_nucleotide_sequence: str | None = None
    shortest_nucleotide_sequence: str | None = None