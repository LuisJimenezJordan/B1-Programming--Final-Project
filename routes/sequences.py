# sequences.py
# Contains all endpoints for managing DNA sequence entries — creating, listing,
# fetching, updating, and deleting sequences stored in sequences.txt.

from fastapi import APIRouter, HTTPException
from schema import NucSeqCreate, NucSeqUpdate, NucSeq, NucSeqSummary
from storage import load_sequences, save_sequences

router = APIRouter()


# --- Create Sequence Endpoint ---
# Accepts a label and DNA sequence from the user, validates both, auto-generates
# an ID, and saves the new entry to storage. Both nuc_analysed and aa_analysed
# are set to False by default as no analysis has been performed yet.
@router.post("/", response_model=NucSeq)
def create_seq_entry(nucseq_input: NucSeqCreate):
    all_sequences = load_sequences()
    
    # Auto-generate a sequential ID based on the current highest ID in storage
    new_id = max((t["id"] for t in all_sequences), default=0) + 1
    dna_seq = nucseq_input.sequence.upper()
    valid_bases = {"A", "T", "G", "C"}

    # Validate that a sequence was actually entered
    if len(dna_seq) == 0:
        raise HTTPException(status_code=400, detail="Could not create DNA Nucleotide Sequence entry - no nucleotide sequence was entered. Please try again.")

    # Validate minimum biological length — at least one codon (3 bases) is required
    if len(dna_seq) < 3:
        raise HTTPException(status_code=400, detail="DNA sequence too short to be biologically meaningful. A minimum of 3 nucleotides is required to enter a sequence into the DNA Toolkit. Consider resequencing your sample.")

    # Validate that the sequence only contains valid DNA bases
    if not set(dna_seq).issubset(valid_bases):
        raise HTTPException(status_code=400, detail="Could not create DNA Nucleotide Sequence entry - did not enter a valid series of nucleotides. This must consist only of 'A', 'T', 'C', and 'G'.")

    # Validate that a non-empty label was provided
    if len(nucseq_input.label.strip()) == 0:
        raise HTTPException(status_code=400, detail="Could not create DNA Nucleotide Sequence entry - no sequence label was entered. Please try again.")

    # Build the new sequence record and save it to storage
    new_nucseq = {
        "id": new_id,
        "label": nucseq_input.label,
        "sequence": dna_seq,
        "nuc_analysed": False,
        "aa_analysed": False
    }

    all_sequences.append(new_nucseq)
    save_sequences(all_sequences)
    return {**new_nucseq, "message": "A new DNA Nucleotide sequence has been successfully created and added to the DNA Toolkit. You can search for this entry via its unique ID, displayed below, or perform sequence analyses or an amino acid conversion."}


# --- List Sequences Endpoint ---
# Returns all stored sequences. Supports optional filtering by nuc_analysed and/or
# aa_analysed status. Both filters can be applied simultaneously.
# Returns 404 if no sequences are stored, or if filters return no matches.
@router.get("/", response_model=list[NucSeqSummary])
def list_sequences(nuc_analysed: bool | None = None, aa_analysed: bool | None = None):
    all_sequences = load_sequences()

    # Raised if the toolkit has no sequences stored at all
    if len(all_sequences) == 0:
        raise HTTPException(status_code=404, detail="No nucleotide sequences have been submitted to DNA Toolkit.")

    # Apply nucleotide analysis filter if provided
    if nuc_analysed is not None:
        all_sequences = [seq for seq in all_sequences if seq["nuc_analysed"] == nuc_analysed]
    
    # Apply amino acid analysis filter if provided
    if aa_analysed is not None:
        all_sequences = [seq for seq in all_sequences if seq["aa_analysed"] == aa_analysed]

    # Raised if filters were applied but no sequences matched
    if len(all_sequences) == 0:
        raise HTTPException(status_code=404, detail="No sequences match the applied filter criteria.")

    return all_sequences


# --- Fetch Sequence by ID Endpoint ---
# Searches stored sequences for a matching ID and returns the full sequence record.
# Raises 404 if no sequence with the given ID exists.
@router.get("/{id}", response_model=NucSeq)
def fetch_sequence_by_ID(id: int):
    all_sequences = load_sequences()
    for sequence in all_sequences:
        if id == sequence["id"]:
            return {"message": f"DNA Nucleotide Sequence with ID:{id} successfully retrieved.", **sequence}
    raise HTTPException(status_code=404, detail=f"Could not find sequence entry ID:{id}")


# --- Delete All Sequences Endpoint ---
# Overwrites sequences.txt with an empty list, permanently removing all entries.
@router.delete("/")
def delete_all_sequences():
    save_sequences([])
    return {"message": "All entries successfully deleted."}


# --- Delete Sequence by ID Endpoint ---
# Finds the sequence matching the given ID, removes it from the list, and saves
# the updated list back to storage. Returns the deleted sequence for confirmation.
# Raises 404 if no sequence with the given ID exists.
@router.delete("/{id}", response_model=NucSeq)
def delete_sequence_by_ID(id: int):
    all_sequences = load_sequences()
    for sequence in all_sequences:
        if id == sequence["id"]:
            all_sequences.remove(sequence)
            save_sequences(all_sequences)
            return {"message": f"DNA Nucleotide Sequence with ID:{id} successfully deleted. See details of deleted entry below", **sequence}
    raise HTTPException(status_code=404, detail=f"Could not delete sequence entry ID:{id} - ID not found")


# --- Update Sequence Label Endpoint ---
# Finds the sequence matching the given ID and updates its label.
# Validates that the new label is not empty before saving.
# Raises 400 for an empty label, 404 if the ID does not exist.
@router.put("/{id}", response_model=NucSeq)
def update_task_label(id: int, label_input: NucSeqUpdate):
    all_sequences = load_sequences()
    for sequence in all_sequences:
        if id == sequence["id"]:
            if len(label_input.label.strip()) == 0:
                raise HTTPException(status_code=400, detail=f"Could not update sequence label for sequence ID:{id} - no sequence label was entered. Please try again.")
            sequence["label"] = label_input.label
            save_sequences(all_sequences)
            return {"message": f"DNA Nucleotide Sequence label successfully updated, for sequence entry with ID:{id}.", **sequence}
    raise HTTPException(status_code=404, detail=f"Could not update label for sequence ID:{id} - ID not found")