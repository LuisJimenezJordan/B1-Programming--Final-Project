from fastapi import APIRouter, HTTPException
from schema import NucSeqCreate, NucSeqUpdate, NucSeq, NucSeqSummary
from storage import load_sequences, save_sequences

router = APIRouter()

@router.post("/", response_model=NucSeq)
def create_seq_entry(nucseq_input: NucSeqCreate):
     all_sequences = load_sequences()
    
     # Auto-generate ID
     new_id = max((t["id"] for t in all_sequences), default=0) + 1
     dna_seq = nucseq_input.sequence.upper()
     valid_bases = {"A", "T", "G", "C"}
     if len(dna_seq) == 0:
         raise HTTPException(status_code=400, detail=f"Could not create DNA Nucleotide Sequence entry - no nucleotide sequence was entered. Please try again.")

     if len(dna_seq) <3:
          raise HTTPException(status_code=400, detail=f"DNA sequence too short to be biologically meaningful. A minimum of 3 nucleotides is required to enter a sequence into the DNA Toolkit. Consider resequencing your sample.")

     if not set(dna_seq).issubset(valid_bases):
         raise HTTPException(status_code=400, detail=f"Could not create DNA Nucleotide Sequence entry - did not enter a valid series of nucleotides. This must consist only of 'A', 'T', 'C', and 'G'.")

     if len(nucseq_input.label.strip()) == 0:
         raise HTTPException(status_code=400, detail=f"Could not create DNA Nucleotide Sequence entry - no sequence label was entered. Please try again.")

     new_nucseq = {
    "id": new_id,
    "label": nucseq_input.label,
    "sequence": dna_seq,
    "nuc_analysed": False,
    "aa_analysed": False
     }

     all_sequences.append(new_nucseq)
     save_sequences(all_sequences)
     return {**new_nucseq, "message": f"A new DNA Nucleotide sequence has been successfully created and added to the DNA Toolkit. You can search for this entry via its unique ID, displayed below, or perform seqence analyses or an amino acid conversion."}

@router.get("/", response_model=list[NucSeqSummary])
def list_sequences(nuc_analysed: bool | None = None, aa_analysed: bool | None = None):
    all_sequences = load_sequences()
    if len(all_sequences) == 0:
        raise HTTPException(status_code=404, detail="No nucleotide sequences have been submitted to DNA Toolkit.")

    if nuc_analysed is not None:
        all_sequences = [seq for seq in all_sequences if seq["nuc_analysed"] == nuc_analysed]
    
    if aa_analysed is not None:
        all_sequences = [seq for seq in all_sequences if seq["aa_analysed"] == aa_analysed]

    return all_sequences

@router.get("/{id}", response_model = NucSeq)
def fetch_sequence_by_ID(id:int):
     all_sequences = load_sequences()
     for sequence in all_sequences:
        if id == sequence["id"]:
            return {"message": f"DNA Nucletide Sequence with ID:{id} successfully retrieved.", **sequence}
     raise HTTPException(status_code=404, detail=f"Could not find sequence entry ID:{id}")

@router.delete("/")
def delete_all_sequences():
     save_sequences([])
     return {"message": "All entries successfully deleted."
             }

@router.delete("/{id}", response_model = NucSeq)
def delete_sequence_by_ID(id:int):
     all_sequences = load_sequences()
     for sequence in all_sequences:
        if id == sequence["id"]:
            all_sequences.remove(sequence)
            save_sequences(all_sequences)
            return {"message": f"DNA Nucletide Sequence with ID:{id} successfully deleted. See details of deleted entry below", **sequence}
     raise HTTPException(status_code=404, detail=f"Could not delete sequence entry ID:{id} - ID not found")

@router.put("/{id}", response_model = NucSeq)
def update_task_label(id:int, label_input: NucSeqUpdate):
     all_sequences = load_sequences()
     for sequence in all_sequences:
        if id == sequence["id"]:
            if len(label_input.label.strip()) == 0:
                raise HTTPException(status_code=400, detail=f"Could not update sequence label for sequence ID:{id} - no sequence label was entered. Please try again.")
            sequence["label"] = label_input.label
            save_sequences(all_sequences)
            return {"message": f"DNA Nucletide Sequence label successfully updated, for sequence entry with ID:{id}.", **sequence}
     raise HTTPException(status_code=404, detail=f"Could not update label for sequence ID:{id} - ID not found")